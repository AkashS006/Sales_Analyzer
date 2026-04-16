from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QComboBox, QSizePolicy, QPushButton
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor, QPainter
from PySide6.QtCharts import (
    QChart, QChartView, QBarSeries, QBarSet,
    QBarCategoryAxis, QValueAxis, QPieSeries
)
import pandas as pd
from data_manager import DataManager

CARD_BG   = '#FFFFFF'
PAGE_BG   = '#F0F4FA'
ACCENT    = '#4F8EF7'
GREEN     = '#27AE60'
ORANGE    = '#F39C12'
RED       = '#E74C3C'
PURPLE    = '#8E44AD'
DARK_TEXT = '#1E2A3A'
GRAY_TEXT = '#7F8C8D'


def make_kpi_card(title, value, subtitle, color):
    frame = QFrame()
    frame.setFixedHeight(110)
    frame.setStyleSheet(
        f'QFrame {{'
        f'background: {CARD_BG};'
        f'border-radius: 14px;'
        f'border-left: 6px solid {color};'
        f'}}'
    )
    lay = QVBoxLayout(frame)
    lay.setContentsMargins(18, 12, 18, 12)
    lay.setSpacing(2)
    t = QLabel(title)
    t.setFont(QFont('Segoe UI', 9))
    t.setStyleSheet(f'color: {GRAY_TEXT}; border: none;')
    v = QLabel(value)
    v.setFont(QFont('Segoe UI', 22, QFont.Bold))
    v.setStyleSheet(f'color: {DARK_TEXT}; border: none;')
    v.setObjectName('kpi_value')
    s = QLabel(subtitle)
    s.setFont(QFont('Segoe UI', 8))
    s.setStyleSheet(f'color: {color}; border: none;')
    lay.addWidget(t)
    lay.addWidget(v)
    lay.addWidget(s)
    return frame


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f'background: {PAGE_BG};')
        self.dm = DataManager()
        self._build_ui()
        QTimer.singleShot(500, self.refresh)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.refresh)
        self._timer.start(60000)

    def _build_ui(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(24, 20, 24, 20)
        main.setSpacing(18)
        tool_row = QHBoxLayout()
        title = QLabel('Dashboard Overview')
        title.setFont(QFont('Segoe UI', 17, QFont.Bold))
        title.setStyleSheet(f'color: {DARK_TEXT};')
        self._filter_cb = QComboBox()
        self._filter_cb.addItems(['Today', 'This Month', 'This Year', 'All Time'])
        self._filter_cb.setFixedSize(150, 36)
        self._filter_cb.setStyleSheet(
            'QComboBox { background: white; border: 1.5px solid #BDC3C7;'
            ' border-radius: 8px; padding: 4px 12px; font-size: 12px; }'
            'QComboBox::drop-down { border: none; }'
        )
        self._filter_cb.currentIndexChanged.connect(self.refresh)
        refresh_btn = QPushButton('Refresh')
        refresh_btn.setFixedSize(110, 36)
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.setStyleSheet(
            f'QPushButton {{ background: {ACCENT}; color: white;'
            f' border-radius: 8px; font-size: 12px; }}'
            f'QPushButton:hover {{ background: #3a7ae0; }}'
        )
        refresh_btn.clicked.connect(self.refresh)
        tool_row.addWidget(title)
        tool_row.addStretch()
        tool_row.addWidget(self._filter_cb)
        tool_row.addSpacing(8)
        tool_row.addWidget(refresh_btn)
        main.addLayout(tool_row)
        card_row = QHBoxLayout()
        card_row.setSpacing(16)
        self._card_total = make_kpi_card('Total Sales', '0', 'Filtered period', ACCENT)
        self._card_today = make_kpi_card('Todays Sales', '0', 'Today', GREEN)
        self._card_month = make_kpi_card('Monthly Sales', '0', 'This month', ORANGE)
        self._card_stock = make_kpi_card('Stock Net Worth', '0', 'Current inventory', PURPLE)
        for c in (self._card_total, self._card_today, self._card_month, self._card_stock):
            c.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            card_row.addWidget(c)
        main.addLayout(card_row)
        row1 = QHBoxLayout()
        row1.setSpacing(16)
        self._cv_trend = self._blank_chart_view('Sales Trend')
        self._cv_cat   = self._blank_chart_view('Sales by Category')
        row1.addWidget(self._cv_trend)
        row1.addWidget(self._cv_cat)
        main.addLayout(row1, stretch=3)
        row2 = QHBoxLayout()
        row2.setSpacing(16)
        self._cv_pay   = self._blank_chart_view('Payment Methods')
        self._cv_stock = self._blank_chart_view('Stock Levels')
        row2.addWidget(self._cv_pay)
        row2.addWidget(self._cv_stock)
        main.addLayout(row2, stretch=3)

    def _blank_chart_view(self, title=''):
        chart = QChart()
        chart.setTitle(title)
        chart.setBackgroundBrush(QColor(CARD_BG))
        chart.setBackgroundRoundness(14)
        chart.setTitleFont(QFont('Segoe UI', 11, QFont.Bold))
        chart.legend().setVisible(False)
        view = QChartView(chart)
        view.setRenderHint(QPainter.Antialiasing)
        view.setStyleSheet('border-radius: 14px; background: white;')
        view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return view

    def _make_chart(self, title):
        chart = QChart()
        chart.setTitle(title)
        chart.setBackgroundBrush(QColor(CARD_BG))
        chart.setBackgroundRoundness(14)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitleFont(QFont('Segoe UI', 11, QFont.Bold))
        return chart

    def _set_chart(self, view, chart):
        old = view.chart()
        view.setChart(chart)
        if old is not None:
            old.deleteLater()

    def refresh(self):
        try:
            df  = self.dm.load_sales()
            stk = self.dm.load_stocks()
            self._update_kpis(df, stk)
            self._draw_trend(df)
            self._draw_category(df)
            self._draw_payment(df)
            self._draw_stock(stk)
        except Exception as e:
            import traceback
            print(f'[HomePage.refresh] Error: {e}')
            traceback.print_exc()

    def _update_kpis(self, df, stk):
        filt  = self._filter_cb.currentText()
        now   = pd.Timestamp.now()
        today = now.normalize()
        def safe_sum(frame):
            if frame is None or frame.empty: return 0.0
            if 'total_spend' not in frame.columns: return 0.0
            return float(pd.to_numeric(frame['total_spend'], errors='coerce').fillna(0).sum())
        dff = pd.DataFrame()
        if not df.empty and 'purchase_date' in df.columns:
            df = df.copy()
            df['purchase_date'] = pd.to_datetime(df['purchase_date'], errors='coerce')
            if filt == 'Today':
                dff = df[df['purchase_date'] >= today]
            elif filt == 'This Month':
                dff = df[(df['purchase_date'].dt.month == now.month) & (df['purchase_date'].dt.year == now.year)]
            elif filt == 'This Year':
                dff = df[df['purchase_date'].dt.year == now.year]
            else:
                dff = df.copy()
        today_df = pd.DataFrame()
        month_df = pd.DataFrame()
        if not df.empty and 'purchase_date' in df.columns:
            today_df = df[df['purchase_date'] >= today]
            month_df = df[(df['purchase_date'].dt.month == now.month) & (df['purchase_date'].dt.year == now.year)]
        stock_worth = 0.0
        if not stk.empty:
            q = pd.to_numeric(stk.get('quantity',   pd.Series()), errors='coerce').fillna(0)
            p = pd.to_numeric(stk.get('unit_price', pd.Series()), errors='coerce').fillna(0)
            stock_worth = float((q * p).sum())
        self._set_kpi(self._card_total, f'{safe_sum(dff):,.0f}')
        self._set_kpi(self._card_today, f'{safe_sum(today_df):,.0f}')
        self._set_kpi(self._card_month, f'{safe_sum(month_df):,.0f}')
        self._set_kpi(self._card_stock, f'{stock_worth:,.0f}')

    @staticmethod
    def _set_kpi(frame, value):
        lbl = frame.findChild(QLabel, 'kpi_value')
        if lbl:
            lbl.setText(value)

    def _draw_trend(self, df):
        chart = self._make_chart('Sales Trend')
        filt  = self._filter_cb.currentText()
        cats  = []
        vals  = []
        if not df.empty and 'purchase_date' in df.columns:
            df2 = df.copy()
            df2['purchase_date'] = pd.to_datetime(df2['purchase_date'], errors='coerce')
            df2 = df2.dropna(subset=['purchase_date'])
            df2['total_spend'] = pd.to_numeric(df2['total_spend'], errors='coerce').fillna(0)
            if not df2.empty:
                if filt == 'Today':
                    df2['grp'] = df2['purchase_date'].dt.hour
                    grouped = df2.groupby('grp')['total_spend'].sum()
                    cats = [f'{h}:00' for h in range(0, 24, 2)]
                    vals = [float(grouped.get(h, 0)) for h in range(0, 24, 2)]
                elif filt == 'This Year':
                    mnames = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
                    df2['grp'] = df2['purchase_date'].dt.month
                    grouped = df2.groupby('grp')['total_spend'].sum()
                    cats = mnames
                    vals = [float(grouped.get(m + 1, 0)) for m in range(12)]
                else:
                    df2['grp'] = df2['purchase_date'].dt.to_period('D').astype(str)
                    grouped = df2.groupby('grp')['total_spend'].sum().tail(30)
                    cats = list(grouped.index)
                    vals = [float(v) for v in grouped.values]
        if len(vals) < 2:
            cats = ['No Data', '']
            vals = [0.0, 0.0]
        bs = QBarSet('Sales')
        bs.setColor(QColor(ACCENT))
        for v in vals:
            bs.append(v)
        bar = QBarSeries()
        bar.append(bs)
        chart.addSeries(bar)
        axis_x = QBarCategoryAxis()
        axis_x.append(cats)
        axis_x.setLabelsFont(QFont('Segoe UI', 7))
        chart.addAxis(axis_x, Qt.AlignBottom)
        bar.attachAxis(axis_x)
        axis_y = QValueAxis()
        axis_y.setLabelFormat('%.0f')
        axis_y.setLabelsFont(QFont('Segoe UI', 8))
        axis_y.setMin(0)
        chart.addAxis(axis_y, Qt.AlignLeft)
        bar.attachAxis(axis_y)
        chart.legend().setVisible(False)
        self._set_chart(self._cv_trend, chart)

    def _draw_category(self, df):
        chart  = self._make_chart('Sales by Category')
        colors = [ACCENT, GREEN, ORANGE, PURPLE, RED, '#16A085']
        if not df.empty and 'product_category' in df.columns:
            df2 = df.copy()
            df2['total_spend'] = pd.to_numeric(df2['total_spend'], errors='coerce').fillna(0)
            grp  = df2.groupby('product_category')['total_spend'].sum().nlargest(6)
            cats = list(grp.index)
            vals = [float(v) for v in grp.values]
        else:
            cats, vals = ['No Data'], [1.0]
        bar_series = QBarSeries()
        for i, (c, v) in enumerate(zip(cats, vals)):
            bs = QBarSet(c)
            bs.append(v)
            bs.setColor(QColor(colors[i % len(colors)]))
            bar_series.append(bs)
        chart.addSeries(bar_series)
        axis_x = QBarCategoryAxis()
        axis_x.append([''])
        axis_x.setLabelsFont(QFont('Segoe UI', 8))
        chart.addAxis(axis_x, Qt.AlignBottom)
        bar_series.attachAxis(axis_x)
        axis_y = QValueAxis()
        axis_y.setLabelFormat('%.0f')
        axis_y.setLabelsFont(QFont('Segoe UI', 8))
        axis_y.setMin(0)
        chart.addAxis(axis_y, Qt.AlignLeft)
        bar_series.attachAxis(axis_y)
        chart.legend().setVisible(True)
        chart.legend().setFont(QFont('Segoe UI', 8))
        self._set_chart(self._cv_cat, chart)

    def _draw_payment(self, df):
        chart  = self._make_chart('Payment Methods')
        colors = [ACCENT, GREEN, ORANGE, PURPLE, RED, '#16A085']
        series = QPieSeries()
        series.setHoleSize(0.42)
        if not df.empty and 'payment_method' in df.columns:
            df2 = df.copy()
            df2['total_spend'] = pd.to_numeric(df2['total_spend'], errors='coerce').fillna(0)
            grp = df2.groupby('payment_method')['total_spend'].sum()
            for i, (k, v) in enumerate(grp.items()):
                if v > 0:
                    sl = series.append(str(k), float(v))
                    sl.setColor(QColor(colors[i % len(colors)]))
                    sl.setLabelVisible(True)
                    sl.setLabel(f'{k}')
                    sl.setLabelFont(QFont('Segoe UI', 8))
        if series.count() == 0:
            sl = series.append('No Data', 1.0)
            sl.setColor(QColor('#BDC3C7'))
        chart.addSeries(series)
        chart.legend().setVisible(True)
        chart.legend().setFont(QFont('Segoe UI', 8))
        self._set_chart(self._cv_pay, chart)

    def _draw_stock(self, stk):
        chart = self._make_chart('Stock Levels Top 8')
        if not stk.empty and 'quantity' in stk.columns:
            stk2 = stk.copy()
            stk2['quantity'] = pd.to_numeric(stk2['quantity'], errors='coerce').fillna(0)
            top   = stk2.nlargest(8, 'quantity')
            names = [str(n) for n in top['product_name'].tolist()]
            qtys  = [float(q) for q in top['quantity'].tolist()]
        else:
            names = ['No Stock']
            qtys  = [0.0]
        bs = QBarSet('Quantity')
        bs.setColor(QColor(PURPLE))
        for q in qtys:
            bs.append(q)
        bar = QBarSeries()
        bar.append(bs)
        chart.addSeries(bar)
        axis_x = QBarCategoryAxis()
        axis_x.append(names)
        axis_x.setLabelsFont(QFont('Segoe UI', 7))
        axis_x.setLabelsAngle(-30)
        chart.addAxis(axis_x, Qt.AlignBottom)
        bar.attachAxis(axis_x)
        axis_y = QValueAxis()
        axis_y.setLabelFormat('%d')
        axis_y.setLabelsFont(QFont('Segoe UI', 8))
        axis_y.setMin(0)
        chart.addAxis(axis_y, Qt.AlignLeft)
        bar.attachAxis(axis_y)
        chart.legend().setVisible(False)
        self._set_chart(self._cv_stock, chart)
