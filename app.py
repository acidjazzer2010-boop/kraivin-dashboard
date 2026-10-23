import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os
import re

from exporter import generate_html_report_bytes, send_report_to_email

# Настройка страницы
st.set_page_config(
    page_title="Анализ экономической эффективности", 
    page_icon="🍷", 
    layout="wide"
)

st.title("Анализ денежных потоков, рентабельности и инвестиций")
st.markdown("Интерактивная финансовая модель: партионные закупки, анализ дефицита и расчет стоимости заемного капитала.")

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ФОРМАТИРОВАНИЯ ---
def format_num_spaced(val: float) -> str:
    """Форматирует число с разделителями тысяч через пробел."""
    return f"{int(round(val)):,}".replace(",", " ")

def money_input(label: str, default_val: int, key: str, help_text: str = None) -> int:
    """Виджет ввода денежных сумм с автоматическим разделением тысяч пробелами."""
    if key not in st.session_state:
        st.session_state[key] = format_num_spaced(default_val)
    
    raw_val = st.sidebar.text_input(label, value=st.session_state[key], key=f"raw_{key}", help=help_text)
    
    clean_val = re.sub(r"[^\d]", "", raw_val)
    if not clean_val:
        clean_val = str(default_val)
    
    parsed_int = int(clean_val)
    formatted_str = format_num_spaced(parsed_int)
    
    st.session_state[key] = formatted_str
    st.sidebar.caption(f"Выбрано: **{formatted_str} руб.**")
    return parsed_int

# --- БОКОВАЯ ПАНЕЛЬ (ВВОД ДАННЫХ) ---

st.sidebar.header("Параметры модели")

ru_months_full = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
col_m, col_y = st.sidebar.columns(2)

# Старт по умолчанию: Октябрь 2026
start_month_idx = col_m.selectbox("Месяц старта", range(12), index=9, format_func=lambda x: ru_months_full[x])
start_year = col_y.selectbox("Год старта", [2026, 2027], index=0)

margin_pct = st.sidebar.slider("Маржинальность (%)", min_value=10, max_value=50, value=20, step=1)
period = st.sidebar.selectbox("Горизонт планирования (мес)", [6, 12, 18, 24])

st.sidebar.subheader("Стоимость заемного капитала")
col_cb, col_comm = st.sidebar.columns(2)
cb_rate = col_cb.number_input("Ставка ЦБ РФ (%)", value=17.0, step=0.5, help="Ключевая ставка ЦБ РФ на октябрь 2026 г.")
comm_margin = col_comm.number_input("Комиссия (%)", value=2.0, step=0.5, help="Коммерческая маржа кредитора")
total_interest_rate_annual = cb_rate + comm_margin
st.sidebar.info(f"Итоговая ставка: **{total_interest_rate_annual:.1f}% годовых** ({total_interest_rate_annual/12:.2f}% в мес)")

st.sidebar.subheader("Налоговые параметры")
vat_rate_pct = st.sidebar.selectbox(
    "Ставка НДС (%)", 
    [22, 20, 10, 7, 5, 0], 
    index=0, 
    help="Основная ставка НДС в РФ с 2026 года составляет 22%"
)
vat_multiplier = 1 + (vat_rate_pct / 100)

st.sidebar.subheader("Товарный запас и цикл поставок")
initial_purchase = money_input(
    "Первоначальная закупка товара (руб)", 
    default_val=25_000_000, 
    key="init_purchase_key",
    help_text="Стартовая партия товара (обеспечивает первые N месяцев)"
)
batch_cycle_months = st.sidebar.number_input(
    "На сколько месяцев хватает партии (мес)",
    value=5,
    min_value=1,
    max_value=12,
    step=1
)
initial_cash_buffer = 0

st.sidebar.subheader("Динамика продаж")
aov = money_input(
    "Средняя сумма заказа / AOV (руб)", 
    default_val=150_000, 
    key="aov_key"
)

start_orders = st.sidebar.number_input(
    "Заказов в 1-й месяц (шт)", 
    value=40, 
    step=1,
    min_value=1
)

growth_type = st.sidebar.radio(
    "Логика прироста заказов",
    ["В штуках (+N заказов/мес)", "В процентах (% в месяц)"],
    index=0
)

if growth_type == "В штуках (+N заказов/мес)":
    orders_growth_abs = st.sidebar.slider("Прирост заказов в месяц (шт)", 0, 100, 5, 1)
    orders_growth_pct = 0
else:
    orders_growth_pct = st.sidebar.slider("Ежемесячный прирост заказов (%)", 0, 100, 10, 1)
    orders_growth_abs = 0

max_orders_cap = st.sidebar.number_input("Потолок продаж / лимит в месяц (шт)", value=300, step=10)

st.sidebar.subheader("Команда и постоянные расходы")
monthly_fot = money_input("ФОТ в месяц (руб)", default_val=500_000, key="fot_key")
monthly_warehouse = money_input("Аренда и расходы на склад (руб)", default_val=200_000, key="wh_key")
monthly_office = money_input("Аренда и расходы на офис (руб)", default_val=150_000, key="office_key")

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
        calculated_orders = float(start_orders)
    else:
        if growth_type == "В штуках (+N заказов/мес)":
            calculated_orders = orders[i-1] + orders_growth_abs
        else:
            calculated_orders = orders[i-1] * (1 + (orders_growth_pct / 100))
    orders[i] = min(calculated_orders, float(max_orders_cap))
    rev[i] = orders[i] * aov

cogs_pct = 1 - (margin_pct / 100)
cogs_no_vat = rev * cogs_pct
cogs_vat = cogs_no_vat * vat_multiplier

delay_months_suppliers = max(1, int(round(delay_days / 30))) if delay_days > 0 else 0

# Партионные закупки
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

# Притоки
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

# --- РАСЧЕТ ДОТАЦИЙ, ДОЛГА И СТОИМОСТИ ДЕНЕГ (ПРОЦЕНТОВ) ---
monthly_interest_rate = (total_interest_rate_annual / 100.0) / 12.0

monthly_investments = np.zeros(period)    # Новые транши финансирования
interest_payments = np.zeros(period)      # Выплата процентов в месяц
debt_repayments = np.zeros(period)        # Погашение тела долга из профицита
debt_balance = np.zeros(period)           # Остаток непогашенного тела долга
funded_cash_balance = np.zeros(period)

current_debt = 0.0
curr_cash = float(initial_cash_buffer)

for i in range(period):
    # 1. Проценты на остаток долга на начало месяца
    interest_due = current_debt * monthly_interest_rate
    interest_payments[i] = interest_due
    
    # 2. Операционное сальдо с учетом начисленных процентов
    net_before_financing = inflows[i] - (base_outflows[i] + interest_due)
    potential_cash = curr_cash + net_before_financing
    
    if potential_cash < 0:
        # Кассовый разрыв -> привлекаем дотацию
        needed_injection = abs(potential_cash)
        monthly_investments[i] = needed_injection
        current_debt += needed_injection
        curr_cash = 0.0
        debt_repayments[i] = 0.0
    else:
        # Профицит денег -> свободные средства направляем на гашение долга
        monthly_investments[i] = 0.0
        repay_amount = min(potential_cash, current_debt)
        debt_repayments[i] = repay_amount
        current_debt -= repay_amount
        curr_cash = potential_cash - repay_amount
        
    debt_balance[i] = current_debt
    funded_cash_balance[i] = curr_cash

total_outflows = base_outflows + interest_payments
net_cf_raw = inflows - base_outflows
cum_cf_raw = np.cumsum(net_cf_raw)
max_deficit = min(min(cum_cf_raw), 0)

total_interest_paid = np.sum(interest_payments)
total_investments_injected = np.sum(monthly_investments)
max_debt_peak = np.max(debt_balance)

# Чистая прибыль за вычетом всех расходов и процентов за кредит
net_profit = sum(rev * (margin_pct / 100)) - sum(opex) - sum(taxes_and_commissions) - total_interest_paid
roi = (net_profit / sum(rev)) * 100 if sum(rev) > 0 else 0

sum_purchases = sum(cogs_payments)
total_fot = sum(np.full(period, monthly_fot))
total_warehouse = sum(np.full(period, monthly_warehouse))
total_office = sum(np.full(period, monthly_office))
total_taxes = sum(taxes_and_commissions)
total_other_opex = sum(opex) - total_fot - total_warehouse - total_office

# --- ВЫВОД KPI ---
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Сумма дотаций (тело долга)", format_num_spaced(total_investments_injected) + " руб.")
col2.metric(f"Уплаченные проценты ({total_interest_rate_annual:.1f}%)", format_num_spaced(total_interest_paid) + " руб.")
col3.metric("Пиковый остаток долга", format_num_spaced(max_debt_peak) + " руб.")
col4.metric("Чистая прибыль (с %)", format_num_spaced(net_profit) + " руб.")
col5.metric("Рентабельность по ЧП", f"{roi:.1f}%")

st.divider()

# --- ПАНЕЛЬ ЭКСПОРТА ---
st.subheader("📤 Экспорт отчета в HTML")
html_data = generate_html_report_bytes(
    period=period,
    start_date=f"{ru_months_full[start_month_idx]} {start_year}",
    sum_rev=format_num_spaced(sum(rev)) + " руб.",
    max_deficit=format_num_spaced(max_deficit) + " руб.",
    net_profit=format_num_spaced(net_profit) + " руб.",
    roi=f"{roi:.1f}%",
    initial_cash_buffer=format_num_spaced(initial_cash_buffer) + " руб.",
    initial_purchase=format_num_spaced(initial_purchase) + " руб.",
    x_labels=x_labels,
    cash_balance=funded_cash_balance,
    inflows=inflows,
    outflows=total_outflows,
    net_cf=inflows - total_outflows,
    rev=rev,
    opex=opex,
    taxes_and_commissions=taxes_and_commissions,
    cogs_payments=cogs_payments,
    cum_cf=cum_cf_raw,
    factoring_share=factoring_share,
    margin_pct=margin_pct,
    sum_purchases=sum_purchases,
    total_fot=total_fot,
    total_taxes=total_taxes,
    total_other_opex=total_other_opex
)

tab_ex1, tab_ex2 = st.tabs(["📥 Скачать HTML-отчет", "✉️ Отправить HTML на email"])
with tab_ex1:
    st.download_button("💾 Скачать файл отчета", data=html_data, file_name="Kraivin_Financial_Report.html", mime="text/html", use_container_width=True)
with tab_ex2:
    email_input = st.text_input("Email получателя", "partner@krayvin.ru")
    if st.button("🚀 Отправить отчет на email"):
        if send_report_to_email(email_input, html_data):
            st.success("Отчет успешно отправлен!")
        else:
            st.error("Ошибка при отправке.")

st.divider()

# --- ВИЗУАЛИЗАЦИЯ НА ВКЛАДКАХ ---
st.subheader("📊 Аналитические панели и графики")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "💳 Стоимость долга и Проценты",
    "📦 Товарный цикл и Склад",
    "💰 Ликвидность и Денежный поток", 
    "📈 Рентабельность и EBITDA", 
    "📉 Структура расходов с учетом %",
    "📊 Заказы и Выручка"
])

with tab1:
    st.markdown("### Обслуживание долга и начисленные проценты")
    st.caption(f"Проценты начисляются по ставке {total_interest_rate_annual:.1f}% годовых на остаток непогашенного долга.")
    
    fig_debt = go.Figure()
    
    # Начисленные проценты (столбцы)
    fig_debt.add_trace(go.Bar(
        x=x_labels, y=interest_payments,
        name='Проценты к уплате (руб)',
        marker_color='#B88645',
        text=[f"{format_num_spaced(v)} руб" if v > 0 else "" for v in interest_payments],
        textposition='outside'
    ))
    
    # Остаток тела долга (линия)
    fig_debt.add_trace(go.Scatter(
        x=x_labels, y=debt_balance,
        name='Остаток долга (тело)',
        yaxis='y2',
        mode='lines+markers+text',
        line=dict(color='#642A38', width=3),
        text=[f"{v/1_000_000:.1f}М" if v > 0 else "0" for v in debt_balance],
        textposition='top center'
    ))
    
    fig_debt.update_layout(
        xaxis_title="Месяц",
        yaxis_title="Проценты в месяц (руб)",
        yaxis2=dict(title="Остаток долга (руб)", overlaying='y', side='right', showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified"
    )
    st.plotly_chart(fig_debt, use_container_width=True)
    
    # Детальная таблица движения долга
    debt_df = pd.DataFrame({
        "Месяц": x_labels,
        "Привлечено дотаций": [format_num_spaced(v) for v in monthly_investments],
        "Проценты за месяц": [format_num_spaced(v) for v in interest_payments],
        "Погашено тела долга": [format_num_spaced(v) for v in debt_repayments],
        "Остаток долга на конец месяца": [format_num_spaced(v) for v in debt_balance],
        "Свободный остаток денег на счете": [format_num_spaced(v) for v in funded_cash_balance]
    })
    st.dataframe(debt_df, hide_index=True, use_container_width=True)

with tab2:
    st.markdown("### График партионных закупок и динамика склада")
    st.caption("Показывает моменты крупных оплат партий товара и постепенное списание складского остатка в течение 5 месяцев.")
    
    fig_stock = go.Figure()
    fig_stock.add_trace(go.Bar(
        x=x_labels, y=cogs_payments, name='Оплата партии поставщикам (руб)', marker_color='#642A38',
        text=[f"{v/1_000_000:.1f}М" if v > 0 else "" for v in cogs_payments], textposition='outside'
    ))
    fig_stock.add_trace(go.Scatter(
        x=x_labels, y=inventory_balance, name='Остаток товара на складе (руб)', yaxis='y2',
        mode='lines+markers+text', line=dict(color='#B88645', width=3),
        text=[f"{v/1_000_000:.1f}М" for v in inventory_balance], textposition='top center'
    ))
    fig_stock.update_layout(
        xaxis_title="Месяц", yaxis_title="Оплата партии (руб)",
        yaxis2=dict(title="Остаток склада (руб)", overlaying='y', side='right', showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified"
    )
    st.plotly_chart(fig_stock, use_container_width=True)

with tab3:
    st.markdown("### Динамика ликвидности (с учетом обслуживания долга)")
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=x_labels, y=cum_cf_raw, mode='lines+markers+text', name='Баланс без дотаций (чистый разрыв)',
        text=[f"{v:,.0f}".replace(",", " ") for v in cum_cf_raw], textposition="top center",
        line=dict(color='#A27B5C', width=2, dash='dash')
    ))
    fig1.add_trace(go.Scatter(
        x=x_labels, y=funded_cash_balance, mode='lines+markers+text', name='Остаток на счете (с фондированием)',
        text=[f"{v:,.0f}".replace(",", " ") for v in funded_cash_balance], textposition="bottom center",
        line=dict(color='#642A38', width=3), fill='tozeroy', fillcolor='rgba(100, 42, 56, 0.1)'
    ))
    fig1.add_hline(y=0, line_dash="dot", line_color="red", annotation_text="Граница дефицита")
    fig1.update_layout(xaxis_title="Месяц", yaxis_title="Рубли", hovermode="x unified")
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("### Структура помесячного денежного потока")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=x_labels, y=inflows, name='Притоки от продаж', marker_color='#E3C293', text=[f"{v:,.0f}".replace(",", " ") for v in inflows], textposition='auto'))
    fig2.add_trace(go.Bar(x=x_labels, y=-total_outflows, name='Выплаты (закупки + OPEX + %)', marker_color='#642A38', text=[f"{v:,.0f}".replace(",", " ") for v in total_outflows], textposition='auto'))
    fig2.update_layout(barmode='relative', xaxis_title="Месяц", yaxis_title="Рубли", hovermode="x unified")
    st.plotly_chart(fig2, use_container_width=True)

with tab4:
    st.markdown("### Динамика EBITDA")
    fig3 = go.Figure()
    ebitda_vals = rev - opex - taxes_and_commissions - cogs_vat
    fig3.add_trace(go.Bar(x=x_labels, y=ebitda_vals, name='EBITDA', marker_color='#642A38', text=[f"{v:,.0f}".replace(",", " ") for v in ebitda_vals], textposition='auto'))
    fig3.add_trace(go.Scatter(x=x_labels, y=[margin_pct]*period, name='Маржинальность (%)', yaxis='y2', line=dict(color='#E3C293', width=3)))
    fig3.update_layout(xaxis_title="Месяц", yaxis_title="EBITDA (руб)", yaxis2=dict(title="Маржа (%)", overlaying='y', side='right', range=[0, 50]))
    st.plotly_chart(fig3, use_container_width=True)

with tab5:
    st.markdown("### Структура совокупных расходов (с процентами по кредиту)")
    exp_labels = ['Склад', 'Офис', 'ФОТ (Команда)', 'Прочие OPEX', 'Налоги и сборы', 'Закупки товара', 'Проценты по долгу']
    exp_vals = [total_warehouse, total_office, total_fot, total_other_opex, total_taxes, sum_purchases, total_interest_paid]
    tot_exp = sum(exp_vals) or 1
    exp_pcts = [v / tot_exp * 100 for v in exp_vals]
    
    fig6 = go.Figure(data=[go.Bar(
        y=exp_labels, x=exp_pcts, orientation='h',
        text=[f"{p:.1f}% ({format_num_spaced(v)} руб)" for p, v in zip(exp_pcts, exp_vals)], textposition='auto',
        marker_color=['#8B5E3C', '#A27B5C', '#E3C293', '#D0C2B8', '#B88645', '#642A38', '#C0392B']
    )])
    fig6.update_layout(xaxis_title="Доля в расходах (%)", yaxis=dict(autorange="reversed"), margin=dict(t=10, b=0, l=0, r=0))
    st.plotly_chart(fig6, use_container_width=True)

with tab6:
    st.markdown("### Прогноз количества заказов и выручки")
    fig_orders = go.Figure()
    fig_orders.add_trace(go.Bar(
        x=x_labels, y=orders, name='Заказы (шт)', marker_color='#642A38',
        text=[f"{int(v)} шт" for v in orders], textposition='outside'
    ))
    fig_orders.add_trace(go.Scatter(
        x=x_labels, y=rev, name='Выручка (руб)', yaxis='y2',
        mode='lines+markers+text', line=dict(color='#E3C293', width=3),
        text=[f"{v/1_000_000:.1f}М" for v in rev], textposition='top center'
    ))
    fig_orders.update_layout(
        xaxis_title="Месяц", yaxis_title="Заказов в месяц (шт)",
        yaxis2=dict(title="Выручка (руб)", overlaying='y', side='right', showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified"
    )
    st.plotly_chart(fig_orders, use_container_width=True)
