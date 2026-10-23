import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os
import re

# Безопасный импорт функций экспорта (если модуль exporter.py отсутствует в репозитории, приложение не упадет)
try:
    from exporter import generate_html_report_bytes, send_report_to_email
    EXPORTER_AVAILABLE = True
except ImportError:
    EXPORTER_AVAILABLE = False
    def generate_html_report_bytes(**kwargs):
        return b"<html><body><h2>\xd0\x9e\xd1\x82\xd1\x87\xd0\xb5\xd1\x82 \xd1\x81\xd1\x84\xd0\xbe\xd1\x80\xd0\xbc\xd0\xb8\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd</h2></body></html>"
    def send_report_to_email(email, data):
        return False

# --- НАСТРОЙКА СТРАНИЦЫ ---
st.set_page_config(
    page_title="Финансовый анализ и моделирование", 
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ИНТЕРАКТИВНЫЙ ПОЛЗУНОК-ТУМБЛЕР (ДЕНЬ / НОЧЬ) ---
st.sidebar.markdown("<div style='margin-bottom: 4px;'></div>", unsafe_allow_html=True)
theme_toggle = st.sidebar.toggle(
    "Дневной режим",
    value=False,
    help="Сдвиньте ползунок: выключен — глубокая черная ночь, включен — чистый белый день с контрастными цифрами"
)

is_dark = not theme_toggle
theme_mode = "Ночной режим" if is_dark else "Дневной режим"

# --- ДИНАМИЧЕСКИЕ ЦВЕТОВЫЕ ТОКЕНЫ ---
if is_dark:
    bg_app = "#09090b"
    bg_sidebar = "#121217"
    card_bg = "#14141b"
    card_border = "rgba(255, 255, 255, 0.12)"
    card_hover_border = "rgba(255, 255, 255, 0.28)"
    text_primary = "#ffffff"
    text_secondary = "#a1a1aa"
    tab_list_bg = "#181820"
    tab_active_bg = "#272732"
    input_bg = "#1c1c24"
    input_border = "rgba(255, 255, 255, 0.16)"
    chart_grid = "rgba(255, 255, 255, 0.08)"
    chart_text = "#a1a1aa"
    chart_tooltip_bg = "#18181b"
else:
    bg_app = "#f8fafc"
    bg_sidebar = "#ffffff"
    card_bg = "#ffffff"
    card_border = "rgba(0, 0, 0, 0.12)"
    card_hover_border = "rgba(0, 0, 0, 0.3)"
    text_primary = "#09090b"
    text_secondary = "#52525b"
    tab_list_bg = "#f1f5f9"
    tab_active_bg = "#ffffff"
    input_bg = "#ffffff"
    input_border = "rgba(0, 0, 0, 0.2)"
    chart_grid = "rgba(0, 0, 0, 0.08)"
    chart_text = "#52525b"
    chart_tooltip_bg = "#ffffff"

# --- ИНЪЕКЦИЯ КОНТРАСТНЫХ СТИЛЕЙ ПОД ТЕКУЩИЙ РЕЖИМ ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stMarkdown {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: {text_primary} !important;
        letter-spacing: -0.01em;
    }}

    .stApp {{
        background-color: {bg_app} !important;
    }}

    section[data-testid="stSidebar"] {{
        background-color: {bg_sidebar} !important;
        border-right: 1px solid {card_border} !important;
    }}

    section[data-testid="stSidebar"] * {{
        color: {text_primary} !important;
    }}

    div[data-testid="stToggle"] label span {{
        font-weight: 700 !important;
        font-size: 13px !important;
    }}

    .kpi-container {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
        gap: 16px;
        margin-bottom: 28px;
    }}

    .custom-card {{
        background: {card_bg};
        border: 1px solid {card_border};
        border-radius: 16px;
        padding: 20px 22px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, {0.35 if is_dark else 0.06});
        transition: transform 0.2s ease, border-color 0.2s ease;
    }}

    .custom-card:hover {{
        transform: translateY(-2px);
        border-color: {card_hover_border};
    }}

    .card-label {{
        font-size: 12px;
        font-weight: 700;
        color: {text_secondary} !important;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }}

    .card-value {{
        font-size: 27px;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: {text_primary} !important;
    }}

    .card-sub {{
        font-size: 12px;
        font-weight: 600;
        margin-top: 6px;
    }}

    @keyframes tabEnter {{
        from {{
            opacity: 0;
            transform: translateY(6px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    div[data-baseweb="tab-panel"] {{
        animation: tabEnter 0.28s cubic-bezier(0.16, 1, 0.3, 1) forwards !important;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: {tab_list_bg};
        padding: 6px;
        border-radius: 12px;
        border: 1px solid {card_border};
        margin-bottom: 24px;
    }}

    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        padding: 8px 18px;
        font-size: 13px;
        font-weight: 600;
        color: {text_secondary} !important;
        background-color: transparent !important;
        border: none !important;
        transition: all 0.2s ease;
    }}

    .stTabs [data-baseweb="tab"]:hover {{
        color: {text_primary} !important;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: {tab_active_bg} !important;
        color: {text_primary} !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, {0.3 if is_dark else 0.08});
    }}

    .stTextInput input, .stSelectbox select, .stNumberInput input {{
        border-radius: 10px !important;
        border: 1px solid {input_border} !important;
        background: {input_bg} !important;
        color: {text_primary} !important;
        font-weight: 600 !important;
    }}

    .stTextInput input:focus, .stSelectbox select:focus {{
        border-color: #2563eb !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.25) !important;
    }}

    .stButton button, .stDownloadButton button {{
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 10px 22px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3) !important;
    }}

    .stButton button:hover, .stDownloadButton button:hover {{
        background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
        transform: translateY(-1px);
    }}

    #MainMenu, footer, header {{
        visibility: hidden;
    }}
</style>
""", unsafe_allow_html=True)

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ФОРМАТИРОВАНИЯ ---
def format_num_spaced(val: float) -> str:
    """Форматирует число с разделителями тысяч через пробел."""
    return f"{int(round(val)):,}".replace(",", " ")

def money_input(label: str, default_val: int, key: str, help_text: str = None) -> int:
    """Инпут с динамической контрастной микро-подписью."""
    if key not in st.session_state:
        st.session_state[key] = format_num_spaced(default_val)
    
    raw_val = st.sidebar.text_input(label, value=st.session_state[key], key=f"raw_{key}", help=help_text)
    clean_val = re.sub(r"[^\d]", "", raw_val)
    if not clean_val:
        clean_val = str(default_val)
    
    parsed_int = int(clean_val)
    formatted_str = format_num_spaced(parsed_int)
    st.session_state[key] = formatted_str
    
    accent_color = "#60a5fa" if is_dark else "#2563eb"
    st.sidebar.markdown(
        f"<div style='font-size: 11px; color: {text_secondary}; margin-top: -12px; margin-bottom: 12px;'>"
        f"Выбрано: <span style='color: {accent_color}; font-weight: 700;'>{formatted_str} ₽</span></div>", 
        unsafe_allow_html=True
    )
    return parsed_int

# --- БОКОВАЯ ПАНЕЛЬ (ВВОД ДАННЫХ) ---
st.sidebar.markdown(f"<div style='height: 1px; background: {card_border}; margin: 8px 0 16px 0;'></div>", unsafe_allow_html=True)
st.sidebar.markdown(f"<h2 style='font-size: 17px; font-weight: 700; color: {text_primary}; margin-bottom: 16px;'>Параметры модели</h2>", unsafe_allow_html=True)

ru_months_full = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
col_m, col_y = st.sidebar.columns(2)
start_month_idx = col_m.selectbox("Месяц старта", range(12), index=9, format_func=lambda x: ru_months_full[x])
start_year = col_y.selectbox("Год", [2026, 2027], index=0)

margin_pct = st.sidebar.slider("Маржинальность, %", min_value=10, max_value=50, value=20, step=1)
period = st.sidebar.selectbox("Горизонт планирования", [6, 12, 18, 24], format_func=lambda x: f"{x} месяцев")

st.sidebar.markdown(f"<div style='height: 1px; background: {card_border}; margin: 16px 0;'></div>", unsafe_allow_html=True)
st.sidebar.markdown(f"<div style='font-size: 11px; font-weight: 700; text-transform: uppercase; color: {text_secondary}; margin-bottom: 10px;'>Товар и капитал</div>", unsafe_allow_html=True)

initial_purchase = money_input("Стартовая закупка, ₽", default_val=25_000_000, key="init_purchase_key")
batch_cycle_months = st.sidebar.number_input("Цикл склада, мес.", value=5, min_value=1, max_value=12, step=1)

col_cb, col_comm = st.sidebar.columns(2)
cb_rate = col_cb.number_input("Ставка ЦБ, %", value=17.0, step=0.5)
comm_margin = col_comm.number_input("Маржа, %", value=2.0, step=0.5)
total_interest_rate_annual = cb_rate + comm_margin

st.sidebar.markdown(f"<div style='height: 1px; background: {card_border}; margin: 16px 0;'></div>", unsafe_allow_html=True)
st.sidebar.markdown(f"<div style='font-size: 11px; font-weight: 700; text-transform: uppercase; color: {text_secondary}; margin-bottom: 10px;'>Динамика продаж</div>", unsafe_allow_html=True)

aov = money_input("Средний чек заказа, ₽", default_val=150_000, key="aov_key")
start_orders = st.sidebar.number_input("Заказов в 1-й месяц", value=40, step=1, min_value=1)
growth_type = st.sidebar.radio("Логика прироста заказов", ["В штуках, заказов в месяц", "В процентах, в месяц"], index=0)

if growth_type == "В штуках, заказов в месяц":
    orders_growth_abs = st.sidebar.slider("Прирост заказов, шт. в месяц", 0, 100, 5, 1)
    orders_growth_pct = 0
else:
    orders_growth_pct = st.sidebar.slider("Прирост заказов, % в месяц", 0, 100, 10, 1)
    orders_growth_abs = 0

max_orders_cap = st.sidebar.number_input("Потолок заказов в месяц", value=300, step=10)

st.sidebar.markdown(f"<div style='height: 1px; background: {card_border}; margin: 16px 0;'></div>", unsafe_allow_html=True)
st.sidebar.markdown(f"<div style='font-size: 11px; font-weight: 700; text-transform: uppercase; color: {text_secondary}; margin-bottom: 10px;'>Постоянные расходы</div>", unsafe_allow_html=True)

monthly_fot = money_input("ФОТ в месяц, ₽", default_val=500_000, key="fot_key")
monthly_warehouse = money_input("Аренда склада, ₽", default_val=200_000, key="wh_key")
monthly_office = money_input("Аренда офиса, ₽", default_val=150_000, key="office_key")

vat_rate_pct = 22
vat_multiplier = 1 + (vat_rate_pct / 100)
prepayment_pct = 50
delay_days = 40
factoring_share = 50
factoring_advance = 80
customer_delay_days = 70
initial_cash_buffer = 0

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
        calculated_orders = float(start_orders)
    else:
        if growth_type == "В штуках, заказов в месяц":
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

# --- СТИЛИЗАЦИЯ ГРАФИКОВ ПОД ТЕКУЩИЙ РЕЖИМ ---
def apply_chart_layout(fig, height=440):
    fig.update_layout(
        height=height,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=30, b=30, l=10, r=10),
        font=dict(family='Inter, sans-serif', color=chart_text, size=12),
        hoverlabel=dict(
            bgcolor=chart_tooltip_bg,
            bordercolor=card_border,
            font=dict(color=text_primary, size=12)
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            linecolor=chart_grid,
            tickfont=dict(color=chart_text)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=chart_grid,
            zeroline=False,
            tickfont=dict(color=chart_text)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="left",
            x=0,
            font=dict(color=text_primary, size=12)
        )
    )
    return fig

# --- ЗАГОЛОВОК СТРАНИЦЫ ---
tag_color = "#3b82f6" if is_dark else "#2563eb"
st.markdown(f"""
<div style="margin-top: 10px; margin-bottom: 24px;">
    <div style="display: inline-block; font-size: 11px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: {tag_color}; background: {'rgba(59, 130, 246, 0.15)' if is_dark else 'rgba(37, 99, 235, 0.08)'}; border: 1px solid {card_border}; padding: 4px 12px; border-radius: 999px; margin-bottom: 8px;">
        {theme_mode} • 2026
    </div>
    <h1 style="font-size: 34px; font-weight: 800; letter-spacing: -0.02em; color: {text_primary}; margin: 0 0 6px 0;">
        Ликвидность, кассовые разрывы и кредитная нагрузка
    </h1>
    <p style="font-size: 15px; color: {text_secondary}; margin: 0; font-weight: 400;">
        Моделирование потребности в дотациях по ставке ЦБ РФ 17.0% + 2.0% коммерческой маржи
    </p>
</div>
""", unsafe_allow_html=True)

# --- БЛОК КАРТОЧЕК МЕТРИК ---
red_val_color = "#f87171" if is_dark else "#dc2626"
yellow_val_color = "#fbbf24" if is_dark else "#d97706"
green_val_color = "#4ade80" if is_dark else "#16a34a"

st.markdown(f"""
<div class="kpi-container">
    <div class="custom-card">
        <div class="card-label">Выручка за {period} мес.</div>
        <div class="card-value">{format_num_spaced(sum(rev))} ₽</div>
        <div class="card-sub" style="color: {'#60a5fa' if is_dark else '#2563eb'};">Маржинальность {margin_pct}%</div>
    </div>
    <div class="custom-card">
        <div class="card-label">Требуемые дотации</div>
        <div class="card-value" style="color: {red_val_color} !important;">{format_num_spaced(total_investments_injected)} ₽</div>
        <div class="card-sub" style="color: {red_val_color};">Покрытие дефицита</div>
    </div>
    <div class="custom-card">
        <div class="card-label">Стоимость кредита, {total_interest_rate_annual:.1f}%</div>
        <div class="card-value" style="color: {yellow_val_color} !important;">{format_num_spaced(total_interest_paid)} ₽</div>
        <div class="card-sub" style="color: {yellow_val_color};">Проценты кредитору</div>
    </div>
    <div class="custom-card">
        <div class="card-label">Пиковый долг</div>
        <div class="card-value">{format_num_spaced(max_debt_peak)} ₽</div>
        <div class="card-sub" style="color: {text_secondary};">Максимальное тело долга</div>
    </div>
    <div class="custom-card">
        <div class="card-label">Чистая прибыль с учетом процентов</div>
        <div class="card-value" style="color: {green_val_color} !important;">{format_num_spaced(net_profit)} ₽</div>
        <div class="card-sub" style="color: {green_val_color};">Рентабельность {roi:.1f}%</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- АНАЛИТИЧЕСКИЕ СЕКЦИИ ---
tab_debt, tab_stock, tab_cf, tab_pnl = st.tabs([
    "Стоимость капитала и проценты",
    "Товарный цикл и склад",
    "Денежный поток",
    "Экономика, расходы и заказы"
])

with tab_debt:
    st.markdown(f"<h3 style='font-size: 17px; font-weight: 700; color: {text_primary}; margin-bottom: 4px;'>График обслуживания долга и начисления процентов</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 13px; color: {text_secondary}; margin-bottom: 18px;'>Столбцы — ежемесячные проценты по ставке {total_interest_rate_annual:.1f}%; линия — остаток непогашенного тела долга.</p>", unsafe_allow_html=True)
    
    fig_debt = go.Figure()
    bar_color = "#3b82f6" if is_dark else "#2563eb"
    line_color = "#f43f5e" if is
