import os
import pandas as pd
from datetime import datetime

DATA_DIR     = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data")
SALES_CSV    = os.path.join(DATA_DIR, "sales.csv")
USER_CSV     = os.path.join(DATA_DIR, "user.csv")
STOCKS_CSV   = os.path.join(DATA_DIR, "stocks.csv")
EMPLOYEE_CSV = os.path.join(DATA_DIR, "employee.csv")


class DataManager:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.initialize_data()

    # ─────────────────────────────────────────────────────────
    # INITIALIZE
    # ─────────────────────────────────────────────────────────

    def initialize_data(self):
        self._init_csv(SALES_CSV, [
            "customer_id", "customer_name", "age", "gender",
            "mobile_number", "city", "purchase_date",
            "product_category", "product_name", "quantity",
            "unit_price", "total_spend", "payment_method",
            "channel", "customer_segment"
        ])
        self._init_csv(USER_CSV, [
            "customer_id", "customer_name", "gender", "mobile_number"
        ])
        self._init_csv(STOCKS_CSV, [
            "product_id", "product_name", "category",
            "quantity", "unit_price", "added_date"
        ])
        self._init_csv(EMPLOYEE_CSV, [
            "employee_id", "employee_name", "gender", "mobile_number"
        ])

    @staticmethod
    def _init_csv(path: str, columns: list):
        if not os.path.exists(path):
            pd.DataFrame(columns=columns).to_csv(path, index=False)

    # ─────────────────────────────────────────────────────────
    # SALES
    # ─────────────────────────────────────────────────────────

    def load_sales(self) -> pd.DataFrame:
        try:
            if not os.path.exists(SALES_CSV):
                return pd.DataFrame()
            df = pd.read_csv(SALES_CSV, dtype=str)
            if df.empty:
                return df
            # Parse dates
            if "purchase_date" in df.columns:
                df["purchase_date"] = pd.to_datetime(
                    df["purchase_date"], errors="coerce")
            # Parse numeric columns
            for col in ("age", "quantity", "unit_price", "total_spend"):
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
            return df
        except Exception as e:
            print(f"[DataManager] load_sales error: {e}")
            return pd.DataFrame()

    def save_sale(self, record: dict) -> bool:
        """Append one sale record and reduce stock quantity."""
        try:
            df = self.load_sales()
            # Convert dates back to string for CSV storage
            rec = dict(record)
            if isinstance(rec.get("purchase_date"), pd.Timestamp):
                rec["purchase_date"] = rec["purchase_date"].strftime("%Y-%m-%d")
            new_row = pd.DataFrame([rec])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(SALES_CSV, index=False)
            # Reduce stock
            self.reduce_stock(
                str(record.get("product_name", "")),
                int(record.get("quantity", 0))
            )
            return True
        except Exception as e:
            print(f"[DataManager] save_sale error: {e}")
            return False

    # ─────────────────────────────────────────────────────────
    # USERS / CUSTOMERS
    # ─────────────────────────────────────────────────────────

    def load_users(self) -> pd.DataFrame:
        try:
            if not os.path.exists(USER_CSV):
                return pd.DataFrame()
            return pd.read_csv(USER_CSV, dtype=str)
        except Exception as e:
            print(f"[DataManager] load_users error: {e}")
            return pd.DataFrame()

    def save_user(self, record: dict) -> bool:
        try:
            df = self.load_users()
            new_row = pd.DataFrame([record])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(USER_CSV, index=False)
            return True
        except Exception as e:
            print(f"[DataManager] save_user error: {e}")
            return False

    def get_next_customer_id(self) -> str:
        df = self.load_users()
        return self._next_id(df, "customer_id", "CID")

    def get_user_by_id(self, cid: str) -> dict | None:
        df = self.load_users()
        if df.empty:
            return None
        match = df[df["customer_id"].astype(str).str.upper() == cid.upper()]
        return match.iloc[0].to_dict() if not match.empty else None

    # ─────────────────────────────────────────────────────────
    # STOCKS
    # ─────────────────────────────────────────────────────────

    def load_stocks(self) -> pd.DataFrame:
        try:
            if not os.path.exists(STOCKS_CSV):
                return pd.DataFrame()
            df = pd.read_csv(STOCKS_CSV, dtype=str)
            for col in ("quantity", "unit_price"):
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
            return df
        except Exception as e:
            print(f"[DataManager] load_stocks error: {e}")
            return pd.DataFrame()

    def save_stock(self, record: dict) -> bool:
        try:
            df = self.load_stocks()
            name = str(record["product_name"]).strip().lower()
            mask = df["product_name"].astype(str).str.strip().str.lower() == name

            if mask.any():
                # Update existing product
                df.loc[mask, "quantity"] = (
                    pd.to_numeric(df.loc[mask, "quantity"], errors="coerce")
                    .fillna(0) + int(record["quantity"])
                )
                df.loc[mask, "unit_price"] = float(record["unit_price"])
            else:
                # Insert new product
                new_row = pd.DataFrame([{
                    "product_id":   record.get("product_id", self.get_next_product_id()),
                    "product_name": record["product_name"],
                    "category":     record.get("category", ""),
                    "quantity":     int(record["quantity"]),
                    "unit_price":   float(record["unit_price"]),
                    "added_date":   record.get("added_date",
                                               datetime.now().strftime("%Y-%m-%d")),
                }])
                df = pd.concat([df, new_row], ignore_index=True)

            df.to_csv(STOCKS_CSV, index=False)
            return True
        except Exception as e:
            print(f"[DataManager] save_stock error: {e}")
            return False

    def get_next_product_id(self) -> str:
        df = self.load_stocks()
        return self._next_id(df, "product_id", "PRD")

    def reduce_stock(self, product_name: str, qty: int) -> bool:
        """Subtract qty from a product. Floor at 0."""
        try:
            if not product_name or qty <= 0:
                return False
            df = self.load_stocks()
            if df.empty:
                return False
            mask = (df["product_name"].astype(str)
                    .str.strip().str.lower() == product_name.strip().lower())
            if mask.any():
                current = float(df.loc[mask, "quantity"].values[0])
                df.loc[mask, "quantity"] = max(0.0, current - qty)
                df.to_csv(STOCKS_CSV, index=False)
            return True
        except Exception as e:
            print(f"[DataManager] reduce_stock error: {e}")
            return False

    # ─────────────────────────────────────────────────────────
    # EMPLOYEES
    # ─────────────────────────────────────────────────────────

    def load_employees(self) -> pd.DataFrame:
        try:
            if not os.path.exists(EMPLOYEE_CSV):
                return pd.DataFrame()
            return pd.read_csv(EMPLOYEE_CSV, dtype=str)
        except Exception as e:
            print(f"[DataManager] load_employees error: {e}")
            return pd.DataFrame()

    def save_employee(self, record: dict) -> bool:
        try:
            df = self.load_employees()
            new_row = pd.DataFrame([record])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(EMPLOYEE_CSV, index=False)
            return True
        except Exception as e:
            print(f"[DataManager] save_employee error: {e}")
            return False

    def get_next_employee_id(self) -> str:
        df = self.load_employees()
        return self._next_id(df, "employee_id", "EMP")

    # ─────────────────────────────────────────────────────────
    # SHARED HELPER
    # ─────────────────────────────────────────────────────────

    @staticmethod
    def _next_id(df: pd.DataFrame, col: str, prefix: str) -> str:
        """Generate next sequential ID like CID001, EMP003 etc."""
        if df.empty or col not in df.columns:
            return f"{prefix}001"
        nums = []
        for val in df[col].dropna():
            try:
                nums.append(int(str(val).upper().replace(prefix, "")))
            except ValueError:
                pass
        nxt = max(nums) + 1 if nums else 1
        return f"{prefix}{nxt:03d}"
