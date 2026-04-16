from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox
)
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QFont, QRegularExpressionValidator

from data_manager import DataManager

ACCENT    = "#4F8EF7"
DARK_TEXT = "#1E2A3A"
CARD_BG   = "#FFFFFF"
PAGE_BG   = "#F0F4FA"
GREEN     = "#27AE60"


def styled_input(placeholder: str, read_only=False) -> QLineEdit:
    le = QLineEdit()
    le.setPlaceholderText(placeholder)
    le.setReadOnly(read_only)
    le.setFixedHeight(42)
    le.setStyleSheet(f"""
        QLineEdit {{
            background: {'#F5F6FA' if read_only else 'white'};
            border: 1.5px solid #BDC3C7;
            border-radius: 8px;
            padding: 0 12px;
            font-size: 13px;
            color: {DARK_TEXT};
        }}
        QLineEdit:focus {{ border-color: {ACCENT}; }}
    """)
    return le


def form_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setFont(QFont("Segoe UI", 10, QFont.Bold))
    lbl.setStyleSheet(f"color: {DARK_TEXT};")
    return lbl


class AddEmployeePage(QWidget):
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

        title = QLabel("🧑‍💼 Employee Management")
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

        form_title = QLabel("➕ Add New Employee")
        form_title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        form_title.setStyleSheet(f"color: {DARK_TEXT};")
        fc.addWidget(form_title)

        sep = QFrame(); sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #ECF0F1;")
        fc.addWidget(sep)
        fc.addSpacing(4)

        # Employee ID
        fc.addWidget(form_label("Employee ID"))
        self._eid_input = styled_input("Auto-generated", read_only=True)
        self._eid_input.setText(self.dm.get_next_employee_id())
        fc.addWidget(self._eid_input)

        # Name
        fc.addWidget(form_label("Employee Name *"))
        self._name_input = styled_input("Enter full name")
        fc.addWidget(self._name_input)

        # Gender
        fc.addWidget(form_label("Gender *"))
        self._gender_cb = QComboBox()
        self._gender_cb.addItems(["Select Gender", "Male", "Female", "Other"])
        self._gender_cb.setFixedHeight(42)
        self._gender_cb.setStyleSheet("""
            QComboBox {
                background: white; border: 1.5px solid #BDC3C7;
                border-radius: 8px; padding: 0 12px; font-size: 13px;
            }
            QComboBox:focus { border-color: #4F8EF7; }
            QComboBox::drop-down { border: none; }
        """)
        fc.addWidget(self._gender_cb)

        # Mobile
        fc.addWidget(form_label("Mobile Number *"))
        self._mobile_input = styled_input("10-digit mobile number")
        validator = QRegularExpressionValidator(
            QRegularExpression(r"[0-9]{0,10}"))
        self._mobile_input.setValidator(validator)
        fc.addWidget(self._mobile_input)

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

        self._save_btn = QPushButton("💾 Save Employee")
        self._save_btn.setFixedHeight(44)
        self._save_btn.setCursor(Qt.PointingHandCursor)
        self._save_btn.setStyleSheet(f"""
            QPushButton {{
                background: {ACCENT}; color: white;
                border-radius: 10px; font-size: 13px; font-weight: bold;
            }}
            QPushButton:hover {{ background: #3a7ae0; }}
        """)
        self._save_btn.clicked.connect(self._save_employee)

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

        tbl_title = QLabel("📋 Employee Records")
        tbl_title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        tbl_title.setStyleSheet(f"color: {DARK_TEXT};")
        tc.addWidget(tbl_title)

        self._table = QTableWidget()
        self._table.setColumnCount(4)
        self._table.setHorizontalHeaderLabels(
            ["Employee ID", "Name", "Gender", "Mobile"])
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

    def _save_employee(self):
        name   = self._name_input.text().strip()
        gender = self._gender_cb.currentText()
        mobile = self._mobile_input.text().strip()
        eid    = self._eid_input.text()

        if not name:
            QMessageBox.warning(self, "Validation", "Employee name is required.")
            return
        if gender == "Select Gender":
            QMessageBox.warning(self, "Validation", "Please select a gender.")
            return
        if len(mobile) != 10:
            QMessageBox.warning(self, "Validation", "Mobile must be 10 digits.")
            return

        record = {
            "employee_id": eid,
            "employee_name": name,
            "gender": gender,
            "mobile_number": mobile,
        }
        self.dm.save_employee(record)
        QMessageBox.information(self, "Success",
                                f"Employee {name} saved with ID {eid}!")
        self._clear_form()
        self._refresh_table()

    def _clear_form(self):
        self._name_input.clear()
        self._gender_cb.setCurrentIndex(0)
        self._mobile_input.clear()
        self._eid_input.setText(self.dm.get_next_employee_id())

    def _refresh_table(self):
        df = self.dm.load_employees()
        self._table.setRowCount(0)
        if df.empty:
            return
        for _, row in df.iterrows():
            r = self._table.rowCount()
            self._table.insertRow(r)
            for c, key in enumerate(
                    ["employee_id", "employee_name", "gender", "mobile_number"]):
                item = QTableWidgetItem(str(row.get(key, "")))
                item.setTextAlignment(Qt.AlignCenter)
                self._table.setItem(r, c, item)
        self._eid_input.setText(self.dm.get_next_employee_id())
