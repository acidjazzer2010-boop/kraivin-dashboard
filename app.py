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

st.title("Анализ денежных потоков и рентабельности")
st.markdown("Интерактивная финансовая модель для сценарного анализа кассовых разрывов.")

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ФОРМАТИРОВАНИЯ ---
def format_num_spaced(val: int) -> str:
    """Форматирует целое число с разделителями тысяч через пробел."""
    return f"{int(val):,}".replace(",", " ")

def money_input(label: str, default_val: int, key: str, help_text: str = None) -> int:
    """Виджет ввода денежных сумм с автоматическим разделением тысяч пробелами."""
    if key not in st.session_state:
        st.session_state[key] = format_num_spaced(default_val)
    
    raw_val = st.sidebar.text_input(label, value=st.session_state[key], key=f"raw_{key}", help=help_text)
    
    # Очищаем ввод от пробелов, запятых и букв
    clean_val = re.sub(r"[^\d]", "", raw_val)
    if not clean_val:
        clean_val = str(default_val)
    
    parsed_int = int(clean_val)
    formatted_str = format_num_spaced(parsed_int)
    
    # Обновляем состояние с пробелами
    st.session_state[key] = formatted_str
    
    # Визуальная подсказка под полем ввода с точным форматированием
    st.sidebar.caption(f"Выбрано: **{formatted_str} руб.**")
    return parsed_int

# --- БОКОВАЯ ПАНЕЛЬ (ВВОД ДАННЫХ) ---

st.sidebar.header("Параметры модели")

ru_months_full = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
col_m, col_y = st.sidebar.columns(2)
start_month_idx = col_m.selectbox("Месяц старта", range(12), format_func=lambda x: ru_months_full[x])
start_year = col_y.selectbox("Год старта", [2026, 2027])

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

st.sidebar.subheader("Стартовый капитал и закупки")
initial_purchase = money_input(
    "Первоначальная закупка товара (руб)", 
    default_val=5_000_000, 
    key="init_purchase_key",
    help_text="Введите сумму (можно с пробелами)"
)

initial_cash_buffer = money_input(
    "Стартовый буфер на счете (руб)", 
    default_val=2_000_000, 
    key="init_buffer_key",
    help_text="Остаток свободных ДС на старте"
)

st.sidebar.subheader("Динамика продаж")
aov = money_input(
    "Средняя сумма заказа / AOV (руб)", 
    default_val=150_000, 
    key="aov_key"
)

start_orders = st.sidebar.number_input(
    "Заказов в 1-й месяц (шт)", 
    value=40, 
    step=1
)
orders_growth = st.sidebar.slider("Ежемесячный прирост заказов (%)", 0, 100, 15, step=1)
scale_factor = st.sidebar.slider("Коэффициент масштабирования продаж", 0.5, 3.0, 1.0, 0.1)

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
        orders[i] = start_orders * scale_factor
    else:
        orders[i] = orders[i-1] * (1 + (orders_growth / 100))
    rev[i] = orders[i] * aov

cogs_pct = 1 - (margin_pct / 100)
cogs_no_vat = rev * cogs_pct
cogs_vat = cogs_no_vat * vat_multiplier

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

outflows = cogs_payments + opex + taxes_and_commissions
net_cf = inflows - outflows

cum_cf = np.cumsum(net_cf)
cash_balance = cum_cf + initial_cash_buffer

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

def format_rub(val):
    return f"{val:,.0f}".replace(",", " ") + " руб."

col1, col2, col3, col4 = st.columns(4)
col1.metric(f"Выручка (за {period} мес)", format_rub(sum(rev)))
col2.metric("Макс. кассовый разрыв", format_rub(max_deficit))
col3.metric("Чистая прибыль", format_rub(net_profit))
col4.metric("Рентабельность по ЧП", f"{roi:.1f}%")

st.divider()

# --- ПАНЕЛЬ ЭКСПОРТА ---
st.subheader("📤 Экспорт отчета в HTML")

html_data = generate_html_report_bytes(
    period=period,
    start_date=f"{ru_months_full[start_month_idx]} {start_year}",
    sum_rev=format_rub(sum(rev)),
    max_deficit=format_rub(max_deficit),
    net_profit=format_rub(net_profit),
    roi=f"{roi:.1f}%",
    initial_cash_buffer=format_rub(initial_cash_buffer),
    initial_purchase=format_rub(initial_purchase),
    x_labels=x_labels,
    cash_balance=cash_balance,
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

tab1, tab2, tab3 = st.tabs(["💰 Ликвидность и Денежный поток", "📈 Рентабельность и Источники", "📉 Накопленный итог и Расходы"])

with tab1:
    st.markdown("### Динамика ликвидности и остаток средств")
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=x_labels, y=cash_balance, mode='lines+markers+text', name='Остаток ДС',
        text=[f"{v:,.0f}".replace(",", " ") for v in cash_balance], textposition="top center",
        line=dict(color='#642A38', width=3), fill='tozeroy', fillcolor='rgba(100, 42, 56, 0.1)'
    ))
    fig1.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Дефицит")
    fig1.update_layout(xaxis_title="Месяц", yaxis_title="Рубли", hovermode="x unified")
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("### Структура месячного денежного потока")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=x_labels, y=inflows, name='Поступления', marker_color='#E3C293', text=[f"{v:,.0f}".replace(",", " ") for v in inflows], textposition='auto'))
    fig2.add_trace(go.Bar(x=x_labels, y=-outflows, name='Выплаты', marker_color='#642A38', text=[f"{v:,.0f}".replace(",", " ") for v in outflows], textposition='auto'))
    fig2.add_trace(go.Scatter(x=x_labels, y=net_cf, name='Чистый поток', marker_color='#B88645', mode='lines+markers'))
    fig2.update_layout(barmode='relative', xaxis_title="Месяц", yaxis_title="Рубли", hovermode="x unified")
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.markdown("### Динамика маржинальности и операционной прибыли (EBITDA)")
    fig3 = go.Figure()
    ebitda_vals = rev - opex - taxes_and_commissions - (cogs_payments * 0.3)
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

with tab3:
    st.markdown("### Накопленный денежный поток")
    fig5 = go.Figure()
    total_cash = cum_cf + initial_cash_buffer
    fig5.add_trace(go.Scatter(
        x=x_labels, y=total_cash, mode='lines+markers+text', name='Накопленный ДС',
        text=[f"{v:,.0f}".replace(",", " ") for v in total_cash], textposition="top center",
        line=dict(color='#642A38', width=3), fill='tozeroy', fillcolor='rgba(227, 194, 147, 0.2)'
    ))
    fig5.add_hline(y=initial_cash_buffer, line_dash="dash", line_color="#B88645", annotation_text="Стартовый буфер")
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
