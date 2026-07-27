import os
import io
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

import numpy as np
import matplotlib.pyplot as plt

def _fig_to_base64(fig):
    img_io = io.BytesIO()
    fig.savefig(img_io, format='png', bbox_inches='tight', facecolor=fig.get_facecolor())
    img_io.seek(0)
    encoded = base64.b64encode(img_io.read()).decode('utf-8')
    plt.close(fig)
    return encoded

def create_chart_liquidity_base64(x_labels, cash_balance):
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.plot(x_labels, cash_balance, color='#642A38', linewidth=3, marker='o', markersize=5, markerfacecolor='#E3C293')
    ax.fill_between(x_labels, cash_balance, 0, color='#642A38', alpha=0.08)
    ax.axhline(0, color='#D32F2F', linestyle='--', linewidth=1.5, label='Критический порог (0)')
    ax.set_ylabel("Остаток (руб.)", fontsize=10, fontweight='bold', color='#333333')
    plt.xticks(rotation=25, ha='right', fontsize=9, color='#555555')
    plt.yticks(fontsize=9, color='#555555')
    plt.grid(axis='y', linestyle=':', alpha=0.6, color='#CCCCCC')
    for spine in ['top', 'right']: ax.spines[spine].set_visible(False)
    ax.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#E0E0E0', fontsize=9)
    plt.tight_layout()
    return _fig_to_base64(fig)

def create_chart_cash_flow_base64(x_labels, inflows, outflows, net_cf):
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    x_indices = np.arange(len(x_labels))
    width = 0.35
    ax.bar(x_indices - width/2, inflows, width, label='Поступления', color='#E3C293', alpha=0.9)
    ax.bar(x_indices + width/2, -outflows, width, label='Выплаты', color='#642A38', alpha=0.9)
    ax.plot(x_indices, net_cf, color='#B88645', linewidth=2.5, marker='s', markersize=5, label='Чистый поток')
    ax.set_xticks(x_indices)
    ax.set_xticklabels(x_labels, rotation=25, ha='right', fontsize=9, color='#555555')
    ax.set_ylabel("Сумма (руб.)", fontsize=10, fontweight='bold', color='#333333')
    plt.yticks(fontsize=9, color='#555555')
    plt.grid(axis='y', linestyle=':', alpha=0.6, color='#CCCCCC')
    for spine in ['top', 'right']: ax.spines[spine].set_visible(False)
    ax.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#E0E0E0', fontsize=9)
    plt.tight_layout()
    return _fig_to_base64(fig)

def create_chart_margin_ebitda_base64(x_labels, rev, opex, taxes_and_commissions, cogs_payments, margin_pct):
    fig, ax1 = plt.subplots(figsize=(10, 4.2), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')
    ax1.set_facecolor('#FFFFFF')
    ebitda = rev - opex - taxes_and_commissions - (cogs_payments * 0.3)
    ax1.bar(x_labels, ebitda, color='#642A38', alpha=0.85, width=0.45, label='EBITDA')
    ax1.set_ylabel("EBITDA (руб.)", color='#642A38', fontsize=10, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor='#642A38', labelsize=9)
    plt.xticks(rotation=25, ha='right', fontsize=9, color='#555555')
    ax2 = ax1.twinx()
    ax2.plot(x_labels, [margin_pct]*len(x_labels), color='#E3C293', linewidth=2.5, marker='o', markersize=5, label='Маржинальность (%)')
    ax2.set_ylabel("Маржа (%)", color='#B88645', fontsize=10, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor='#B88645', labelsize=9)
    ax2.set_ylim(0, 50)
    plt.grid(axis='y', linestyle=':', alpha=0.3, color='#CCCCCC')
    for spine in ['top']: 
        ax1.spines[spine].set_visible(False)
        ax2.spines[spine].set_visible(False)
    plt.tight_layout()
    return _fig_to_base64(fig)

def create_chart_sources_base64(x_labels, rev, factoring_share):
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    x_indices = np.arange(len(x_labels))
    width = 0.45
    factoring_inflows = rev * 1.2 * (factoring_share / 100)
    direct_inflows = rev * 1.2 * ((100 - factoring_share) / 100)
    ax.bar(x_indices, direct_inflows, width, label='Оплата от клиентов', color='#642A38', alpha=0.9)
    ax.bar(x_indices, factoring_inflows, width, bottom=direct_inflows, label='Факторинг', color='#E3C293', alpha=0.9)
    ax.set_xticks(x_indices)
    ax.set_xticklabels(x_labels, rotation=25, ha='right', fontsize=9, color='#555555')
    ax.set_ylabel("Поступления (руб.)", fontsize=10, fontweight='bold', color='#333333')
    plt.yticks(fontsize=9, color='#555555')
    plt.grid(axis='y', linestyle=':', alpha=0.6, color='#CCCCCC')
    for spine in ['top', 'right']: ax.spines[spine].set_visible(False)
    ax.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#E0E0E0', fontsize=9)
    plt.tight_layout()
    return _fig_to_base64(fig)

def create_chart_cumulative_base64(x_labels, cum_cf, initial_cash_buffer):
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    total_cash_line = cum_cf + initial_cash_buffer
    ax.plot(x_labels, total_cash_line, color='#642A38', linewidth=3, marker='o', markersize=5, label='Накопленный ДС')
    ax.axhline(initial_cash_buffer, color='#B88645', linestyle='--', linewidth=1.5, label='Стартовый буфер')
    ax.axhline(0, color='#D32F2F', linestyle=':', linewidth=1.5, label='Нулевой уровень')
    ax.fill_between(x_labels, total_cash_line, initial_cash_buffer, where=(total_cash_line >= initial_cash_buffer), color='#642A38', alpha=0.08, interpolate=True)
    ax.set_ylabel("Баланс (руб.)", fontsize=10, fontweight='bold', color='#333333')
    plt.xticks(rotation=25, ha='right', fontsize=9, color='#555555')
    plt.yticks(fontsize=9, color='#555555')
    plt.grid(axis='y', linestyle=':', alpha=0.6, color='#CCCCCC')
    for spine in ['top', 'right']: ax.spines[spine].set_visible(False)
    ax.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#E0E0E0', fontsize=9)
    plt.tight_layout()
    return _fig_to_base64(fig)

def create_chart_expenses_bar_base64(sum_purchases, total_fot, total_taxes, total_other_opex):
    fig, ax = plt.subplots(figsize=(10, 3.8), dpi=200)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    categories = ['Операционные расходы', 'Налоги и сборы', 'ФОТ (Команда)', 'Закупки товара']
    values = [total_other_opex, total_taxes, total_fot, sum_purchases]
    total = sum(values) if sum(values) > 0 else 1
    percentages = [v / total * 100 for v in values]
    colors = ['#D0C2B8', '#B88645', '#E3C293', '#642A38']
    y_pos = np.arange(len(categories))
    bars = ax.barh(y_pos, percentages, color=colors, height=0.55)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories, fontsize=10, fontweight='bold', color='#333333')
    ax.set_xlabel("Доля в расходах (%)", fontsize=10, fontweight='bold', color='#333333')
    ax.set_xlim(0, 100)
    for bar, pct in zip(bars, percentages):
        width = bar.get_width()
        ax.text(width + 2, bar.get_y() + bar.get_height()/2, f'{pct:.1f}%', va='center', ha='left', fontsize=9, fontweight='bold', color='#333333')
    plt.grid(axis='x', linestyle=':', alpha=0.6, color='#CCCCCC')
    for spine in ['top', 'right', 'left']: ax.spines[spine].set_visible(False)
    plt.tight_layout()
    return _fig_to_base64(fig)


def generate_html_report_bytes(**kwargs):
    period = kwargs.get('period', 12)
    start_date = kwargs.get('start_date', '')
    sum_rev = kwargs.get('sum_rev', '')
    max_deficit = kwargs.get('max_deficit', '')
    net_profit = kwargs.get('net_profit', '')
    roi = kwargs.get('roi', '')
    initial_cash_buffer = kwargs.get('initial_cash_buffer', '')
    initial_purchase = kwargs.get('initial_purchase', '')
    
    x_labels = kwargs.get('x_labels', [])
    cash_balance = kwargs.get('cash_balance', [])
    inflows = kwargs.get('inflows', [])
    outflows = kwargs.get('outflows', [])
    net_cf = kwargs.get('net_cf', [])
    rev = kwargs.get('rev', [])
    opex = kwargs.get('opex', [])
    taxes = kwargs.get('taxes_and_commissions', [])
    cogs = kwargs.get('cogs_payments', [])
    cum_cf = kwargs.get('cum_cf', [])
    factoring_share = kwargs.get('factoring_share', 0)
    margin_pct = kwargs.get('margin_pct', 20)
    sum_purchases = kwargs.get('sum_purchases', 0)
    total_fot = kwargs.get('total_fot', 0)
    total_taxes = kwargs.get('total_taxes', 0)
    total_other_opex = kwargs.get('total_other_opex', 0)

    img_liq = create_chart_liquidity_base64(x_labels, cash_balance)
    img_cf = create_chart_cash_flow_base64(x_labels, inflows, outflows, net_cf)
    img_ebitda = create_chart_margin_ebitda_base64(x_labels, rev, opex, taxes, cogs, margin_pct)
    img_sources = create_chart_sources_base64(x_labels, rev, factoring_share)
    img_cum = create_chart_cumulative_base64(x_labels, cum_cf, initial_cash_buffer if isinstance(initial_cash_buffer, (int, float)) else 0)
    img_exp = create_chart_expenses_bar_base64(sum_purchases, total_fot, total_taxes, total_other_opex)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>КРАЙВИН — Финансовый отчет</title>
        <style>
            body {{
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                color: #2D2D2D;
                margin: 0;
                padding: 30px;
                background-color: #FAFAF8;
            }}
            .container {{
                max-width: 900px;
                margin: 0 auto;
            }}
            .header {{
                background: linear-gradient(135deg, #642A38 0%, #451C26 100%);
                color: white;
                padding: 30px;
                border-radius: 12px;
                margin-bottom: 25px;
                box-shadow: 0 4px 15px rgba(100, 42, 56, 0.15);
            }}
            .header h1 {{
                margin: 0 0 10px 0;
                font-size: 28px;
                font-weight: 700;
                letter-spacing: 0.5px;
            }}
            .header p {{
                margin: 0;
                color: #E3C293;
                font-size: 15px;
            }}
            .card {{
                background: white;
                border: 1px solid #E5E0DC;
                border-radius: 12px;
                padding: 25px;
                margin-bottom: 25px;
                box-shadow: 0 4px 12px rgba(100, 42, 56, 0.04);
            }}
            .kpi-grid {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 15px;
            }}
            .kpi-col {{
                background: #FDFCFB;
                border: 1px solid #E5E0DC;
                border-radius: 8px;
                padding: 15px;
            }}
            .kpi-label {{
                font-size: 11px;
                font-weight: 700;
                color: #888888;
                text-transform: uppercase;
                margin-bottom: 5px;
            }}
            .kpi-value {{
                font-size: 18px;
                font-weight: 700;
                color: #642A38;
            }}
            h2 {{
                font-size: 18px;
                color: #642A38;
                margin-top: 0;
                margin-bottom: 15px;
                border-bottom: 2px solid #E3C293;
                padding-bottom: 8px;
            }}
            .chart-container {{
                text-align: center;
                margin-top: 10px;
            }}
            .chart-container img {{
                max-width: 100%;
                height: auto;
                border-radius: 8px;
            }}
            table.data-table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
                font-size: 12px;
            }}
            table.data-table th {{
                background: #642A38;
                color: white;
                padding: 10px;
                text-align: center;
                font-weight: 600;
            }}
            table.data-table td {{
                padding: 9px 10px;
                border-bottom: 1px solid #E5E0DC;
                text-align: right;
            }}
            table.data-table td:first-child {{
                text-align: center;
                font-weight: 600;
            }}
            table.data-table tr:nth-child(even) td {{
                background: #F4F1EE;
            }}
            @media print {{
                body {{ background-color: white; padding: 0; }}
                .card {{ border: none; box-shadow: none; padding: 10px 0; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>КРАЙВИН — Финансовая модель</h1>
                <p>Горизонт планирования: {period} мес. &nbsp;|&nbsp; Старт: {start_date} &nbsp;|&nbsp; Инвестиционный аналитический отчёт</p>
            </div>

            <div class="card">
                <h2>Ключевые финансовые результаты (KPI)</h2>
                <div class="kpi-grid">
                    <div class="kpi-col">
                        <div class="kpi-label">Суммарная выручка</div>
                        <div class="kpi-value">{sum_rev}</div>
                    </div>
                    <div class="kpi-col">
                        <div class="kpi-label">Макс. кассовый разрыв</div>
                        <div class="kpi-value">{max_deficit}</div>
                    </div>
                    <div class="kpi-col">
                        <div class="kpi-label">Чистая прибыль</div>
                        <div class="kpi-value">{net_profit}</div>
                    </div>
                    <div class="kpi-col">
                        <div class="kpi-label">Рентабельность по ЧП</div>
                        <div class="kpi-value">{roi}</div>
                    </div>
                    <div class="kpi-col">
                        <div class="kpi-label">Стартовый буфер ДС</div>
                        <div class="kpi-value">{initial_cash_buffer}</div>
                    </div>
                    <div class="kpi-col">
                        <div class="kpi-label">Первоначальная закупка</div>
                        <div class="kpi-value">{initial_purchase}</div>
                    </div>
                </div>
            </div>

            <div class="card">
                <h2>1. Динамика ликвидности и остаток средств</h2>
                <div class="chart-container"><img src="data:image/png;base64,{img_liq}" /></div>
            </div>

            <div class="card">
                <h2>2. Структура месячного денежного потока</h2>
                <div class="chart-container"><img src="data:image/png;base64,{img_cf}" /></div>
            </div>

            <div class="card">
                <h2>3. Динамика маржинальности и EBITDA</h2>
                <div class="chart-container"><img src="data:image/png;base64,{img_ebitda}" /></div>
            </div>

            <div class="card">
                <h2>4. Структура притока ДС по источникам</h2>
                <div class="chart-container"><img src="data:image/png;base64,{img_sources}" /></div>
            </div>

            <div class="card">
                <h2>5. Накопленный денежный поток (Cumulative Cash Flow)</h2>
                <div class="chart-container"><img src="data:image/png;base64,{img_cum}" /></div>
            </div>

            <div class="card">
                <h2>6. Структура совокупных расходов</h2>
                <div class="chart-container"><img src="data:image/png;base64,{img_exp}" /></div>
            </div>

            <div class="card">
                <h2>7. Детализация денежных потоков по месяцам</h2>
                <table class="data-table">
                    <tr>
                        <th>Месяц</th>
                        <th>Выручка (руб)</th>
                        <th>Поступления (руб)</th>
                        <th>Выплаты (руб)</th>
                        <th>Остаток ДС (руб)</th>
                    </tr>
    """
    
    rows_count = min(len(x_labels), 12)
    for i in range(rows_count):
        html_content += f"""
                    <tr>
                        <td>{x_labels[i]}</td>
                        <td>{rev[i]:,.0f}".replace(",", " ")</td>
                        <td>{inflows[i]:,.0f}".replace(",", " ")</td>
                        <td>{outflows[i]:,.0f}".replace(",", " ")</td>
                        <td>{cash_balance[i]:,.0f}".replace(",", " ")</td>
                    </tr>
        """
        
    html_content += """
                </table>
            </div>
        </div>
    </body>
    </html>
    """

    html_io = io.BytesIO(html_content.encode('utf-8'))
    html_io.seek(0)
    return html_io


def send_report_to_email(to_email, html_bytes):
    smtp_server = os.getenv("SMTP_SERVER", "smtp.yandex.ru")
    smtp_port = int(os.getenv("SMTP_PORT", 465))
    sender_email = os.getenv("SMTP_USER", "finance@krayvin.ru")
    sender_password = os.getenv("SMTP_PASSWORD", "ваш_пароль_приложения")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = "🍷 КРАЙВИН: Премиальный финансовый отчёт (HTML Лонгрид)"

    body = "Здравствуйте!\n\nВо вложении находится профессиональный инвестиционный отчет компании КРАЙВИН в формате интерактивного HTML-лонгрида.\n\nС уважением,\nФинансовый департамент КРАЙВИН"
    msg.attach(MIMEText(body, 'plain'))

    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(html_bytes.getvalue())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename="Kraivin_Financial_Report.html")
    msg.attach(attachment)

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"SMTP Error: {e}")
        return False
