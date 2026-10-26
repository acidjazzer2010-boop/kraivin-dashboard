"""app.py: Точка входа приложения Streamlit с кэшированием и API-рендером."""

import io
import json
import logging
import os
from PIL import Image, ImageFilter
import pandas as pd
import streamlit as st

from engine import ModelParams, calculate_financial_model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FinModel")

st.set_page_config(
    page_title="Архитектура Капитала // Финансовое Моделирование",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Очистка дефолтного Streamlit UI
st.markdown(
    """
<style>
#MainMenu, header, footer, .stDeployButton { visibility: hidden !important; display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section.main { background-color: #050508 !important; }
iframe { border: none !important; }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def generate_and_cache_blueprint(
    input_path: str,
    output_path: str,
    threshold: int = 22,
    gain: float = 4.6,
    blur_radius: float = 0.3,
) -> bool:
    """Генерирует контур и сохраняет чистый PNG в static/ без Base64."""
    if not os.path.exists(input_path):
        logger.warning(
            f"Файл чертежа {input_path} не найден. Пропуск генерации."
        )
        return False
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img = Image.open(input_path).convert("L")
        smoothed = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        edges = smoothed.filter(ImageFilter.FIND_EDGES)

        def isolate_lines(p):
            return 0 if p < threshold else int(min(255, (p - threshold) * gain))

        alpha = edges.point(isolate_lines)
        gold = Image.new("RGBA", img.size, (229, 193, 88, 255))
        gold.putalpha(alpha)
        gold.save(output_path, format="PNG", optimize=True)
        logger.info(f"Контур успешно сгенерирован и сохранен в {output_path}")
        return True
    except Exception as e:
        logger.error(f"Ошибка обработки изображения: {e}")
        return False


# Инициализация сессии и параметров
if "params" not in st.session_state:
    st.session_state.params = ModelParams()

# Кэширование чертежа
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
BLUEPRINT_SRC = "1000400438.jpg"
BLUEPRINT_DST = os.path.join(STATIC_DIR, "blueprint_silhouette.png")
blueprint_ready = generate_and_cache_blueprint(BLUEPRINT_SRC, BLUEPRINT_DST)

# Расчет модели на сервере Python
calc_data = calculate_financial_model(st.session_state.params)
json_payload = json.dumps(calc_data, ensure_ascii=False)

# Сборка чистого HTML (шаблонизация)
TEMPLATE_PATH = os.path.join(
    os.path.dirname(__file__), "templates", "index.html"
)
CSS_PATH = os.path.join(STATIC_DIR, "styles.css")
JS_PATH = os.path.join(STATIC_DIR, "dashboard.js")

with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
    html_template = f.read()

with open(CSS_PATH, "r", encoding="utf-8") as f:
    inline_css = f.read()

with open(JS_PATH, "r", encoding="utf-8") as f:
    inline_js = f.read()

# Инъекция данных и минифицированных стилей
rendered_html = (
    html_template.replace("/* __INLINE_CSS__ */", inline_css)
    .replace("/* __INLINE_JS__ */", inline_js)
    .replace("__FIN_DATA_JSON__", json_payload)
)

# Рендер через современный изолированный iframe с фиксированной высотой
st.components.v1.html(rendered_html, height=1350, scrolling=True)
