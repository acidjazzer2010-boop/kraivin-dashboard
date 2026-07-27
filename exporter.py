import os
import io
import time
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

def generate_gamma_presentation(metrics_data):
    """
    Интеграция с Gamma Generate API для создания профессиональной инвестиционной презентации с ИИ-версткой.
    Документация: https://developers.gamma.app/
    """
    api_key = os.getenv("GAMMA_API_KEY", "your_gamma_api_key_here")
    url = "https://public-api.gamma.app/v1.0/generations"
    
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    
    # Формируем структурированный промпт для ИИ-дизайнера презентаций
    prompt_text = f"""
    Create a professional, modern financial and investment pitch deck for the wine trading company 'Krayvin'.
    The presentation must follow a high-end fintech / VC design style with clean card layouts, dark wine red (#642A38) and warm sand (#E3C293) accents, light background, and strong visual hierarchy.
    
    Key Financial Metrics to include across structured slides:
    1. Title Slide: Krayvin Financial Model & Cash Flow Analysis (Period: {metrics_data.get('period')} months, Start: {metrics_data.get('start_date')}).
    2. Executive Summary / KPIs:
       - Total Revenue: {metrics_data.get('sum_rev')}
       - Max Cash Deficit: {metrics_data.get('max_deficit')}
       - Net Profit: {metrics_data.get('net_profit')}
       - Net Profit Margin (ROI): {metrics_data.get('roi')}
       - Initial Cash Buffer: {metrics_data.get('initial_cash_buffer')}
       - Initial Stock Purchase: {metrics_data.get('initial_purchase')}
    3. Liquidity & Cash Gap Management: Analysis of cash balance dynamics, safety buffer zones, and risk mitigation.
    4. Revenue & Cash Flow Structure: Breakdown of client payments vs. factoring share ({metrics_data.get('factoring_share')}%).
    5. Profitability & EBITDA: Operational profitability dynamics alongside planned margin structure ({metrics_data.get('margin_pct')}%).
    6. Expense Breakdown: Detailed structure including COGS, team payroll (FOT), taxes, and operating expenses.
    7. Monthly Cash Flow Forecast Table: Comprehensive structured financial overview.
    """
    
    payload = {
        "inputText": prompt_text,
        "format": "presentation",
        "textMode": "generate",
        "numCards": 7,
        "exportAs": "pptx",
        "imageOptions": {
            "source": "webFreeToUseCommercially"
        },
        "textOptions": {
            "tone": "professional",
            "audience": "executive investors"
        }
    }

    try:
        # 1. Запуск асинхронной генерации
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code not in [200, 201, 202]:
            print(f"Gamma API Init Error [{response.status_code}]: {response.text}")
            return None
            
        data = response.json()
        generation_id = data.get("generationId")
        if not generation_id:
            return None
            
        # 2. Опрос статуса генерации (Polling каждые 5 секунд, до 2 минут)
        status_url = f"https://public-api.gamma.app/v1.0/generations/{generation_id}"
        for _ in range(24):
            time.sleep(5)
            status_resp = requests.get(status_url, headers=headers, timeout=15)
            if status_resp.status_code == 200:
                status_data = status_resp.json()
                status = status_data.get("status")
                if status == "completed":
                    return {
                        "gammaUrl": status_data.get("gammaUrl"),
                        "exportUrl": status_data.get("exportUrl") # Ссылка на скачивание готового PPTX
                    }
                elif status == "failed":
                    print("Gamma generation failed.")
                    return None
        return None
    except Exception as e:
        print(f"Gamma API Exception: {e}")
        return None

def send_report_to_email(to_email, presentation_link):
    smtp_server = os.getenv("SMTP_SERVER", "smtp.yandex.ru")
    smtp_port = int(os.getenv("SMTP_PORT", 465))
    sender_email = os.getenv("SMTP_USER", "finance@krayvin.ru")
    sender_password = os.getenv("SMTP_PASSWORD", "ваш_пароль_приложения")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = "🍷 КРАЙВИН: ИИ-финансовый отчёт (премиум-верстка Gamma)"

    body = f"Здравствуйте!\n\nИнвестиционный отчет компании КРАЙВИН успешно сгенерирован с помощью ИИ-платформы.\n\nВы можете ознакомиться с интерактивной презентацией по ссылке:\n{presentation_link}\n\nС уважением,\nФинансовый департамент КРАЙВИН"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"SMTP Error: {e}")
        return False
