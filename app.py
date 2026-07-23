import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os

# Настройка страницы
st.set_page_config(
    page_title="КРАЙВИН - анализ экономической эффективности", 
    page_icon="🍷", 
    layout="wide"
)

st.title("КРАЙВИН: Анализ денежных потоков и рентабельности")
st.markdown("Интерактивная финансовая модель для сценарного анализа кассовых разрывов.")

# --- БОКОВАЯ ПАНЕЛЬ (ВВОД ДАННЫХ) ---

# Добавление логотипа компании
logo_path = "КРАЙВИН лого винный квадрат.png"
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)
else:
    st.sidebar.info("💡 Загрузите файл 'КРАЙВИН лого винный квадрат.png' в папку с кодом для отображения логотипа.")

st.sidebar.header("Параметры модели")

# Календарные настройки
ru_months_full = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
col_m, col_y = st.sidebar.columns(2)
start_month_idx = col_m.selectbox("Месяц старта", range(12), format_func=lambda x: ru_months_full[x])
start_year = col_y.selectbox("Год старта", [2026, 2027])

margin_pct = st.sidebar.slider("Маржинальность (%)", min_value=10, max_value=50, value=20, step=1)
period = st.sidebar.selectbox("Горизонт планирования (мес)", [6, 12, 18, 24])

initial_investment = st.sidebar.number_input(
    "Доступный капитал / Инвестиции (руб)", 
    value=7_000_000, 
    step=500_000
)

st.sidebar.subheader("Динамика продаж")
aov = st.sidebar.number_input("Средняя сумма заказа (руб)", value=150_000, step=10_000)
start_orders = st.sidebar.number_input("Заказов в 1-й месяц (шт)", value=40, step=1)
orders_growth = st.sidebar.slider("Ежемесячный прирост заказов (%)", 0, 100, 15, step=1)

st.sidebar.subheader("Работа с поставщиками")
prepayment_pct = st.sidebar.slider("Предоплата поставщикам (%)", 0, 100, 50, step=10)
delay_days = st.sidebar.slider("Отсрочка на остаток (дней)", 0, 90, 40, step=5)

st.sidebar.subheader("Факторинг")
factoring_share = st.sidebar.slider("Доля выручки в факторинге (%)", 0, 100, 50, step=10)
factoring_advance = st.sidebar.slider("Аванс от фактора (%)", 50, 100, 80, step=5)

# --- РАСЧЕТНАЯ ЧАСТЬ (МАТЕМАТИКА) ---

# Генерация подписей для оси X (Месяц Год)
ru_months_short = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
x_labels = []
for i in range(period):
    m_idx = (start_month_idx + i) % 12
    y_offset = (start_month_idx + i) // 12
    x_labels.append(f"{ru_months_short[m_idx]} {start_year + y_offset}")

# Динамический расчет выручки через заказы и чек
orders = np.zeros(period)
rev = np.zeros(period)

for i in range(period):
    if i == 0:
        orders[i] = start_orders
    else:
        # Увеличиваем количество заказов на заданный процент
        orders[i] = orders[i-1] * (1 + (orders_growth / 100))
    
    # Выручка = кол-во заказов * средний чек
    rev[i] = orders[i] * aov

cogs_pct = 1 - (margin_pct / 100)
cogs_no_vat = rev * cogs_pct
cogs_vat = cogs_no_vat * 1.2

# Симуляция выплат поставщикам
delay_months = max(1, int(round(delay_days / 30))) if delay_days > 0 else 0
cogs_payments = np.zeros(period)

for i in range(period):
    # Предоплата
    cogs_payments[i] += cogs_vat[i] * (prepayment_pct / 100)
    # Постоплата
    if i + delay_months < period:
        cogs_payments[i + delay_months] += cogs_vat[i] * ((100 - prepayment_pct) / 100)

# Симуляция поступлений (Факторинг + Прямые платежи)
inflows = np.zeros(period)
for i in range(period):
    inflows[i] += rev[i] * 1.2 * (factoring_share / 100) * (factoring_advance / 100)
    
    if i + 2 < period:
        inflows[i + 2] += rev[i] * 1.2 * ((100 - factoring_share) / 100)
        inflows[i + 2] += rev[i] * 1.2 * (factoring_share / 100) * ((100 - factoring_advance) / 100)

# Операционные расходы
opex = np.full(period, 650_000)
for i in range(6, period):
    opex[i] = 850_000
taxes_and_commissions = rev * 0.05

outflows = cogs_payments + opex + taxes_and_commissions
net_cf = inflows - outflows

# Накопленный итог
cum_cf = np.cumsum(net_cf)
cash_balance = cum_cf + initial_investment

# --- KPI МЕТРИКИ ---
max_deficit = min(min(cum_cf), 0)
net_profit = sum(rev * (margin_pct / 100)) - sum(opex) - sum(taxes_and_commissions)
roi = (net_profit / sum(rev)) * 100 if sum(rev) > 0 else 0

# Функция для пробелов в метриках
def format_rub(val):
    return f"{val:,.0f}".replace(",", " ") + " руб."

# Выводим 4 метрики
col1, col2, col3, col4 = st.columns(4)
col1.metric(f"Выручка (за {period} мес)", format_rub(sum(rev)))
col2.metric("Макс. кассовый разрыв", format_rub(max_deficit))
col3.metric("Чистая прибыль", format_rub(net_profit))
col4.metric("Рентабельность по ЧП", f"{roi:.1f}%")

st.divider()

# --- ВИЗУАЛИЗАЦИЯ (ГРАФИКИ PLOTLY) ---
st.subheader("Динамика ликвидности и остаток средств")

fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=x_labels, 
    y=cash_balance, 
    mode='lines+markers', 
    name='Остаток ДС',
    line=dict(color='#642A38', width=3), # Уточненный фирменный винный
    fill='tozeroy',
    fillcolor='rgba(100, 42, 56, 0.1)', # Соответствующая полупрозрачная заливка
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
    x=x_labels, y=inflows, name='Поступления', marker_color='#E3C293', # Фирменный песочный
    hovertemplate='%{y:,.0f} руб.<extra></extra>'
))
fig2.add_trace(go.Bar(
    x=x_labels, y=-outflows, name='Выплаты', marker_color='#642A38', # Уточненный фирменный винный
    hovertemplate='%{y:,.0f} руб.<extra></extra>'
))
fig2.add_trace(go.Scatter(
    x=x_labels, y=net_cf, name='Чистый поток', marker_color='#B88645', # Темно-песочный (бронза)
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
