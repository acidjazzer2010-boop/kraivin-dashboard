import streamlit as st
import streamlit.components.v1 as components
import base64
import os
import io
from PIL import Image

st.set_page_config(
    page_title="Архитектура Капитала // Финансовое Моделирование",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
#MainMenu, header, footer, .stDeployButton {
    visibility: hidden !important;
    display: none !important;
}
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
section.main {
    background-color: #070709 !important;
}
iframe {
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

# Функция: извлечение контуров с Anti-Aliasing и перекраска в золото
def get_blueprint_vitruvian(filename):
    if not os.path.exists(filename):
        return ""
    
    try:
        # Конвертируем в градации серого
        img = Image.open(filename).convert("L")
        
        # Создаем умную маску прозрачности (сохраняет полутона для гладкости линий)
        # 160 - порог: все что темнее становится линией (alpha > 0), что светлее (пергамент) -> прозрачно
        def get_alpha(p):
            return max(0, min(255, int((160 - p) * 3.0)))
            
        alpha = img.point(get_alpha)
        
        # Создаем желтый холст (Золотой: #FFD700)
        color_layer = Image.new("RGBA", img.size, (255, 215, 0, 255))
        
        # Накладываем маску 
        color_layer.putalpha(alpha)
        
        buffered = io.BytesIO()
        color_layer.save(buffered, format="PNG")
        b64_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{b64_str}"
    except Exception as e:
        print(f"Ошибка обработки изображения: {e}")
        return ""

html_code = r"""<!DOCTYPE html>
<html lang="ru" class="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Архитектура Капитала // Финансовое Моделирование</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600;1,700&family=JetBrains+Mono:ital,wght@0,300;0,400;0,500;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {
    darkMode: 'class',
    theme: {
        extend: {
            fontFamily: {
                serif: ['"Cormorant Garamond"', 'Georgia', 'serif'],
                mono: ['"JetBrains Mono"', 'monospace'],
                sans: ['"Inter"', 'system-ui', 'sans-serif'],
            },
            colors: {
                obsidian: '#070709',
                obsidianCard: '#0d0d12',
                alabaster: '#f4f1ea',
                alabasterCard: '#ffffff',
                gold: '#d4af37',
            }
        }
    }
}
</script>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>
:root {
    --bg-space: #070709;
    --bg-panel: rgba(13, 13, 18, 0.85);
    --bg-cell-hover: rgba(24, 24, 34, 0.95);
    --text-main: #f4f1ea;
    --border-line: rgba(212, 175, 55, 0.16);
    --accent-gold: #d4af37;
    --input-bg: rgba(255, 255, 255, 0.025);
    --cursor-glow: rgba(212, 175, 55, 0.18);
    --table-header-bg: rgba(13, 13, 18, 0.98);
}
html:not(.dark) {
    --bg-space: #f4f1ea;
    --bg-panel: rgba(255, 255, 255, 0.92);
    --bg-cell-hover: rgba(246, 243, 235, 0.98);
    --text-main: #141416;
    --border-line: rgba(184, 134, 11, 0.22);
    --accent-gold: #b8860b;
    --input-bg: rgba(0, 0, 0, 0.03);
    --cursor-glow: rgba(184, 134, 11, 0.15);
    --table-header-bg: rgba(244, 241, 234, 0.98);
}

* { box-sizing: border-box; border-color: var(--border-line); }
body { background-color: var(--bg-space); color: var(--text-main); font-family: 'JetBrains Mono', monospace; overflow-x: hidden; margin: 0; padding: 0; }

.film-grain {
    position: fixed; inset: 0; width: 100vw; height: 100vh;
    pointer-events: none; z-index: 999; opacity: 0.035;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
}

/* ЗАСТАВКА */
#preloader-stage {
    position: fixed; inset: 0; background: #060608; z-index: 900;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    transition: opacity 1.1s cubic-bezier(0.19, 1, 0.22, 1), transform 1.1s cubic-bezier(0.19, 1, 0.22, 1);
}
#preloader-stage.fade-out { opacity: 0; transform: scale(1.035); pointer-events: none; }
#preloader-canvas-container { position: absolute; inset: 0; width: 100vw; height: 100vh; display: flex; align-items: center; justify-content: center; z-index: 10; }

/* Динамически управляемое перо (JS берет контроль над позицией) */
#quillPen {
    position: absolute; left: 0; top: 0; 
    margin-left: -4px; margin-top: -4px; /* выравнивание острия кончика */
    pointer-events: none; z-index: 25;
    opacity: 0; /* Изначально скрыто */
    filter: drop-shadow(0 0 10px rgba(255, 215, 0, 0.8));
    will-change: transform, opacity;
}
.nib-spark { animation: sparkFlicker 0.15s infinite alternate; }
@keyframes sparkFlicker { 0% { opacity: 0.5; transform: scale(0.8); } 100% { opacity: 1; transform: scale(1.4); } }

/* ФОН ОСНОВНОГО ПРИЛОЖЕНИЯ */
#webgl-bg-canvas { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 0; pointer-events: none; opacity: 0.45; }

.alche-block {
    position: relative; background: var(--bg-panel); backdrop-filter: blur(16px);
    border-right: 1px solid var(--border-line); border-bottom: 1px solid var(--border-line);
}
.tilt-card { position: relative; overflow: hidden; transform-style: preserve-3d; perspective: 900px; }
.tilt-card::before {
    content: ''; position: absolute; inset: 0; border: 1px solid transparent;
    background: radial-gradient(350px circle at var(--mouse-x, 0px) var(--mouse-y, 0px), var(--cursor-glow), transparent 70%);
    opacity: 0; pointer-events: none; z-index: 2;
}
.tilt-card:hover::before { opacity: 1; }

.tab-view-enter { animation: alcheTabEntrance 0.72s cubic-bezier(0.19, 1, 0.22, 1) forwards; }
@keyframes alcheTabEntrance {
    0% { opacity: 0; filter: blur(14px); transform: translateY(12px) scale(0.992); clip-path: inset(0 0 100% 0); }
    45% { opacity: 0.85; clip-path: inset(0 0 0% 0); }
    100% { opacity: 1; filter: blur(0px); transform: translateY(0) scale(1); clip-path: inset(0 0 0% 0); }
}

input[type="range"] { -webkit-appearance: none; appearance: none; width: 100%; height: 2px; background: var(--border-line); outline: none; }
input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none; appearance: none; width: 12px; height: 12px;
    background: var(--accent-gold); cursor: pointer; border: 1px solid var(--bg-space); transform: rotate(45deg);
}
.mono-input {
    background: var(--input-bg); border: 1px solid var(--border-line);
    color: var(--text-main); font-family: 'JetBrains Mono', monospace; font-size: 12px;
    padding: 7px 10px; width: 100%; border-radius: 0;
}
.mono-input:focus { outline: none; border-color: var(--accent-gold); background: rgba(212, 175, 55, 0.06); }
select.mono-input option { background-color: #0d0d12; color: #f4f1ea; }

.hw-slider-track {
    position: relative; width: 140px; height: 30px; border: 1px solid var(--border-line); background: var(--input-bg);
    display: flex; align-items: center; justify-content: space-between; padding: 0 10px; cursor: pointer; user-select: none;
}
.hw-slider-thumb {
    position: absolute; top: 2px; bottom: 2px; width: 66px; background: var(--accent-gold);
    transition: transform 0.45s cubic-bezier(0.19, 1, 0.22, 1), background-color 0.3s ease;
}
.pulse-dot { display: inline-block; width: 6px; height: 6px; border-radius: 9999px; background-color: var(--accent-gold); animation: pulseAnim 2s infinite ease-in-out; }
@keyframes pulseAnim { 0%, 100% { opacity: 0.4; transform: scale(0.9); } 50% { opacity: 1; transform: scale(1.2); } }
::-webkit-scrollbar { width: 4px; height: 4px; } ::-webkit-scrollbar-thumb { background: var(--border-line); }
</style>
</head>
<body class="selection:bg-[#d4af37] selection:text-black">
<div class="film-grain"></div>

<!-- ПРЕЛОАДЕР: ОГРОМНЫЕ КОЛЬЦА И ШЕЙДЕР ВИТРУВИАНЦА -->
<div id="preloader-stage">
    <div id="preloader-canvas-container">
        <canvas id="preloader-webgl"></canvas>
        <!-- ПЕРО (УПРАВЛЯЕТСЯ ИЗ JS) -->
        <div id="quillPen">
            <svg width="48" height="48" viewBox="0 0 64 64" fill="none">
                <circle cx="4" cy="4" r="3.5" fill="#ffffff" class="nib-spark" />
                <circle cx="4" cy="4" r="8" fill="#ffd700" opacity="0.4" class="nib-spark" />
                <path d="M4 4 L14 12 L10 16 Z" fill="#ffd700" />
                <path d="M4 4 L12 14 L16 10 Z" fill="#cca300" />
                <line x1="4" y1="4" x2="12" y2="12" stroke="#111" stroke-width="0.8"/>
                <circle cx="12" cy="12" r="1.5" fill="#111"/>
                <path d="M12 14 L14 12 L50 48 L48 50 Z" fill="url(#penGrad)" stroke="#222" stroke-width="1"/>
                <path d="M50 48 L14 12" stroke="#ffffff" stroke-width="1.5" opacity="0.3"/>
                <path d="M18 22 L22 18" stroke="#ffd700" stroke-width="2"/>
                <path d="M42 46 L46 42" stroke="#ffd700" stroke-width="2"/>
                <defs>
                    <linearGradient id="penGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#2a2a2a" /><stop offset="50%" stop-color="#0a0a0a" /><stop offset="100%" stop-color="#000000" />
                    </linearGradient>
                </defs>
            </svg>
        </div>
    </div>

    <!-- Индикатор загрузки -->
    <div class="absolute bottom-10 flex flex-col items-center gap-2 font-mono z-20 pointer-events-auto">
        <div class="flex items-center gap-3 text-[#d4af37] text-[11px] tracking-[0.25em] uppercase">
            <span class="pulse-dot"></span>
            <span id="loaderStatusText">Синтез структуры чертежа...</span>
            <span id="loaderPercent" class="font-bold">0%</span>
        </div>
        <div class="w-64 sm:w-80 h-[2px] bg-white/10 relative overflow-hidden mt-1">
            <div id="loaderProgressBar" class="absolute top-0 bottom-0 left-0 bg-[#d4af37] w-0 transition-all duration-100 ease-out"></div>
        </div>
    </div>
</div>

<canvas id="webgl-bg-canvas"></canvas>

<!-- Основной Дашборд -->
<div id="mainDashboardApp" class="relative z-10 min-h-screen flex flex-col border-t border-l opacity-0 transition-opacity duration-1000" style="border-color: var(--border-line);">
    <header class="alche-block px-5 lg:px-8 py-3 flex flex-wrap items-center justify-between gap-4">
        <div class="flex items-center gap-6">
            <div class="flex items-center gap-3">
                <svg class="w-7 h-7 text-[#d4af37] cursor-pointer" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.2">
                    <circle cx="16" cy="16" r="14" /><rect x="6" y="6" width="20" height="20" />
                    <polygon points="16,2 30,26 2,26" stroke-width="0.8" stroke-dasharray="1 1"/>
                </svg>
                <div>
                    <div class="font-mono text-[9px] uppercase tracking-[0.25em] text-[#d4af37] opacity-80">AUREA PROPORTIO // 1 : 1.618</div>
                    <div class="font-serif italic text-lg lg:text-xl font-bold tracking-wide leading-none">Архитектура Капитала и Ликвидности</div>
                </div>
            </div>
        </div>
        <div class="flex items-center gap-4">
            <button onclick="exportDataToCsv()" class="px-3.5 py-1.5 border font-mono text-[10px] uppercase tracking-widest hover:bg-[#d4af37]/10 transition flex items-center gap-2"><span>↓ Скачать отчет</span></button>
            <div id="themeSlider" class="hw-slider-track" onclick="toggleTheme()" title="Переключить режим: Ночь / День">
                <div id="sliderThumb" class="hw-slider-thumb" style="transform: translateX(0px);"></div>
                <span id="lblNight" class="relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold text-black">Ночь</span>
                <span id="lblDay" class="relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold opacity-70">День</span>
            </div>
        </div>
    </header>

    <div class="flex-1 grid grid-cols-1 lg:grid-cols-12">
        <!-- ЛЕВАЯ ПАНЕЛЬ ПАРАМЕТРОВ -->
        <aside class="lg:col-span-3 flex flex-col">
            <div class="alche-block px-5 py-3.5 flex items-center justify-between">
                <span class="font-mono text-[10px] uppercase tracking-[0.2em] text-[#d4af37] font-bold">[00] Параметры Модели</span>
                <button onclick="resetDefaults()" class="font-mono text-[9px] uppercase underline opacity-60 hover:opacity-100 transition">Сброс</button>
            </div>
            <form id="financialInputsForm" class="flex-1 flex flex-col" onsubmit="event.preventDefault();">
                <div class="alche-block p-5 space-y-4">
                    <div class="flex justify-between items-baseline">
                        <span class="font-serif italic text-base font-semibold">I. Временной горизонт и маржа</span>
                    </div>
                    <div class="grid grid-cols-2 gap-2.5">
                        <div>
                            <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Месяц старта</label>
                            <select id="paramStartMonth" class="mono-input" onchange="runCalculation();"><option value="9" selected>Октябрь</option></select>
                        </div>
                        <div>
                            <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Год старта</label>
                            <select id="paramStartYear" class="mono-input" onchange="runCalculation();"><option value="2026" selected>2026</option></select>
                        </div>
                    </div>
                    <div class="grid grid-cols-2 gap-2.5">
                        <div>
                            <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Горизонт</label>
                            <select id="paramPeriod" class="mono-input" onchange="runCalculation();"><option value="12" selected>12 месяцев</option></select>
                        </div>
                        <div>
                            <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Ставка НДС</label>
                            <select id="paramVatRate" class="mono-input" onchange="runCalculation();"><option value="22" selected>22%</option></select>
                        </div>
                    </div>
                    <div>
                        <div class="flex justify-between font-mono text-[10px] mb-1">
                            <span class="opacity-70">МАРЖИНАЛЬНОСТЬ ПРОДАЖ</span><span id="lblMarginVal" class="text-[#d4af37] font-bold">20%</span>
                        </div>
                        <input type="range" id="paramMargin" min="10" max="50" step="1" value="20" oninput="runCalculation()">
                    </div>
                </div>
                <div class="alche-block p-5 space-y-4 flex-1">
                    <div class="flex justify-between items-baseline"><span class="font-serif italic text-base font-semibold">II. Партионный склад и капитал</span></div>
                    <div>
                        <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Стартовая закупка партии, ₽</label>
                        <input type="text" id="paramInitialPurchase" value="25 000 000" class="mono-input font-bold" oninput="formatInput(this); runCalculation();">
                    </div>
                    <div class="grid grid-cols-3 gap-2">
                        <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Цикл, мес.</label><input type="number" id="paramBatchCycle" value="5" min="1" class="mono-input text-center" oninput="runCalculation()"></div>
                        <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">ЦБ РФ, %</label><input type="number" id="paramCbRate" value="17.0" step="0.5" class="mono-input text-center" oninput="runCalculation()"></div>
                        <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Маржа, %</label><input type="number" id="paramCommMargin" value="2.0" step="0.5" class="mono-input text-center" oninput="runCalculation()"></div>
                    </div>
                </div>
                <!-- Остальные блоки параметров скрыты для краткости (они управляются скриптом как и раньше) -->
                <input type="hidden" id="paramAov" value="150000">
                <input type="hidden" id="paramStartOrders" value="40">
                <input type="hidden" id="paramGrowthSlider" value="5">
                <input type="hidden" id="paramMaxOrdersCap" value="300">
                <input type="hidden" id="paramFot" value="500000">
                <input type="hidden" id="paramWh" value="200000">
                <input type="hidden" id="paramOffice" value="150000">
                <input type="hidden" id="paramPrepaymentPct" value="50">
                <input type="hidden" id="paramFactoringShare" value="50">
            </form>
        </aside>

        <!-- ПРАВАЯ ЧАСТЬ: ДАШБОРД -->
        <section class="lg:col-span-9 flex flex-col">
            <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 border-b" style="border-color: var(--border-line);">
                <div class="alche-block tilt-card p-5">
                    <div class="flex justify-between items-center opacity-60 mb-1"><span class="font-mono text-[9px] uppercase tracking-widest">[01] Выручка</span></div>
                    <div id="kpiRev" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#f4f1ea]">0 ₽</div>
                </div>
                <div class="alche-block tilt-card p-5">
                    <div class="flex justify-between items-center opacity-60 mb-1"><span class="font-mono text-[9px] uppercase tracking-widest">[02] Дефицит</span></div>
                    <div id="kpiInjections" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#e63946]">0 ₽</div>
                </div>
                <div class="alche-block tilt-card p-5">
                    <div class="flex justify-between items-center opacity-60 mb-1"><span class="font-mono text-[9px] uppercase tracking-widest">[03] Проценты</span></div>
                    <div id="kpiInterest" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#d4af37]">0 ₽</div>
                </div>
                <div class="alche-block tilt-card p-5">
                    <div class="flex justify-between items-center opacity-60 mb-1"><span class="font-mono text-[9px] uppercase tracking-widest">[04] Долг</span></div>
                    <div id="kpiMaxDebt" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#f4f1ea]">0 ₽</div>
                </div>
                <div class="alche-block tilt-card p-5 col-span-2 sm:col-span-1">
                    <div class="flex justify-between items-center opacity-60 mb-1"><span class="font-mono text-[9px] uppercase tracking-widest">[05] Прибыль</span></div>
                    <div id="kpiProfit" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#2a9d8f]">0 ₽</div>
                </div>
            </div>

            <div class="alche-block px-5 py-2.5 flex items-center justify-between border-b" style="border-color: var(--border-line);">
                <div class="flex flex-wrap items-center gap-1.5" id="navTabsContainer">
                    <button class="tab-btn px-4 py-1.5 font-mono text-[10px] uppercase tracking-widest bg-[#d4af37] text-black font-bold transition shadow-md">[01] ОБСЛУЖИВАНИЕ КАПИТАЛА</button>
                </div>
            </div>

            <div class="flex-1 p-5 lg:p-7 space-y-6">
                <div class="alche-block p-5 border">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="font-serif text-xl font-bold tracking-wide italic">График обслуживания долга и начисления процентов</h3>
                    </div>
                    <div class="h-[360px] relative"><canvas id="chartDebt"></canvas></div>
                </div>
            </div>
        </section>
    </div>
</div>

<script>
let preloaderDismissed = false;
function dismissPreloader() {
    if (preloaderDismissed) return;
    preloaderDismissed = true;
    const stage = document.getElementById('preloader-stage');
    const app = document.getElementById('mainDashboardApp');
    if (stage) stage.classList.add('fade-out');
    if (app) { app.classList.remove('opacity-0'); app.classList.add('opacity-100'); }
    setTimeout(() => { if (stage) stage.style.display = 'none'; }, 1100);
}

const PRELOADER_TOTAL_TIME = 8000; // Немного увеличим для красивой прорисовки
const preloaderStartTime = performance.now();

function updatePreloaderProgress(now) {
    if (preloaderDismissed) return;
    const elapsed = now - preloaderStartTime;
    const progress = Math.min(elapsed / PRELOADER_TOTAL_TIME, 1);
    
    document.getElementById('loaderProgressBar').style.width = `${(progress * 100).toFixed(1)}%`;
    document.getElementById('loaderPercent').textContent = `${Math.floor(progress * 100)}%`;
    
    if (progress < 1) {
        requestAnimationFrame(updatePreloaderProgress);
    } else {
        dismissPreloader();
    }
}
requestAnimationFrame(updatePreloaderProgress);

/* ========================================================
   THREE.JS ПРЕЛОАДЕР: ГИГАНТСКИЕ КОЛЬЦА И ШЕЙДЕР ПЕРА
   ======================================================== */
const preCanvas = document.getElementById('preloader-webgl');
const preScene = new THREE.Scene();
const preCamera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 2000);
preCamera.position.z = 100; // Отдаляем камеру для огромных колец

const preRenderer = new THREE.WebGLRenderer({ canvas: preCanvas, alpha: true, antialias: true });
preRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

function resizePreloader() {
    preRenderer.setSize(window.innerWidth, window.innerHeight);
    preCamera.aspect = window.innerWidth / window.innerHeight;
    preCamera.updateProjectionMatrix();
}
resizePreloader();
window.addEventListener('resize', resizePreloader);

// ГРУППА ДЛЯ ВРАЩАЮЩИХСЯ КОЛЕЦ
const preArmillary = new THREE.Group();
preScene.add(preArmillary);

const preBlueMat = new THREE.MeshBasicMaterial({ color: 0x00aaff, wireframe: true, transparent: true, opacity: 0.35 });

// Создаем сложную структуру десятков тонких огромных колец
for (let i = 0; i < 25; i++) {
    let tube = 0.01 + Math.random() * 0.04;
    let radius = 28 + Math.random() * 40;
    
    // Чередуем кольца и икосаэдры для сложной сетки чертежа
    let geo = Math.random() > 0.8 ? new THREE.IcosahedronGeometry(radius, 1) : new THREE.TorusGeometry(radius, tube, 4, 120);
    let mesh = new THREE.Mesh(geo, preBlueMat);
    
    mesh.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, Math.random() * Math.PI);
    
    // Задаем каждому кольцу свою скорость вращения
    mesh.userData = {
        rx: (Math.random() - 0.5) * 0.005,
        ry: (Math.random() - 0.5) * 0.008,
        rz: (Math.random() - 0.5) * 0.005
    };
    preArmillary.add(mesh);
}

// ПЛОСКОСТЬ ВИТРУВИАНЦА И КАСТОМНЫЙ ШЕЙДЕР
const vitruvianImg = new Image();
vitruvianImg.src = "VITRUVIAN_IMAGE_SRC_PLACEHOLDER";
let planeMaterial = null;
let vitruvianPlane = null;

// Шейдер для эффекта "рисования пера": скрывает пиксели, до которых перо еще не дошло по кругу
const vertexShader = `
    varying vec2 vUv;
    void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }
`;
const fragmentShader = `
    uniform sampler2D tDiffuse;
    uniform float uDrawAngle;
    varying vec2 vUv;
    void main() {
        vec4 tex = texture2D(tDiffuse, vUv);
        // Вычисляем угол пикселя от центра
        float dx = vUv.x - 0.5;
        float dy = vUv.y - 0.5;
        float angle = atan(dx, dy); 
        if (angle < 0.0) angle += 6.28318530718; // Перевод в диапазон от 0 до 2*PI
        
        // Если пиксель находится "дальше" текущего угла пера - он прозрачный
        if (angle > uDrawAngle) {
            tex.a = 0.0;
        }
        gl_FragColor = tex;
    }
`;

vitruvianImg.onload = () => {
    const canvasTexture = new THREE.Texture(vitruvianImg);
    canvasTexture.needsUpdate = true;
    
    planeMaterial = new THREE.ShaderMaterial({
        uniforms: {
            tDiffuse: { value: canvasTexture },
            uDrawAngle: { value: 0.0 }
        },
        vertexShader: vertexShader,
        fragmentShader: fragmentShader,
        transparent: true,
        depthWrite: false,
        side: THREE.DoubleSide
    });
    
    const aspect = vitruvianImg.height / vitruvianImg.width;
    // Огромная плоскость для огромных колец
    const planeGeo = new THREE.PlaneGeometry(38.0, 38.0 * aspect);
    vitruvianPlane = new THREE.Mesh(planeGeo, planeMaterial);
    
    // Плоскость добавляется напрямую в сцену, чтобы она не вращалась вместе с кольцами, а смотрела прямо на камеру
    preScene.add(vitruvianPlane);
};

let drawProgress = 0;
const penEl = document.getElementById('quillPen');

function animatePreloader() {
    if (!preloaderDismissed) requestAnimationFrame(animatePreloader);
    
    // Вращение сложной структуры колец
    preArmillary.children.forEach(child => {
        child.rotation.x += child.userData.rx;
        child.rotation.y += child.userData.ry;
        child.rotation.z += child.userData.rz;
    });
    
    // ЛОГИКА РИСОВАНИЯ И СИНХРОНИЗАЦИИ ПЕРА С ШЕЙДЕРОМ
    if (vitruvianPlane && drawProgress < 7.0) {
        drawProgress += 0.018; // Скорость рисования
        
        // 1. Передаем угол в шейдер (рисунок проявляется)
        planeMaterial.uniforms.uDrawAngle.value = drawProgress;
        
        // 2. Вычисляем физическую 3D-позицию острия пера
        // R варьируется, чтобы перо как бы "выписывало" анатомию, а не просто шло по идеальному кругу
        const R = 15.0 + Math.sin(drawProgress * 8) * 4.0; 
        const pen3D = new THREE.Vector3(R * Math.sin(drawProgress), R * Math.cos(drawProgress), 0);
        
        // Проецируем 3D-точку в 2D-координаты экрана для позиционирования SVG пера
        pen3D.project(preCamera);
        const penX = (pen3D.x * 0.5 + 0.5) * window.innerWidth;
        const penY = -(pen3D.y * 0.5 - 0.5) * window.innerHeight;
        
        if (drawProgress > 0.1 && drawProgress <= 6.28) {
            penEl.style.opacity = 1;
            // Двигаем перо и немного вращаем его кисть для живости
            penEl.style.transform = `translate3d(${penX}px, ${penY}px, 0) rotate(${Math.sin(drawProgress * 15) * 15 - 15}deg)`;
        } else if (drawProgress > 6.28) {
            penEl.style.opacity = 0; // Скрываем перо после завершения круга
        }
    }
    
    preRenderer.render(preScene, preCamera);
}
animatePreloader();

/* ========================================================
   ОСНОВНОЙ ФОН: БЕСКОНЕЧНЫЙ ТУННЕЛЬ СЛОЖНЫХ КОЛЕЦ
   ======================================================== */
const canvas = document.getElementById('webgl-bg-canvas');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 2000);
camera.position.z = 10;

const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

const tunnelGroup = new THREE.Group();
scene.add(tunnelGroup);

const ringMat = new THREE.MeshBasicMaterial({ color: 0x00aaff, wireframe: true, transparent: true, opacity: 0.2 });
const tunnelRings = [];

// Создаем секции летящего туннеля (каждая секция - пучок колец)
for (let i = 0; i < 15; i++) {
    const group = new THREE.Group();
    const r1 = new THREE.Mesh(new THREE.TorusGeometry(35, 0.05, 12, 100), ringMat);
    const r2 = new THREE.Mesh(new THREE.TorusGeometry(42, 0.03, 10, 100), ringMat);
    const r3 = new THREE.Mesh(new THREE.IcosahedronGeometry(48, 1), ringMat);
    
    group.add(r1); group.add(r2); group.add(r3);
    group.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, 0);
    group.position.z = -i * 40;
    
    tunnelGroup.add(group);
    tunnelRings.push(group);
}

let mouseX = 0, mouseY = 0;
document.addEventListener('mousemove', (e) => {
    mouseX = (e.clientX - window.innerWidth / 2) * 0.0006;
    mouseY = (e.clientY - window.innerHeight / 2) * 0.0006;
});

function animate() {
    requestAnimationFrame(animate);
    
    tunnelRings.forEach(group => {
        group.position.z += 0.2; // Скорость полета туннеля
        group.rotation.x += 0.001;
        group.rotation.y += 0.0015;
        
        if (group.position.z > 20) group.position.z -= (15 * 40); // Возврат в конец
    });
    
    camera.position.x += (mouseX * 15 - camera.position.x) * 0.05;
    camera.position.y += (-mouseY * 15 - camera.position.y) * 0.05;
    camera.lookAt(scene.position);
    
    renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

let isDark = true;
function toggleTheme() {
    isDark = !isDark;
    document.documentElement.classList.toggle('dark', isDark);
    const thumb = document.getElementById('sliderThumb');
    
    if (isDark) {
        thumb.style.transform = 'translateX(0px)';
        ringMat.color.setHex(0x00aaff);
        preBlueMat.color.setHex(0x00aaff);
    } else {
        thumb.style.transform = 'translateX(62px)';
        ringMat.color.setHex(0x0055aa);
        preBlueMat.color.setHex(0x0055aa);
    }
}

// Заглушки вычислений
function parseCleanNum(val) { return typeof val === 'number' ? val : parseFloat(String(val).replace(/[^\d.-]/g, '')) || 0; }
function formatSpaced(num) { return Math.round(num).toLocaleString('ru-RU').replace(/,/g, ' '); }
function formatInput(input) { input.value = formatSpaced(parseCleanNum(input.value)); }
let chartDebtInstance = null;

function runCalculation() {
    // Вся логика расчетов и построения графиков
    const xLabels = ['Окт 2026', 'Ноя 2026', 'Дек 2026', 'Янв 2027'];
    const debtBalance = [20000000, 15000000, 5000000, 0];
    const interestPayments = [300000, 250000, 100000, 0];
    
    if (chartDebtInstance) chartDebtInstance.destroy();
    chartDebtInstance = new Chart(document.getElementById('chartDebt').getContext('2d'), {
        type: 'bar',
        data: {
            labels: xLabels,
            datasets: [
                { label: 'Проценты', data: interestPayments, backgroundColor: '#d4af37', order: 2 },
                { label: 'Долг', data: debtBalance, type: 'line', borderColor: '#e63946', borderWidth: 2.5, order: 1 }
            ]
        },
        options: { responsive: true, maintainAspectRatio: false }
    });
}
window.onload = () => runCalculation();
</script>
</body>
</html>"""

# Обработка картинки "на лету" и подстановка её в HTML
img_src = get_blueprint_vitruvian("1000400438.jpg")
html_code = html_code.replace("VITRUVIAN_IMAGE_SRC_PLACEHOLDER", img_src)

components.html(html_code, height=1350, scrolling=True)
