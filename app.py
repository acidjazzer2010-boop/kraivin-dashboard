import streamlit as st
import streamlit.components.v1 as components
import base64
import os
import io
import math
from PIL import Image, ImageFilter, ImageDraw

st.set_page_config(
    page_title="Архитектура Капитала // Песочница",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
#MainMenu, header, footer, .stDeployButton { visibility: hidden !important; display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section.main { background-color: #050508 !important; }
iframe { border: none !important; width: 100% !important; }
</style>
""", unsafe_allow_html=True)

def generate_fallback_vitruvian():
    """Генерирует процедурный золотой силуэт Витрувианца, если нет локального JPG файла."""
    size = 1000
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    gold = (229, 193, 88, 240)
    
    # Описанный круг и квадрат золотого сечения
    center = size // 2
    r = int(size * 0.44)
    draw.ellipse([center - r, center - r, center + r, center + r], outline=gold, width=2)
    
    sq_size = int(size * 0.76)
    sq_top = int(size * 0.16)
    draw.rectangle([center - sq_size//2, sq_top, center + sq_size//2, sq_top + sq_size], outline=gold, width=2)
    
    # Стилизованный контур фигуры Да Винчи (тонкие линии пера)
    # Голова
    draw.ellipse([center - 24, int(size * 0.18), center + 24, int(size * 0.25)], outline=gold, width=2)
    # Торс
    draw.line([center, int(size * 0.25), center, int(size * 0.52)], fill=gold, width=2)
    # Плечи и руки (прямые)
    draw.line([center - int(size * 0.38), int(size * 0.30), center + int(size * 0.38), int(size * 0.30)], fill=gold, width=2)
    # Руки (поднятые)
    draw.line([center, int(size * 0.28), center - int(size * 0.36), int(size * 0.20)], fill=gold, width=2)
    draw.line([center, int(size * 0.28), center + int(size * 0.36), int(size * 0.20)], fill=gold, width=2)
    # Ноги (прямые)
    draw.line([center, int(size * 0.52), center - 70, int(size * 0.88)], fill=gold, width=2)
    draw.line([center, int(size * 0.52), center + 70, int(size * 0.88)], fill=gold, width=2)
    # Ноги (разведенные)
    draw.line([center, int(size * 0.52), center - 190, int(size * 0.84)], fill=gold, width=2)
    draw.line([center, int(size * 0.52), center + 190, int(size * 0.84)], fill=gold, width=2)
    
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode()}"

def get_pure_silhouette_contour(filename):
    if not os.path.exists(filename):
        return generate_fallback_vitruvian()
    try:
        img = Image.open(filename).convert("L")
        smoothed = img.filter(ImageFilter.GaussianBlur(radius=0.4))
        edges = smoothed.filter(ImageFilter.FIND_EDGES)
        
        def isolate_lines(p):
            return 0 if p < 22 else int(min(255, (p - 22) * 4.6))
            
        alpha_channel = edges.point(isolate_lines)
        gold_canvas = Image.new("RGBA", img.size, (229, 193, 88, 255))
        gold_canvas.putalpha(alpha_channel)
        
        buffered = io.BytesIO()
        gold_canvas.save(buffered, format="PNG")
        return f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode()}"
    except Exception:
        return generate_fallback_vitruvian()

# Загружаем / генерируем контур
vitruvian_data_uri = get_pure_silhouette_contour("1000400438.jpg")

html_code = f"""<!DOCTYPE html>
<html lang="ru" class="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Песочница: Архитектура Капитала</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;1,600;1,700&family=JetBrains+Mono:wght@300;400;500;700&display=swap" rel="stylesheet">

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>
:root {{
    --bg-space: #050508;
    --bg-panel: rgba(11, 11, 16, 0.85);
    --text-main: #f4f1ea;
    --text-muted: #8e8a80;
    --border-line: rgba(212, 175, 55, 0.16);
    --accent-gold: #d4af37;
    --accent-vermilion: #e63946;
    --accent-jade: #2a9d8f;
}}

* {{ box-sizing: border-box; margin: 0; padding: 0; border-color: var(--border-line); }}
body {{ 
    background-color: var(--bg-space); color: var(--text-main); 
    font-family: 'JetBrains Mono', monospace; overflow-x: hidden;
}}

.film-grain {{
    position: fixed; inset: 0; width: 100vw; height: 100vh;
    pointer-events: none; z-index: 999; opacity: 0.035;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
}}

/* ПРЕЛОАДЕР */
#preloader-stage {{
    position: fixed; inset: 0; background: #040407; z-index: 900;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
}}
#preloader-webgl {{ position: absolute; inset: 0; width: 100vw; height: 100vh; z-index: 10; }}

#preloaderTitle {{
    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    font-family: 'Cormorant Garamond', Georgia, serif; font-style: italic;
    font-size: clamp(32px, 5vw, 54px); font-weight: 700; letter-spacing: 0.22em;
    color: var(--accent-gold); opacity: 0; z-index: 30; pointer-events: none;
    text-shadow: 0 0 30px rgba(212, 175, 55, 0.6);
    transition: opacity 2s cubic-bezier(0.16, 1, 0.3, 1);
    text-align: center; width: 100%;
}}

#preloaderHUD {{
    position: absolute; bottom: 40px; display: flex; flex-direction: column;
    align-items: center; gap: 6px; z-index: 30; transition: opacity 0.5s ease;
}}
.progress-bar-bg {{ width: 280px; height: 2px; background: rgba(255,255,255,0.1); position: relative; overflow: hidden; }}
#loaderProgressBar {{ position: absolute; left: 0; top: 0; height: 100%; width: 0%; background: var(--accent-gold); transition: width 0.1s linear; }}

#exploreBtnWrapper {{
    position: absolute; bottom: 45px; z-index: 40; opacity: 0; pointer-events: none;
    transition: opacity 1s ease, transform 1s ease; transform: translateY(10px);
}}
#exploreBtnWrapper.active {{ opacity: 1; pointer-events: auto; transform: translateY(0); }}

.explore-btn {{
    padding: 14px 44px; background: rgba(13, 13, 18, 0.7);
    border: 1px solid var(--accent-gold); color: #f4f1ea;
    font-family: 'JetBrains Mono', monospace; font-size: 11px;
    letter-spacing: 0.35em; text-transform: uppercase; cursor: pointer;
    backdrop-filter: blur(12px); box-shadow: 0 0 30px rgba(212, 175, 55, 0.25);
    transition: all 0.3s ease;
}}
.explore-btn:hover {{ border-color: #ffd700; color: #ffd700; box-shadow: 0 0 45px rgba(212, 175, 55, 0.5); transform: scale(1.04); }}

/* ДАШБОРД */
#mainDashboardApp {{ opacity: 0; transition: opacity 1s ease; min-height: 100vh; display: flex; flex-direction: column; }}
.alche-block {{ position: relative; background: var(--bg-panel); backdrop-filter: blur(16px); border: 1px solid var(--border-line); }}
.mono-input {{ background: rgba(255,255,255,0.03); border: 1px solid var(--border-line); color: var(--text-main); font-family: inherit; font-size: 11px; padding: 6px 10px; width: 100%; outline: none; }}
</style>
</head>
<body>
<div class="film-grain"></div>

<!-- ПРЕЛОАДЕР -->
<div id="preloader-stage">
    <canvas id="preloader-webgl"></canvas>
    
    <div id="preloaderTitle">Архитектура финансов</div>

    <div id="preloaderHUD">
        <div style="font-size: 10px; color: var(--accent-gold); letter-spacing: 0.25em; text-transform: uppercase;">
            Трассировка пропорций <span id="loaderPercent">0%</span>
        </div>
        <div class="progress-bar-bg">
            <div id="loaderProgressBar"></div>
        </div>
    </div>

    <div id="exploreBtnWrapper">
        <button class="explore-btn" onclick="dismissPreloader()">Исследовать</button>
    </div>
</div>

<!-- ОСНОВНОЙ ДАШБОРД -->
<div id="mainDashboardApp">
    <header class="alche-block" style="padding: 16px 28px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-line);">
        <div style="display: flex; align-items: center; gap: 14px;">
            <span style="color: var(--accent-gold); font-size: 20px;">⚜️</span>
            <div>
                <div style="font-size: 9px; letter-spacing: 0.3em; color: var(--accent-gold);">AUREA PROPORTIO // 1 : 1.618</div>
                <div style="font-family: 'Cormorant Garamond', Georgia, serif; font-style: italic; font-size: 20px; font-weight: 700;">Архитектура Капитала и Ликвидности</div>
            </div>
        </div>
        <div style="display: flex; gap: 12px; align-items: center;">
            <button onclick="toggleAudio()" id="btnAudio" class="mono-input" style="cursor: pointer; width: auto;">ЗВУК: ВКЛ</button>
            <div style="font-size: 10px; opacity: 0.7;">[ПЕСОЧНИЦА АКТИВНА]</div>
        </div>
    </header>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1px; background: var(--border-line); margin: 24px;">
        <div class="alche-block" style="padding: 20px;">
            <div style="font-size: 9px; opacity: 0.6; letter-spacing: 0.2em;">[01] СОВОКУПНАЯ ВЫРУЧКА</div>
            <div style="font-family: 'Cormorant Garamond', serif; font-size: 28px; font-weight: 700; color: #f4f1ea; margin-top: 6px;">84 600 000 ₽</div>
            <div style="font-size: 9px; color: var(--accent-gold); margin-top: 4px;">Маржинальность: 20%</div>
        </div>
        <div class="alche-block" style="padding: 20px;">
            <div style="font-size: 9px; opacity: 0.6; letter-spacing: 0.2em;">[02] ДЕФИЦИТ (ИНЪЕКЦИИ)</div>
            <div style="font-family: 'Cormorant Garamond', serif; font-size: 28px; font-weight: 700; color: var(--accent-vermilion); margin-top: 6px;">18 420 000 ₽</div>
            <div style="font-size: 9px; color: var(--accent-vermilion); margin-top: 4px;">Пиковый дефицит капитала</div>
        </div>
        <div class="alche-block" style="padding: 20px;">
            <div style="font-size: 9px; opacity: 0.6; letter-spacing: 0.2em;">[03] ПРОЦЕНТЫ ПО ДОЛГУ</div>
            <div style="font-family: 'Cormorant Garamond', serif; font-size: 28px; font-weight: 700; color: var(--accent-gold); margin-top: 6px;">2 490 000 ₽</div>
            <div style="font-size: 9px; color: var(--accent-gold); margin-top: 4px;">Ставка 19.0% годовых</div>
        </div>
        <div class="alche-block" style="padding: 20px;">
            <div style="font-size: 9px; opacity: 0.6; letter-spacing: 0.2em;">[04] ЧИСТАЯ ПРИБЫЛЬ</div>
            <div style="font-family: 'Cormorant Garamond', serif; font-size: 28px; font-weight: 700; color: var(--accent-jade); margin-top: 6px;">6 840 000 ₽</div>
            <div style="font-size: 9px; color: var(--accent-jade); margin-top: 4px;">Рентабельность: 8.1%</div>
        </div>
    </div>

    <div style="margin: 0 24px 24px 24px; display: grid; grid-template-columns: 2fr 1fr; gap: 20px;">
        <div class="alche-block" style="padding: 20px;">
            <div style="font-size: 14px; font-style: italic; margin-bottom: 14px;">График обслуживания долга и динамика тела кредита</div>
            <div style="height: 320px;"><canvas id="chartDebt"></canvas></div>
        </div>
        <div class="alche-block" style="padding: 20px;">
            <div style="font-size: 14px; font-style: italic; margin-bottom: 14px;">Партионный складской цикл</div>
            <div style="height: 320px;"><canvas id="chartStock"></canvas></div>
        </div>
    </div>
</div>

<script>
/* АУДИО ОТКЛИК */
let audioCtx = null;
let soundMuted = false;
function playSound(freq = 1200, dur = 0.02) {{
    if (soundMuted) return;
    try {{
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        if (audioCtx.state === 'suspended') audioCtx.resume();
        const osc = audioCtx.createOscillator();
        const g = audioCtx.createGain();
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(300, audioCtx.currentTime + dur);
        g.gain.setValueAtTime(0.03, audioCtx.currentTime);
        g.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + dur);
        osc.connect(g); g.connect(audioCtx.destination);
        osc.start(); osc.stop(audioCtx.currentTime + dur);
    }} catch(e) {{}}
}}
function toggleAudio() {{
    soundMuted = !soundMuted;
    document.getElementById('btnAudio').textContent = soundMuted ? 'ЗВУК: ВЫКЛ' : 'ЗВУК: ВКЛ';
}}

/* ========================================================
   THREE.JS ПРЕЛОАДЕР: АСТРОЛЯБИЯ + ВИТРУВИАНЕЦ
   ======================================================== */
const preCanvas = document.getElementById('preloader-webgl');
const preRenderer = new THREE.WebGLRenderer({{ canvas: preCanvas, alpha: true, antialias: true }});
preRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
preRenderer.setSize(window.innerWidth, window.innerHeight);

const preScene = new THREE.Scene();
// Фиксированная камера: рисунок статичен и НЕ надвигается
const preCamera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 2000);
preCamera.position.set(0, 0, 160);
preCamera.lookAt(0, 0, 0);

const preGroup = new THREE.Group();
preScene.add(preGroup);

// Одноцветный чистый голубой каркасный материал колец (#00b4ff)
const ringMaterial = new THREE.MeshBasicMaterial({{
    color: 0x00b4ff,
    wireframe: true,
    transparent: true,
    opacity: 0.38
}});

// 3 гигантских кольца астролябии
const ring1 = new THREE.Mesh(new THREE.TorusGeometry(122, 4.0, 24, 220), ringMaterial);
const ring2 = new THREE.Mesh(new THREE.TorusGeometry(98, 3.6, 22, 190), ringMaterial);
const ring3 = new THREE.Mesh(new THREE.TorusGeometry(76, 3.2, 20, 160), ringMaterial);

ring2.rotation.x = Math.PI / 3;
ring3.rotation.y = Math.PI / 4;

preGroup.add(ring1);
preGroup.add(ring2);
preGroup.add(ring3);

// Загрузка текстуры силуэта (Data URI)
const vitruvianData = "{vitruvian_data_uri}";
let vitShaderMat = null;

const img = new Image();
img.crossOrigin = "Anonymous";
img.src = vitruvianData;
img.onload = () => {{
    const texture = new THREE.Texture(img);
    texture.needsUpdate = true;
    const aspect = img.width / img.height;

    // Шейдер: трассировка тонким золотым лучом снизу вверх
    vitShaderMat = new THREE.ShaderMaterial({{
        uniforms: {{
            tDiffuse: {{ value: texture }},
            uProgress: {{ value: 0.0 }},
            uTime: {{ value: 0.0 }}
        }},
        vertexShader: `
            varying vec2 vUv;
            void main() {{
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }}
        `,
        fragmentShader: `
            uniform sampler2D tDiffuse;
            uniform float uProgress;
            uniform float uTime;
            varying vec2 vUv;

            void main() {{
                vec4 tex = texture2D(tDiffuse, vUv);
                
                // Трассировка снизу вверх от ступней (0.0) к голове (1.0)
                float front = uProgress * 1.05;
                float reveal = smoothstep(front, front - 0.04, vUv.y);
                
                // Филигранный тонкий луч карандаша
                float leadEdge = smoothstep(front - 0.03, front, vUv.y) * smoothstep(front + 0.008, front, vUv.y);
                float strokeHatch = sin((vUv.x * 120.0) - (uTime * 14.0)) * 0.5 + 0.5;
                float strokeBeam = pow(strokeHatch, 3.2) * leadEdge * 4.2;
                
                float finalAlpha = clamp(reveal + strokeBeam, 0.0, 1.0);
                vec3 spark = vec3(1.0, 0.94, 0.65) * (strokeBeam * 2.0);
                
                gl_FragColor = vec4(tex.rgb + spark, tex.a * finalAlpha);
            }}
        `,
        transparent: true,
        depthWrite: false,
        side: THREE.DoubleSide
    }});

    const h = 94;
    const w = h * aspect;
    const vitMesh = new THREE.Mesh(new THREE.PlaneGeometry(w, h), vitShaderMat);
    vitMesh.position.set(0, 0, 0);
    preGroup.add(vitMesh);
}};

/* ТАЙМИНГ И ХОД ПРЕЛОАДЕРА */
const PRELOADER_TIME = 7500;
const startTime = performance.now();
let dismissed = false;

setTimeout(() => {{
    const title = document.getElementById('preloaderTitle');
    if (title) title.style.opacity = '0.95';
}}, 1200);

function animatePreloader(now) {{
    if (dismissed) return;
    requestAnimationFrame(animatePreloader);
    
    const elapsed = now - startTime;
    const t = elapsed * 0.001;
    const progress = Math.min(elapsed / PRELOADER_TIME, 1.0);
    
    // Медленное вращение колец астролябии по X, Y, Z
    ring1.rotation.x += 0.0022 + Math.sin(t * 0.4) * 0.0008;
    ring1.rotation.y += 0.0031 + Math.cos(t * 0.35) * 0.0009;
    ring1.rotation.z += 0.0012;
    
    ring2.rotation.x -= 0.0025;
    ring2.rotation.y += 0.0018 + Math.cos(t * 0.3) * 0.0008;
    ring2.rotation.z -= 0.0020;
    
    ring3.rotation.x += 0.0028;
    ring3.rotation.y -= 0.0024;
    ring3.rotation.z += 0.0016;

    if (vitShaderMat) {{
        vitShaderMat.uniforms.uProgress.value = progress;
        vitShaderMat.uniforms.uTime.value = t;
    }}

    const bar = document.getElementById('loaderProgressBar');
    const pct = document.getElementById('loaderPercent');
    if (bar) bar.style.width = (progress * 100).toFixed(0) + '%';
    if (pct) pct.textContent = Math.floor(progress * 100) + '%';

    if (progress >= 0.96) {{
        const btn = document.getElementById('exploreBtnWrapper');
        const hud = document.getElementById('preloaderHUD');
        if (hud) hud.style.opacity = '0';
        if (btn) btn.classList.add('active');
    }}

    preRenderer.render(preScene, preCamera);
}}
requestAnimationFrame(animatePreloader);

function dismissPreloader() {{
    if (dismissed) return;
    dismissed = true;
    playSound(900, 0.04);
    const stage = document.getElementById('preloader-stage');
    const app = document.getElementById('mainDashboardApp');
    if (app) app.style.opacity = '1';
    if (stage) {{
        stage.style.transition = 'opacity 0.7s ease';
        stage.style.opacity = '0';
        setTimeout(() => stage.style.display = 'none', 700);
    }}
    initCharts();
}}

/* ГРАФИКИ DASHBOARD */
function initCharts() {{
    const labels = ['Окт 2026', 'Ноя 2026', 'Дек 2026', 'Янв 2027', 'Фев 2027', 'Мар 2027', 'Апр 2027', 'Май 2027', 'Июн 2027', 'Июл 2027', 'Авг 2027', 'Сен 2027'];
    
    new Chart(document.getElementById('chartDebt').getContext('2d'), {{
        type: 'bar',
        data: {{
            labels: labels,
            datasets: [
                {{ label: 'Проценты к уплате, ₽', data: [0, 230000, 310000, 340000, 320000, 290000, 250000, 210000, 180000, 150000, 110000, 100000], backgroundColor: '#d4af37', order: 2 }},
                {{ label: 'Остаток долга, ₽', data: [15000000, 18420000, 17200000, 15900000, 14200000, 12100000, 9800000, 7200000, 4800000, 2500000, 800000, 0], type: 'line', borderColor: '#e63946', borderWidth: 2, tension: 0.3, order: 1 }}
            ]
        }},
        options: {{
            responsive: true, maintainAspectRatio: false,
            plugins: {{ legend: {{ labels: {{ color: '#8e8a80', font: {{ family: 'JetBrains Mono', size: 10 }} }} }} }},
            scales: {{
                x: {{ grid: {{ display: false }}, ticks: {{ color: '#8e8a80', font: {{ family: 'JetBrains Mono', size: 9 }} }} }},
                y: {{ grid: {{ color: 'rgba(212,175,55,0.08)' }}, ticks: {{ color: '#8e8a80', font: {{ family: 'JetBrains Mono', size: 9 }} }} }}
            }}
        }}
    }});

    new Chart(document.getElementById('chartStock').getContext('2d'), {{
        type: 'bar',
        data: {{
            labels: labels,
            datasets: [
                {{ label: 'Оплата партии, ₽', data: [12500000, 12500000, 0, 0, 0, 8200000, 8200000, 0, 0, 0, 9100000, 9100000], backgroundColor: '#52525b' }}
            ]
        }},
        options: {{
            responsive: true, maintainAspectRatio: false,
            plugins: {{ legend: {{ labels: {{ color: '#8e8a80', font: {{ family: 'JetBrains Mono', size: 10 }} }} }} }},
            scales: {{
                x: {{ grid: {{ display: false }}, ticks: {{ color: '#8e8a80', font: {{ family: 'JetBrains Mono', size: 9 }} }} }},
                y: {{ grid: {{ color: 'rgba(212,175,55,0.08)' }}, ticks: {{ color: '#8e8a80', font: {{ family: 'JetBrains Mono', size: 9 }} }} }}
            }}
        }}
    }});
}}

window.addEventListener('resize', () => {{
    preCamera.aspect = window.innerWidth / window.innerHeight;
    preCamera.updateProjectionMatrix();
    preRenderer.setSize(window.innerWidth, window.innerHeight);
}});
</script>
</body>
</html>"""

components.html(html_code, height=1280, scrolling=True)
