from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QPushButton, QLabel, QFrame, QSizePolicy
)
from PySide6.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QRect, QPoint
)
from PySide6.QtGui import QFont, QPainter, QColor

from home         import HomePage
from add_user     import AddUserPage
from add_employee import AddEmployeePage
from add_stocks   import AddStocksPage
from sales_entry  import SalesEntryPage

ACCENT    = "#4F8EF7"
DARK_TEXT = "#1E2A3A"
SIDEBAR_W = 0.28   # 28% of window width


# ── Sidebar Nav Button ────────────────────────────────────────

class SidebarButton(QPushButton):
    def __init__(self, icon_char: str, label: str, parent=None):
        super().__init__(parent)
        self.setText(f"  {icon_char}   {label}")
        self.setFont(QFont("Segoe UI", 11))
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(52)
        self.setCheckable(False)
        self._active = False
        self._apply_style(False)

    def _apply_style(self, active: bool):
        bg     = ACCENT if active else "transparent"
        weight = "600"  if active else "400"
        hover  = "#3a7ae0" if active else "rgba(255,255,255,0.12)"
        self.setStyleSheet(f"""
            QPushButton {{
                background: {bg};
                color: white;
                border: none;
                border-radius: 10px;
                text-align: left;
                padding-left: 16px;
                font-size: 13px;
                font-weight: {weight};
            }}
            QPushButton:hover {{
                background: {hover};
            }}
            QPushButton:pressed {{
                background: #2E6DC8;
            }}
        """)

    def setActive(self, state: bool):
        self._active = state
        self._apply_style(state)


# ── Overlay (click-to-close backdrop) ────────────────────────

class OverlayWidget(QWidget):
    """
    Dark translucent overlay shown behind the sidebar.
    ✅ FIX: Only covers the area to the RIGHT of the sidebar
             so sidebar buttons are never blocked.
    """
    def __init__(self, main_win: "MainWindow", parent=None):
        super().__init__(parent)
        self._main_win = main_win
        self.setStyleSheet("background: rgba(0, 0, 0, 0.45);")
        self.setCursor(Qt.ArrowCursor)
        self.hide()

    def mousePressEvent(self, event):
        self._main_win.close_sidebar()
        event.accept()


# ── Main Window ───────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🛒  Sales Manager")
        self.setMinimumSize(1200, 750)
        self._sidebar_open = False
        self._anim         = None

        self._build_ui()
        self._navigate(0)      # start on Dashboard

    # ─────────────────────────────────────────────────────────
    # BUILD UI
    # ─────────────────────────────────────────────────────────

    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)

        self._root_layout = QVBoxLayout(root)
        self._root_layout.setContentsMargins(0, 0, 0, 0)
        self._root_layout.setSpacing(0)

        # ── header bar ──
        self._build_header()

        # ── body (page stack fills the rest) ──
        self._body = QWidget()
        self._body.setStyleSheet("background: #F0F4FA;")
        body_lay = QVBoxLayout(self._body)
        body_lay.setContentsMargins(0, 0, 0, 0)
        body_lay.setSpacing(0)

        self._stack = QStackedWidget()
        self._pages = [
            HomePage(),
            AddUserPage(),
            AddEmployeePage(),
            AddStocksPage(),
            SalesEntryPage(),
        ]
        for page in self._pages:
            self._stack.addWidget(page)

        body_lay.addWidget(self._stack)
        self._root_layout.addWidget(self._body)

        # ── floating overlay and sidebar (children of root) ──
        self._overlay = OverlayWidget(self, root)
        self._sidebar = self._build_sidebar(root)
        self._sidebar.hide()

    def _build_header(self):
        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1E2A3A, stop:1 #2C3E55);
                border-bottom: 2px solid {ACCENT};
            }}
        """)

        hl = QHBoxLayout(header)
        hl.setContentsMargins(12, 0, 20, 0)
        hl.setSpacing(0)

        # Hamburger
        self._menu_btn = QPushButton("☰")
        self._menu_btn.setFixedSize(44, 44)
        self._menu_btn.setCursor(Qt.PointingHandCursor)
        self._menu_btn.setFont(QFont("Segoe UI", 18))
        self._menu_btn.setStyleSheet("""
            QPushButton {
                color: white;
                background: transparent;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover { background: rgba(255,255,255,0.15); }
            QPushButton:pressed { background: rgba(255,255,255,0.25); }
        """)
        self._menu_btn.clicked.connect(self.toggle_sidebar)

        # App title
        app_title = QLabel("🛒  Sales Manager")
        app_title.setFont(QFont("Segoe UI", 15, QFont.Bold))
        app_title.setStyleSheet("color: white;")

        # Current page breadcrumb
        self._page_label = QLabel("Dashboard")
        self._page_label.setFont(QFont("Segoe UI", 11))
        self._page_label.setStyleSheet("color: rgba(255,255,255,0.65);")

        hl.addWidget(self._menu_btn)
        hl.addSpacing(10)
        hl.addWidget(app_title)
        hl.addStretch()
        hl.addWidget(self._page_label)

        self._root_layout.addWidget(header)

    def _build_sidebar(self, parent: QWidget) -> QFrame:
        sidebar = QFrame(parent)
        sidebar.setObjectName("sidebar")
        sidebar.setStyleSheet(f"""
            QFrame#sidebar {{
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1E2A3A, stop:1 #16202D);
                border-right: 2px solid {ACCENT};
                border-radius: 0px 16px 16px 0px;
            }}
        """)

        lay = QVBoxLayout(sidebar)
        lay.setContentsMargins(12, 24, 12, 24)
        lay.setSpacing(4)

        # Admin heading
        profile = QLabel("👤  Admin Panel")
        profile.setFont(QFont("Segoe UI", 13, QFont.Bold))
        profile.setStyleSheet(
            "color: white; padding: 6px 0 14px 8px; border: none;")
        lay.addWidget(profile)

        # Divider
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFixedHeight(1)
        sep.setStyleSheet("background: rgba(255,255,255,0.15); border: none;")
        lay.addWidget(sep)
        lay.addSpacing(10)

        # Nav items
        nav_items = [
            ("🏠", "Dashboard"),
            ("👤", "Add Customer"),
            ("🧑‍💼", "Add Employee"),
            ("📦", "Add Stocks"),
            ("🧾", "Sales Entry"),
        ]

        self._nav_btns: list[SidebarButton] = []
        for idx, (icon, label) in enumerate(nav_items):
            btn = SidebarButton(icon, label, sidebar)
            # ✅ FIX: capture idx directly — not len() which changes
            btn.clicked.connect(
                lambda checked, i=idx: self._navigate(i))
            lay.addWidget(btn)
            self._nav_btns.append(btn)

        lay.addStretch()

        # Version
        ver = QLabel("v1.0.0  •  Sales Manager")
        ver.setFont(QFont("Segoe UI", 8))
        ver.setStyleSheet(
            "color: rgba(255,255,255,0.35); padding-left: 8px; border: none;")
        lay.addWidget(ver)

        return sidebar

    # ─────────────────────────────────────────────────────────
    # NAVIGATION
    # ─────────────────────────────────────────────────────────

    def _navigate(self, index: int):
        """Switch page, update breadcrumb, close sidebar."""
        print(f"[Nav] Navigating to page {index}")   # debug

        self._stack.setCurrentIndex(index)

        labels = [
            "Dashboard", "Add Customer", "Add Employee",
            "Add Stocks", "Sales Entry"
        ]
        self._page_label.setText(labels[index])

        for i, btn in enumerate(self._nav_btns):
            btn.setActive(i == index)

        self.close_sidebar()

    # ─────────────────────────────────────────────────────────
    # SIDEBAR OPEN / CLOSE
    # ─────────────────────────────────────────────────────────

    def toggle_sidebar(self):
        if self._sidebar_open:
            self.close_sidebar()
        else:
            self.open_sidebar()

    def open_sidebar(self):
        if self._sidebar_open:
            return
        self._sidebar_open = True

        cw = self.centralWidget()
        cw_w = cw.width()
        cw_h = cw.height()
        sw   = round(cw_w * SIDEBAR_W)
        sh   = cw_h - 60          # below header

        # ✅ FIX: overlay only covers area to the RIGHT of sidebar
        #         so sidebar buttons are fully clickable
        overlay_x = sw
        overlay_w = cw_w - sw

        self._overlay.setGeometry(overlay_x, 60, overlay_w, sh)
        self._overlay.show()
        self._overlay.raise_()

        # Sidebar slides in from left
        self._sidebar.setGeometry(-sw, 60, sw, sh)
        self._sidebar.show()
        self._sidebar.raise_()   # ✅ sidebar ABOVE overlay

        anim = QPropertyAnimation(self._sidebar, b"geometry", self)
        anim.setDuration(300)
        anim.setStartValue(QRect(-sw, 60, sw, sh))
        anim.setEndValue(QRect(0,    60, sw, sh))
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()
        self._anim = anim

    def close_sidebar(self):
        if not self._sidebar_open:
            return
        self._sidebar_open = False
        self._overlay.hide()

        sw      = self._sidebar.width()
        sh      = self._sidebar.height()
        start_x = self._sidebar.x()

        anim = QPropertyAnimation(self._sidebar, b"geometry", self)
        anim.setDuration(260)
        anim.setStartValue(QRect(start_x, 60, sw, sh))
        anim.setEndValue(QRect(-sw,       60, sw, sh))
        anim.setEasingCurve(QEasingCurve.InCubic)
        anim.finished.connect(self._sidebar.hide)
        anim.start()
        self._anim = anim

    # ─────────────────────────────────────────────────────────
    # RESIZE
    # ─────────────────────────────────────────────────────────

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cw = self.centralWidget()
        if not cw:
            return

        cw_w = cw.width()
        cw_h = cw.height()
        sw   = round(cw_w * SIDEBAR_W)
        sh   = cw_h - 60

        if self._sidebar_open:
            self._sidebar.setGeometry(0,  60, sw, sh)
            self._overlay.setGeometry(sw, 60, cw_w - sw, sh)
        else:
            # Keep it hidden off-screen
            self._sidebar.setGeometry(-sw, 60, sw, sh)
