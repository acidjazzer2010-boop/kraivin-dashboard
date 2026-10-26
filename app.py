"""Архитектура Капитала // Финансовое Моделирование — Streamlit runner."""
import os
import json
import base64
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Архитектура Капитала // Финансовое Моделирование",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def get_image_b64(filename):
    candidates = [
        filename,
        os.path.join(".", filename),
        os.path.join(os.path.dirname(__file__), filename) if "__file__" in locals() else filename
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    ext = path.split('.')[-1].lower()
                    mime = "image/jpeg" if ext in ["jpg", "jpeg"] else f"image/{ext}"
                    clean_b64 = base64.b64encode(f.read()).decode('utf-8').replace("\n", "").replace("\r", "")
                    return f"data:{mime};base64,{clean_b64}"
            except Exception:
                pass
    return ""

# Изображения изобретений Да Винчи (5 чертежей)
img_files = [
    "1793030578548.jpg",
    "1793030581888.jpg",
    "1793030587821.jpg",
    "1793030589564.jpg",
    "1793030590445.jpg"
]
b64_images = [get_image_b64(f) for f in img_files]
json_images_payload = json.dumps(b64_images)

# Фото Спутника-1 (СССР) для трехмерной пасхалки
sputnik_b64 = get_image_b64("1793046110105.jpg")
json_sputnik_payload = json.dumps(sputnik_b64)

st.markdown("""
<style>
#MainMenu,footer,header[data-testid="stHeader"],[data-testid="stDeployButton"]{visibility:hidden!important;display:none!important}
.block-container,[data-testid="stAppViewBlockContainer"]{padding:0!important;max-width:100%!important;margin:0!important}
section.main,[data-testid="stAppViewContainer"]>.main{background:#070709!important;padding:0!important}
iframe[title="streamlit_component"]{
    border:none!important;
    width:100vw!important;
    height:100vh!important;
    display:block!important;
}
</style>
""", unsafe_allow_html=True)

html_path = os.path.join(os.path.dirname(__file__), "index.html") if "__file__" in locals() else "index.html"
with open(html_path, "r", encoding="utf-8") as f:
    raw_html = f.read()

HTML = raw_html.replace("__JSON_IMAGES_PAYLOAD__", json_images_payload).replace("__SPUTNIK_IMAGE_PAYLOAD__", json_sputnik_payload)
components.html(HTML, height=940, scrolling=False)
