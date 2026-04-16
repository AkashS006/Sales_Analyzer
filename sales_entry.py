from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QDoubleSpinBox, QSpinBox,
    QScrollArea, QDateEdit, QSizePolicy, QGridLayout
)
from PySide6.QtCore import Qt, QDate, QRegularExpression
from PySide6.QtGui import QFont, QRegularExpressionValidator, QColor

from data_manager import DataManager
from datetime import datetime
import pandas as pd

# ── Colour palette ────────────────────────────────────────────
ACCENT    = "#4F8EF7"
DARK_TEXT = "#1E2A3A"
CARD_BG   = "#FFFFFF"
PAGE_BG   = "#F0F4FA"
GREEN     = "#27AE60"
ORANGE    = "#F39C12"
RED       = "#E74C3C"

PAYMENT_METHODS = ["Cash", "Credit Card", "Debit Card",
                   "UPI", "Net Banking", "Wallet"]
CHANNELS        = ["In-Store", "Online", "Phone", "Mobile App"]
SEGMENTS        = ["Regular", "Premium", "VIP", "New Customer"]
CITIES          = ["Mumbai", "Delhi", "Bangalore", "Chennai",
                   "Hyderabad", "Kolkata", "Pune", "Ahmedabad",
                   "Jaipur", "Surat", "Other"]

TABLE_HEADERS = [
    "Customer ID", "Customer Name", "Age", "Gender",
    "Mobile", "City", "Purchase Date", "Category",
    "Product", "Qty", "Unit Price", "Total Spend",
    "Payment", "Channel", "Segment"
]

# CSV column order must match TABLE_HEADERS exactly
COL_MAP = [
    "customer_id", "customer_name", "age", "gender",
    "mobile_number", "city", "purchase_date", "product_category",
    "product_name", "quantity", "unit_price", "total_spend",
    "payment_method", "channel", "customer_segment"
]


# ── Reusable widget helpers ───────────────────────────────────

def styled_input(placeholder: str = "", read_only: bool = False) -> QLineEdit:
    le = QLineEdit()
    le.setPlaceholderText(placeholder)
    le.setReadOnly(read_only)
    le.setFixedHeight(38)
    bg = "#F5F6FA" if read_only else "white"
    le.setStyleSheet(f"""
        QLineEdit {{
            background: {bg};
            border: 1.5px solid #BDC3C7;
            border-radius: 8px;
            padding: 0 10px;
            font-size: 12px;
            color: {DARK_TEXT};
        }}
        QLineEdit:focus {{ border-color: {ACCENT}; }}
        QLineEdit:read-only {{ color: #7F8C8D; }}
    """)
    return le


def styled_combo(items: list) -> QComboBox:
    cb = QComboBox()
    cb.addItems(items)
    cb.setFixedHeight(38)
    cb.setStyleSheet(f"""
        QComboBox {{
            background: white;
            border: 1.5px solid #BDC3C7;
            border-radius: 8px;
            padding: 0 10px;
            font-size: 12px;
            color: {DARK_TEXT};
        }}
        QComboBox:focus {{ border-color: {ACCENT}; }}
        QComboBox::drop-down {{ border: none; width: 24px; }}
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 6px solid #7F8C8D;
            margin-right: 6px;
        }}
        QComboBox QAbstractItemView {{
            font-size: 12px;
            selection-background-color: {ACCENT};
            selection-color: white;
            border: 1px solid #BDC3C7;
        }}
    """)
    return cb


def styled_spinbox(min_val: int = 1, max_val: int = 9999,
                   value: int = 1) -> QSpinBox:
    sb = QSpinBox()
    sb.setRange(min_val, max_val)
    sb.setValue(value)
    sb.setFixedHeight(38)
    sb.setStyleSheet(f"""
        QSpinBox {{
            background: white; border: 1.5px solid #BDC3C7;
            border-radius: 8px; padding: 0 10px;
            font-size: 12px; color: {DARK_TEXT};
        }}
        QSpinBox:focus {{ border-color: {ACCENT}; }}
        QSpinBox::up-button, QSpinBox::down-button {{ width: 20px; }}
    """)
    return sb


def styled_double_spinbox(min_val: float = 0.01,
                           max_val: float = 9_999_999.0,
                           prefix: str = "₹ ") -> QDoubleSpinBox:
    sb = QDoubleSpinBox()
    sb.setRange(min_val, max_val)
    sb.setDecimals(2)
    sb.setPrefix(prefix)
    sb.setFixedHeight(38)
    sb.setStyleSheet(f"""
        QDoubleSpinBox {{
            background: white; border: 1.5px solid #BDC3C7;
            border-radius: 8px; padding: 0 10px;
            font-size: 12px; color: {DARK_TEXT};
        }}
        QDoubleSpinBox:focus {{ border-color: {ACCENT}; }}
        QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{ width: 20px; }}
    """)
    return sb


def form_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setFont(QFont("Segoe UI", 9, QFont.Bold))
    lbl.setStyleSheet(f"color: {DARK_TEXT};")
    return lbl


def section_title(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
    lbl.setStyleSheet(f"""
        color: {DARK_TEXT};
        border-bottom: 2px solid {ACCENT};
        padding-bottom: 4px;
        margin-top: 4px;
    """)
    return lbl


# ── Main Page ─────────────────────────────────────────────────

class SalesEntryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background: {PAGE_BG};")
        self.dm = DataManager()
        self._all_rows = pd.DataFrame()
        self._build_ui()
        self._refresh_table()

    # ─────────────────────────────────────────────────────────
    # UI CONSTRUCTION
    # ─────────────────────────────────────────────────────────

    def _build_ui(self):
        outer = QHBoxLayout(self)
        outer.setContentsMargins(24, 20, 24, 20)
        outer.setSpacing(18)
        outer.addWidget(self._build_form_panel(), stretch=0)
        outer.addWidget(self._build_table_panel(), stretch=1)

    # ── LEFT PANEL ───────────────────────────────────────────

    def _build_form_panel(self) -> QScrollArea:
        form_scroll = QScrollArea()
        form_scroll.setWidgetResizable(True)
        form_scroll.setFixedWidth(490)
        form_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        form_scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical { width: 6px; background: #ECF0F1;
                                  border-radius: 3px; }
            QScrollBar::handle:vertical { background: #BDC3C7;
                                          border-radius: 3px; }
        """)

        form_container = QFrame()
        form_container.setStyleSheet(
            f"background: {CARD_BG}; border-radius: 16px;")
        fc = QVBoxLayout(form_container)
        fc.setContentsMargins(24, 24, 24, 24)
        fc.setSpacing(10)

        hdr = QLabel("🧾  New Sales Entry")
        hdr.setFont(QFont("Segoe UI", 14, QFont.Bold))
        hdr.setStyleSheet(f"color: {DARK_TEXT};")
        fc.addWidget(hdr)
        fc.addSpacing(4)

        fc.addLayout(self._build_customer_section())
        fc.addSpacing(8)
        fc.addLayout(self._build_purchase_section())
        fc.addSpacing(8)
        fc.addLayout(self._build_transaction_section())
        fc.addSpacing(16)
        fc.addLayout(self._build_buttons())
        fc.addStretch()

        form_scroll.setWidget(form_container)
        return form_scroll

    def _build_customer_section(self) -> QVBoxLayout:
        vl = QVBoxLayout()
        vl.setSpacing(6)
        vl.addWidget(section_title("👤  Customer Information"))
        vl.addSpacing(4)

        g = QGridLayout()
        g.setSpacing(10)
        g.setColumnStretch(0, 1)
        g.setColumnStretch(1, 1)

        # Customer ID
        g.addWidget(form_label("Customer ID  *"), 0, 0)
        self._cid_input = styled_input("e.g. CID001")
        self._cid_input.setValidator(
            QRegularExpressionValidator(
                QRegularExpression(r"[A-Za-z0-9]{0,10}")))
        self._cid_input.textChanged.connect(self._auto_fill_customer)
        g.addWidget(self._cid_input, 1, 0)

        # Customer Name (auto-fill)
        g.addWidget(form_label("Customer Name"), 0, 1)
        self._cname_input = styled_input("Auto-filled", read_only=True)
        g.addWidget(self._cname_input, 1, 1)

        # Age
        g.addWidget(form_label("Age"), 2, 0)
        self._age_spin = styled_spinbox(1, 120, 25)
        g.addWidget(self._age_spin, 3, 0)

        # Gender (auto-fill)
        g.addWidget(form_label("Gender"), 2, 1)
        self._gender_input = styled_input("Auto-filled", read_only=True)
        g.addWidget(self._gender_input, 3, 1)

        # Mobile (auto-fill)
        g.addWidget(form_label("Mobile Number"), 4, 0)
        self._mobile_input = styled_input("Auto-filled", read_only=True)
        g.addWidget(self._mobile_input, 5, 0)

        # City
        g.addWidget(form_label("City  *"), 4, 1)
        self._city_cb = styled_combo(["Select City"] + CITIES)
        g.addWidget(self._city_cb, 5, 1)

        vl.addLayout(g)
        return vl

    def _build_purchase_section(self) -> QVBoxLayout:
        vl = QVBoxLayout()
        vl.setSpacing(6)
        vl.addWidget(section_title("🛒  Purchase Information"))
        vl.addSpacing(4)

        g = QGridLayout()
        g.setSpacing(10)
        g.setColumnStretch(0, 1)
        g.setColumnStretch(1, 1)

        # Purchase Date
        g.addWidget(form_label("Purchase Date  *"), 0, 0)
        self._date_edit = QDateEdit()
        self._date_edit.setDate(QDate.currentDate())
        self._date_edit.setCalendarPopup(True)
        self._date_edit.setFixedHeight(38)
        self._date_edit.setStyleSheet(f"""
            QDateEdit {{
                background: white; border: 1.5px solid #BDC3C7;
                border-radius: 8px; padding: 0 10px;
                font-size: 12px; color: {DARK_TEXT};
            }}
            QDateEdit:focus {{ border-color: {ACCENT}; }}
            QDateEdit::drop-down {{ border: none; width: 24px; }}
        """)
        g.addWidget(self._date_edit, 1, 0)

        # Product Category — loaded fresh from stocks.csv
        g.addWidget(form_label("Product Category  *"), 0, 1)
        stk  = self.dm.load_stocks()
        cats = (sorted(stk["category"].dropna().unique().tolist())
                if not stk.empty else [])
        self._pcat_cb = styled_combo(["Select Category"] + cats)
        self._pcat_cb.currentIndexChanged.connect(self._populate_products)
        g.addWidget(self._pcat_cb, 1, 1)

        # Product Name
        g.addWidget(form_label("Product Name  *"), 2, 0)
        self._pname_cb = styled_combo(["Select Product"])
        self._pname_cb.currentIndexChanged.connect(self._auto_fill_price)
        g.addWidget(self._pname_cb, 3, 0)

        # Quantity
        g.addWidget(form_label("Quantity  *"), 2, 1)
        self._qty_spin = styled_spinbox(1, 9999, 1)
        self._qty_spin.valueChanged.connect(self._calc_total)
        g.addWidget(self._qty_spin, 3, 1)

        # Unit Price
        g.addWidget(form_label("Unit Price (₹)  *"), 4, 0)
        self._uprice_spin = styled_double_spinbox()
        self._uprice_spin.valueChanged.connect(self._calc_total)
        g.addWidget(self._uprice_spin, 5, 0)

        # Total Spend
        g.addWidget(form_label("Total Spend (₹)"), 4, 1)
        self._total_input = styled_input("Auto-calculated", read_only=True)
        self._total_input.setStyleSheet(
            self._total_input.styleSheet() +
            f"QLineEdit {{ color: {GREEN}; font-weight: bold; }}"
        )
        g.addWidget(self._total_input, 5, 1)

        vl.addLayout(g)
        return vl

    def _build_transaction_section(self) -> QVBoxLayout:
        vl = QVBoxLayout()
        vl.setSpacing(6)
        vl.addWidget(section_title("💳  Transaction Details"))
        vl.addSpacing(4)

        g = QGridLayout()
        g.setSpacing(10)
        g.setColumnStretch(0, 1)
        g.setColumnStretch(1, 1)

        g.addWidget(form_label("Payment Method  *"), 0, 0)
        self._pay_cb = styled_combo(["Select Method"] + PAYMENT_METHODS)
        g.addWidget(self._pay_cb, 1, 0)

        g.addWidget(form_label("Channel  *"), 0, 1)
        self._channel_cb = styled_combo(["Select Channel"] + CHANNELS)
        g.addWidget(self._channel_cb, 1, 1)

        g.addWidget(form_label("Customer Segment  *"), 2, 0)
        self._segment_cb = styled_combo(["Select Segment"] + SEGMENTS)
        g.addWidget(self._segment_cb, 3, 0)

        vl.addLayout(g)
        return vl

    def _build_buttons(self) -> QHBoxLayout:
        hl = QHBoxLayout()
        hl.setSpacing(12)

        self._clear_btn = QPushButton("🗑  Clear")
        self._clear_btn.setFixedHeight(44)
        self._clear_btn.setCursor(Qt.PointingHandCursor)
        self._clear_btn.setStyleSheet(f"""
            QPushButton {{
                background: #ECF0F1; color: {DARK_TEXT};
                border: none; border-radius: 10px;
                font-size: 13px; font-weight: bold; padding: 0 20px;
            }}
            QPushButton:hover {{ background: #D5D8DC; }}
            QPushButton:pressed {{ background: #BDC3C7; }}
        """)
        self._clear_btn.clicked.connect(self._clear_form)

        self._submit_btn = QPushButton("✅  Submit Sale")
        self._submit_btn.setFixedHeight(44)
        self._submit_btn.setCursor(Qt.PointingHandCursor)
        self._submit_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {ACCENT}, stop:1 #6AA8FF);
                color: white; border: none; border-radius: 10px;
                font-size: 13px; font-weight: bold; padding: 0 20px;
            }}
            QPushButton:hover {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3A7DE8, stop:1 #5A9AFF);
            }}
            QPushButton:pressed {{ background: #2E6DC8; }}
        """)
        self._submit_btn.clicked.connect(self._submit_sale)

        hl.addWidget(self._clear_btn, stretch=1)
        hl.addWidget(self._submit_btn, stretch=2)
        return hl

    # ── RIGHT PANEL (TABLE) ──────────────────────────────────

    def _build_table_panel(self) -> QFrame:
        panel = QFrame()
        panel.setStyleSheet(f"background: {CARD_BG}; border-radius: 16px;")
        vl = QVBoxLayout(panel)
        vl.setContentsMargins(20, 20, 20, 20)
        vl.setSpacing(12)

        # Header row
        hdr_row = QHBoxLayout()
        tbl_title = QLabel("📋  Sales Records")
        tbl_title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        tbl_title.setStyleSheet(f"color: {DARK_TEXT};")
        hdr_row.addWidget(tbl_title)
        hdr_row.addStretch()

        self._row_badge = QLabel("0 records")
        self._row_badge.setStyleSheet(f"""
            background: {ACCENT}; color: white;
            border-radius: 10px; padding: 2px 12px;
            font-size: 11px; font-weight: bold;
        """)
        hdr_row.addWidget(self._row_badge)

        refresh_btn = QPushButton("🔄  Refresh")
        refresh_btn.setFixedHeight(34)
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background: #ECF0F1; color: {DARK_TEXT};
                border: none; border-radius: 8px;
                font-size: 11px; padding: 0 14px;
            }}
            QPushButton:hover {{ background: #D5D8DC; }}
        """)
        refresh_btn.clicked.connect(self._refresh_table)
        hdr_row.addWidget(refresh_btn)
        vl.addLayout(hdr_row)

        # Search bar
        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText(
            "🔍  Search by customer name, ID, product...")
        self._search_input.setFixedHeight(36)
        self._search_input.setStyleSheet(f"""
            QLineEdit {{
                background: #F5F6FA; border: 1.5px solid #BDC3C7;
                border-radius: 8px; padding: 0 12px;
                font-size: 12px; color: {DARK_TEXT};
            }}
            QLineEdit:focus {{ border-color: {ACCENT}; }}
        """)
        self._search_input.textChanged.connect(self._filter_table)
        vl.addWidget(self._search_input)

        # Table
        self._table = QTableWidget()
        self._table.setColumnCount(len(TABLE_HEADERS))
        self._table.setHorizontalHeaderLabels(TABLE_HEADERS)
        self._table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents)
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table.setSelectionBehavior(QTableWidget.SelectRows)
        self._table.setAlternatingRowColors(True)
        self._table.verticalHeader().setVisible(False)
        self._table.setShowGrid(False)
        self._table.setStyleSheet(f"""
            QTableWidget {{
                background: white;
                alternate-background-color: #F8F9FF;
                border: none; font-size: 12px; color: {DARK_TEXT};
            }}
            QHeaderView::section {{
                background: #EAF0FF; color: {DARK_TEXT};
                font-weight: bold; font-size: 11px;
                padding: 8px 6px; border: none;
                border-bottom: 2px solid {ACCENT};
            }}
            QTableWidget::item {{
                padding: 6px 8px;
                border-bottom: 1px solid #F0F0F0;
            }}
            QTableWidget::item:selected {{
                background: #D6E4FF; color: {DARK_TEXT};
            }}
        """)
        vl.addWidget(self._table)

        # Footer summary
        self._summary_lbl = QLabel()
        self._summary_lbl.setStyleSheet(
            f"color: {GREEN}; font-weight: bold; font-size: 12px;")
        vl.addWidget(self._summary_lbl)

        return panel

    # ─────────────────────────────────────────────────────────
    # LOGIC — AUTO-FILL & CALCULATIONS
    # ─────────────────────────────────────────────────────────

    def _auto_fill_customer(self, cid_text: str):
        """
        Look up customer in user.csv as the user types.
        CSV columns: customer_id | customer_name | gender | mobile_number
        """
        cid = cid_text.strip().upper()
        if not cid:
            self._clear_customer_fields()
            return

        df = self.dm.load_users()
        if df.empty:
            return

        match = df[df["customer_id"].astype(str).str.upper() == cid]

        if not match.empty:
            row = match.iloc[0]
            # ✅ FIX: use correct CSV column names
            self._cname_input.setText(str(row.get("customer_name", "")))
            self._gender_input.setText(str(row.get("gender", "")))
            self._mobile_input.setText(str(row.get("mobile_number", "")))
            # Green border = found
            self._set_cid_border(GREEN)
        else:
            self._clear_customer_fields()
            if len(cid) >= 3:
                # Red border = not found after 3 chars
                self._set_cid_border(RED)

    def _set_cid_border(self, color: str):
        self._cid_input.setStyleSheet(f"""
            QLineEdit {{
                background: white;
                border: 2px solid {color};
                border-radius: 8px;
                padding: 0 10px;
                font-size: 12px;
                color: {DARK_TEXT};
            }}
            QLineEdit:focus {{ border-color: {color}; }}
        """)

    def _clear_customer_fields(self):
        self._cname_input.clear()
        self._gender_input.clear()
        self._mobile_input.clear()
        # Reset to default border
        self._cid_input.setStyleSheet(f"""
            QLineEdit {{
                background: white;
                border: 1.5px solid #BDC3C7;
                border-radius: 8px;
                padding: 0 10px;
                font-size: 12px;
                color: {DARK_TEXT};
            }}
            QLineEdit:focus {{ border-color: {ACCENT}; }}
        """)

    def _populate_products(self):
        """Filter products by selected category."""
        self._pname_cb.blockSignals(True)
        self._pname_cb.clear()
        self._pname_cb.addItem("Select Product")

        cat = self._pcat_cb.currentText()
        if cat != "Select Category":
            stk = self.dm.load_stocks()
            if not stk.empty:
                products = (stk[stk["category"] == cat]["product_name"]
                            .dropna().unique().tolist())
                self._pname_cb.addItems(sorted(products))

        self._pname_cb.blockSignals(False)
        self._auto_fill_price()

    def _auto_fill_price(self):
        """Fill unit price from stocks when product is selected."""
        product = self._pname_cb.currentText()
        if product in ("Select Product", ""):
            return
        stk = self.dm.load_stocks()
        if stk.empty:
            return
        match = stk[stk["product_name"] == product]
        if not match.empty:
            price = float(match.iloc[0].get("unit_price", 0))
            self._uprice_spin.setValue(price)

    def _calc_total(self):
        """Live-calculate total spend."""
        total = self._qty_spin.value() * self._uprice_spin.value()
        self._total_input.setText(f"₹ {total:,.2f}")

    # ─────────────────────────────────────────────────────────
    # LOGIC — FORM SUBMIT / CLEAR
    # ─────────────────────────────────────────────────────────

    def _validate(self) -> bool:
        errors = []
        if not self._cid_input.text().strip():
            errors.append("• Customer ID is required.")
        if self._city_cb.currentIndex() == 0:
            errors.append("• Please select a City.")
        if self._pcat_cb.currentIndex() == 0:
            errors.append("• Please select a Product Category.")
        if self._pname_cb.currentIndex() == 0:
            errors.append("• Please select a Product Name.")
        if self._pay_cb.currentIndex() == 0:
            errors.append("• Please select a Payment Method.")
        if self._channel_cb.currentIndex() == 0:
            errors.append("• Please select a Channel.")
        if self._segment_cb.currentIndex() == 0:
            errors.append("• Please select a Customer Segment.")
        if self._uprice_spin.value() <= 0:
            errors.append("• Unit Price must be greater than 0.")

        if errors:
            QMessageBox.warning(
                self, "Validation Error",
                "Please fix the following:\n\n" + "\n".join(errors))
            return False
        return True

    def _submit_sale(self):
        if not self._validate():
            return

        qty   = self._qty_spin.value()
        price = self._uprice_spin.value()
        total = round(qty * price, 2)

        record = {
            "customer_id":      self._cid_input.text().strip().upper(),
            "customer_name":    self._cname_input.text().strip(),
            "age":              self._age_spin.value(),
            "gender":           self._gender_input.text().strip(),
            "mobile_number":    self._mobile_input.text().strip(),
            "city":             self._city_cb.currentText(),
            "purchase_date":    self._date_edit.date().toString("yyyy-MM-dd"),
            "product_category": self._pcat_cb.currentText(),
            "product_name":     self._pname_cb.currentText(),
            "quantity":         qty,
            "unit_price":       price,
            "total_spend":      total,
            "payment_method":   self._pay_cb.currentText(),
            "channel":          self._channel_cb.currentText(),
            "customer_segment": self._segment_cb.currentText(),
        }

        # ✅ FIX: call save_sale (not add_sale); stock reduction handled inside
        success = self.dm.save_sale(record)

        if success:
            display_name = record["customer_name"] or record["customer_id"]
            QMessageBox.information(
                self, "Sale Recorded",
                f"✅  Sale saved successfully!\n\n"
                f"Customer : {display_name}\n"
                f"Product  : {record['product_name']}\n"
                f"Qty      : {qty}\n"
                f"Total    : ₹ {total:,.2f}"
            )
            self._clear_form()
            self._refresh_table()
        else:
            QMessageBox.critical(
                self, "Error",
                "❌  Failed to save the sale record.\n"
                "Please check the console for details.")

    def _clear_form(self):
        self._cid_input.clear()
        self._clear_customer_fields()
        self._age_spin.setValue(25)
        self._city_cb.setCurrentIndex(0)
        self._date_edit.setDate(QDate.currentDate())
        self._pcat_cb.setCurrentIndex(0)
        self._pname_cb.clear()
        self._pname_cb.addItem("Select Product")
        self._qty_spin.setValue(1)
        self._uprice_spin.setValue(0.01)
        self._total_input.clear()
        self._pay_cb.setCurrentIndex(0)
        self._channel_cb.setCurrentIndex(0)
        self._segment_cb.setCurrentIndex(0)

    # ─────────────────────────────────────────────────────────
    # LOGIC — TABLE REFRESH & SEARCH
    # ─────────────────────────────────────────────────────────

    def _refresh_table(self):
        df = self.dm.load_sales()
        self._all_rows = df
        self._populate_table(df)

        if not df.empty and "total_spend" in df.columns:
            total_rev = pd.to_numeric(
                df["total_spend"], errors="coerce").sum()
            self._summary_lbl.setText(
                f"Total Revenue: ₹ {total_rev:,.2f}   |   "
                f"Total Transactions: {len(df)}"
            )
        else:
            self._summary_lbl.setText("No sales data yet.")

    def _populate_table(self, df: pd.DataFrame):
        self._table.setRowCount(0)
        if df is None or df.empty:
            self._row_badge.setText("0 records")
            return

        self._table.setRowCount(len(df))
        for row_idx, (_, row) in enumerate(df.iterrows()):
            for col_idx, col_key in enumerate(COL_MAP):
                raw = row.get(col_key, "")
                val = "" if pd.isna(raw) else str(raw)
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)

                # Colour-code Total Spend
                if col_key == "total_spend":
                    try:
                        amount = float(val)
                        item.setText(f"₹ {amount:,.2f}")
                        if amount >= 10_000:
                            item.setForeground(QColor(GREEN))
                        elif amount >= 5_000:
                            item.setForeground(QColor(ORANGE))
                    except (ValueError, TypeError):
                        pass

                # Colour-code Segment
                if col_key == "customer_segment":
                    colours = {
                        "VIP":          QColor("#8E44AD"),
                        "Premium":      QColor(ACCENT),
                        "Regular":      QColor(GREEN),
                        "New Customer": QColor(ORANGE),
                    }
                    item.setForeground(colours.get(val, QColor(DARK_TEXT)))

                self._table.setItem(row_idx, col_idx, item)

        self._row_badge.setText(f"{len(df)} records")

    def _filter_table(self, text: str):
        if self._all_rows.empty:
            return
        if not text.strip():
            self._populate_table(self._all_rows)
            return
        mask = self._all_rows.apply(
            lambda row: row.astype(str)
            .str.contains(text, case=False, na=False).any(), axis=1)
        self._populate_table(self._all_rows[mask])

    # Public refresh hook called from HomePage
    def refresh(self):
        self._refresh_table()
