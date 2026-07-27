import os
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

import numpy as np
import matplotlib.pyplot as plt

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_matplotlib_chart_1(x_labels, cash_balance):
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=200)
    ax.plot(x_labels, cash_balance, color='#642A38', linewidth=3, marker='o', markersize=6)
    ax.fill_between(x_labels, cash_balance, 0, color='#642A38', alpha=0.1)
    ax.axhline(0, color='red', linestyle='--', linewidth=1.5)
    ax.set_title("Динамика ликвидности и остаток средств", fontsize=14, fontweight='bold', color='#642A38', pad=15)
    ax.set_ylabel("Рубли", fontsize=11, color='#333333')
    plt.xticks(rotation=30, ha='right', fontsize=10)
    plt.grid(axis='y', linestyle=':', alpha=0.5)
    plt.tight_layout()
    
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png', bbox_inches='tight')
    plt.close(fig)
    img_io.seek(0)
    return img_io

def create_matplotlib_chart_2(x_labels, inflows, outflows, net_cf):
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=200)
    x_indices = np.arange(len(x_labels))
    width = 0.35
    
    ax.bar(x_indices - width/2, inflows, width, label='Поступления', color='#E3C293')
    ax.bar(x_indices + width/2, -outflows, width, label='Выплаты', color='#642A38')
    ax.plot(x_indices, net_cf, color='#B88645', linewidth=2.5, marker='o', label='Чистый поток')
    
    ax.set_xticks(x_indices)
    ax.set_xticklabels(x_labels, rotation=30, ha='right', fontsize=10)
    ax.set_title("Структура месячного денежного потока", fontsize=14, fontweight='bold', color='#642A38', pad=15)
    ax.set_ylabel("Рубли", fontsize=11, color='#333333')
    ax.legend(frameon=True, facecolor='white', edgecolor='none')
    plt.grid(axis='y', linestyle=':', alpha=0.5)
    plt.tight_layout()
    
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png', bbox_inches='tight')
    plt.close(fig)
    img_io.seek(0)
    return img_io

def generate_pptx_bytes(period, start_month_idx, start_year, ru_months_full, x_labels, 
                        sum_rev, max_deficit, net_profit, roi, initial_cash_buffer, 
                        initial_purchase, inflows, outflows, cash_balance, rev, net_cf,
                        customer_delay_days, delay_days, factoring_share, logo_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    c_wine = RGBColor(100, 42, 56)
    c_sand = RGBColor(227, 194, 147)
    c_dark = RGBColor(30, 30, 30)
    c_light_bg = RGBColor(248, 246, 244)
    c_white = RGBColor(255, 255, 255)
    c_card_border = RGBColor(220, 210, 205)

    font_black = "ua-BRAND-black"
    font_bold = "ua-BRAND-bold"
    font_regular = "ua-BRAND-regular"

    blank_layout = prs.slide_layouts[6]

    def add_corner_logo(slide):
        if logo_path and os.path.exists(logo_path):
            slide.shapes.add_picture(logo_path, Inches(11.8), Inches(0.4), width=Inches(1.1))

    def format_rub(val):
        return f"{val:,.0f}".replace(",", " ") + " руб."

    # СЛАЙД 1: ТИТУЛЬНЫЙ
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = c_wine
    bg1.line.fill.background()

    accent1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(2.0), Inches(0.15), Inches(3.5))
    accent1.fill.solid()
    accent1.fill.fore_color.rgb = c_sand
    accent1.line.fill.background()

    if logo_path and os.path.exists(logo_path):
        slide1.shapes.add_picture(logo_path, Inches(1.2), Inches(0.8), width=Inches(1.8))

    txBox = slide1.shapes.add_textbox(Inches(1.2), Inches(2.5), Inches(10.5), Inches(3.5))
    tf = txBox.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "КРАЙВИН"
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.color.rgb = c_white
    p.font.name = font_black

    p2 = tf.add_paragraph()
    p2.text = "Финансовая модель и анализ денежных потоков"
    p2.font.size = Pt(26)
    p2.font.color.rgb = c_sand
    p2.font.name = font_bold
    p2.space_before = Pt(10)

    p3 = tf.add_paragraph()
    p3.text = f"Горизонт планирования: {period} мес.  |  Старт: {ru_months_full[start_month_idx]} {start_year}"
    p3.font.size = Pt(16)
    p3.font.color.rgb = c_white
    p3.font.name = font_regular
    p3.space_before = Pt(35)

    # СЛАЙД 2: KPI КАРТОЧКИ
    slide2 = prs.slides.add_slide(blank_layout)
    bg2 = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg2.fill.solid()
    bg2.fill.fore_color.rgb = c_light_bg
    bg2.line.fill.background()
    add_corner_logo(slide2)

    title_box2 = slide2.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(10.0), Inches(0.8))
    p_t2 = title_box2.text_frame.paragraphs[0]
    p_t2.text = "Ключевые финансовые результаты"
    p_t2.font.size = Pt(28)
    p_t2.font.bold = True
    p_t2.font.color.rgb = c_wine
    p_t2.font.name = font_bold

    kpis = [
        ("Суммарная выручка", format_rub(sum_rev)),
        ("Макс. кассовый разрыв", format_rub(max_deficit)),
        ("Чистая прибыль", format_rub(net_profit)),
        ("Рентабельность по ЧП", f"{roi:.1f}%"),
        ("Начальный буфер ДС", format_rub(initial_cash_buffer)),
        ("Первоначальная закупка", format_rub(initial_purchase))
    ]

    card_w, card_h = Inches(3.6), Inches(2.1)
    start_x, start_y = Inches(0.8), Inches(1.6)
    gap_x, gap_y = Inches(0.4), Inches(0.35)

    for idx, (label, val) in enumerate(kpis):
        col_idx = idx % 3
        row_idx = idx // 3
        x = start_x + col_idx * (card_w + gap_x)
        y = start_y + row_idx * (card_h + gap_y)

        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, card_w, card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = c_white
        card.line.color.rgb = c_card_border
        card.line.width = Pt(1)

        tf_card = card.text_frame
        tf_card.word_wrap = True
        tf_card.margin_left = Inches(0.25)
        tf_card.margin_top = Inches(0.2)
        
        p_lbl = tf_card.paragraphs[0]
        p_lbl.text = label.upper()
        p_lbl.font.size = Pt(11)
        p_lbl.font.color.rgb = RGBColor(120, 120, 120)
        p_lbl.font.bold = True
        p_lbl.font.name = font_bold

        p_val = tf_card.add_paragraph()
        p_val.text = val
        p_val.font.size = Pt(20)
        p_val.font.color.rgb = c_wine
        p_val.font.bold = True
        p_val.font.name = font_black
        p_val.space_before = Pt(8)

    # СЛАЙД 3: ГРАФИК ЛИКВИДНОСТИ
    slide3 = prs.slides.add_slide(blank_layout)
    bg3 = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg3.fill.solid()
    bg3.fill.fore_color.rgb = c_light_bg
    bg3.line.fill.background()
    add_corner_logo(slide3)

    tbox3 = slide3.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10.0), Inches(0.8))
    tbox3.text_frame.paragraphs[0].text = "Динамика ликвидности и остаток средств"
    tbox3.text_frame.paragraphs[0].font.size = Pt(26)
    tbox3.text_frame.paragraphs[0].font.bold = True
    tbox3.text_frame.paragraphs[0].font.color.rgb = c_wine
    tbox3.text_frame.paragraphs[0].font.name = font_bold

    chart1_img = create_matplotlib_chart_1(x_labels, cash_balance)
    slide3.shapes.add_picture(chart1_img, Inches(0.8), Inches(1.3), width=Inches(11.7))

    # СЛАЙД 4: ГРАФИК ДЕНЕЖНОГО ПОТОКА
    slide4 = prs.slides.add_slide(blank_layout)
    bg4 = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg4.fill.solid()
    bg4.fill.fore_color.rgb = c_light_bg
    bg4.line.fill.background()
    add_corner_logo(slide4)

    tbox4 = slide4.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10.0), Inches(0.8))
    tbox4.text_frame.paragraphs[0].text = "Структура месячного денежного потока"
    tbox4.text_frame.paragraphs[0].font.size = Pt(26)
    tbox4.text_frame.paragraphs[0].font.bold = True
    tbox4.text_frame.paragraphs[0].font.color.rgb = c_wine
    tbox4.text_frame.paragraphs[0].font.name = font_bold

    chart2_img = create_matplotlib_chart_2(x_labels, inflows, outflows, net_cf)
    slide4.shapes.add_picture(chart2_img, Inches(0.8), Inches(1.3), width=Inches(11.7))

    # СЛАЙД 5: ТАБЛИЦА ДЕТАЛИЗАЦИИ
    slide5 = prs.slides.add_slide(blank_layout)
    bg5 = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg5.fill.solid()
    bg5.fill.fore_color.rgb = c_light_bg
    bg5.line.fill.background()
    add_corner_logo(slide5)

    title_box5 = slide5.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(10.0), Inches(0.8))
    p_t5 = title_box5.text_frame.paragraphs[0]
    p_t5.text = "Детализация денежных потоков по месяцам"
    p_t5.font.size = Pt(28)
    p_t5.font.bold = True
    p_t5.font.color.rgb = c_wine
    p_t5.font.name = font_bold

    rows = min(period + 1, 13)
    cols = 5
    table_shape = slide5.shapes.add_table(rows, cols, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.2))
    table = table_shape.table
    
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(2.4)
    table.columns[2].width = Inches(2.4)
    table.columns[3].width = Inches(2.4)
    table.columns[4].width = Inches(2.3)

    headers = ["Месяц", "Выручка (руб)", "Поступления (руб)", "Выплаты (руб)", "Остаток ДС (руб)"]
    for col_idx, text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = text
        cell.fill.solid()
        cell.fill.fore_color.rgb = c_wine
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = c_white
            p.font.name = font_bold
            p.alignment = PP_ALIGN.CENTER

    for i in range(rows - 1):
        row_data = [
            str(x_labels[i]),
            f"{rev[i]:,.0f}".replace(",", " "),
            f"{inflows[i]:,.0f}".replace(",", " "),
            f"{outflows[i]:,.0f}".replace(",", " "),
            f"{cash_balance[i]:,.0f}".replace(",", " ")
        ]
        for col_idx, val in enumerate(row_data):
            cell = table.cell(i+1, col_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = c_white if i % 2 == 0 else RGBColor(240, 235, 230)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(12)
                p.font.color.rgb = c_dark
                p.font.name = font_regular
                p.alignment = PP_ALIGN.CENTER if col_idx == 0 else PP_ALIGN.RIGHT

    ppt_io = io.BytesIO()
    prs.save(ppt_io)
    ppt_io.seek(0)
    return ppt_io

def send_report_to_email(to_email, pptx_bytes):
    """
    Реальная отправка письма с презентацией через SMTP-сервер.
    Настройки smtp (сервер, порт, логин, пароль) берутся из переменных окружения Streamlit Secrets.
    """
    # Читаем параметры из st.secrets или задаем дефолтные значения
    smtp_server = os.getenv("SMTP_SERVER", "smtp.yandex.ru")
    smtp_port = int(os.getenv("SMTP_PORT", 465))
    sender_email = os.getenv("SMTP_USER", "finance@kraivin.ru")
    sender_password = os.getenv("SMTP_PASSWORD", "ваш_пароль_приложения")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = "КРАЙВИН: Финансовый отчёт и модель денежных потоков"

    body = "Здравствуйте!\n\nВо вложении находится актуальный финансовый отчет КРАЙВИН в формате PowerPoint.\n\nС уважением,\nФинансовый департамент КРАЙВИН"
    msg.attach(MIMEText(body, 'plain'))

    # Прикрепляем файл презентации
    attachment = MIMEBase('application', 'vnd.openxmlformats-officedocument.presentationml.presentation')
    attachment.set_payload(pptx_bytes.getvalue())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename="Kraivin_Investment_Report.pptx")
    msg.attach(attachment)

    try:
        # Подключение к SMTP-серверу по SSL
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"SMTP Error: {e}")
        return False

def send_report_to_max(chat_id, pptx_bytes):
    # Заглушка под корпоративный мессенджер
    return True
