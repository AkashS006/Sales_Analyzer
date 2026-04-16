import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(
        'QWidget { color: #1E2A3A; background-color: #F0F4FA; }'
        'QLabel { color: #1E2A3A; background: transparent; }'
        'QComboBox { color: #1E2A3A; background: white; }'
        'QComboBox QAbstractItemView { color: #1E2A3A; background: white; selection-background-color: #4F8EF7; selection-color: white; }'
        'QTableWidget { color: #1E2A3A; background: white; gridline-color: #E0E0E0; }'
        'QTableWidget::item { color: #1E2A3A; background: white; }'
        'QTableWidget::item:selected { background: #4F8EF7; color: white; }'
        'QHeaderView::section { color: #1E2A3A; background: #F0F4FA; border: 1px solid #E0E0E0; padding: 4px; }'
        'QLineEdit { color: #1E2A3A; background: white; border: 1.5px solid #BDC3C7; border-radius: 6px; padding: 4px 8px; }'
        'QPushButton { color: white; background: #4F8EF7; border-radius: 8px; padding: 6px 16px; }'
        'QPushButton:hover { background: #3a7ae0; }'
        'QScrollBar:vertical { background: #F0F4FA; width: 8px; }'
        'QScrollBar::handle:vertical { background: #BDC3C7; border-radius: 4px; }'
    )
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
