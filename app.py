import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os
import io

# Импорт библиотеки для генерации PowerPoint
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

# Настройка страницы
st.set_page_config(
    page_title="КРАЙВИН - анализ экономической эффективности", 
    page_icon="🍷", 
    layout="wide"
)

st.title("КРАЙВИН: Анализ денежных потоков и рентабельности")
st.markdown("Интерактивная финансовая модель для сценарного анализа кассовых разрывов.")

# --- БОКОВАЯ ПАНЕЛЬ (ВВОД ДАННЫХ) ---

logo_path = "КРАЙВИН лого винный квадрат.png"
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)
else:
    st.sidebar.info("💡 Загрузите файл 'КРАЙВИН лого винный квадрат.png' в папку с кодом для отображения логотипа.")

st.sidebar.header("Параметры модели")

ru_months_full = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
col_m, col_y = st.sidebar.columns(2)
start_month_idx = col_m.selectbox("Месяц старта", range(12), format_func=lambda x: ru_months_full[x])
start_year = col_y.selectbox("Год старта", [2026, 2027])

margin_pct = st.sidebar.slider("Маржинальность (%)", min_value=10, max_value=50, value=20, step=1)
period = st.sidebar.selectbox("Горизонт планирования (мес)", [6, 12, 18, 24])

st.sidebar.subheader("Стартовый капитал и закупки")
initial_purchase = st.sidebar.number_input("Первоначальная закупка товара (руб)", value=5_000_000, step=500_000)
initial_cash_buffer = st.sidebar.number_input("Стартовый денежный буфер (на счете)", value=2_000_000, step=500_000)

st.sidebar.subheader("Динамика продаж")
aov = st.sidebar.number_input("Средняя сумма заказа (руб)", value=150_000, step=10_000)
start_orders = st.sidebar.number_input("Заказов в 1-й месяц (шт)", value=40, step=1)
orders_growth = st.sidebar.slider("Ежемесячный прирост заказов (%)", 0, 100, 15, step=1)
scale_factor = st.sidebar.slider("Коэффициент масштабирования продаж", 0.5, 3.0, 1.0, 0.1)

st.sidebar.subheader("Команда и расходы")
monthly_fot = st.sidebar.number_input("ФОТ в месяц (руб)", value=500_000, step=50_000)

st.sidebar.subheader("Работа с поставщиками")
prepayment_pct = st.sidebar.slider("Предоплата поставщикам (%)", 0, 100, 50, step=10)
delay_days = st.sidebar.slider("Отсрочка на остаток (дней)", 0, 90, 40, step=5)

st.sidebar.subheader("Факторинг")
factoring_share = st.sidebar.slider("Доля выручки в факторинге (%)", 0, 100, 50, step=10)
factoring_advance = st.sidebar.slider("Аванс от фактора (%)", 50, 100, 80, step=5)

st.sidebar.subheader("Условия с покупателями")
customer_delay_days = st.sidebar.slider("Отсрочка платежа покупателям (дней)", 0, 120, 70, step=5)

# --- РАСЧЕТНАЯ ЧАСТЬ (МАТЕМАТИКА) ---

ru_months_short = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
x_labels = []
for i in range(period):
    m_idx = (start_month_idx + i) % 12
    y_offset = (start_month_idx + i) // 12
    x_labels.append(f"{ru_months_short[m_idx]} {start_year + y_offset}")

orders = np.zeros(period)
rev = np.zeros(period)

for i in range(period):
    if i == 0:
        orders[i] = start_orders * scale_factor
    else:
        orders[i] = orders[i-1] * (1 + (orders_growth / 100))
    rev[i] = orders[i] * aov

cogs_pct = 1 - (margin_pct / 100)
cogs_no_vat = rev * cogs_pct
cogs_vat = cogs_no_vat * 1.2

delay_months_suppliers = max(1, int(round(delay_days / 30))) if delay_days > 0 else 0
cogs_payments = np.zeros(period)

for i in range(period):
    cogs_payments[i] += cogs_vat[i] * (prepayment_pct / 100)
    if i + delay_months_suppliers < period:
        cogs_payments[i + delay_months_suppliers] += cogs_vat[i] * ((100 - prepayment_pct) / 100)

initial_prep = initial_purchase * (prepayment_pct / 100)
initial_post = initial_purchase * ((100 - prepayment_pct) / 100)

cogs_payments[0] += initial_prep
if delay_months_suppliers < period:
    cogs_payments[delay_months_suppliers] += initial_post

customer_delay_months = max(0, int(round(customer_delay_days / 30)))

inflows = np.zeros(period)
for i in range(period):
    inflows[i] += rev[i] * 1.2 * (factoring_share / 100) * (factoring_advance / 100)
    
    target_month = i + customer_delay_months
    if target_month < period:
        inflows[target_month] += rev[i] * 1.2 * ((100 - factoring_share) / 100)
        inflows[target_month] += rev[i] * 1.2 * (factoring_share / 100) * ((100 - factoring_advance) / 100)

base_other_opex = 150_000
opex = np.full(period, base_other_opex + monthly_fot)
for i in range(6, period):
    opex[i] = (base_other_opex * 1.2) + monthly_fot

taxes_and_commissions = rev * 0.05

outflows = cogs_payments + opex + taxes_and_commissions
net_cf = inflows - outflows

cum_cf = np.cumsum(net_cf)
cash_balance = cum_cf + initial_cash_buffer

# --- KPI МЕТРИКИ ---
max_deficit = min(min(cum_cf), 0)
net_profit = sum(rev * (margin_pct / 100)) - sum(opex) - sum(taxes_and_commissions) - (initial_purchase * 0.15)
roi = (net_profit / sum(rev)) * 100 if sum(rev) > 0 else 0

def format_rub(val):
    return f"{val:,.0f}".replace(",", " ") + " руб."

col1, col2, col3, col4 = st.columns(4)
col1.metric(f"Выручка (за {period} мес)", format_rub(sum(rev)))
col2.metric("Макс. кассовый разрыв", format_rub(max_deficit))
col3.metric("Чистая прибыль", format_rub(net_profit))
col4.metric("Рентабельность по ЧП", f"{roi:.1f}%")

st.divider()

# --- ФУНКЦИЯ ГЕНЕРАЦИИ ПРЕЗЕНТАЦИИ (POWERPOINT) ---
def generate_pptx():
    prs = Presentation()
    
    # Цвета бренда КРАЙВИН
    wine_color = RGBColor(100, 42, 56)   # #642A38
    sand_color = RGBColor(227, 194, 147) # #E3C293
    dark_gray = RGBColor(50, 50, 50)
    
    # Слайд 1: Титульный
    slide_layout = prs.slide_layouts[0] # Заголовочный слайд
    slide1 = prs.slides.add_slide(slide_layout)
    title = slide1.shapes.title
    subtitle = slide1.placeholders[1]
    
    title.text = "КРАЙВИН"
    subtitle.text = f"Анализ экономической эффективности и денежных потоков\nПериод планирования: {period} месяцев (Старт: {ru_months_full[start_month_idx]} {start_year})"
    
    # Слайд 2: Ключевые финансовые показатели
    slide_layout_2 = prs.slide_layouts[1] # Заголовок и содержимое
    slide2 = prs.slides.add_slide(slide_layout_2)
    slide2.shapes.title.text = "Ключевые финансовые результаты"
    
    tf = slide2.placeholders[1].text_frame
    tf.text = f"• Общая выручка за период: {format_rub(sum(rev))}"
    
    p2 = tf.add_paragraph()
    p2.text = f"• Максимальный кассовый разрыв: {format_rub(max_deficit)}"
    
    p3 = tf.add_paragraph()
    p3.text = f"• Чистая прибыль: {format_rub(net_profit)}"
    
    p4 = tf.add_paragraph()
    p4.text = f"• Рентабельность по чистой прибыли: {roi:.1f}%"

    p5 = tf.add_paragraph()
    p5.text = f"• Начальный денежный буфер: {format_rub(initial_cash_buffer)}"

    # Слайд 3: Таблица по месяцам
    slide3 = prs.slides.add_slide(slide_layout_2)
    slide3.shapes.title.text = "Детализация по месяцам"
    
    # Создаем таблицу в презентации
    rows = period + 1
    cols = 5
    left = Inches(0.5)
    top = Inches(1.5)
    width = Inches(9.0)
    height = Inches(4.5)
    
    table_shape = slide3.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table
    
    # Шапка таблицы
    headers = ["Месяц", "Выручка", "Поступления", "Выплаты", "Остаток ДС"]
    for col_idx, text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = text
        
    # Заполнение строк таблицы данными
    for i in range(period):
        table.cell(i+1, 0).text = str(x_labels[i])
        table.cell(i+1, 1).text = f"{rev[i]:,.0f}".replace(",", " ")
        table.cell(i+1, 2).text = f"{inflows[i]:,.0f}".replace(",", " ")
        table.cell(i+1, 3).text = f"{outflows[i]:,.0f}".replace(",", " ")
        table.cell(i+1, 4).text = f"{cash_balance[i]:,.0f}".replace(",", " ")

    # Сохранение во временный буфер памяти
    ppt_io = io.BytesIO()
    prs.save(ppt_io)
    ppt_io.seek(0)
    return ppt_io

# Кнопка скачивания презентации в интерфейсе
st.sidebar.divider()
st.sidebar.subheader("Экспорт отчета")
if st.sidebar.button("📥 Скачать презентацию (PPTX)"):
    pptx_data = generate_pptx()
    st.sidebar.download_button(
        label="💾 Нажмите для сохранения файла",
        data=pptx_data,
        file_name="Kraivin_Financial_Report.pptx",
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )

# --- ВИЗУАЛИЗАЦИЯ (ГРАФИКИ PLOTLY) ---
st.subheader("Динамика ликвидности и остаток средств")

fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=x_labels, 
    y=cash_balance, 
    mode='lines+markers', 
    name='Остаток ДС',
    line=dict(color='#642A38', width=3),
    fill='tozeroy',
    fillcolor='rgba(100, 42, 56, 0.1)',
    hovertemplate='%{y:,.0f} руб.<extra></extra>'
))
fig1.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Дефицит")
fig1.update_layout(
    xaxis_title="Месяц", 
    yaxis_title="Рубли", 
    hovermode="x unified",
    separators=", "
)
fig1.update_yaxes(tickformat=",.0f")
st.plotly_chart(fig1, use_container_width=True)


st.subheader("Структура месячного денежного потока")
fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=x_labels, y=inflows, name='Поступления', marker_color='#E3C293',
    hovertemplate='%{y:,.0f} руб.<extra></extra>'
))
fig2.add_trace(go.Bar(
    x=x_labels, y=-outflows, name='Выплаты', marker_color='#642A38',
    hovertemplate='%{y:,.0f} руб.<extra></extra>'
))
fig2.add_trace(go.Scatter(
    x=x_labels, y=net_cf, name='Чистый поток', marker_color='#B88645',
    mode='lines+markers',
    hovertemplate='%{y:,.0f} руб.<extra></extra>'
))

fig2.update_layout(
    barmode='relative', 
    xaxis_title="Месяц", 
    yaxis_title="Рубли", 
    hovermode="x unified",
    separators=", "
)
fig2.update_yaxes(tickformat=",.0f")
st.plotly_chart(fig2, use_container_width=True)
