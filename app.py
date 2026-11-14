import base64
import glob
import json
import os
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Архитектура Капитала // Rota Fortunae",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Скрываем стандартный интерфейс Streamlit для полноэкранного режима
st.markdown(
    """
    <style>
        #MainMenu, header, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {
            display: none !important;
        }
        .stApp {
            background-color: #070709 !important;
        }
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        iframe {
            display: block !important;
            width: 100vw !important;
            height: 100vh !important;
            border: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def encode_image_to_data_uri(filepath: str) -> str:
    """Кодирует локальное изображение в Base64 Data URI для работы внутри iframe."""
    ext = os.path.splitext(filepath)[1].lower().lstrip(".")
    mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
    with open(filepath, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def load_discovery_images(folder_name: str = "images") -> list[str]:
    """Собирает до 5 изображений чертежей из папки images/ для 3D-карточек прелоадера."""
    folder_path = os.path.join(BASE_DIR, folder_name)
    if not os.path.isdir(folder_path):
        return []
    files = []
    for pattern in ("*.png", "*.jpg", "*.jpeg", "*.webp"):
        files.extend(glob.glob(os.path.join(folder_path, pattern)))
    return [encode_image_to_data_uri(p) for p in sorted(files)[:5]]


def build_dashboard_html() -> str:
    """Читает index.html и внедряет Base64-ресурсы."""
    index_path = os.path.join(BASE_DIR, "index.html")
    if not os.path.exists(index_path):
        st.error("Файл index.html не найден в корне репозитория.")
        st.stop()

    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # 1. Подстановка текстуры спутника 1793046110105.jpg
    sputnik_path = os.path.join(BASE_DIR, "1793046110105.jpg")
    if os.path.exists(sputnik_path):
        sputnik_src = encode_image_to_data_uri(sputnik_path)
    else:
        sputnik_src = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"

    html_content = html_content.replace("__SPUTNIK_TEXTURE_SRC__", sputnik_src)
    html_content = html_content.replace("1793046110105.jpg", sputnik_src)

    # 2. Подстановка массива изображений чертежей Да Винчи
    discovery_images = load_discovery_images("images")
    images_json = json.dumps(discovery_images)

    if "typeof __JSON_IMAGES_PAYLOAD__" in html_content:
        html_content = html_content.replace(
            "typeof __JSON_IMAGES_PAYLOAD__ !== 'undefined' ? __JSON_IMAGES_PAYLOAD__ : []",
            images_json,
        )
    else:
        html_content = html_content.replace("__JSON_IMAGES_PAYLOAD__", images_json)

    return html_content


html_output = build_dashboard_html()
components.html(html_output, height=1080, scrolling=True)
