import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Архитектура Капитала // Rota Fortunae",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Убираем стандартные отступы и шапку Streamlit, чтобы 3D-дашборд занял 100% экрана
st.markdown("""
    <style>
        #MainMenu, header, footer {visibility: hidden;}
        .block-container {padding: 0 !important; max-width: 100% !important;}
        iframe {display: block; border: none;}
    </style>
""", unsafe_allow_html=True)

html_code = r"""<!DOCTYPE html>
<html lang="ru" class="dark">
<head>
...
<!-- ВЕСЬ ВАШ HTML-КОД БЕЗ ИЗМЕНЕНИЙ -->
...
</html>"""

components.html(html_code, height=950, scrolling=True)
