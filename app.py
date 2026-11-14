import base64
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

BLUEPRINT_FILES = [
    "1793030578548.jpg",
    "1793030581888.jpg",
    "1793030587821.jpg",
    "1793030589564.jpg",
    "1793030590445.jpg",
]


def encode_image_to_data_uri(filename: str) -> str:
    filepath = os.path.join(BASE_DIR, filename)
    if not os.path.exists(filepath):
        return ""
    ext = os.path.splitext(filepath)[1].lower().lstrip(".")
    mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
    with open(filepath, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def build_dashboard_html() -> str:
    index_path = os.path.join(BASE_DIR, "index.html")
    if not os.path.exists(index_path):
        st.error("Файл index.html не найден в корне репозитория.")
        st.stop()

    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    discovery_images = [
        uri for name in BLUEPRINT_FILES if (uri := encode_image_to_data_uri(name))
    ]
    html_content = html_content.replace("__JSON_IMAGES_PAYLOAD__", json.dumps(discovery_images))

    return html_content


html_output = build_dashboard_html()
components.html(html_output, height=1080, scrolling=True)
