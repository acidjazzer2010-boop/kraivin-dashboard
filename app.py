import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Настройка страницы
st.set_page_config(page_title="КРАЙВИН - анализ экономической эффективности", layout="wide")
st.title("КРАЙВИН: Анализ денежных потоков и рентабельности")
st.markdown("Интерактивная финансовая модель для сценарного анализа кассовых разрывов.")

# --- БОКОВАЯ ПАНЕЛЬ (ВВОД ДАННЫХ) ---
st.sidebar.header("Параметры модели")
margin_pct = st.sidebar.slider("Маржинальность (%)", min_value=10, max_value=50, value=20, step=1)
period = st.sidebar.selectbox("Горизонт планирования (мес)", [6, 12, 18, 24])

# Оставляем точный ручной ввод для инвестиций
initial_investment = st.sidebar.number_input(
    "Доступный капитал / Инвестиции (руб)", 
    value=7_000_000, 
    step=500_000
)

st.sidebar.subheader("Работа с поставщиками")
prepayment_pct = st.sidebar.slider("Предоплата поставщикам (%)", 0, 100, 50, step=10)
delay_days = st.sidebar.slider("Отсрочка на остаток (дней)", 0, 90, 40, step=5)

st.sidebar.subheader("Факторинг")
factoring_share = st.sidebar.slider("Доля выручки в факторинге (%)", 0, 100, 50, step=10)
factoring_advance = st.sidebar.slider("Аванс от фактора (%)", 50, 100, 80, step=5)

# --- РАСЧЕТНАЯ ЧАСТЬ (МАТЕМАТИКА) ---
# Базовая выручка с плавным ростом
base_rev = [
    6_000_000, 
    8_400_000, 
    12_000_000, 
    14_400_000, 
    16_800_000, 
    18_000_000
]
rev = np.zeros(period)
for i in range(period):
    if i < len(base_rev):
        rev[i] = base_rev[i]
    else:
        rev[i] = rev[i-1] * 1.05 # Рост 5% в месяц после 6-го месяца

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

col1, col2, col3 = st.columns(3)
col1.metric("Максимальный кассовый разрыв", format_rub(max_deficit))
col2.metric(f"Чистая прибыль (за {period} мес)", format_rub(net_profit))
col3.metric("Рентабельность по ЧП", f"{roi:.1f}%")

st.divider()

# --- ВИЗУАЛИЗАЦИЯ (ГРАФИКИ PLOTLY) ---
st.subheader("Динамика ликвидности и остаток средств")

fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=list(range(1, period + 1)), 
    y=cash_balance, 
    mode='lines+markers', 
    name='Остаток ДС',
    line=dict(color='blue', width=3),
    fill='tozeroy',
    fillcolor='rgba(0, 0, 255, 0.1)',
    hovertemplate='%{y:,.0f} руб.<extra></extra>'
))
fig1.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Дефицит")
fig1.update_layout(
    xaxis_title="Месяц", 
    yaxis_title="Рубли", 
    hovermode="x unified",
    separators=", " # Заменяет запятую на пробел для тысяч
)
fig1.update_yaxes(tickformat=",.0f")
st.plotly_chart(fig1, use_container_width=True)


st.subheader("Структура месячного денежного потока")
fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=list(range(1, period + 1)), y=inflows, name='Поступления', marker_color='#2ca02c',
    hovertemplate='%{y:,.0f} руб.<extra></extra>'
))
fig2.add_trace(go.Bar(
    x=list(range(1, period + 1)), y=-outflows, name='Выплаты', marker_color='#d62728',
    hovertemplate='%{y:,.0f} руб.<extra></extra>'
))
fig2.add_trace(go.Scatter(
    x=list(range(1, period + 1)), y=net_cf, name='Чистый поток', marker_color='orange', mode='lines+markers',
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
