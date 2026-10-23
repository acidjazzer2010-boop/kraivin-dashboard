import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os
import re

from exporter import generate_html_report_bytes, send_report_to_email

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(
    page_title="Kraivin Capital & Liquidity Suite", 
    page_icon="", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ИНЪЕКЦИЯ ДИЗАЙН-СИСТЕМЫ APPLE / SF PRO + ПЛАВНЫЕ ПЕРЕХОДЫ ---
st.markdown("""
<style>
    @import url('https://fonts.cdnfonts.com/css/sf-pro-display');

    /* Базовая типографика Apple */
    html, body, [class*="css"], .stMarkdown {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", sans-serif !important;
        color: #1d1d1f;
        -webkit-font-smoothing: antialiased;
        letter-spacing: -0.015em;
    }

    /* Фон приложения */
    .stApp {
        background-color: #f5f5f7;
    }

    /* Боковая панель с эффектом Frosted Glass */
    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.72) !important;
        backdrop-filter: blur(25px) saturate(180%);
        -webkit-backdrop-filter: blur(25px) saturate(180%);
        border-right: 1px solid rgba(0, 0, 0, 0.08);
    }

    /* Карточки KPI в стиле Apple Glass */
    .apple-kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin-bottom: 28px;
    }

    .apple-card {
        background: rgba(255, 255, 255, 0.82);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 0, 0, 0.06);
        border-radius: 18px;
        padding: 22px 24px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.03), 0 1px 3px rgba(0, 0, 0, 0.02);
        transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .apple-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
    }

    .apple-card-label {
        font-size: 13px;
        font-weight: 500;
        color: #86868b;
        letter-spacing: -0.01em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .apple-card-value {
        font-size: 26px;
        font-weight: 600;
        letter-spacing: -0.03em;
        color: #1d1d1f;
    }

    .apple-card-sub {
        font-size: 12px;
        font-weight: 500;
        color: #0071e3;
        margin-top: 4px;
    }

    /* --- КИНЕМАТИЧЕСКАЯ АНИМАЦИЯ ПЕРЕКЛЮЧЕНИЯ ВКЛАДОК --- */
    @keyframes appleTabEnter {
        0% {
            opacity: 0;
            transform: translateY(8px) scale(0.995);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    /* Контейнер активной вкладки */
    div[data-baseweb="tab-panel"] {
        animation: appleTabEnter 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards !important;
        will-change: opacity, transform;
    }

    /* Навигационная панель табов (Apple Segmented Control) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: rgba(0, 0, 0, 0.05);
        padding: 4px;
        border-radius: 12px;
        border-bottom: none !important;
        margin-bottom: 24px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 18px;
        font-size: 14px;
        font-weight: 500;
        color: #6e6e73 !important;
        background-color: transparent !important;
        border: none !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #1d1d1f !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #1d1d1f !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08), 0 0.5px 2px rgba(0, 0, 0, 0.04);
    }

    /* Поля ввода и кнопки */
    .stTextInput input, .stSelectbox select, .stNumberInput input {
        border-radius: 12px !important;
        border: 1px solid rgba(0, 0, 0, 0.12) !important;
        background: #ffffff !important;
        padding: 10px 14px !important;
        font-size: 14px !important;
        box-shadow: none !important;
        transition: all 0.2s ease !important;
    }

    .stTextInput input:focus, .stSelectbox select:focus {
        border-color: #0071e3 !important;
        box-shadow: 0 0 0 3px rgba(0, 113, 227, 0.15) !important;
    }

    .stButton button, .stDownloadButton button {
        background-color: #0071e3 !important;
        color: #ffffff !important;
        border-radius: 980px !important;
        border: none !important;
        padding: 10px 22px !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        letter-spacing: -0.01em !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 2px 8px rgba(0, 113, 227, 0.25) !important;
    }

    .stButton button:hover, .stDownloadButton button:hover {
        background-color: #0077ed !important;
        transform: scale(1.01);
    }

    /* Скрытие стандартных футеров */
    #MainMenu, footer, header {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ФОРМАТИРОВАНИЯ ---
def format_num_spaced(val: float) -> str:
    """Форматирует число с разделителями тысяч через неразрывный пробел."""
    return f"{int(round(val)):,}".replace(",", "\u00A0")

def money_input(label: str, default_val: int, key: str, help_text: str = None) -> int:
    """Элегантный инпут с динамической микро-подписью."""
    if key not in st.session_state:
        st.session_state[key] = format_num_spaced(default_val)
    
    raw_val = st.sidebar.text_input(label, value=st.session_state[key], key=f"raw_{key}", help=help_text)
    clean_val = re.sub(r"[^\d]", "", raw_val)
    if not clean_val:
        clean_val = str(default_val)
    
    parsed_int = int(clean_val)
    formatted_str = format_num_spaced(parsed_int)
    st.session_state[key] = formatted_str
    
    st.sidebar.markdown(f"<div style='font-size: 11px; color: #86868b; margin-top: -12px; margin-bottom: 12px;'>Итог: <span style='color: #1d1d1f; font-weight: 500;'>{formatted_str} ₽</span></div>", unsafe_allow_html=True)
    return parsed_int

# --- БОКОВАЯ ПАНЕЛЬ (ПАРАМЕТРЫ) ---
st.sidebar.markdown("<h2 style='font-size: 18px; font-weight: 600; margin-bottom: 20px; letter-spacing: -0.02em;'>Конфигурация модели</h2>", unsafe_allow_html=True)

ru_months_full = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
col_m, col_y = st.sidebar.columns(2)
start_month_idx = col_m.selectbox("Месяц старта", range(12), index=9, format_func=lambda x: ru_months_full[x])
start_year = col_y.selectbox("Год", [2026, 2027], index=0)

margin_pct = st.sidebar.slider("Маржинальность (%)", min_value=10, max_value=50, value=20, step=1)
period = st.sidebar.selectbox("Горизонт моделирования", [6, 12, 18, 24], format_func=lambda x: f"{x} месяцев")

st.sidebar.markdown("<div style='height: 1px; background: rgba(0,0,0,0.06); margin: 20px 0;'></div>", unsafe_allow_html=True)
st.sidebar.markdown("<div style='font-size: 12px; font-weight: 600; text-transform: uppercase; color: #86868b; margin-bottom: 12px;'>Капитал & Закупки</div>", unsafe_allow_html=True)

initial_purchase = money_input("Стартовая закупка (₽)", default_val=25_000_000, key="init_purchase_key")
batch_cycle_months = st.sidebar.number_input("Цикл склада (мес)", value=5, min_value=1, max_value=12, step=1)

col_cb, col_comm = st.sidebar.columns(2)
cb_rate = col_cb.number_input("Ставка ЦБ (%)", value=17.0, step=0.5)
comm_margin = col_comm.number_input("Маржа (%)", value=2.0, step=0.5)
total_interest_rate_annual = cb_rate + comm_margin

st.sidebar.markdown("<div style='height: 1px; background: rgba(0,0,0,0.06); margin: 20px 0;'></div>", unsafe_allow_html=True)
st.sidebar.markdown("<div style='font-size: 12px; font-weight: 600; text-transform: uppercase; color: #86868b; margin-bottom: 12px;'>Динамика заказов</div>", unsafe_allow_html=True)

aov = money_input("Средний чек AOV (₽)", default_val=150_000, key="aov_key")
start_orders = st.sidebar.number_input("Заказов в 1-й месяц", value=40, step=1, min_value=1)
growth_type = st.sidebar.radio("Логика масштабирования", ["В штуках (+N/мес)", "В процентах (%/мес)"], index=0)

if growth_type == "В штуках (+N/мес)":
    orders_growth_abs = st.sidebar.slider("Прирост заказов", 0, 100, 5, 1)
    orders_growth_pct = 0
else:
    orders_growth_pct = st.sidebar.slider("Прирост заказов (%)", 0, 100, 10, 1)
    orders_growth_abs = 0

max_orders_cap = st.sidebar.number_input("Лимит емкости в месяц", value=300, step=10)

st.sidebar.markdown("<div style='height: 1px; background: rgba(0,0,0,0.06); margin: 20px 0;'></div>", unsafe_allow_html=True)
st.sidebar.markdown("<div style='font-size: 12px; font-weight: 600; text-transform: uppercase; color: #86868b; margin-bottom: 12px;'>Операционные расходы</div>", unsafe_allow_html=True)

monthly_fot = money_input("ФОТ команды (₽)", default_val=500_000, key="fot_key")
monthly_warehouse = money_input("Складской комплекс (₽)", default_val=200_000, key="wh_key")
monthly_office = money_input("Офис и администрация (₽)", default_val=150_000, key="office_key")

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

# --- ШАБЛОН ДИЗАЙНА ДЛЯ ГРАФИКОВ (APPLE MINIMALISM) ---
def apply_apple_chart_layout(fig, height=440):
    fig.update_layout(
        height=height,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20, b=30, l=10, r=10),
        font=dict(family='-apple-system, BlinkMacSystemFont, "SF Pro Text"', color='#86868b', size=12),
        hoverlabel=dict(
            bgcolor="rgba(255, 255, 255, 0.95)",
            bordercolor="rgba(0,0,0,0.08)",
            font=dict(family='-apple-system, BlinkMacSystemFont, "SF Pro Text"', color='#1d1d1f', size=12)
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            linecolor='rgba(0,0,0,0.06)',
            tickfont=dict(color='#86868b')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.04)',
            zeroline=False,
            tickfont=dict(color='#86868b')
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="left",
            x=0,
            font=dict(color='#1d1d1f', size=13)
        )
    )
    return fig

# --- ЗАГОЛОВОК СТРАНИЦЫ ---
st.markdown("""
<div style="margin-top: 10px; margin-bottom: 28px;">
    <div style="display: inline-block; font-size: 12px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #0071e3; background: rgba(0, 113, 227, 0.08); padding: 5px 12px; border-radius: 980px; margin-bottom: 8px;">
        Financial Model Suite 2026
    </div>
    <h1 style="font-size: 38px; font-weight: 700; letter-spacing: -0.035em; color: #1d1d1f; margin: 0 0 6px 0;">
        Ликвидность & Долговая нагрузка
    </h1>
    <p style="font-size: 16px; color: #86868b; margin: 0; font-weight: 400;">
        Моделирование кассовых разрывов, складского цикла и стоимости фондирования по ставке ЦБ РФ 17.0% + 2.0%
    </p>
</div>
""", unsafe_allow_html=True)

# --- БЛОК KPI КАРТОЧЕК APPLE GLASS ---
st.markdown(f"""
<div class="apple-kpi-container">
    <div class="apple-card">
        <div class="apple-card-label">Выручка за {period} мес</div>
        <div class="apple-card-value">{format_num_spaced(sum(rev))} ₽</div>
        <div class="apple-card-sub">С маржинальностью {margin_pct}%</div>
    </div>
    <div class="apple-card">
        <div class="apple-card-label">Объем дотаций</div>
        <div class="apple-card-value">{format_num_spaced(total_investments_injected)} ₽</div>
        <div class="apple-card-sub" style="color: #ff3b30;">Кассовый дефицит</div>
    </div>
    <div class="apple-card">
        <div class="apple-card-label">Стоимость денег ({total_interest_rate_annual:.1f}%)</div>
        <div class="apple-card-value">{format_num_spaced(total_interest_paid)} ₽</div>
        <div class="apple-card-sub">Проценты кредитору</div>
    </div>
    <div class="apple-card">
        <div class="apple-card-label">Пиковый долг</div>
        <div class="apple-card-value">{format_num_spaced(max_debt_peak)} ₽</div>
        <div class="apple-card-sub">Максимум на балансе</div>
    </div>
    <div class="apple-card">
        <div class="apple-card-label">Чистая прибыль</div>
        <div class="apple-card-value">{format_num_spaced(net_profit)} ₽</div>
        <div class="apple-card-sub" style="color: #34c759;">Рентабельность {roi:.1f}%</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- АНАЛИТИЧЕСКИЕ СЕКЦИИ НА ТАБАХ (С АНИМАЦИЕЙ ПЕРЕХОДА) ---
tab_debt, tab_stock, tab_cf, tab_pnl = st.tabs([
    "Обслуживание капитала",
    "Складской цикл",
    "Денежный поток",
    "Экономика и заказы"
])

with tab_debt:
    st.markdown("<h3 style='font-size: 18px; font-weight: 600; margin-bottom: 4px;'>График обслуживания долга и начисления процентов</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 13px; color: #86868b; margin-bottom: 20px;'>Столбцы отражают ежемесячные выплаты процентов; линия показывает динамику непогашенного тела долга.</p>", unsafe_allow_html=True)
    
    fig_debt = go.Figure()
    fig_debt.add_trace(go.Bar(
        x=x_labels, y=interest_payments,
        name='Проценты за месяц',
        marker=dict(color='#0071e3', opacity=0.85, line=dict(width=0)),
        text=[f"{v/1000:,.0f}k ₽" if v > 0 else "" for v in interest_payments],
        textposition='outside'
    ))
    fig_debt.add_trace(go.Scatter(
        x=x_labels, y=debt_balance,
        name='Остаток долга',
        yaxis='y2',
        mode='lines+markers',
        line=dict(color='#1d1d1f', width=3, shape='spline'),
        marker=dict(size=6, color='#1d1d1f')
    ))
    fig_debt.update_layout(
        yaxis2=dict(overlaying='y', side='right', showgrid=False, tickfont=dict(color='#86868b'))
    )
    st.plotly_chart(apply_apple_chart_layout(fig_debt), use_container_width=True)
    
    # Элегантная таблица
    debt_df = pd.DataFrame({
        "Период": x_labels,
        "Дотация (вход)": [f"{format_num_spaced(v)} ₽" for v in monthly_investments],
        "Проценты (19%)": [f"{format_num_spaced(v)} ₽" for v in interest_payments],
        "Погашение долга": [f"{format_num_spaced(v)} ₽" for v in debt_repayments],
        "Остаток долга": [f"{format_num_spaced(v)} ₽" for v in debt_balance],
        "Свободный кэш": [f"{format_num_spaced(v)} ₽" for v in funded_cash_balance]
    })
    st.dataframe(debt_df, hide_index=True, use_container_width=True)

with tab_stock:
    st.markdown("<h3 style='font-size: 18px; font-weight: 600; margin-bottom: 4px;'>Транши поставок и списание запасов</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 13px; color: #86868b; margin-bottom: 20px;'>Закупки производятся дискретными циклами каждые 5 месяцев без ложного ежемесячного дублирования.</p>", unsafe_allow_html=True)
    
    fig_stock = go.Figure()
    fig_stock.add_trace(go.Bar(
        x=x_labels, y=cogs_payments,
        name='Оплата партии поставщику',
        marker=dict(color='#e5e5ea', line=dict(color='rgba(0,0,0,0.1)', width=1)),
        text=[f"{v/1_000_000:.1f}M ₽" if v > 0 else "" for v in cogs_payments],
        textposition='outside'
    ))
    fig_stock.add_trace(go.Scatter(
        x=x_labels, y=inventory_balance,
        name='Остаток склада',
        yaxis='y2',
        mode='lines+markers',
        line=dict(color='#ff9500', width=3, shape='spline'),
        marker=dict(size=6, color='#ff9500')
    ))
    fig_stock.update_layout(
        yaxis2=dict(overlaying='y', side='right', showgrid=False, tickfont=dict(color='#86868b'))
    )
    st.plotly_chart(apply_apple_chart_layout(fig_stock), use_container_width=True)

with tab_cf:
    st.markdown("<h3 style='font-size: 18px; font-weight: 600; margin-bottom: 4px;'>Структура помесячного денежного потока</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 13px; color: #86868b; margin-bottom: 20px;'>Сравнение входящей выручки с обязательными платежами (закупки, аренда, ФОТ и налоги).</p>", unsafe_allow_html=True)
    
    fig_cf = go.Figure()
    fig_cf.add_trace(go.Bar(
        x=x_labels, y=inflows,
        name='Поступления от продаж',
        marker=dict(color='#34c759', opacity=0.85)
    ))
    fig_cf.add_trace(go.Bar(
        x=x_labels, y=-total_outflows,
        name='Совокупные выплаты',
        marker=dict(color='#1d1d1f', opacity=0.85)
    ))
    st.plotly_chart(apply_apple_chart_layout(fig_cf), use_container_width=True)

with tab_pnl:
    col_pnl1, col_pnl2 = st.columns([1, 1])
    
    with col_pnl1:
        st.markdown("<h4 style='font-size: 16px; font-weight: 600; margin-bottom: 12px;'>Динамика заказов и выручки</h4>", unsafe_allow_html=True)
        fig_ord = go.Figure()
        fig_ord.add_trace(go.Bar(
            x=x_labels, y=orders, name='Заказы (шт)',
            marker=dict(color='#0071e3', opacity=0.7)
        ))
        fig_ord.add_trace(go.Scatter(
            x=x_labels, y=rev, name='Выручка (₽)', yaxis='y2',
            mode='lines', line=dict(color='#1d1d1f', width=2, shape='spline')
        ))
        fig_ord.update_layout(yaxis2=dict(overlaying='y', side='right', showgrid=False))
        st.plotly_chart(apply_apple_chart_layout(fig_ord, height=360), use_container_width=True)

    with col_pnl2:
        st.markdown("<h4 style='font-size: 16px; font-weight: 600; margin-bottom: 12px;'>Структура затрат с учетом процентов</h4>", unsafe_allow_html=True)
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
            hole=0.68,
            marker=dict(colors=['#d1d1d6', '#c7c7cc', '#aeaeb2', '#8e8e93', '#636366', '#1d1d1f', '#0071e3'])
        )])
        fig_pie.update_layout(
            height=360,
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=10, b=10, l=10, r=10),
            showlegend=True,
            legend=dict(orientation="v", x=1.05, y=0.5, font=dict(family='-apple-system', size=11))
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# --- ЭКСПОРТ (FOOTER ACTION) ---
st.markdown("<div style='height: 1px; background: rgba(0,0,0,0.06); margin: 36px 0 24px 0;'></div>", unsafe_allow_html=True)
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
        label="Скачать сводный Executive Report",
        data=html_data,
        file_name="Executive_Financial_Report.html",
        mime="text/html",
        use_container_width=True
    )
