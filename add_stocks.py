from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QDoubleSpinBox, QSpinBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

from data_manager import DataManager
from datetime import datetime

ACCENT    = "#4F8EF7"
DARK_TEXT = "#1E2A3A"
CARD_BG   = "#FFFFFF"
PAGE_BG   = "#F0F4FA"
PURPLE    = "#8E44AD"
GREEN     = "#27AE60"
RED       = "#E74C3C"

CATEGORIES = [
    "Electronics", "Clothing", "Groceries", "Furniture",
    "Sports", "Books", "Toys", "Beauty", "Automotive", "Other"
]


def styled_input(placeholder: str, read_only=False) -> QLineEdit:
    le = QLineEdit()
    le.setPlaceholderText(placeholder)
    le.setReadOnly(read_only)
    le.setFixedHeight(42)
    le.setStyleSheet(f"""
        QLineEdit {{
            background: {'#F5F6FA' if read_only else 'white'};
            border: 1.5px solid #BDC3C7;
            border-radius: 8px; padding: 0 12px;
            font-size: 13px; color: {DARK_TEXT};
        }}
        QLineEdit:focus {{ border-color: {ACCENT}; }}
    """)
    return le


def form_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setFont(QFont("Segoe UI", 10, QFont.Bold))
    lbl.setStyleSheet(f"color: {DARK_TEXT};")
    return lbl


class AddStocksPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background: {PAGE_BG};")
        self.dm = DataManager()
        self._build_ui()
        self._refresh_table()

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 20, 24, 20)
        outer.setSpacing(18)

        title = QLabel("📦 Stock Management")
        title.setFont(QFont("Segoe UI", 17, QFont.Bold))
        title.setStyleSheet(f"color: {DARK_TEXT};")
        outer.addWidget(title)

        split = QHBoxLayout()
        split.setSpacing(18)

        # ─── FORM CARD ─────────────────────────────
        form_card = QFrame()
        form_card.setFixedWidth(400)
        form_card.setStyleSheet(f"background: {CARD_BG}; border-radius: 16px;")
        fc = QVBoxLayout(form_card)
        fc.setContentsMargins(28, 28, 28, 28)
        fc.setSpacing(14)

        form_title = QLabel("➕ Add / Update Stock")
        form_title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        form_title.setStyleSheet(f"color: {DARK_TEXT};")
        fc.addWidget(form_title)

        # info banner
        info = QLabel("ℹ️  If product already exists, quantity will be added.")
        info.setFont(QFont("Segoe UI", 9))
        info.setWordWrap(True)
        info.setStyleSheet(f"""
            background: #EBF5FB;
            border-left: 4px solid {ACCENT};
            border-radius: 6px;
            padding: 8px 10px;
            color: #1A5276;
        """)
        fc.addWidget(info)

        sep = QFrame(); sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #ECF0F1;")
        fc.addWidget(sep)

        # Product ID
        fc.addWidget(form_label("Product ID"))
        self._pid_input = styled_input("Auto-generated", read_only=True)
        self._pid_input.setText(self.dm.get_next_product_id())
        fc.addWidget(self._pid_input)

        # Product Name
        fc.addWidget(form_label("Product Name *"))
        self._pname_input = styled_input("Enter product name")
        self._pname_input.textChanged.connect(self._check_existing)
        fc.addWidget(self._pname_input)

        # Status label
        self._status_lbl = QLabel("")
        self._status_lbl.setFont(QFont("Segoe UI", 9))
        self._status_lbl.setStyleSheet("color: #27AE60;")
        fc.addWidget(self._status_lbl)

        # Category
        fc.addWidget(form_label("Category *"))
        self._cat_cb = QComboBox()
        self._cat_cb.addItems(["Select Category"] + CATEGORIES)
        self._cat_cb.setFixedHeight(42)
        self._cat_cb.setStyleSheet("""
            QComboBox {
                background: white; border: 1.5px solid #BDC3C7;
                border-radius: 8px; padding: 0 12px; font-size: 13px;
            }
            QComboBox:focus { border-color: #4F8EF7; }
            QComboBox::drop-down { border: none; }
        """)
        fc.addWidget(self._cat_cb)

        # Quantity
        fc.addWidget(form_label("Quantity *"))
        self._qty_spin = QSpinBox()
        self._qty_spin.setRange(1, 99999)
        self._qty_spin.setValue(1)
        self._qty_spin.setFixedHeight(42)
        self._qty_spin.setStyleSheet("""
            QSpinBox {
                background: white; border: 1.5px solid #BDC3C7;
                border-radius: 8px; padding: 0 12px; font-size: 13px;
            }
            QSpinBox:focus { border-color: #4F8EF7; }
        """)
        fc.addWidget(self._qty_spin)

        # Unit Price
        fc.addWidget(form_label("Unit Price (₹) *"))
        self._price_spin = QDoubleSpinBox()
        self._price_spin.setRange(0.01, 9_999_999.99)
        self._price_spin.setDecimals(2)
        self._price_spin.setPrefix("₹ ")
        self._price_spin.setFixedHeight(42)
        self._price_spin.setStyleSheet("""
            QDoubleSpinBox {
                background: white; border: 1.5px solid #BDC3C7;
                border-radius: 8px; padding: 0 12px; font-size: 13px;
            }
            QDoubleSpinBox:focus { border-color: #4F8EF7; }
        """)
        fc.addWidget(self._price_spin)

        fc.addSpacing(10)

        btn_row = QHBoxLayout()
        self._clear_btn = QPushButton("🗑 Clear")
        self._clear_btn.setFixedHeight(44)
        self._clear_btn.setCursor(Qt.PointingHandCursor)
        self._clear_btn.setStyleSheet(f"""
            QPushButton {{
                background: #ECF0F1; color: {DARK_TEXT};
                border-radius: 10px; font-size: 13px;
            }}
            QPushButton:hover {{ background: #D5D8DC; }}
        """)
        self._clear_btn.clicked.connect(self._clear_form)

        self._save_btn = QPushButton("💾 Save Stock")
        self._save_btn.setFixedHeight(44)
        self._save_btn.setCursor(Qt.PointingHandCursor)
        self._save_btn.setStyleSheet(f"""
            QPushButton {{
                background: {PURPLE}; color: white;
                border-radius: 10px; font-size: 13px; font-weight: bold;
            }}
            QPushButton:hover {{ background: #7D3C98; }}
        """)
        self._save_btn.clicked.connect(self._save_stock)

        btn_row.addWidget(self._clear_btn)
        btn_row.addWidget(self._save_btn)
        fc.addLayout(btn_row)
        fc.addStretch()

        # ─── TABLE CARD ────────────────────────────
        table_card = QFrame()
        table_card.setStyleSheet(f"background: {CARD_BG}; border-radius: 16px;")
        tc = QVBoxLayout(table_card)
        tc.setContentsMargins(20, 20, 20, 20)
        tc.setSpacing(12)

        # header row
        tbl_hdr = QHBoxLayout()
        tbl_title = QLabel("📋 Stock Inventory")
        tbl_title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        tbl_title.setStyleSheet(f"color: {DARK_TEXT};")
        tbl_hdr.addWidget(tbl_title)
        tbl_hdr.addStretch()

        # summary labels
        self._total_lbl = QLabel("Total Items: 0")
        self._worth_lbl = QLabel("Net Worth: ₹0")
        for lbl in [self._total_lbl, self._worth_lbl]:
            lbl.setFont(QFont("Segoe UI", 10, QFont.Bold))
            lbl.setStyleSheet(f"""
                background: #EBF5FB; border-radius: 6px;
                padding: 4px 10px; color: {DARK_TEXT};
            """)
        tbl_hdr.addWidget(self._total_lbl)
        tbl_hdr.addWidget(self._worth_lbl)
        tc.addLayout(tbl_hdr)

        self._table = QTableWidget()
        self._table.setColumnCount(6)
        self._table.setHorizontalHeaderLabels(
            ["Product ID", "Product Name", "Category",
             "Quantity", "Unit Price (₹)", "Total Value (₹)"])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._table.setAlternatingRowColors(True)
        self._table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table.setSelectionBehavior(QTableWidget.SelectRows)
        self._table.verticalHeader().setVisible(False)
        self._table.setStyleSheet("""
            QTableWidget {
                border: none; font-size: 12px;
                alternate-background-color: #F8FAFF;
                gridline-color: #ECF0F1;
            }
            QHeaderView::section {
                background: #1E2A3A; color: white;
                font-weight: bold; padding: 8px;
                border: none; font-size: 12px;
            }
        """)
        tc.addWidget(self._table)

        split.addWidget(form_card)
        split.addWidget(table_card)
        outer.addLayout(split)

    def _check_existing(self, text: str):
        df = self.dm.load_stocks()
        if not df.empty and text.strip():
            mask = df["product_name"].str.lower() == text.strip().lower()
            if mask.any():
                cur_qty = df.loc[mask, "quantity"].values[0]
                self._status_lbl.setText(
                    f"✅ Product exists — Current qty: {cur_qty} (will add to it)")
                self._status_lbl.setStyleSheet("color: #27AE60;")
                cat = df.loc[mask, "category"].values[0]
                idx = self._cat_cb.findText(str(cat))
                if idx >= 0:
                    self._cat_cb.setCurrentIndex(idx)
            else:
                self._status_lbl.setText("🆕 New product will be created")
                self._status_lbl.setStyleSheet("color: #E67E22;")
        else:
            self._status_lbl.setText("")

    def _save_stock(self):
        pname = self._pname_input.text().strip()
        cat   = self._cat_cb.currentText()
        qty   = self._qty_spin.value()
        price = self._price_spin.value()
        pid   = self._pid_input.text()

        if not pname:
            QMessageBox.warning(self, "Validation", "Product name is required.")
            return
        if cat == "Select Category":
            QMessageBox.warning(self, "Validation", "Please select a category.")
            return

        record = {
            "product_id":   pid,
            "product_name": pname,
            "category":     cat,
            "quantity":     qty,
            "unit_price":   price,
            "added_date":   datetime.now().strftime("%Y-%m-%d"),
        }
        self.dm.save_stock(record)
        QMessageBox.information(self, "Success", f"Stock updated for '{pname}'!")
        self._clear_form()
        self._refresh_table()

    def _clear_form(self):
        self._pname_input.clear()
        self._cat_cb.setCurrentIndex(0)
        self._qty_spin.setValue(1)
        self._price_spin.setValue(0.01)
        self._status_lbl.setText("")
        self._pid_input.setText(self.dm.get_next_product_id())

    def _refresh_table(self):
        df = self.dm.load_stocks()
        self._table.setRowCount(0)
        if df.empty:
            self._total_lbl.setText("Total Items: 0")
            self._worth_lbl.setText("Net Worth: ₹0")
            return

        total_worth = 0
        for _, row in df.iterrows():
            r = self._table.rowCount()
            self._table.insertRow(r)
            qty   = float(row.get("quantity", 0))
            price = float(row.get("unit_price", 0))
            val   = qty * price
            total_worth += val

            for c, (key, fmt) in enumerate([
                ("product_id",   "{}"),
                ("product_name", "{}"),
                ("category",     "{}"),
                ("quantity",     "{:.0f}"),
                ("unit_price",   "₹{:.2f}"),
            ]):
                item = QTableWidgetItem(fmt.format(row.get(key, "")))
                item.setTextAlignment(Qt.AlignCenter)
                self._table.setItem(r, c, item)

            val_item = QTableWidgetItem(f"₹{val:,.2f}")
            val_item.setTextAlignment(Qt.AlignCenter)
            if qty < 5:
                val_item.setForeground(QColor(RED))
            self._table.setItem(r, 5, val_item)

        self._total_lbl.setText(f"Total Items: {len(df)}")
        self._worth_lbl.setText(f"Net Worth: ₹{total_worth:,.0f}")
        self._pid_input.setText(self.dm.get_next_product_id())
