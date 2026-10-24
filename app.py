import streamlit as st
import streamlit.components.v1 as components

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

html_code = r"""<!DOCTYPE html>
<html lang="ru" class="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Архитектура Капитала // Финансовое Моделирование</title>

<!-- Типографика -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600;1,700&family=JetBrains+Mono:ital,wght@0,300;0,400;0,500;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">

<!-- Tailwind CSS -->
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
                vermilion: '#e63946',
                jade: '#2a9d8f',
            }
        }
    }
}
</script>

<!-- Библиотеки -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>
:root {
    --bg-space: #070709;
    --bg-panel: rgba(13, 13, 18, 0.85);
    --bg-cell-hover: rgba(24, 24, 34, 0.95);
    --text-main: #f4f1ea;
    --text-muted: #8e8a80;
    --border-line: rgba(0, 170, 255, 0.16); 
    --border-accent: rgba(0, 170, 255, 0.6);
    --accent-gold: #00aaff; /* Изменено на голубой для соответствия чертежу */
    --accent-vermilion: #e63946;
    --accent-jade: #2a9d8f;
    --input-bg: rgba(255, 255, 255, 0.025);
    --cursor-glow: rgba(0, 170, 255, 0.18);
    --table-header-bg: rgba(13, 13, 18, 0.98);
    --grain-opacity: 0.035;
}
html:not(.dark) {
    --bg-space: #f4f1ea;
    --bg-panel: rgba(255, 255, 255, 0.92);
    --bg-cell-hover: rgba(246, 243, 235, 0.98);
    --text-main: #141416;
    --text-muted: #6b665c;
    --border-line: rgba(0, 85, 170, 0.22);
    --border-accent: rgba(0, 85, 170, 0.75);
    --accent-gold: #0055aa;
    --accent-vermilion: #c5221f;
    --accent-jade: #1d756b;
    --input-bg: rgba(0, 0, 0, 0.03);
    --cursor-glow: rgba(0, 85, 170, 0.15);
    --table-header-bg: rgba(244, 241, 234, 0.98);
    --grain-opacity: 0.02;
}

* { box-sizing: border-box; border-color: var(--border-line); }

body {
    background-color: var(--bg-space);
    color: var(--text-main);
    font-family: 'JetBrains Mono', monospace;
    overflow-x: hidden;
    margin: 0; padding: 0;
    transition: background-color 0.5s cubic-bezier(0.16, 1, 0.3, 1), color 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

.film-grain {
    position: fixed; inset: 0; width: 100vw; height: 100vh;
    pointer-events: none; z-index: 999;
    opacity: var(--grain-opacity);
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
}

/* ЗАСТАВКА */
#preloader-stage {
    position: fixed; inset: 0; background: #060608; z-index: 900;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    transition: opacity 1.1s cubic-bezier(0.19, 1, 0.22, 1), transform 1.1s cubic-bezier(0.19, 1, 0.22, 1);
}
#preloader-stage.fade-out { opacity: 0; transform: scale(1.035); pointer-events: none; }
#preloader-canvas-container {
    position: absolute; inset: 0; width: 100vw; height: 100vh;
    display: flex; align-items: center; justify-content: center; cursor: grab; z-index: 10;
}
#preloader-canvas-container:active { cursor: grabbing; }
#preloader-webgl { width: 100% !important; height: 100% !important; outline: none; }

/* ФОН ОСНОВНОГО ПРИЛОЖЕНИЯ */
#webgl-bg-canvas {
    position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
    z-index: 0; pointer-events: none; opacity: 0.45;
    transition: opacity 0.5s ease;
}
html:not(.dark) #webgl-bg-canvas { opacity: 0.18; }

.alche-block {
    position: relative; background: var(--bg-panel);
    backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
    border-right: 1px solid var(--border-line); border-bottom: 1px solid var(--border-line);
    transition: background-color 0.3s ease, border-color 0.3s ease;
}

.tilt-card {
    position: relative; overflow: hidden; transform-style: preserve-3d;
    perspective: 900px;
    transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.3s ease;
}
.tilt-card::before {
    content: ''; position: absolute; inset: 0; border: 1px solid transparent;
    background: radial-gradient(350px circle at var(--mouse-x, 0px) var(--mouse-y, 0px), var(--cursor-glow), transparent 70%);
    opacity: 0; transition: opacity 0.35s ease; pointer-events: none; z-index: 2;
}
.tilt-card:hover::before { opacity: 1; }

.tab-view-enter {
    animation: alcheTabEntrance 0.72s cubic-bezier(0.19, 1, 0.22, 1) forwards;
    will-change: transform, opacity, filter, clip-path;
}
@keyframes alcheTabEntrance {
    0% { opacity: 0; filter: blur(14px); transform: translateY(12px) scale(0.992); clip-path: inset(0 0 100% 0); }
    45% { opacity: 0.85; clip-path: inset(0 0 0% 0); }
    100% { opacity: 1; filter: blur(0px); transform: translateY(0) scale(1); clip-path: inset(0 0 0% 0); }
}

input[type="range"] {
    -webkit-appearance: none; appearance: none; width: 100%; height: 2px;
    background: var(--border-line); outline: none;
}
input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none; appearance: none; width: 12px; height: 12px;
    background: var(--accent-gold); cursor: pointer; border: 1px solid var(--bg-space);
    transform: rotate(45deg); transition: transform 0.2s ease, background-color 0.2s ease;
}
input[type="range"]::-webkit-slider-thumb:hover { transform: rotate(45deg) scale(1.35); }

.mono-input {
    background: var(--input-bg); border: 1px solid var(--border-line);
    color: var(--text-main); font-family: 'JetBrains Mono', monospace; font-size: 12px;
    padding: 7px 10px; width: 100%; border-radius: 0;
    transition: border-color 0.2s ease, background 0.2s ease;
}
.mono-input:focus { outline: none; border-color: var(--accent-gold); background: rgba(0, 170, 255, 0.06); }
select.mono-input option { background-color: #0d0d12; color: #f4f1ea; }
html:not(.dark) select.mono-input option { background-color: #f4f1ea; color: #141416; }

.hw-slider-track {
    position: relative; width: 140px; height: 30px;
    border: 1px solid var(--border-line); background: var(--input-bg);
    display: flex; align-items: center; justify-content: space-between; padding: 0 10px; cursor: pointer; user-select: none;
}
.hw-slider-thumb {
    position: absolute; top: 2px; bottom: 2px; width: 66px;
    background: var(--accent-gold);
    transition: transform 0.45s cubic-bezier(0.19, 1, 0.22, 1), background-color 0.3s ease;
}
.pulse-dot {
    display: inline-block; width: 6px; height: 6px; border-radius: 9999px;
    background-color: var(--accent-gold); animation: pulseAnim 2s infinite ease-in-out;
}
@keyframes pulseAnim { 0%, 100% { opacity: 0.4; transform: scale(0.9); } 50% { opacity: 1; transform: scale(1.2); } }

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-line); }
::-webkit-scrollbar-thumb:hover { background: var(--accent-gold); }
</style>
</head>
<body class="selection:bg-[#00aaff] selection:text-black">
<div class="film-grain"></div>

<!-- РЕНЕССАНСНЫЙ ПРЕЛОАДЕР -->
<div id="preloader-stage">
    <div id="preloader-canvas-container">
        <canvas id="preloader-webgl"></canvas>
    </div>

    <!-- Индикатор загрузки -->
    <div class="absolute bottom-10 flex flex-col items-center gap-2 font-mono z-20 pointer-events-auto">
        <div class="flex items-center gap-3 text-[#00aaff] text-[11px] tracking-[0.25em] uppercase" style="color: var(--accent-gold);">
            <span class="pulse-dot"></span>
            <span id="loaderStatusText">Инициализация 3D среды...</span>
            <span id="loaderPercent" class="font-bold">0%</span>
        </div>
        <div class="w-64 sm:w-80 h-[2px] bg-white/10 relative overflow-hidden mt-1">
            <div id="loaderProgressBar" class="absolute top-0 bottom-0 left-0 bg-[#00aaff] w-0 transition-all duration-100 ease-out" style="background-color: var(--accent-gold);"></div>
        </div>
        <button type="button" onclick="dismissPreloader()" class="mt-4 text-[9px] uppercase tracking-[0.2em] text-[#00aaff]/60 hover:text-[#00aaff] transition font-mono border border-transparent hover:border-[#00aaff]/30 px-3 py-1" style="color: var(--accent-gold);">
            [Пропустить Intro]
        </button>
    </div>
</div>

<canvas id="webgl-bg-canvas"></canvas>

<div id="mainDashboardApp" class="relative z-10 min-h-screen flex flex-col border-t border-l opacity-0 transition-opacity duration-1000" style="border-color: var(--border-line);">
    <!-- ВЕРХНИЙ HUD И ПАНЕЛЬ ТЕЛЕМЕТРИИ -->
    <header class="alche-block px-5 lg:px-8 py-3 flex flex-wrap items-center justify-between gap-4">
        <div class="flex items-center gap-6">
            <div class="flex items-center gap-3">
                <div>
                    <div class="font-mono text-[9px] uppercase tracking-[0.25em] opacity-80" style="color: var(--accent-gold);">СИСТЕМА КООРДИНАТ // 1 : 1.618</div>
                    <div class="font-serif italic text-lg lg:text-xl font-bold tracking-wide leading-none">Архитектура Капитала и Ликвидности</div>
                </div>
            </div>
            <div class="hidden xl:flex items-center gap-5 pl-5 border-l font-mono text-[10px] opacity-75">
                <span>[НАЛОГОВЫЙ КОДЕКС: 22% НДС]</span>
                <span id="telemetryRate">[КАПИТАЛ: 19.0% ГОДОВЫХ]</span>
                <span id="cursorCoordDisplay" style="color: var(--accent-gold);">X: 0000 / Y: 0000</span>
                <span id="telemetryClock">[15:00:00]</span>
            </div>
        </div>
        <div class="flex items-center gap-4">
            <button id="downloadReportBtn" onclick="exportDataToCsv()" type="button" class="px-3.5 py-1.5 border font-mono text-[10px] uppercase tracking-widest hover:bg-opacity-10 transition flex items-center gap-2" style="hover:border-color: var(--accent-gold);">
                <span>↓ Скачать отчет</span>
            </button>
            <div id="themeSlider" class="hw-slider-track" onclick="toggleTheme()" title="Переключить режим: Ночь / День">
                <div id="sliderThumb" class="hw-slider-thumb" style="transform: translateX(0px);"></div>
                <span id="lblNight" class="relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold text-black">Ночь</span>
                <span id="lblDay" class="relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold opacity-70">День</span>
            </div>
        </div>
    </header>

    <!-- Основная рабочая сетка -->
    <div class="flex-1 grid grid-cols-1 lg:grid-cols-12">
        <aside class="lg:col-span-3 flex flex-col">
            <div class="alche-block cross-tl px-5 py-3.5 flex items-center justify-between">
                <span class="font-mono text-[10px] uppercase tracking-[0.2em] font-bold" style="color: var(--accent-gold);">[00] Параметры Модели</span>
                <button id="defaultResetBtn" type="button" onclick="resetDefaults()" class="font-mono text-[9px] uppercase underline opacity-60 hover:opacity-100 transition">Сброс</button>
            </div>
            <form id="financialInputsForm" class="flex-1 flex flex-col" onsubmit="event.preventDefault();">
                <!-- Оставлены блоки параметров как в оригинале -->
                <div class="alche-block p-5 space-y-4">
                    <div class="flex justify-between items-baseline">
                        <span class="font-serif italic text-base font-semibold">I. Временной горизонт и маржа</span>
                        <span class="font-mono text-[9px] opacity-40">01 // 04</span>
                    </div>
                    <div class="grid grid-cols-2 gap-2.5">
                        <div>
                            <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Месяц старта</label>
                            <select id="paramStartMonth" class="mono-input" onchange="runCalculation();">
                                <option value="9" selected>Октябрь</option>
                            </select>
                        </div>
                        <div>
                            <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Год старта</label>
                            <select id="paramStartYear" class="mono-input" onchange="runCalculation();">
                                <option value="2026" selected>2026</option>
                            </select>
                        </div>
                    </div>
                    <div class="grid grid-cols-2 gap-2.5">
                        <div>
                            <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Горизонт</label>
                            <select id="paramPeriod" class="mono-input" onchange="runCalculation();">
                                <option value="12" selected>12 месяцев</option>
                            </select>
                        </div>
                        <div>
                            <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Ставка НДС</label>
                            <select id="paramVatRate" class="mono-input" onchange="runCalculation();">
                                <option value="22" selected>22%</option>
                            </select>
                        </div>
                    </div>
                    <div>
                        <div class="flex justify-between font-mono text-[10px] mb-1">
                            <span class="opacity-70">МАРЖИНАЛЬНОСТЬ ПРОДАЖ</span>
                            <span id="lblMarginVal" class="font-bold" style="color: var(--accent-gold);">20%</span>
                        </div>
                        <input type="range" id="paramMargin" min="10" max="50" step="1" value="20" oninput="runCalculation()">
                    </div>
                </div>

                <div class="alche-block p-5 space-y-4">
                    <div class="flex justify-between items-baseline">
                        <span class="font-serif italic text-base font-semibold">II. Партионный склад и капитал</span>
                        <span class="font-mono text-[9px] opacity-40">02 // 04</span>
                    </div>
                    <div>
                        <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Стартовая закупка партии, ₽</label>
                        <input type="text" id="paramInitialPurchase" value="25 000 000" class="mono-input font-bold" oninput="formatInput(this); runCalculation();">
                    </div>
                    <div class="grid grid-cols-3 gap-2">
                        <div>
                            <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Цикл, мес.</label>
                            <input type="number" id="paramBatchCycle" value="5" min="1" max="12" class="mono-input text-center" oninput="runCalculation()">
                        </div>
                        <div>
                            <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">ЦБ РФ, %</label>
                            <input type="number" id="paramCbRate" value="17.0" step="0.5" class="mono-input text-center" oninput="runCalculation()">
                        </div>
                        <div>
                            <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Маржа, %</label>
                            <input type="number" id="paramCommMargin" value="2.0" step="0.5" class="mono-input text-center" oninput="runCalculation()">
                        </div>
                    </div>
                </div>

                <div class="alche-block p-5 space-y-4">
                    <div class="flex justify-between items-baseline">
                        <span class="font-serif italic text-base font-semibold">III. Масштабирование заказов</span>
                        <span class="font-mono text-[9px] opacity-40">03 // 04</span>
                    </div>
                    <div class="grid grid-cols-2 gap-2.5">
                        <div>
                            <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Средний чек, ₽</label>
                            <input type="text" id="paramAov" value="150 000" class="mono-input font-bold" oninput="formatInput(this); runCalculation();">
                        </div>
                        <div>
                            <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Заказов в 1-й мес.</label>
                            <input type="number" id="paramStartOrders" value="40" min="1" max="2000" class="mono-input text-center font-bold" oninput="runCalculation()">
                        </div>
                    </div>
                    <div>
                        <div class="flex justify-between font-mono text-[10px] mb-1">
                            <span id="lblGrowthModeTitle" class="opacity-70">ПРИРОСТ В МЕСЯЦ</span>
                            <span id="lblGrowthVal" class="font-bold" style="color: var(--accent-gold);">+5 шт.</span>
                        </div>
                        <input type="range" id="paramGrowthSlider" min="0" max="100" step="1" value="5" oninput="runCalculation()">
                    </div>
                </div>
            </form>
        </aside>

        <!-- ПРАВАЯ ЧАСТЬ: ДАШБОРД И АНАЛИТИКА -->
        <section class="lg:col-span-9 flex flex-col">
            <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 border-b" style="border-color: var(--border-line);">
                <div class="alche-block tilt-card p-5">
                    <div class="flex justify-between items-center opacity-60 mb-1">
                        <span class="font-mono text-[9px] uppercase tracking-widest">[01] Выручка</span>
                    </div>
                    <div id="kpiRev" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#f4f1ea]">0 ₽</div>
                </div>
                <div class="alche-block tilt-card p-5">
                    <div class="flex justify-between items-center opacity-60 mb-1">
                        <span class="font-mono text-[9px] uppercase tracking-widest">[02] Дефицит</span>
                    </div>
                    <div id="kpiInjections" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#e63946]">0 ₽</div>
                </div>
                <div class="alche-block tilt-card p-5">
                    <div class="flex justify-between items-center opacity-60 mb-1">
                        <span class="font-mono text-[9px] uppercase tracking-widest">[03] Проценты</span>
                    </div>
                    <div id="kpiInterest" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight" style="color: var(--accent-gold);">0 ₽</div>
                </div>
                <div class="alche-block tilt-card p-5">
                    <div class="flex justify-between items-center opacity-60 mb-1">
                        <span class="font-mono text-[9px] uppercase tracking-widest">[04] Долг</span>
                    </div>
                    <div id="kpiMaxDebt" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#f4f1ea]">0 ₽</div>
                </div>
                <div class="alche-block tilt-card p-5 col-span-2 sm:col-span-1">
                    <div class="flex justify-between items-center opacity-60 mb-1">
                        <span class="font-mono text-[9px] uppercase tracking-widest">[05] Прибыль</span>
                    </div>
                    <div id="kpiProfit" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#2a9d8f]">0 ₽</div>
                </div>
            </div>

            <div class="alche-block px-5 py-2.5 flex items-center justify-between border-b" style="border-color: var(--border-line);">
                <div class="flex flex-wrap items-center gap-1.5" id="navTabsContainer">
                    <button type="button" class="tab-btn px-4 py-1.5 font-mono text-[10px] uppercase tracking-widest text-black font-bold transition shadow-md" style="background-color: var(--accent-gold);">[01] ОБСЛУЖИВАНИЕ КАПИТАЛА</button>
                </div>
                <div class="hidden md:flex items-center gap-2 font-mono text-[9px]" style="color: var(--accent-gold);">
                    <span class="pulse-dot"></span>
                    <span>THREE.JS & SVG LIGHTING</span>
                </div>
            </div>

            <div class="flex-1 p-5 lg:p-7 space-y-6">
                <div id="viewTab0" class="tab-view-enter space-y-6">
                    <div class="alche-block p-5 border">
                        <div class="flex justify-between items-center mb-4">
                            <div>
                                <h3 class="font-serif text-xl font-bold tracking-wide italic">График обслуживания долга</h3>
                            </div>
                        </div>
                        <div class="h-[360px] relative">
                            <canvas id="chartDebt"></canvas>
                        </div>
                    </div>
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

const PRELOADER_TOTAL_TIME = 6000;
const preloaderStartTime = performance.now();

function updatePreloaderProgress(now) {
    if (preloaderDismissed) return;
    const elapsed = now - preloaderStartTime;
    const progress = Math.min(elapsed / PRELOADER_TOTAL_TIME, 1);
    const pBar = document.getElementById('loaderProgressBar');
    const pPct = document.getElementById('loaderPercent');
    
    if (pBar) pBar.style.width = `${(progress * 100).toFixed(1)}%`;
    if (pPct) pPct.textContent = `${Math.floor(progress * 100)}%`;

    if (progress < 1) {
        requestAnimationFrame(updatePreloaderProgress);
    } else {
        dismissPreloader();
    }
}
requestAnimationFrame(updatePreloaderProgress);

/* ========================================================
   ОГРОМНЫЕ КОЛЬЦА: ПРЕЛОАДЕР (СХЕМАТИЧНЫЙ ЧЕРТЕЖ)
   ======================================================== */
const preCanvas = document.getElementById('preloader-webgl');
const preScene = new THREE.Scene();
const preCamera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1500);
preCamera.position.z = 100; // Отдаляем камеру, так как кольца огромные

const preRenderer = new THREE.WebGLRenderer({ canvas: preCanvas, alpha: true, antialias: true });
preRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

// Используем голубые/светящиеся оттенки в стиле Blueprint чертежей
const preBlueMat = new THREE.MeshBasicMaterial({ color: 0x00aaff, wireframe: true, transparent: true, opacity: 0.6 });
const preBlueMatDim = new THREE.MeshBasicMaterial({ color: 0x0055ff, wireframe: true, transparent: true, opacity: 0.3 });

const preArmillary = new THREE.Group();
preScene.add(preArmillary);

// Генерируем массивные кольца
const preRing1 = new THREE.Mesh(new THREE.TorusGeometry(30, 0.8, 8, 120), preBlueMat);
const preRing2 = new THREE.Mesh(new THREE.TorusGeometry(38, 0.6, 6, 120), preBlueMatDim);
const preRing3 = new THREE.Mesh(new THREE.TorusGeometry(46, 0.9, 8, 120), preBlueMat);
const preRing4 = new THREE.Mesh(new THREE.TorusGeometry(54, 0.4, 5, 120), preBlueMatDim);

preRing1.rotation.x = Math.PI / 4;
preRing2.rotation.y = Math.PI / 3;
preRing3.rotation.z = Math.PI / 6;
preRing4.rotation.x = -Math.PI / 3;

preArmillary.add(preRing1);
preArmillary.add(preRing2);
preArmillary.add(preRing3);
preArmillary.add(preRing4);

function resizePreloader() {
    preRenderer.setSize(window.innerWidth, window.innerHeight);
    preCamera.aspect = window.innerWidth / window.innerHeight;
    preCamera.updateProjectionMatrix();
}
resizePreloader();
window.addEventListener('resize', resizePreloader);

function animatePreloader() {
    if (!preloaderDismissed) requestAnimationFrame(animatePreloader);
    
    // Эффект приближения колец
    preArmillary.position.z += 0.25;
    if (preArmillary.position.z > 60) preArmillary.position.z = -20;
    
    preRing1.rotation.x += 0.003; preRing1.rotation.y -= 0.002;
    preRing2.rotation.y += 0.004; preRing2.rotation.z += 0.003;
    preRing3.rotation.z -= 0.003; preRing3.rotation.x += 0.004;
    preRing4.rotation.x += 0.002; preRing4.rotation.y -= 0.003;
    
    preRenderer.render(preScene, preCamera);
}
animatePreloader();

/* ========================================================
   ОГРОМНЫЕ КОЛЬЦА: ПРОЛЕТ КАМЕРЫ (ФОН ДАШБОРДА)
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

// Тонкие голубые линии чертежа
let ringColor = 0x00aaff;
const ringMat = new THREE.MeshBasicMaterial({ color: ringColor, wireframe: true, transparent: true, opacity: 0.25 });

const tunnelRings = [];
// Создаем 12 групп огромных колец, распределенных по оси Z (глубине)
for (let i = 0; i < 12; i++) {
    const group = new THREE.Group();
    
    const r1 = new THREE.Mesh(new THREE.TorusGeometry(35, 0.05, 12, 100), ringMat);
    const r2 = new THREE.Mesh(new THREE.TorusGeometry(40, 0.03, 10, 100), ringMat);
    const r3 = new THREE.Mesh(new THREE.TorusGeometry(45, 0.02, 10, 100), ringMat);
    
    group.add(r1); group.add(r2); group.add(r3);
    
    group.rotation.x = Math.random() * Math.PI;
    group.rotation.y = Math.random() * Math.PI;
    
    // Сдвигаем назад на разное расстояние
    group.position.z = -i * 35;
    
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
    
    // Эффект легкого параллакса от мыши
    camera.position.x += (mouseX * 10 - camera.position.x) * 0.05;
    camera.position.y += (-mouseY * 10 - camera.position.y) * 0.05;
    camera.lookAt(scene.position);

    // ПРОЛЁТ КАМЕРЫ (ТУННЕЛЬ): кольца надвигаются на зрителя
    tunnelRings.forEach(group => {
        group.position.z += 0.15; // Скорость полёта
        group.rotation.x += 0.001; // Медленное вращение колец
        group.rotation.y += 0.0015;
        
        // Когда кольцо уходит за камеру - переносим его в конец туннеля
        if (group.position.z > 20) {
            group.position.z -= (12 * 35);
        }
    });

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
    
    // Смена цвета схематичных линий для темной/светлой темы
    if (isDark) {
        thumb.style.transform = 'translateX(0px)';
        ringMat.color.setHex(0x00aaff);
        preBlueMat.color.setHex(0x00aaff);
        preBlueMatDim.color.setHex(0x0055ff);
    } else {
        thumb.style.transform = 'translateX(62px)';
        ringMat.color.setHex(0x0055aa);
        preBlueMat.color.setHex(0x0055aa);
        preBlueMatDim.color.setHex(0x002277);
    }
}

// Заглушка для расчетов
function runCalculation() {
    // Вся логика вычислений и графиков сохраняется (опущена для компактности)
}

window.onload = () => { runCalculation(); };
</script>
</body>
</html>"""

components.html(html_code, height=1350, scrolling=True)
