import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os
import re

from exporter import generate_html_report_bytes, send_report_to_email

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(
    page_title="Kraivin Financial Analytics", 
    page_icon="🍷", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ГЛУБОКАЯ ЧЕРНАЯ ТЕМА С ВЫСОКИМ КОНТРАСТОМ ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"], .stMarkdown {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #f4f4f5 !important;
        letter-spacing: -0.01em;
    }

    /* Фон приложения */
    .stApp {
        background-color: #09090b !important;
    }

    /* Боковая панель */
    section[data-testid="stSidebar"] {
        background-color: #121217 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    section[data-testid="stSidebar"] * {
        color: #e4e4e7 !important;
    }

    /* Карточки метрик (Dark Glass) */
    .dark-kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
        gap: 16px;
        margin-bottom: 28px;
    }

    .dark-card {
        background: #14141b;
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 20px 22px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .dark-card:hover {
        transform: translateY(-2px);
        border-color: rgba(255, 255, 255, 0.25);
    }

    .dark-card-label {
        font-size: 12px;
        font-weight: 600;
        color: #a1a1aa !important;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .dark-card-value {
        font-size: 26px;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #ffffff !important;
        text-shadow: 0 2px 8px rgba(0,0,0,0.5);
    }

    .dark-card-sub {
        font-size: 12px;
        font-weight: 500;
        margin-top: 6px;
    }

    /* Переходы между вкладками */
    @keyframes darkTabFade {
        from {
            opacity: 0;
            transform: translateY(6px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    div[data-baseweb="tab-panel"] {
        animation: darkTabFade 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards !important;
    }

    /* Навигация табов */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #181820;
        padding: 5px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 24px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 18px;
        font-size: 13px;
        font-weight: 600;
        color: #a1a1aa !important;
        background-color: transparent !important;
        border: none !important;
        transition: all 0.2s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #ffffff !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #272732 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }

    /* Инпуты в сайдбаре */
    .stTextInput input, .stSelectbox select, .stNumberInput input {
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        background: #1c1c24 !important;
        color: #ffffff !important;
        font-weight: 500 !important;
    }

    .stTextInput input:focus, .stSelectbox select:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3) !important;
    }

    /* Кнопки */
    .stButton button, .stDownloadButton button {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        padding: 10px 22px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
    }

    .stButton button:hover, .stDownloadButton button:hover {
        background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
        transform: translateY(-1px);
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ФОРМАТИРОВАНИЯ ---
def format_num_spaced(val: float) -> str:
    """Форматирует число с разделителями тысяч через пробел."""
    return f"{int(round(val)):,}".replace(",", " ")

def money_input(label: str, default_val: int, key: str, help_text: str = None) -> int:
    """Инпут с белым контрастным отображением суммы."""
    if key not in st.session_state:
        st.session_state[key] = format_num_spaced(default_val)
    
    raw_val = st.sidebar.text_input(label, value=st.session_state[key], key=f"raw_{key}", help=help_text)
    clean_val = re.sub(r"[^\d]", "", raw_val)
    if not clean_val:
        clean_val = str(default_val)
    
    parsed_int = int(clean_val)
    formatted_str = format_num_spaced(parsed_int)
    st.session_state[key] = formatted_str
    
    st.sidebar.markdown(
        f"<div style='font-size: 11px; color: #a1a1aa; margin-top: -12px; margin-bottom: 12px;'>"
        f"Выбрано: <span style='color: #60a5fa; font-weight: 600;'>{formatted_str} ₽</span></div>", 
        unsafe_allow_html=True
    )
    return parsed_int

# --- БОКОВАЯ ПАНЕЛЬ (ВВОД ДАННЫХ) ---
st.sidebar.markdown("<h2 style='font-size: 18px; font-weight: 700; color: #ffffff; margin-bottom: 18px;'>Параметры модели</h2>", unsafe_allow_html=True)

ru_months_full = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
col_m, col_y = st.sidebar.columns(2)
start_month_idx = col_m.selectbox("Месяц старта", range(12), index=9, format_func=lambda x: ru_months_full[x])
start_year = col_y.selectbox("Год", [2026, 2027], index=0)

margin_pct = st.sidebar.slider("Маржинальность (%)", min_value=10, max_value=50, value=20, step=1)
period = st.sidebar.selectbox("Горизонт планирования", [6, 12, 18, 24], format_func=lambda x: f"{x} месяцев")

st.sidebar.markdown("<div style='height: 1px; background: rgba(255,255,255,0.08); margin: 16px 0;'></div>", unsafe_allow_html=True)
st.sidebar.markdown("<div style='font-size: 11px; font-weight: 700; text-transform: uppercase; color: #a1a1aa; margin-bottom: 10px;'>Товар & Капитал</div>", unsafe_allow_html=True)

initial_purchase = money_input("Стартовая закупка (₽)", default_val=25_000_000, key="init_purchase_key")
batch_cycle_months = st.sidebar.number_input("Цикл склада (мес)", value=5, min_value=1, max_value=12, step=1)

col_cb, col_comm = st.sidebar.columns(2)
cb_rate = col_cb.number_input("Ставка ЦБ (%)", value=17.0, step=0.5)
comm_margin = col_comm.number_input("Маржа (%)", value=2.0, step=0.5)
total_interest_rate_annual = cb_rate + comm_margin

st.sidebar.markdown("<div style='height: 1px; background: rgba(255,255,255,0.08); margin: 16px 0;'></div>", unsafe_allow_html=True)
st.sidebar.markdown("<div style='font-size: 11px; font-weight: 700; text-transform: uppercase; color: #a1a1aa; margin-bottom: 10px;'>Динамика продаж</div>", unsafe_allow_html=True)

aov = money_input("Средний чек AOV (₽)", default_val=150_000, key="aov_key")
start_orders = st.sidebar.number_input("Заказов в 1-й месяц", value=40, step=1, min_value=1)
growth_type = st.sidebar.radio("Логика прироста заказов", ["В штуках (+N/мес)", "В процентах (%/мес)"], index=0)

if growth_type == "В штуках (+N/мес)":
    orders_growth_abs = st.sidebar.slider("Прирост заказов (шт/мес)", 0, 100, 5, 1)
    orders_growth_pct = 0
else:
    orders_growth_pct = st.sidebar.slider("Прирост заказов (%/мес)", 0, 100, 10, 1)
    orders_growth_abs = 0

max_orders_cap = st.sidebar.number_input("Потолок заказов в месяц", value=300, step=10)

st.sidebar.markdown("<div style='height: 1px; background: rgba(255,255,255,0.08); margin: 16px 0;'></div>", unsafe_allow_html=True)
st.sidebar.markdown("<div style='font-size: 11px; font-weight: 700; text-transform: uppercase; color: #a1a1aa; margin-bottom: 10px;'>Постоянные расходы</div>", unsafe_allow_html=True)

monthly_fot = money_input("ФОТ в месяц (₽)", default_val=500_000, key="fot_key")
monthly_warehouse = money_input("Аренда склада (₽)", default_val=200_000, key="wh_key")
monthly_office = money_input("Аренда офиса (₽)", default_val=150_000, key="office_key")

vat_rate_pct = 22
vat_multiplier = 1 + (vat_rate_pct / 100)
prepayment_pct = 50
delay_days = 40
factoring_share = 50
factoring_advance = 80
customer_delay_days = 70
initial_cash_buffer = 0

# --- РАСЧЕТНАЯ ЧАСТЬ ---
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
        calculated_orders = float(start_orders)
    else:
        if growth_type == "В штуках (+N/мес)":
            calculated_orders = orders[i-1] + orders_growth_abs
        else:
            calculated_orders = orders[i-1] * (1 + (orders_growth_pct / 100))
    orders[i] = min(calculated_orders, float(max_orders_cap))
    rev[i] = orders[i] * aov

cogs_pct = 1 - (margin_pct / 100)
cogs_no_vat = rev * cogs_pct
cogs_vat = cogs_no_vat * vat_multiplier

delay_months_suppliers = max(1, int(round(delay_days / 30))) if delay_days > 0 else 0
cogs_payments = np.zeros(period)
inventory_deliveries = np.zeros(period)

initial_prep = initial_purchase * (prepayment_pct / 100)
initial_post = initial_purchase * ((100 - prepayment_pct) / 100)
cogs_payments[0] += initial_prep
if delay_months_suppliers < period:
    cogs_payments[delay_months_suppliers] += initial_post
inventory_deliveries[0] = initial_purchase

for batch_start in range(batch_cycle_months, period, batch_cycle_months):
    batch_end = min(batch_start + batch_cycle_months, period)
    needed_batch_cogs = float(np.sum(cogs_vat[batch_start:batch_end]))
    inventory_deliveries[batch_start] = needed_batch_cogs
    
    cogs_payments[batch_start] += needed_batch_cogs * (prepayment_pct / 100)
    post_pay_m = batch_start + delay_months_suppliers
    if post_pay_m < period:
        cogs_payments[post_pay_m] += needed_batch_cogs * ((100 - prepayment_pct) / 100)

inventory_balance = np.zeros(period)
curr_inv = 0.0
for i in range(period):
    curr_inv += inventory_deliveries[i] - cogs_vat[i]
    inventory_balance[i] = max(curr_inv, 0.0)

customer_delay_months = max(0, int(round(customer_delay_days / 30)))
inflows = np.zeros(period)
for i in range(period):
    inflows[i] += rev[i] * vat_multiplier * (factoring_share / 100) * (factoring_advance / 100)
    target_month = i + customer_delay_months
    if target_month < period:
        inflows[target_month] += rev[i] * vat_multiplier * ((100 - factoring_share) / 100)
        inflows[target_month] += rev[i] * vat_multiplier * (factoring_share / 100) * ((100 - factoring_advance) / 100)

base_other_opex = 150_000
fixed_infrastructure_opex = monthly_warehouse + monthly_office
base_total_non_fot_opex = base_other_opex + fixed_infrastructure_opex

opex = np.full(period, base_total_non_fot_opex + monthly_fot)
for i in range(6, period):
    opex[i] = (base_total_non_fot_opex * 1.2) + monthly_fot

taxes_and_commissions = rev * 0.05
base_outflows = cogs_payments + opex + taxes_and_commissions

# Логика долгового фондирования
monthly_interest_rate = (total_interest_rate_annual / 100.0) / 12.0
monthly_investments = np.zeros(period)
interest_payments = np.zeros(period)
debt_repayments = np.zeros(period)
debt_balance = np.zeros(period)
funded_cash_balance = np.zeros(period)

current_debt = 0.0
curr_cash = 0.0

for i in range(period):
    interest_due = current_debt * monthly_interest_rate
    interest_payments[i] = interest_due
    net_before_financing = inflows[i] - (base_outflows[i] + interest_due)
    potential_cash = curr_cash + net_before_financing
    
    if potential_cash < 0:
        needed_injection = abs(potential_cash)
        monthly_investments[i] = needed_injection
        current_debt += needed_injection
        curr_cash = 0.0
        debt_repayments[i] = 0.0
    else:
        monthly_investments[i] = 0.0
        repay_amount = min(potential_cash, current_debt)
        debt_repayments[i] = repay_amount
        current_debt -= repay_amount
        curr_cash = potential_cash - repay_amount
        
    debt_balance[i] = current_debt
    funded_cash_balance[i] = curr_cash

total_outflows = base_outflows + interest_payments
total_interest_paid = np.sum(interest_payments)
total_investments_injected = np.sum(monthly_investments)
max_debt_peak = np.max(debt_balance)

net_profit = sum(rev * (margin_pct / 100)) - sum(opex) - sum(taxes_and_commissions) - total_interest_paid
roi = (net_profit / sum(rev)) * 100 if sum(rev) > 0 else 0

# --- СТИЛЬ ГРАФИКОВ ДЛЯ ТЕМНОЙ ТЕМЫ (ЧЕТКИЙ И КОНТРАСТНЫЙ) ---
def apply_dark_chart_layout(fig, height=440):
    fig.update_layout(
        height=height,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=30, b=30, l=10, r=10),
        font=dict(family='Inter, sans-serif', color='#d4d4d8', size=12),
        hoverlabel=dict(
            bgcolor="#18181b",
            bordercolor="rgba(255,255,255,0.2)",
            font=dict(color='#ffffff', size=12)
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            linecolor='rgba(255,255,255,0.15)',
            tickfont=dict(color='#a1a1aa')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.07)',
            zeroline=False,
            tickfont=dict(color='#a1a1aa')
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="left",
            x=0,
            font=dict(color='#f4f4f5', size=12)
        )
    )
    return fig

# --- ЗАГОЛОВОК СТРАНИЦЫ ---
st.markdown("""
<div style="margin-top: 10px; margin-bottom: 24px;">
    <div style="display: inline-block; font-size: 11px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #60a5fa; background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.3); padding: 4px 12px; border-radius: 999px; margin-bottom: 8px;">
        Dark Pro Edition • 2026
    </div>
    <h1 style="font-size: 34px; font-weight: 700; letter-spacing: -0.02em; color: #ffffff; margin: 0 0 6px 0;">
        Ликвидность, Кассовые разрывы & Кредитная нагрузка
    </h1>
    <p style="font-size: 15px; color: #a1a1aa; margin: 0; font-weight: 400;">
        Моделирование потребности в дотациях по ставке ЦБ РФ 17.0% + 2.0% коммерческой маржи
    </p>
</div>
""", unsafe_allow_html=True)

# --- БЛОК KPI КАРТОЧЕК (ЧЕТКИЕ БЕЛЫЕ ЦИФРЫ) ---
st.markdown(f"""
<div class="dark-kpi-container">
    <div class="dark-card">
        <div class="dark-card-label">Выручка ({period} мес)</div>
        <div class="dark-card-value">{format_num_spaced(sum(rev))} ₽</div>
        <div class="dark-card-sub" style="color: #60a5fa;">Маржинальность {margin_pct}%</div>
    </div>
    <div class="dark-card">
        <div class="dark-card-label">Требуемые дотации</div>
        <div class="dark-card-value" style="color: #f87171 !important;">{format_num_spaced(total_investments_injected)} ₽</div>
        <div class="dark-card-sub" style="color: #ef4444;">Покрытие дефицита</div>
    </div>
    <div class="dark-card">
        <div class="dark-card-label">Стоимость кредита ({total_interest_rate_annual:.1f}%)</div>
        <div class="dark-card-value" style="color: #fbbf24 !important;">{format_num_spaced(total_interest_paid)} ₽</div>
        <div class="dark-card-sub" style="color: #f59e0b;">Проценты банку</div>
    </div>
    <div class="dark-card">
        <div class="dark-card-label">Пиковый долг</div>
        <div class="dark-card-value">{format_num_spaced(max_debt_peak)} ₽</div>
        <div class="dark-card-sub" style="color: #a1a1aa;">Макс. тело долга</div>
    </div>
    <div class="dark-card">
        <div class="dark-card-label">Чистая прибыль (с %)</div>
        <div class="dark-card-value" style="color: #4ade80 !important;">{format_num_spaced(net_profit)} ₽</div>
        <div class="dark-card-sub" style="color: #22c55e;">Рентабельность {roi:.1f}%</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- АНАЛИТИЧЕСКИЕ СЕКЦИИ (ТАБЫ С АНИМАЦИЕЙ) ---
tab_debt, tab_stock, tab_cf, tab_pnl = st.tabs([
    "💳 Стоимость капитала & Проценты",
    "📦 Товарный цикл & Склад",
    "💰 Денежный поток (Cash Flow)",
    "📈 Экономика, Расходы & Заказы"
])

with tab_debt:
    st.markdown("<h3 style='font-size: 17px; font-weight: 600; color: #ffffff; margin-bottom: 4px;'>График обслуживания долга и начисления процентов</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 13px; color: #a1a1aa; margin-bottom: 18px;'>Столбцы — ежемесячные проценты по ставке 19%; линия — остаток непогашенного тела долга.</p>", unsafe_allow_html=True)
    
    fig_debt = go.Figure()
    fig_debt.add_trace(go.Bar(
        x=x_labels, y=interest_payments,
        name='Проценты за месяц',
        marker=dict(color='#3b82f6', line=dict(color='#60a5fa', width=1)),
        text=[f"{v/1000:,.0f}k ₽" if v > 0 else "" for v in interest_payments],
        textposition='outside',
        textfont=dict(color='#ffffff')
    ))
    fig_debt.add_trace(go.Scatter(
        x=x_labels, y=debt_balance,
        name='Остаток тела долга',
        yaxis='y2',
        mode='lines+markers+text',
        line=dict(color='#f43f5e', width=3, shape='spline'),
        marker=dict(size=7, color='#f43f5e'),
        text=[f"{v/1_000_000:.1f}M" if v > 0 else "" for v in debt_balance],
        textposition='top center',
        textfont=dict(color='#fda4af')
    ))
    fig_debt.update_layout(
        yaxis2=dict(overlaying='y', side='right', showgrid=False, tickfont=dict(color='#fda4af'))
    )
    st.plotly_chart(apply_dark_chart_layout(fig_debt), use_container_width=True)
    
    debt_df = pd.DataFrame({
        "Период": x_labels,
        "Дотация (вход)": [f"{format_num_spaced(v)} ₽" for v in monthly_investments],
        "Проценты (19%)": [f"{format_num_spaced(v)} ₽" for v in interest_payments],
        "Погашено тела долга": [f"{format_num_spaced(v)} ₽" for v in debt_repayments],
        "Остаток долга на конец": [f"{format_num_spaced(v)} ₽" for v in debt_balance],
        "Свободный остаток счета": [f"{format_num_spaced(v)} ₽" for v in funded_cash_balance]
    })
    st.dataframe(debt_df, hide_index=True, use_container_width=True)

with tab_stock:
    st.markdown("<h3 style='font-size: 17px; font-weight: 600; color: #ffffff; margin-bottom: 4px;'>Транши поставок и списание запасов</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 13px; color: #a1a1aa; margin-bottom: 18px;'>Закупки производятся дискретными циклами каждые 5 месяцев без ложного ежемесячного дублирования.</p>", unsafe_allow_html=True)
    
    fig_stock = go.Figure()
    fig_stock.add_trace(go.Bar(
        x=x_labels, y=cogs_payments,
        name='Оплата партии поставщику',
        marker=dict(color='#3f3f46', line=dict(color='#71717a', width=1)),
        text=[f"{v/1_000_000:.1f}M ₽" if v > 0 else "" for v in cogs_payments],
        textposition='outside',
        textfont=dict(color='#ffffff')
    ))
    fig_stock.add_trace(go.Scatter(
        x=x_labels, y=inventory_balance,
        name='Остаток склада',
        yaxis='y2',
        mode='lines+markers+text',
        line=dict(color='#f59e0b', width=3, shape='spline'),
        marker=dict(size=7, color='#f59e0b'),
        text=[f"{v/1_000_000:.1f}M" for v in inventory_balance],
        textposition='top center',
        textfont=dict(color='#fcd34d')
    ))
    fig_stock.update_layout(
        yaxis2=dict(overlaying='y', side='right', showgrid=False, tickfont=dict(color='#fcd34d'))
    )
    st.plotly_chart(apply_dark_chart_layout(fig_stock), use_container_width=True)

with tab_cf:
    st.markdown("<h3 style='font-size: 17px; font-weight: 600; color: #ffffff; margin-bottom: 4px;'>Структура помесячного денежного потока</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 13px; color: #a1a1aa; margin-bottom: 18px;'>Сопоставление притоков от факторинга/клиентов и полных выплат (закупки + OPEX + проценты).</p>", unsafe_allow_html=True)
    
    fig_cf = go.Figure()
    fig_cf.add_trace(go.Bar(
        x=x_labels, y=inflows,
        name='Притоки от продаж',
        marker=dict(color='#22c55e', line=dict(color='#4ade80', width=1)),
        text=[f"{v/1_000_000:.1f}M" for v in inflows],
        textposition='auto',
        textfont=dict(color='#000000', size=11)
    ))
    fig_cf.add_trace(go.Bar(
        x=x_labels, y=-total_outflows,
        name='Выплаты (закупки + OPEX + %)',
        marker=dict(color='#ef4444', line=dict(color='#f87171', width=1)),
        text=[f"{v/1_000_000:.1f}M" for v in total_outflows],
        textposition='auto',
        textfont=dict(color='#ffffff', size=11)
    ))
    fig_cf.update_layout(barmode='relative')
    st.plotly_chart(apply_dark_chart_layout(fig_cf), use_container_width=True)

with tab_pnl:
    col_pnl1, col_pnl2 = st.columns([1, 1])
    
    with col_pnl1:
        st.markdown("<h4 style='font-size: 15px; font-weight: 600; color: #ffffff; margin-bottom: 12px;'>Динамика заказов и выручки</h4>", unsafe_allow_html=True)
        fig_ord = go.Figure()
        fig_ord.add_trace(go.Bar(
            x=x_labels, y=orders, name='Заказы (шт)',
            marker=dict(color='#3b82f6', opacity=0.8),
            text=[f"{int(v)}" for v in orders], textposition='outside',
            textfont=dict(color='#ffffff')
        ))
        fig_ord.add_trace(go.Scatter(
            x=x_labels, y=rev, name='Выручка (₽)', yaxis='y2',
            mode='lines+markers', line=dict(color='#10b981', width=3, shape='spline'),
            marker=dict(size=6, color='#10b981')
        ))
        fig_ord.update_layout(yaxis2=dict(overlaying='y', side='right', showgrid=False, tickfont=dict(color='#6ee7b7')))
        st.plotly_chart(apply_dark_chart_layout(fig_ord, height=360), use_container_width=True)

    with col_pnl2:
        st.markdown("<h4 style='font-size: 15px; font-weight: 600; color: #ffffff; margin-bottom: 12px;'>Структура затрат с учетом процентов</h4>", unsafe_allow_html=True)
        exp_labels = ['Склад', 'Офис', 'ФОТ', 'Прочие OPEX', 'Налоги 5%', 'Закупки', 'Проценты по долгу']
        total_fot = sum(np.full(period, monthly_fot))
        total_warehouse = sum(np.full(period, monthly_warehouse))
        total_office = sum(np.full(period, monthly_office))
        total_taxes = sum(taxes_and_commissions)
        sum_purchases = sum(cogs_payments)
        total_other_opex = sum(opex) - total_fot - total_warehouse - total_office
        
        exp_vals = [total_warehouse, total_office, total_fot, total_other_opex, total_taxes, sum_purchases, total_interest_paid]
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=exp_labels,
            values=exp_vals,
            hole=0.62,
            textinfo='percent',
            textfont=dict(color='#ffffff', size=11),
            marker=dict(colors=['#52525b', '#71717a', '#3b82f6', '#6366f1', '#a855f7', '#f43f5e', '#fbbf24'])
        )])
        fig_pie.update_layout(
            height=360,
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=10, b=10, l=10, r=10),
            showlegend=True,
            legend=dict(orientation="v", x=1.02, y=0.5, font=dict(color='#d4d4d8', size=11))
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# --- ПАНЕЛЬ ЭКСПОРТА ---
st.markdown("<div style='height: 1px; background: rgba(255,255,255,0.08); margin: 36px 0 24px 0;'></div>", unsafe_allow_html=True)
col_down, col_space = st.columns([1, 2])
with col_down:
    html_data = generate_html_report_bytes(
        period=period,
        start_date=f"{ru_months_full[start_month_idx]} {start_year}",
        sum_rev=format_num_spaced(sum(rev)) + " ₽",
        max_deficit=format_num_spaced(max_debt_peak) + " ₽",
        net_profit=format_num_spaced(net_profit) + " ₽",
        roi=f"{roi:.1f}%",
        initial_cash_buffer="0 ₽",
        initial_purchase=format_num_spaced(initial_purchase) + " ₽",
        x_labels=x_labels,
        cash_balance=funded_cash_balance,
        inflows=inflows,
        outflows=total_outflows,
        net_cf=inflows - total_outflows,
        rev=rev,
        opex=opex,
        taxes_and_commissions=taxes_and_commissions,
        cogs_payments=cogs_payments,
        cum_cf=debt_balance,
        factoring_share=factoring_share,
        margin_pct=margin_pct,
        sum_purchases=sum_purchases,
        total_fot=total_fot,
        total_taxes=total_taxes,
        total_other_opex=total_other_opex
    )
    st.download_button(
        label="📥 Скачать полный Executive Report",
        data=html_data,
        file_name="Executive_Financial_Report.html",
        mime="text/html",
        use_container_width=True
    )
