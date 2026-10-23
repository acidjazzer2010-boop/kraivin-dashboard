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
st.markdown("Интерактивная финансовая модель: партионные закупки товара, анализ кассовых разрывов и график дотаций.")

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ФОРМАТИРОВАНИЯ ---
def format_num_spaced(val: int) -> str:
    """Форматирует целое число с разделителями тысяч через пробел."""
    return f"{int(val):,}".replace(",", " ")

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
    step=1,
    help="В течение этого срока новые закупки не производятся — товар списывается со склада"
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
    index=0,
    help="В штуках — линейный рост. В процентах — сложный экспоненциальный прирост."
)

if growth_type == "В штуках (+N заказов/мес)":
    orders_growth_abs = st.sidebar.slider(
        "Прирост заказов в месяц (шт)", 
        min_value=0, 
        max_value=100, 
        value=5, 
        step=1
    )
    orders_growth_pct = 0
else:
    orders_growth_pct = st.sidebar.slider(
        "Ежемесячный прирост заказов (%)", 
        min_value=0, 
        max_value=100, 
        value=10, 
        step=1
    )
    orders_growth_abs = 0

max_orders_cap = st.sidebar.number_input(
    "Потолок продаж / лимит в месяц (шт)",
    value=300,
    step=10,
    help="Предельное число заказов в месяц с учетом емкости рынка/склада"
)

st.sidebar.subheader("Команда и постоянные расходы")
monthly_fot = money_input(
    "ФОТ в месяц (руб)", 
    default_val=500_000, 
    key="fot_key"
)
monthly_warehouse = money_input(
    "Аренда и расходы на склад (руб)", 
    default_val=200_000, 
    key="wh_key"
)
monthly_office = money_input(
    "Аренда и расходы на офис (руб)", 
    default_val=150_000, 
    key="office_key"
)

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

# Себестоимость проданного товара (COGS)
cogs_pct = 1 - (margin_pct / 100)
cogs_no_vat = rev * cogs_pct
cogs_vat = cogs_no_vat * vat_multiplier

delay_months_suppliers = max(1, int(round(delay_days / 30))) if delay_days > 0 else 0

# --- РАСЧЕТ ПЛАТЕЖЕЙ ЗА ПАРТИОННЫЕ ЗАКУПКИ (БЕЗ ЕЖЕМЕСЯЧНОГО ДУБЛИРОВАНИЯ) ---
cogs_payments = np.zeros(period)
inventory_deliveries = np.zeros(period)  # Поступление партий на склад

# 1. Стартовая партия (25 млн руб.) обеспечивает первые batch_cycle_months месяцев
initial_prep = initial_purchase * (prepayment_pct / 100)
initial_post = initial_purchase * ((100 - prepayment_pct) / 100)

cogs_payments[0] += initial_prep
if delay_months_suppliers < period:
    cogs_payments[delay_months_suppliers] += initial_post
inventory_deliveries[0] = initial_purchase

# 2. Следующие партии закупаются раз в batch_cycle_months (например, в мес. 5/6, мес. 10/11)
for batch_start in range(batch_cycle_months, period, batch_cycle_months):
    batch_end = min(batch_start + batch_cycle_months, period)
    # Суммарная себестоимость товаров, необходимых на следующие N месяцев
    needed_batch_cogs = float(np.sum(cogs_vat[batch_start:batch_end]))
    inventory_deliveries[batch_start] = needed_batch_cogs
    
    # Оплата новой партии: аванс + остаток через отсрочку
    cogs_payments[batch_start] += needed_batch_cogs * (prepayment_pct / 100)
    post_pay_m = batch_start + delay_months_suppliers
    if post_pay_m < period:
        cogs_payments[post_pay_m] += needed_batch_cogs * ((100 - prepayment_pct) / 100)

# Динамика складского остатка в рублях себестоимости
inventory_balance = np.zeros(period)
curr_inv = 0.0
for i in range(period):
    curr_inv += inventory_deliveries[i] - cogs_vat[i]
    inventory_balance[i] = max(curr_inv, 0.0)

# --- ПРИТОКИ С УЧЕТОМ ФАКТОРИНГА И ОТСРОЧЕК КЛИЕНТАМ ---
customer_delay_months = max(0, int(round(customer_delay_days / 30)))
inflows = np.zeros(period)
for i in range(period):
    inflows[i] += rev[i] * vat_multiplier * (factoring_share / 100) * (factoring_advance / 100)
    
    target_month = i + customer_delay_months
    if target_month < period:
        inflows[target_month] += rev[i] * vat_multiplier * ((100 - factoring_share) / 100)
        inflows[target_month] += rev[i] * vat_multiplier * (factoring_share / 100) * ((100 - factoring_advance) / 100)

# Постоянные расходы
base_other_opex = 150_000
fixed_infrastructure_opex = monthly_warehouse + monthly_office
base_total_non_fot_opex = base_other_opex + fixed_infrastructure_opex

opex = np.full(period, base_total_non_fot_opex + monthly_fot)
for i in range(6, period):
    opex[i] = (base_total_non_fot_opex * 1.2) + monthly_fot

taxes_and_commissions = rev * 0.05

outflows = cogs_payments + opex + taxes_and_commissions
net_cf = inflows - outflows

cum_cf = np.cumsum(net_cf)
cash_balance_raw = cum_cf + initial_cash_buffer

# --- РАСЧЕТ ДОТАЦИЙ ДЛЯ ПОКРЫТИЯ КАЖДОГО РАЗРЫВА ---
monthly_investments = np.zeros(period)
funded_cash_balance = np.zeros(period)
curr_balance = initial_cash_buffer

for i in range(period):
    potential_balance = curr_balance + net_cf[i]
    if potential_balance < 0:
        needed_injection = abs(potential_balance)
        monthly_investments[i] = needed_injection
        curr_balance = 0.0
    else:
        monthly_investments[i] = 0.0
        curr_balance = potential_balance
    funded_cash_balance[i] = curr_balance

cum_investments = np.cumsum(monthly_investments)
total_investments_required = cum_investments[-1]

sum_purchases = sum(cogs_payments)
total_fot = sum(np.full(period, monthly_fot))
total_warehouse = sum(np.full(period, monthly_warehouse))
total_office = sum(np.full(period, monthly_office))
total_taxes = sum(taxes_and_commissions)
total_other_opex = sum(opex) - total_fot - total_warehouse - total_office

# --- KPI МЕТРИКИ ---
max_deficit = min(min(cum_cf), 0)
net_profit = sum(rev * (margin_pct / 100)) - sum(opex) - sum(taxes_and_commissions) - (initial_purchase * 0.15)
roi = (net_profit / sum(rev)) * 100 if sum(rev) > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(f"Выручка (за {period} мес)", format_num_spaced(sum(rev)) + " руб.")
col2.metric("Сумма дотаций (инвестиций)", format_num_spaced(total_investments_required) + " руб.")
col3.metric("Макс. кассовый разрыв", format_num_spaced(max_deficit) + " руб.")
col4.metric("Чистая прибыль", format_num_spaced(net_profit) + " руб.")
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
    outflows=outflows,
    net_cf=net_cf,
    rev=rev,
    opex=opex,
    taxes_and_commissions=taxes_and_commissions,
    cogs_payments=cogs_payments,
    cum_cf=cum_cf,
    factoring_share=factoring_share,
    margin_pct=margin_pct,
    sum_purchases=sum_purchases,
    total_fot=total_fot,
    total_taxes=total_taxes,
    total_other_opex=total_other_opex
)

tab_ex1, tab_ex2 = st.tabs(["📥 Скачать HTML-отчет", "✉️ Отправить HTML на email"])

with tab_ex1:
    st.download_button(
        label="💾 Скачать файл отчета",
        data=html_data,
        file_name="Kraivin_Financial_Report.html",
        mime="text/html",
        use_container_width=True
    )

with tab_ex2:
    email_input = st.text_input("Email получателя", "partner@krayvin.ru")
    if st.button("🚀 Отправить отчет на email"):
        if send_report_to_email(email_input, html_data):
            st.success("Отчет успешно отправлен!")
        else:
            st.error("Ошибка при отправке.")

st.divider()

# --- ВИЗУАЛИЗАЦИЯ НА ВКЛАДКАХ С ПОДПИСЯМИ ЗНАЧЕНИЙ ---
st.subheader("📊 Аналитические панели и графики")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📦 Товарный цикл и Склад",
    "💸 Необходимые Инвестиции (Дотации)",
    "💰 Ликвидность и Денежный поток", 
    "📈 Рентабельность и Источники", 
    "📉 Накопленный итог и Расходы",
    "📊 Заказы и Выручка"
])

with tab1:
    st.markdown("### График партионных закупок и динамика склада")
    st.caption("Показывает моменты крупных оплат партий товара и постепенное списание складского остатка в течение 5 месяцев.")
    
    fig_stock = go.Figure()
    
    # Оплаты партий товара
    fig_stock.add_trace(go.Bar(
        x=x_labels,
        y=cogs_payments,
        name='Оплата партии поставщикам (руб)',
        marker_color='#642A38',
        text=[f"{v/1_000_000:.1f}М" if v > 0 else "" for v in cogs_payments],
        textposition='outside'
    ))
    
    # Остаток на складе
    fig_stock.add_trace(go.Scatter(
        x=x_labels,
        y=inventory_balance,
        name='Остаток товара на складе (руб себестоимости)',
        yaxis='y2',
        mode='lines+markers+text',
        line=dict(color='#B88645', width=3),
        text=[f"{v/1_000_000:.1f}М" for v in inventory_balance],
        textposition='top center'
    ))
    
    fig_stock.update_layout(
        xaxis_title="Месяц",
        yaxis_title="Оплата закупки в месяце (руб)",
        yaxis2=dict(
            title="Остаток склада (руб)",
            overlaying='y',
            side='right',
            showgrid=False
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified"
    )
    st.plotly_chart(fig_stock, use_container_width=True)

with tab2:
    st.markdown("### График потребности в инвестициях (дотациях)")
    st.caption("Пики дотаций приходятся на месяцы финансирования крупных партий (1-й и 6-й месяцы).")
    
    fig_inv = go.Figure()
    fig_inv.add_trace(go.Bar(
        x=x_labels, 
        y=monthly_investments, 
        name='Дотация в месяце (руб)',
        marker_color='#B88645',
        text=[f"{v:,.0f}".replace(",", " ") if v > 0 else "" for v in monthly_investments],
        textposition='outside'
    ))
    
    fig_inv.add_trace(go.Scatter(
        x=x_labels, 
        y=cum_investments, 
        name='Накопленный объем дотаций',
        yaxis='y2',
        mode='lines+markers+text',
        line=dict(color='#642A38', width=3),
        text=[f"{v:,.0f}".replace(",", " ") if v > 0 else "" for v in cum_investments],
        textposition='top left'
    ))
    
    fig_inv.update_layout(
        xaxis_title="Месяц",
        yaxis_title="Сумма дотации за месяц (руб)",
        yaxis2=dict(
            title="Накопленные дотации (руб)",
            overlaying='y',
            side='right',
            showgrid=False
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified"
    )
    st.plotly_chart(fig_inv, use_container_width=True)
    
    inv_df = pd.DataFrame({
        "Месяц": x_labels,
        "Выручка (руб)": [format_num_spaced(v) for v in rev],
        "Оплата товара (руб)": [format_num_spaced(v) for v in cogs_payments],
        "Поступления от клиентов/фактора": [format_num_spaced(v) for v in inflows],
        "Все выплаты (закупка + OPEX)": [format_num_spaced(v) for v in outflows],
        "Чистое сальдо месяца": [format_num_spaced(v) for v in net_cf],
        "Требуемая дотация в месяце": [format_num_spaced(v) for v in monthly_investments],
        "Всего инвестировано накопленно": [format_num_spaced(v) for v in cum_investments]
    })
    st.dataframe(inv_df, hide_index=True, use_container_width=True)

with tab3:
    st.markdown("### Динамика ликвидности (с учетом дотаций и без)")
    fig1 = go.Figure()
    
    fig1.add_trace(go.Scatter(
        x=x_labels, y=cash_balance_raw, mode='lines+markers+text', name='Баланс без дотаций (кассовый разрыв)',
        text=[f"{v:,.0f}".replace(",", " ") for v in cash_balance_raw], textposition="top center",
        line=dict(color='#A27B5C', width=2, dash='dash')
    ))
    
    fig1.add_trace(go.Scatter(
        x=x_labels, y=funded_cash_balance, mode='lines+markers+text', name='Баланс на счете с дотациями',
        text=[f"{v:,.0f}".replace(",", " ") for v in funded_cash_balance], textposition="bottom center",
        line=dict(color='#642A38', width=3), fill='tozeroy', fillcolor='rgba(100, 42, 56, 0.1)'
    ))
    
    fig1.add_hline(y=0, line_dash="dot", line_color="red", annotation_text="Граница дефицита")
    fig1.update_layout(xaxis_title="Месяц", yaxis_title="Рубли", hovermode="x unified")
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("### Структура месячного денежного потока")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=x_labels, y=inflows, name='Поступления от продаж', marker_color='#E3C293', text=[f"{v:,.0f}".replace(",", " ") for v in inflows], textposition='auto'))
    fig2.add_trace(go.Bar(x=x_labels, y=-outflows, name='Выплаты (закупки + OPEX)', marker_color='#642A38', text=[f"{v:,.0f}".replace(",", " ") for v in outflows], textposition='auto'))
    fig2.add_trace(go.Scatter(x=x_labels, y=net_cf, name='Чистый поток', marker_color='#B88645', mode='lines+markers'))
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

    st.markdown("### Структура притока денежных средств по источникам")
    fig4 = go.Figure()
    dir_inf = rev * vat_multiplier * ((100 - factoring_share) / 100)
    fact_inf = rev * vat_multiplier * (factoring_share / 100)
    fig4.add_trace(go.Bar(x=x_labels, y=dir_inf, name='Оплата от клиентов', marker_color='#642A38'))
    fig4.add_trace(go.Bar(x=x_labels, y=fact_inf, name='Факторинг', marker_color='#E3C293'))
    fig4.update_layout(barmode='stack', xaxis_title="Месяц", yaxis_title="Рубли", hovermode="x unified")
    st.plotly_chart(fig4, use_container_width=True)

with tab5:
    st.markdown("### Накопленный денежный поток (без внешних вливаний)")
    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(
        x=x_labels, y=cum_cf, mode='lines+markers+text', name='Накопленный чистый поток',
        text=[f"{v:,.0f}".replace(",", " ") for v in cum_cf], textposition="top center",
        line=dict(color='#642A38', width=3), fill='tozeroy', fillcolor='rgba(227, 194, 147, 0.2)'
    ))
    fig5.add_hline(y=0, line_dash="dot", line_color="red", annotation_text="Нулевой баланс")
    fig5.update_layout(xaxis_title="Месяц", yaxis_title="Рубли", hovermode="x unified")
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("### Структура совокупных расходов")
    exp_labels = ['Склад', 'Офис', 'ФОТ (Команда)', 'Прочие OPEX', 'Налоги и сборы', 'Закупки товара']
    exp_vals = [total_warehouse, total_office, total_fot, total_other_opex, total_taxes, sum_purchases]
    tot_exp = sum(exp_vals) or 1
    exp_pcts = [v / tot_exp * 100 for v in exp_vals]
    
    fig6 = go.Figure(data=[go.Bar(
        y=exp_labels, x=exp_pcts, orientation='h',
        text=[f"{p:.1f}%" for p in exp_pcts], textposition='auto',
        marker_color=['#8B5E3C', '#A27B5C', '#E3C293', '#D0C2B8', '#B88645', '#642A38']
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
