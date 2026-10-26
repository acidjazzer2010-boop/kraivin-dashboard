"""
Архитектура Капитала // Финансовое Моделирование
Запуск: streamlit run app.py
"""
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Архитектура Капитала // Финансовое Моделирование",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Скрываем UI Streamlit по data-testid (устойчиво к обновлениям)
st.markdown("""
<style>
#MainMenu, footer, header[data-testid="stHeader"],
[data-testid="stDeployButton"] { visibility: hidden !important; display: none !important; }
.block-container, [data-testid="stAppViewBlockContainer"] {
    padding: 0 !important; max-width: 100% !important; margin: 0 !important;
}
section.main, [data-testid="stAppViewContainer"] > .main {
    background-color: #070709 !important; padding: 0 !important;
}
iframe[title="streamlit_component"] {
    border: none !important; width: 100vw !important; display: block !important;
}
body { overflow: hidden; }  /* родительская страница Streamlit — не iframe */
</style>
""", unsafe_allow_html=True)

HTML = r"""<!DOCTYPE html>
<html lang="ru" class="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Архитектура Капитала // Финансовое Моделирование</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600;1,700&family=JetBrains+Mono:ital,wght@0,300;0,400;0,500;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">

<script src="https://cdn.tailwindcss.com/3.4.1"></script>
<script>
tailwind.config = {
    darkMode: 'class',
    theme: { extend: {
        fontFamily: {
            serif: ['"Cormorant Garamond"', 'Georgia', 'serif'],
            mono:  ['"JetBrains Mono"', 'monospace'],
            sans:  ['"Inter"', 'system-ui', 'sans-serif'],
        },
        colors: {
            obsidian: '#070709', obsidianCard: '#0d0d12',
            alabaster: '#f4f1ea', gold: '#d4af37',
            vermilion: '#e63946', jade: '#2a9d8f',
        }
    }}
}
</script>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

<style>
:root {
    --bg-space: #070709;
    --bg-panel: rgba(13, 13, 18, 0.85);
    --bg-cell-hover: rgba(24, 24, 34, 0.95);
    --text-main: #f4f1ea;
    --text-muted: #8e8a80;
    --border-line: rgba(212, 175, 55, 0.16);
    --border-accent: rgba(212, 175, 55, 0.6);
    --accent-gold: #d4af37;
    --accent-vermilion: #e63946;
    --accent-jade: #2a9d8f;
    --input-bg: rgba(255, 255, 255, 0.025);
    --cursor-glow: rgba(212, 175, 55, 0.2);
    --table-header-bg: rgba(13, 13, 18, 0.98);
    --grain-opacity: 0.035;
}
html:not(.dark) {
    --bg-space: #f4f1ea;
    --bg-panel: rgba(255, 255, 255, 0.92);
    --bg-cell-hover: rgba(246, 243, 235, 0.98);
    --text-main: #141416;
    --text-muted: #6b665c;
    --border-line: rgba(184, 134, 11, 0.22);
    --border-accent: rgba(184, 134, 11, 0.75);
    --accent-gold: #b8860b;
    --accent-vermilion: #c5221f;
    --accent-jade: #1d756b;
    --input-bg: rgba(0, 0, 0, 0.03);
    --cursor-glow: rgba(184, 134, 11, 0.15);
    --table-header-bg: rgba(244, 241, 234, 0.98);
    --grain-opacity: 0.02;
}

* { box-sizing: border-box; border-color: var(--border-line); margin: 0; padding: 0; }

/* FIX: overflow скрываем только до окончания прелоадера */
html, body {
    width: 100%;
    min-height: 100vh;
    min-height: 100dvh;
    margin: 0; padding: 0;
    background-color: var(--bg-space);
    color: var(--text-main);
    font-family: 'JetBrains Mono', monospace;
}
body.preloading { overflow: hidden; }

/* A11Y: видимый фокус */
:focus-visible { outline: 2px solid var(--accent-gold); outline-offset: 2px; }
button:focus:not(:focus-visible) { outline: none; }

.film-grain {
    position: fixed; inset: 0; width: 100vw; height: 100vh; height: 100dvh;
    pointer-events: none; z-index: 999; opacity: var(--grain-opacity);
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
}

/* ПРЕЛОАДЕР */
#preloader-stage {
    position: fixed; top: 0; left: 0;
    width: 100vw; height: 100vh; height: 100dvh;
    background: radial-gradient(circle at center, #0a0b12 0%, #030306 100%);
    z-index: 900; overflow: hidden;
}
#preloader-webgl {
    position: absolute; inset: 0;
    width: 100%; height: 100%; z-index: 10; cursor: grab;
}
#preloader-webgl:active { cursor: grabbing; }

.preloader-fixed-hud {
    position: absolute; inset: 0;
    width: 100%; height: 100%;
    z-index: 30; pointer-events: none; user-select: none;
}

#preloaderTitle {
    position: absolute; top: 48px; left: 50%; transform: translateX(-50%);
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-style: italic;
    font-size: clamp(20px, 3.5vw, 46px);
    font-weight: 700; letter-spacing: 0.28em;
    color: var(--accent-gold); opacity: 0;
    text-shadow: 0 0 45px rgba(212, 175, 55, 0.85);
    transition: opacity 1.8s cubic-bezier(0.16, 1, 0.3, 1);
    text-align: center; white-space: nowrap;
}
#preloaderTitle.locked-on { opacity: 1 !important; }

.bottom-dock {
    position: absolute; bottom: 44px; left: 50%; transform: translateX(-50%);
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    width: 340px; height: 56px;
}
#preloaderHUD {
    display: flex; flex-direction: column; align-items: center; gap: 8px;
    transition: opacity 0.4s ease;
}
.progress-bar-bg {
    width: 280px; height: 2px;
    background: rgba(255, 255, 255, 0.12);
    position: relative; overflow: hidden;
}
#loaderProgressBar {
    position: absolute; left: 0; top: 0; height: 100%; width: 0%;
    background: var(--accent-gold); box-shadow: 0 0 10px var(--accent-gold);
    transition: width 0.1s linear;
}
#exploreBtnWrapper {
    position: absolute; opacity: 0; pointer-events: none;
    transition: opacity 0.6s cubic-bezier(0.19, 1, 0.22, 1), transform 0.6s cubic-bezier(0.19, 1, 0.22, 1);
    transform: translateY(8px);
}
#exploreBtnWrapper.active { opacity: 1; pointer-events: auto; transform: translateY(0); }

.explore-btn {
    padding: 13px 46px;
    background: rgba(13, 13, 18, 0.9);
    border: 1px solid rgba(212, 175, 55, 0.95);
    color: #f4f1ea;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px; letter-spacing: 0.38em;
    text-transform: uppercase; cursor: pointer;
    backdrop-filter: blur(14px); overflow: hidden;
    transition: all 0.3s ease;
    box-shadow: 0 0 40px rgba(212, 175, 55, 0.35), inset 0 0 16px rgba(212, 175, 55, 0.18);
}
.explore-btn::before {
    content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.45), transparent);
    transition: left 0.7s ease;
}
.explore-btn:hover {
    border-color: #ffd700; color: #ffd700;
    box-shadow: 0 0 60px rgba(212, 175, 55, 0.7), inset 0 0 24px rgba(212, 175, 55, 0.35);
    transform: scale(1.05);
}
.explore-btn:hover::before { left: 100%; }

/* ДАШБОРД */
#mainDashboardApp {
    display: none; position: relative; z-index: 10;
    min-height: 100vh; min-height: 100dvh;
}
#mainDashboardApp.ready { display: flex; }

#webgl-bg-canvas {
    position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; height: 100dvh;
    z-index: 0; pointer-events: none; opacity: 0.35;
}
html:not(.dark) #webgl-bg-canvas { opacity: 0.18; }

.alche-block {
    position: relative; background: var(--bg-panel); backdrop-filter: blur(20px);
    border-right: 1px solid var(--border-line); border-bottom: 1px solid var(--border-line);
}
.cross-tl::before { content: '+'; position: absolute; top: -6px; left: -4px; font-family: 'JetBrains Mono', monospace; font-size: 10px; line-height: 1; color: var(--accent-gold); pointer-events: none; z-index: 10; }
.cross-br::after { content: '+'; position: absolute; bottom: -6px; right: -4px; font-family: 'JetBrains Mono', monospace; font-size: 10px; line-height: 1; color: var(--accent-gold); pointer-events: none; z-index: 10; }

.tilt-card {
    position: relative; overflow: hidden; transform-style: preserve-3d; perspective: 1000px;
    transition: transform 0.25s cubic-bezier(0.2, 0, 0.2, 1), border-color 0.3s ease;
}
.tilt-card::before {
    content: ''; position: absolute; inset: -1px; border: 1px solid transparent;
    background: radial-gradient(350px circle at var(--mouse-x, 0px) var(--mouse-y, 0px), var(--cursor-glow), transparent 75%);
    opacity: 0; transition: opacity 0.4s ease; pointer-events: none; z-index: 2;
}
.tilt-card:hover::before { opacity: 1; }

.tab-view-enter { animation: tabEntrance 0.6s cubic-bezier(0.19, 1, 0.22, 1) forwards; }
@keyframes tabEntrance {
    0% { opacity: 0; filter: blur(8px); transform: translateY(8px); }
    100% { opacity: 1; filter: blur(0px); transform: translateY(0); }
}

input[type="range"] { -webkit-appearance: none; appearance: none; width: 100%; height: 2px; background: var(--border-line); outline: none; }
input[type="range"]::-webkit-slider-thumb { -webkit-appearance: none; appearance: none; width: 12px; height: 12px; background: var(--accent-gold); cursor: pointer; border: 1px solid var(--bg-space); transform: rotate(45deg); transition: transform 0.2s ease; }
input[type="range"]::-webkit-slider-thumb:hover { transform: rotate(45deg) scale(1.4); }

.mono-input { background: var(--input-bg); border: 1px solid var(--border-line); color: var(--text-main); font-family: 'JetBrains Mono', monospace; font-size: 11px; padding: 6px 9px; width: 100%; border-radius: 0; outline: none; transition: border-color 0.2s ease; }
.mono-input:focus { border-color: var(--accent-gold); background: rgba(212, 175, 55, 0.06); }
select.mono-input option { background-color: #0d0d12; color: #f4f1ea; }

.hw-slider-track { position: relative; width: 130px; height: 28px; border: 1px solid var(--border-line); background: var(--input-bg); display: flex; align-items: center; justify-content: space-between; padding: 0 10px; cursor: pointer; user-select: none; }
.hw-slider-thumb { position: absolute; top: 2px; bottom: 2px; width: 62px; background: var(--accent-gold); transition: transform 0.45s cubic-bezier(0.19, 1, 0.22, 1); }
.pulse-dot { display: inline-block; width: 6px; height: 6px; border-radius: 9999px; background-color: var(--accent-gold); animation: pulseAnim 2s infinite ease-in-out; }
@keyframes pulseAnim { 0%, 100% { opacity: 0.4; transform: scale(0.9); } 50% { opacity: 1; transform: scale(1.2); } }

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-line); }
::-webkit-scrollbar-thumb:hover { background: var(--accent-gold); }
* { scrollbar-width: thin; scrollbar-color: var(--border-line) transparent; }

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
</style>
</head>
<body class="preloading selection:bg-[#d4af37] selection:text-black">
<div class="film-grain" aria-hidden="true"></div>

<div id="preloader-stage">
    <canvas id="preloader-webgl"></canvas>
    <div class="preloader-fixed-hud">
        <div id="preloaderTitle">Архитектура финансов</div>
        <div class="bottom-dock">
            <div id="preloaderHUD">
                <div class="flex items-center gap-3 text-[#d4af37] text-[10px] tracking-[0.25em] uppercase font-mono">
                    <span class="pulse-dot" aria-hidden="true"></span>
                    <span id="loaderStatusText">Трассировка кинематических узлов...</span>
                    <span id="loaderPercent" class="font-bold">0%</span>
                </div>
                <div class="progress-bar-bg mt-1">
                    <div id="loaderProgressBar"></div>
                </div>
            </div>
            <div id="exploreBtnWrapper">
                <button id="exploreBtn" onclick="triggerLiquidTransition(event)" class="explore-btn">
                    Исследовать
                </button>
            </div>
        </div>
    </div>
</div>

<canvas id="webgl-bg-canvas"></canvas>

<div id="mainDashboardApp" class="flex-col border-t border-l opacity-0 transition-opacity duration-1000">
    <header class="alche-block px-5 lg:px-8 py-3 flex flex-wrap items-center justify-between gap-4 border-b">
        <div class="flex items-center gap-6">
            <div class="flex items-center gap-3 cursor-pointer" onclick="playClickSound(1500, 0.04)">
                <svg class="w-7 h-7 text-[#d4af37]" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true">
                    <circle cx="16" cy="16" r="14" /><rect x="6" y="6" width="20" height="20" />
                    <polygon points="16,2 30,26 2,26" stroke-width="0.8" stroke-dasharray="1 1"/>
                    <line x1="2" y1="16" x2="30" y2="16" stroke-dasharray="2 2"/>
                    <line x1="16" y1="2" x2="16" y2="30" stroke-dasharray="2 2"/>
                </svg>
                <div>
                    <div class="font-mono text-[9px] uppercase tracking-[0.25em] text-[#d4af37] opacity-80">AUREA PROPORTIO // 1 : 1.618</div>
                    <div class="font-serif italic text-lg lg:text-xl font-bold tracking-wide leading-none">Архитектура Капитала и Ликвидности</div>
                </div>
            </div>
            <div class="hidden xl:flex items-center gap-5 pl-5 border-l font-mono text-[10px] opacity-75">
                <span>[НАЛОГОВЫЙ КОДЕКС: 22% НДС]</span>
                <span id="telemetryRate">[КАПИТАЛ: 16.0% ГОДОВЫХ]</span>
                <span id="cursorCoordDisplay" class="text-[#d4af37]" aria-hidden="true">X: 0000 / Y: 0000</span>
                <span id="telemetryClock">[15:00:00]</span>
            </div>
        </div>
        <div class="flex items-center gap-4">
            <button id="downloadReportBtn" onclick="exportDataToCsv()" type="button" class="px-3.5 py-1.5 border font-mono text-[10px] uppercase tracking-widest hover:border-[#d4af37] hover:bg-[#d4af37]/10 transition flex items-center gap-2">
                <span>↓ Скачать отчет</span>
            </button>
            <div id="themeSlider" class="hw-slider-track" onclick="toggleTheme()"
                 role="switch" aria-checked="true" aria-label="Переключить режим: Ночь / День" tabindex="0">
                <div id="sliderThumb" class="hw-slider-thumb" style="transform: translateX(0px);"></div>
                <span id="lblNight" class="relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold text-black">Ночь</span>
                <span id="lblDay" class="relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold opacity-70">День</span>
            </div>
        </div>
    </header>

    <div class="flex-1 grid grid-cols-1 lg:grid-cols-12">
        <aside class="lg:col-span-3 flex flex-col border-r">
            <div class="alche-block cross-tl px-5 py-3.5 flex items-center justify-between">
                <span class="font-mono text-[10px] uppercase tracking-[0.2em] text-[#d4af37] font-bold">[00] Параметры Модели</span>
                <button id="defaultResetBtn" type="button" onclick="resetDefaults()" class="font-mono text-[9px] uppercase underline opacity-60 hover:opacity-100 transition">Сброс</button>
            </div>
            <form id="financialInputsForm" class="flex-1 flex flex-col" onsubmit="event.preventDefault();">
                <div class="alche-block p-5 space-y-4">
                    <div class="flex justify-between items-baseline">
                        <span class="font-serif italic text-base font-semibold">I. Временной горизонт и маржа</span>
                        <span class="font-mono text-[9px] opacity-40" aria-hidden="true">01 // 04</span>
                    </div>
                    <div class="grid grid-cols-2 gap-2.5">
                        <div>
                            <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Месяц старта</label>
                            <select id="paramStartMonth" class="mono-input" onchange="playClickSound(); runCalculation();">
                                <option value="0">Январь</option><option value="1">Февраль</option><option value="2">Март</option><option value="3">Апрель</option>
                                <option value="4">Май</option><option value="5">Июнь</option><option value="6">Июль</option><option value="7">Август</option>
                                <option value="8">Сентябрь</option><option value="9" selected>Октябрь</option><option value="10">Ноябрь</option><option value="11">Декабрь</option>
                            </select>
                        </div>
                        <div>
                            <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Год старта</label>
                            <select id="paramStartYear" class="mono-input" onchange="playClickSound(); runCalculation();">
                                <option value="2026" selected>2026</option><option value="2027">2027</option>
                            </select>
                        </div>
                    </div>
                    <div class="grid grid-cols-2 gap-2.5">
                        <div>
                            <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Горизонт</label>
                            <select id="paramPeriod" class="mono-input" onchange="playClickSound(); runCalculation();">
                                <option value="6">6 месяцев</option><option value="12" selected>12 месяцев</option>
                                <option value="18">18 месяцев</option><option value="24">24 месяца</option>
                            </select>
                        </div>
                        <div>
                            <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Ставка НДС</label>
                            <select id="paramVatRate" class="mono-input" onchange="playClickSound(); runCalculation();">
                                <option value="22" selected>22%</option><option value="20">20%</option><option value="10">10%</option><option value="0">0%</option>
                            </select>
                        </div>
                    </div>
                    <div>
                        <div class="flex justify-between font-mono text-[10px] mb-1">
                            <span class="opacity-70">МАРЖИНАЛЬНОСТЬ ПРОДАЖ</span><span id="lblMarginVal" class="text-[#d4af37] font-bold">20%</span>
                        </div>
                        <input type="range" id="paramMargin" min="10" max="50" step="1" value="20" oninput="scheduleCalc()">
                    </div>
                </div>

                <div class="alche-block p-5 space-y-4">
                    <div class="flex justify-between items-baseline"><span class="font-serif italic text-base font-semibold">II. Партионный склад и кредитование</span><span class="font-mono text-[9px] opacity-40" aria-hidden="true">02 // 04</span></div>
                    <div>
                        <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Стартовая закупка партии, ₽</label>
                        <input type="text" id="paramInitialPurchase" value="25 000 000" class="mono-input font-bold" inputmode="numeric" oninput="formatInput(this); scheduleCalc();">
                    </div>
                    <div class="grid grid-cols-3 gap-2">
                        <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Цикл, мес.</label><input type="number" id="paramBatchCycle" value="5" min="1" max="12" class="mono-input text-center" oninput="scheduleCalc()"></div>
                        <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">ЦБ РФ, %</label><input type="number" id="paramCbRate" value="14.0" step="0.5" class="mono-input text-center font-bold text-[#d4af37]" oninput="scheduleCalc()"></div>
                        <div><label class="block font-mono text-[8px] uppercase opacity-70 mb-1" title="Коммерческая наценка кредитора">Комиссия, %</label><input type="number" id="paramCommMargin" value="2.0" step="0.5" class="mono-input text-center" oninput="scheduleCalc()"></div>
                    </div>
                    <div class="p-3 border space-y-3" style="border-color: rgba(212, 175, 55, 0.25); background: rgba(212, 175, 55, 0.02);">
                        <div class="font-mono text-[8px] uppercase tracking-widest text-[#d4af37] font-bold">[УСЛОВИЯ ПОСТАВЩИКА]</div>
                        <div>
                            <div class="flex justify-between font-mono text-[9px] mb-1">
                                <span class="opacity-70">ПРЕДОПЛАТА ПОСТАВЩИКУ</span>
                                <span id="lblSupplierPrepVal" class="text-[#d4af37] font-bold">50%</span>
                            </div>
                            <input type="range" id="paramSupplierPrepay" min="0" max="100" step="10" value="50" oninput="scheduleCalc()">
                        </div>
                        <div>
                            <div class="flex justify-between font-mono text-[9px] mb-1">
                                <span class="opacity-70">ОТСРОЧКА ОСТАТКА</span>
                                <span id="lblSupplierDelayVal" class="text-[#d4af37] font-bold">1 мес.</span>
                            </div>
                            <input type="range" id="paramSupplierDelay" min="0" max="6" step="1" value="1" oninput="scheduleCalc()">
                        </div>
                    </div>
                </div>

                <div class="alche-block p-5 space-y-4">
                    <div class="flex justify-between items-baseline"><span class="font-serif italic text-base font-semibold">III. Масштабирование заказов</span><span class="font-mono text-[9px] opacity-40" aria-hidden="true">03 // 04</span></div>
                    <div class="grid grid-cols-2 gap-2.5">
                        <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Средний чек, ₽</label><input type="text" id="paramAov" value="150 000" class="mono-input font-bold" inputmode="numeric" oninput="formatInput(this); scheduleCalc();"></div>
                        <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Заказов в 1-й мес.</label><input type="number" id="paramStartOrders" value="40" min="1" max="2000" class="mono-input text-center font-bold" oninput="scheduleCalc()"></div>
                    </div>
                    <div>
                        <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Логика прироста</label>
                        <div class="grid grid-cols-2 border">
                            <button type="button" id="btnModeAbs" onclick="setGrowthMode('abs')" class="py-1 font-mono text-[9px] uppercase tracking-wider bg-[#d4af37] text-black font-bold transition">В штуках</button>
                            <button type="button" id="btnModePct" onclick="setGrowthMode('pct')" class="py-1 font-mono text-[9px] uppercase tracking-wider opacity-60 hover:opacity-100 transition">В процентах</button>
                        </div>
                    </div>
                    <div>
                        <div class="flex justify-between font-mono text-[10px] mb-1"><span id="lblGrowthModeTitle" class="opacity-70">ПРИРОСТ В МЕСЯЦ</span><span id="lblGrowthVal" class="text-[#d4af37] font-bold">+5 шт.</span></div>
                        <input type="range" id="paramGrowthSlider" min="0" max="100" step="1" value="5" oninput="scheduleCalc()">
                    </div>
                    <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Потолок продаж в месяц, шт.</label><input type="number" id="paramMaxOrdersCap" value="300" min="10" step="10" class="mono-input text-center" oninput="scheduleCalc()"></div>
                </div>

                <div class="alche-block p-5 space-y-4 flex-1">
                    <div class="flex justify-between items-baseline"><span class="font-serif italic text-base font-semibold">IV. Постоянные затраты и факторинг</span><span class="font-mono text-[9px] opacity-40" aria-hidden="true">04 // 04</span></div>
                    <div class="grid grid-cols-3 gap-2">
                        <div><label class="block font-mono text-[8px] uppercase opacity-70 mb-1">ФОТ, ₽</label><input type="text" id="paramFot" value="500 000" class="mono-input" inputmode="numeric" oninput="formatInput(this); scheduleCalc();"></div>
                        <div><label class="block font-mono text-[8px] uppercase opacity-70 mb-1">Склад, ₽</label><input type="text" id="paramWh" value="200 000" class="mono-input" inputmode="numeric" oninput="formatInput(this); scheduleCalc();"></div>
                        <div><label class="block font-mono text-[8px] uppercase opacity-70 mb-1">Офис, ₽</label><input type="text" id="paramOffice" value="150 000" class="mono-input" inputmode="numeric" oninput="formatInput(this); scheduleCalc();"></div>
                    </div>
                    <div class="pt-1">
                        <div>
                            <div class="flex justify-between font-mono text-[9px] mb-1">
                                <span class="opacity-70">ДОЛЯ ФАКТОРИНГА В ВЫРУЧКЕ</span>
                                <span id="lblFactShareVal" class="text-[#d4af37] font-bold">50%</span>
                            </div>
                            <input type="range" id="paramFactoringShare" min="0" max="100" step="10" value="50" oninput="scheduleCalc()">
                        </div>
                    </div>
                </div>
            </form>
        </aside>

        <section class="lg:col-span-9 flex flex-col">
            <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 border-b">
                <div class="alche-block tilt-card p-5" onmouseenter="scrambleTitle(this)">
                    <div class="flex justify-between items-center opacity-60 mb-1"><span class="metric-title font-mono text-[9px] uppercase tracking-widest" data-original="[01] Выручка">[01] Выручка</span></div>
                    <div id="kpiRev" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#f4f1ea]">0 ₽</div>
                    <div class="font-mono text-[9px] text-[#d4af37] mt-1.5 opacity-90" id="kpiRevSub">Маржа: 20%</div>
                </div>
                <div class="alche-block tilt-card p-5" onmouseenter="scrambleTitle(this)">
                    <div class="flex justify-between items-center opacity-60 mb-1"><span class="metric-title font-mono text-[9px] uppercase tracking-widest" data-original="[02] Дефицит">[02] Дефицит</span></div>
                    <div id="kpiInjections" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#e63946]">0 ₽</div>
                    <div class="font-mono text-[9px] text-[#e63946] mt-1.5 opacity-90">Внешние дотации</div>
                </div>
                <div class="alche-block tilt-card p-5" onmouseenter="scrambleTitle(this)">
                    <div class="flex justify-between items-center opacity-60 mb-1"><span class="metric-title font-mono text-[9px] uppercase tracking-widest" data-original="[03] Проценты">[03] Проценты</span></div>
                    <div id="kpiInterest" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#d4af37]">0 ₽</div>
                    <div id="kpiRateSub" class="font-mono text-[9px] text-[#d4af37] mt-1.5 opacity-90">Ставка 16.0%</div>
                </div>
                <div class="alche-block tilt-card p-5" onmouseenter="scrambleTitle(this)">
                    <div class="flex justify-between items-center opacity-60 mb-1"><span class="metric-title font-mono text-[9px] uppercase tracking-widest" data-original="[04] Пиковый долг">[04] Пиковый долг</span></div>
                    <div id="kpiMaxDebt" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#f4f1ea]">0 ₽</div>
                    <div class="font-mono text-[9px] opacity-60 mt-1.5">Максимум тела</div>
                </div>
                <div class="alche-block tilt-card p-5 col-span-2 sm:col-span-1" onmouseenter="scrambleTitle(this)">
                    <div class="flex justify-between items-center opacity-60 mb-1"><span class="metric-title font-mono text-[9px] uppercase tracking-widest" data-original="[05] Прибыль">[05] Прибыль</span></div>
                    <div id="kpiProfit" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#2a9d8f]">0 ₽</div>
                    <div id="kpiRoiSub" class="font-mono text-[9px] text-[#2a9d8f] mt-1.5 opacity-90">Рентабельность: 0%</div>
                </div>
            </div>

            <div class="alche-block px-5 py-2.5 flex items-center justify-between border-b">
                <div class="flex flex-wrap items-center gap-1.5" id="navTabsContainer">
                    <button type="button" onclick="selectTab(0)" class="tab-btn px-4 py-1.5 font-mono text-[10px] uppercase tracking-widest bg-[#d4af37] text-black font-bold transition shadow-md">[01] ОБСЛУЖИВАНИЕ КАПИТАЛА</button>
                    <button type="button" onclick="selectTab(1)" class="tab-btn px-4 py-1.5 font-mono text-[10px] uppercase tracking-widest opacity-70 hover:opacity-100 transition">[02] СКЛАДСКОЙ ЦИКЛ</button>
                    <button type="button" onclick="selectTab(2)" class="tab-btn px-4 py-1.5 font-mono text-[10px] uppercase tracking-widest opacity-70 hover:opacity-100 transition">[03] ДЕНЕЖНЫЙ ПОТОК</button>
                    <button type="button" onclick="selectTab(3)" class="tab-btn px-4 py-1.5 font-mono text-[10px] uppercase tracking-widest opacity-70 hover:opacity-100 transition">[04] ЭКОНОМИКА И ЗАКАЗЫ</button>
                </div>
            </div>

            <div class="flex-1 p-5 lg:p-7 space-y-6">
                <div id="viewTab0" class="tab-view-enter space-y-6">
                    <div class="alche-block p-5 border">
                        <div class="flex justify-between items-center mb-4">
                            <div>
                                <h3 class="font-serif text-xl font-bold tracking-wide italic">График обслуживания долга и начисления процентов</h3>
                                <p class="font-mono text-[10px] opacity-60">Ежемесячные проценты по совокупной ставке кредитора (столбцы) и динамика тела долга (кривая)</p>
                            </div>
                        </div>
                        <div class="h-[360px] relative"><canvas id="chartDebt"></canvas></div>
                    </div>
                    <div class="alche-block border overflow-x-auto">
                        <table class="w-full text-left font-mono text-[11px]">
                            <thead class="border-b" style="background-color: var(--table-header-bg);">
                                <tr class="text-[9px] uppercase tracking-widest text-[#d4af37]"><th class="p-3">Период</th><th class="p-3">Дотация (вход)</th><th class="p-3">Проценты</th><th class="p-3">Погашение долга</th><th class="p-3">Остаток долга</th><th class="p-3">Свободный остаток</th></tr>
                            </thead>
                            <tbody id="tableDebtBody" class="divide-y"></tbody>
                        </table>
                    </div>
                </div>

                <div id="viewTab1" class="hidden space-y-6">
                    <div class="alche-block p-5 border">
                        <div class="flex justify-between items-center mb-4">
                            <div>
                                <h3 class="font-serif text-xl font-bold tracking-wide italic">Партионные закупки и истощение склада</h3>
                                <p class="font-mono text-[10px] opacity-60">Закупка дискретными циклами с учетом предоплаты и отсрочки поставщика</p>
                            </div>
                        </div>
                        <div class="h-[400px] relative"><canvas id="chartStock"></canvas></div>
                    </div>
                </div>

                <div id="viewTab2" class="hidden space-y-6">
                    <div class="alche-block p-5 border">
                        <div class="flex justify-between items-center mb-4">
                            <div>
                                <h3 class="font-serif text-xl font-bold tracking-wide italic">Структура помесячного денежного потока</h3>
                                <p class="font-mono text-[10px] opacity-60">Сопоставление входящей выручки и совокупных выплат (закупки, аренда, ФОТ и налоги)</p>
                            </div>
                        </div>
                        <div class="h-[400px] relative"><canvas id="chartCF"></canvas></div>
                    </div>
                </div>

                <div id="viewTab3" class="hidden space-y-6">
                    <div class="grid grid-cols-1 xl:grid-cols-2 gap-6">
                        <div class="alche-block p-5 border">
                            <h3 class="font-serif text-xl font-bold tracking-wide italic mb-1">Динамика заказов и выручки</h3>
                            <p class="font-mono text-[10px] opacity-60 mb-4">Рост клиентской базы и масштабирование объемов отгрузок</p>
                            <div class="h-[320px] relative"><canvas id="chartOrders"></canvas></div>
                        </div>
                        <div class="alche-block p-5 border">
                            <h3 class="font-serif text-xl font-bold tracking-wide italic mb-1">Структура совокупных затрат</h3>
                            <p class="font-mono text-[10px] opacity-60 mb-4">Доли расходов с учетом себестоимости, инфраструктуры и процентов по долгу</p>
                            <div class="h-[320px] relative"><canvas id="chartPie"></canvas></div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
</div>

<script>
'use strict';

const REDUCE_MOTION = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ЗВУКОВОЙ ДВИЖОК — lazy init AudioContext */
let audioCtx = null;
function playClickSound(freq = 1200, duration = 0.02) {
    try {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        if (audioCtx.state === 'suspended') audioCtx.resume();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(320, audioCtx.currentTime + duration);
        gain.gain.setValueAtTime(0.035, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
    } catch (e) {}
}

/* DEBOUNCE runCalculation — ключевой фикс перф-а (слайдер) */
let _calcTimer = null;
function scheduleCalc(delay = 70) {
    if (_calcTimer) clearTimeout(_calcTimer);
    _calcTimer = setTimeout(() => { _calcTimer = null; runCalculation(); }, delay);
}

let preloaderDismissed = false;
function dismissPreloader() {
    if (preloaderDismissed) return;
    preloaderDismissed = true;
    const stage = document.getElementById('preloader-stage');
    const app = document.getElementById('mainDashboardApp');

    document.body.classList.remove('preloading');

    if (app) {
        app.classList.add('ready');
        void app.offsetWidth;
        app.classList.remove('opacity-0');
        app.classList.add('opacity-100');
    }

    // FIX: освобождаем WebGL-контекст прелоадера (лимит ~8-16 контекстов на браузер)
    setTimeout(() => {
        if (stage) stage.style.display = 'none';
        try {
            preScene.traverse(obj => {
                if (obj.geometry) obj.geometry.dispose();
                if (obj.material) {
                    if (Array.isArray(obj.material)) obj.material.forEach(m => m.dispose());
                    else obj.material.dispose();
                }
            });
            preRenderer.dispose();
            preRenderer.forceContextLoss();
            snapshotTarget.dispose();
        } catch (e) {}
    }, 600);
}

const PRELOADER_TOTAL_TIME = 9000;
const preloaderStartTime = performance.now();

setTimeout(() => {
    const pt = document.getElementById('preloaderTitle');
    if (pt) pt.classList.add('locked-on');
}, 900);

let drawingCompleted = false;
function updatePreloaderProgress(now) {
    if (preloaderDismissed) return;
    const elapsed = now - preloaderStartTime;
    const progress = Math.min(elapsed / PRELOADER_TOTAL_TIME, 1);

    const bar = document.getElementById('loaderProgressBar');
    const pct = document.getElementById('loaderPercent');
    if (bar) bar.style.width = `${(progress * 100).toFixed(0)}%`;
    if (pct) pct.textContent = `${Math.floor(progress * 100)}%`;

    if (progress >= 0.96 && !drawingCompleted) {
        drawingCompleted = true;
        const hud = document.getElementById('preloaderHUD');
        const btn = document.getElementById('exploreBtnWrapper');
        if (hud) hud.style.opacity = '0';
        if (btn) btn.classList.add('active');
    }

    if (progress < 1) requestAnimationFrame(updatePreloaderProgress);
}
requestAnimationFrame(updatePreloaderProgress);

/* =========================================================================
   THREE.JS ПРЕЛОАДЕР: ЦИКЛОПИЧЕСКИЕ КОЛЬЦА
   ========================================================================= */
const preCanvas = document.getElementById('preloader-webgl');
// FIX: preserveDrawingBuffer больше не нужен — снимаем из render target, а не с canvas
const preRenderer = new THREE.WebGLRenderer({ canvas: preCanvas, alpha: true, antialias: true });
preRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
preRenderer.setSize(window.innerWidth, window.innerHeight);

const preScene = new THREE.Scene();
const preCamera = new THREE.PerspectiveCamera(48, window.innerWidth / window.innerHeight, 1, 6000);

const baseCamZ = 390;
let targetCamPos = new THREE.Vector3(0, 0, baseCamZ);
let currentLookTarget = new THREE.Vector3(0, 0, 0);
let targetLookTarget = new THREE.Vector3(0, 0, 0);

preCamera.position.copy(targetCamPos);

const preGroup = new THREE.Group();
preScene.add(preGroup);

const megaRingWireMat = new THREE.MeshBasicMaterial({
    color: 0x00c3ff, wireframe: true, transparent: true, opacity: 0.38
});
const secondaryWireMat = new THREE.MeshBasicMaterial({
    color: 0x0077aa, wireframe: true, transparent: true, opacity: 0.22
});

function createCyclopeanTrussRing(mainRadius, tubeWidth, tubeDepth, segments) {
    const group = new THREE.Group();
    const coreMesh = new THREE.Mesh(
        new THREE.TorusGeometry(mainRadius, tubeWidth * 0.45, 12, segments),
        megaRingWireMat
    );
    group.add(coreMesh);

    const linePts = [];
    const rOuter = mainRadius + tubeWidth;
    const rInner = mainRadius - tubeWidth;
    const zOffset = tubeDepth;

    for (let i = 0; i < segments; i++) {
        const a1 = (i / segments) * Math.PI * 2;
        const a2 = ((i + 1) / segments) * Math.PI * 2;

        const p1_topOut = new THREE.Vector3(Math.cos(a1) * rOuter, Math.sin(a1) * rOuter, zOffset);
        const p2_topOut = new THREE.Vector3(Math.cos(a2) * rOuter, Math.sin(a2) * rOuter, zOffset);
        const p1_botOut = new THREE.Vector3(Math.cos(a1) * rOuter, Math.sin(a1) * rOuter, -zOffset);
        const p2_botOut = new THREE.Vector3(Math.cos(a2) * rOuter, Math.sin(a2) * rOuter, -zOffset);

        const p1_topIn = new THREE.Vector3(Math.cos(a1) * rInner, Math.sin(a1) * rInner, zOffset);
        const p2_topIn = new THREE.Vector3(Math.cos(a2) * rInner, Math.sin(a2) * rInner, zOffset);
        const p1_botIn = new THREE.Vector3(Math.cos(a1) * rInner, Math.sin(a1) * rInner, -zOffset);
        const p2_botIn = new THREE.Vector3(Math.cos(a2) * rInner, Math.sin(a2) * rInner, -zOffset);

        linePts.push(p1_topOut, p2_topOut, p1_botOut, p2_botOut);
        linePts.push(p1_topIn, p2_topIn, p1_botIn, p2_botIn);
        linePts.push(p1_topOut, p1_botOut, p1_topIn, p1_botIn);
        linePts.push(p1_topOut, p1_topIn, p1_botOut, p2_botIn);

        if (i % 2 === 0) {
            linePts.push(p1_topOut, p2_botOut);
            linePts.push(p1_topIn, p2_botIn);
            linePts.push(p1_topOut, p2_topIn);
        }

        if (i % 3 === 0) {
            const toothR = rOuter + tubeWidth * 0.42;
            const pTooth = new THREE.Vector3(Math.cos(a1) * toothR, Math.sin(a1) * toothR, 0);
            linePts.push(p1_topOut, pTooth, pTooth, p1_botOut);
        }
    }

    const trussMesh = new THREE.LineSegments(
        new THREE.BufferGeometry().setFromPoints(linePts),
        megaRingWireMat
    );
    group.add(trussMesh);

    const subMesh = new THREE.Mesh(
        new THREE.TorusGeometry(mainRadius - tubeWidth * 1.6, tubeWidth * 0.18, 8, Math.floor(segments * 0.75)),
        secondaryWireMat
    );
    group.add(subMesh);
    return group;
}

const astrolabeRings = [];
const aRing1 = createCyclopeanTrussRing(340, 18.0, 12.0, 180);
const aRing2 = createCyclopeanTrussRing(255, 14.0, 10.0, 150);
const aRing3 = createCyclopeanTrussRing(175, 11.0, 8.0, 130);

aRing2.rotation.x = Math.PI / 3.4;
aRing2.rotation.z = Math.PI / 6.0;
aRing3.rotation.y = Math.PI / 3.0;

preGroup.add(aRing1);
preGroup.add(aRing2);
preGroup.add(aRing3);

astrolabeRings.push(
    { group: aRing1, sx: 0.00045, sy: 0.00065, sz: 0.00025, px: 0.2, py: 1.1 },
    { group: aRing2, sx: -0.00055, sy: 0.00040, sz: -0.00045, px: 2.3, py: 0.7 },
    { group: aRing3, sx: 0.00060, sy: -0.00050, sz: 0.00035, px: 1.5, py: 3.2 }
);

function createBlueprintLineMaterial() {
    return new THREE.ShaderMaterial({
        uniforms: { uHover: { value: 0.0 }, uTime: { value: 0.0 } },
        vertexShader: `
            varying vec3 vPos;
            void main() { vPos = position; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }
        `,
        fragmentShader: `
            uniform float uHover; uniform float uTime; varying vec3 vPos;
            void main() {
                float wave = sin((vPos.x + vPos.y + vPos.z) * 0.2 - uTime * 3.5) * 0.5 + 0.5;
                vec3 baseGold = vec3(0.85, 0.71, 0.25);
                vec3 brightGlow = vec3(1.0, 0.96, 0.82);
                vec3 col = mix(baseGold, brightGlow, wave * 0.4 + uHover * 0.6);
                float alpha = clamp(0.70 + wave * 0.30 + uHover * 0.30, 0.0, 1.0);
                gl_FragColor = vec4(col, alpha);
            }
        `,
        transparent: true, depthWrite: false
    });
}

/* 3D-ЧЕРТЕЖИ */
function buildUltra3DAerialScrew() {
    const pts = [];
    const h = 70, radiusMax = 36;
    for (let i = 0; i < 6; i++) {
        const a1 = (i / 6) * Math.PI * 2, a2 = ((i + 1) / 6) * Math.PI * 2;
        const x1 = Math.cos(a1) * 4, z1 = Math.sin(a1) * 4;
        const x2 = Math.cos(a2) * 4, z2 = Math.sin(a2) * 4;
        pts.push(new THREE.Vector3(x1, -h/2, z1), new THREE.Vector3(x1, h/2, z1));
        for (let y = -h/2; y < h/2; y += 4) {
            pts.push(new THREE.Vector3(x1, y, z1), new THREE.Vector3(x2, y, z2));
            pts.push(new THREE.Vector3(x1, y, z1), new THREE.Vector3(x2, y + 4, z2));
        }
    }
    const coils = 3.2, steps = 160;
    for (let helix = 0; helix < 2; helix++) {
        const hOffset = helix * Math.PI;
        for (let i = 0; i < steps; i++) {
            const t1 = i / steps, t2 = (i + 1) / steps;
            const a1 = t1 * Math.PI * 2 * coils + hOffset;
            const a2 = t2 * Math.PI * 2 * coils + hOffset;
            const y1 = -h/2 + t1 * h, y2 = -h/2 + t2 * h;
            const r1 = 6 + t1 * (radiusMax - 6);
            const r2 = 6 + t2 * (radiusMax - 6);
            const pEdge1 = new THREE.Vector3(Math.cos(a1) * r1, y1, Math.sin(a1) * r1);
            const pEdge2 = new THREE.Vector3(Math.cos(a2) * r2, y2, Math.sin(a2) * r2);
            pts.push(pEdge1, pEdge2);
            if (i % 2 === 0) {
                const pCenter = new THREE.Vector3(Math.cos(a1) * 4, y1, Math.sin(a1) * 4);
                pts.push(pCenter, pEdge1);
                const pMid = new THREE.Vector3(Math.cos(a1 + 0.15) * (r1 * 0.6), y1 + 1.2, Math.sin(a1 + 0.15) * (r1 * 0.6));
                pts.push(pCenter, pMid, pMid, pEdge1);
            }
        }
    }
    for (let r = 16; r <= 38; r += 10) {
        for (let i = 0; i < 48; i++) {
            const a1 = (i / 48) * Math.PI * 2, a2 = ((i + 1) / 48) * Math.PI * 2;
            pts.push(new THREE.Vector3(Math.cos(a1)*r, -h/2, Math.sin(a1)*r), new THREE.Vector3(Math.cos(a2)*r, -h/2, Math.sin(a2)*r));
            if (r === 38 && i % 2 === 0) {
                pts.push(new THREE.Vector3(Math.cos(a1)*r, -h/2, Math.sin(a1)*r), new THREE.Vector3(Math.cos(a1)*(r+4), -h/2, Math.sin(a1)*(r+4)));
            }
        }
    }
    return new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(pts), createBlueprintLineMaterial());
}

function buildUltra3DClockworkGears() {
    const pts = [];
    function buildVolumetricGear(cx, cy, cz, radius, thickness, teeth, spokes) {
        const z1 = cz - thickness/2, z2 = cz + thickness/2;
        for (let i = 0; i < teeth * 2; i++) {
            const a1 = (i / (teeth * 2)) * Math.PI * 2;
            const a2 = ((i + 1) / (teeth * 2)) * Math.PI * 2;
            const r1 = (i % 2 === 0) ? radius + 3.0 : radius - 1.5;
            const r2 = ((i + 1) % 2 === 0) ? radius + 3.0 : radius - 1.5;
            const pF1 = new THREE.Vector3(cx + Math.cos(a1)*r1, cy + Math.sin(a1)*r1, z1);
            const pF2 = new THREE.Vector3(cx + Math.cos(a2)*r2, cy + Math.sin(a2)*r2, z1);
            const pB1 = new THREE.Vector3(cx + Math.cos(a1)*r1, cy + Math.sin(a1)*r1, z2);
            const pB2 = new THREE.Vector3(cx + Math.cos(a2)*r2, cy + Math.sin(a2)*r2, z2);
            pts.push(pF1, pF2, pB1, pB2, pF1, pB1);
        }
        for (let s = 0; s < spokes; s++) {
            const sa = (s / spokes) * Math.PI * 2;
            pts.push(new THREE.Vector3(cx, cy, z1), new THREE.Vector3(cx + Math.cos(sa)*radius, cy + Math.sin(sa)*radius, z1));
            pts.push(new THREE.Vector3(cx, cy, z2), new THREE.Vector3(cx + Math.cos(sa)*radius, cy + Math.sin(sa)*radius, z2));
            pts.push(new THREE.Vector3(cx + Math.cos(sa)*radius*0.5, cy + Math.sin(sa)*radius*0.5, z1),
                     new THREE.Vector3(cx + Math.cos(sa + 0.3)*radius*0.8, cy + Math.sin(sa + 0.3)*radius*0.8, z2));
        }
    }
    buildVolumetricGear(-16, 8, -6, 26, 6, 28, 6);
    buildVolumetricGear(18, -12, 6, 18, 5, 20, 5);
    buildVolumetricGear(16, 22, 0, 11, 4, 12, 4);
    for (let i = 0; i < 12; i++) {
        const a = (i / 12) * Math.PI * 2;
        pts.push(new THREE.Vector3(-16 + Math.cos(a)*3, 8 + Math.sin(a)*3, -24), new THREE.Vector3(-16 + Math.cos(a)*3, 8 + Math.sin(a)*3, 24));
        pts.push(new THREE.Vector3(18 + Math.cos(a)*2.5, -12 + Math.sin(a)*2.5, -20), new THREE.Vector3(18 + Math.cos(a)*2.5, -12 + Math.sin(a)*2.5, 20));
    }
    const b = 42;
    pts.push(new THREE.Vector3(-b, -b, 0), new THREE.Vector3(b, -b, 0));
    pts.push(new THREE.Vector3(b, -b, 0), new THREE.Vector3(b, b, 0));
    pts.push(new THREE.Vector3(b, b, 0), new THREE.Vector3(-b, b, 0));
    pts.push(new THREE.Vector3(-b, b, 0), new THREE.Vector3(-b, -b, 0));
    for (let c = -b; c <= b; c += 7) {
        pts.push(new THREE.Vector3(c, -b, 0), new THREE.Vector3(c, -b + 2, 0));
        pts.push(new THREE.Vector3(-b, c, 0), new THREE.Vector3(-b + 2, c, 0));
    }
    return new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(pts), createBlueprintLineMaterial());
}

function buildUltra3DOrnithopter() {
    const pts = [];
    const ribCount = 14;
    const sparTop = [], sparBot = [];
    for (let i = 0; i <= 36; i++) {
        const t = i / 36;
        const x = -44 + t * 88;
        const yT = Math.sin(t * Math.PI) * 20 - 6;
        const zT = -Math.cos(t * Math.PI) * 12;
        sparTop.push(new THREE.Vector3(x, yT, zT));
        sparBot.push(new THREE.Vector3(x, yT - 3.5, zT + 2));
    }
    for (let i = 0; i < sparTop.length - 1; i++) {
        pts.push(sparTop[i], sparTop[i+1], sparBot[i], sparBot[i+1], sparTop[i], sparBot[i], sparTop[i], sparBot[i+1]);
    }
    for (let r = 0; r < ribCount; r++) {
        const t = r / (ribCount - 1);
        const idx = Math.floor(t * (sparTop.length - 1));
        const rootT = sparTop[idx];
        const chordLen = 34 - Math.abs(t - 0.5) * 22;
        let prevUpper = null, prevLower = null;
        for (let s = 0; s <= 6; s++) {
            const st = s / 6;
            const ribUpper = new THREE.Vector3(rootT.x + (t - 0.5) * st * 10, rootT.y - st * chordLen, rootT.z + Math.sin(st * Math.PI) * 7);
            const ribLower = new THREE.Vector3(rootT.x + (t - 0.5) * st * 10, rootT.y - st * chordLen - 2.5 * (1.0 - st), rootT.z + Math.sin(st * Math.PI) * 3);
            if (prevUpper) pts.push(prevUpper, ribUpper, prevLower, ribLower, ribUpper, ribLower);
            prevUpper = ribUpper; prevLower = ribLower;
            if (s === 6) {
                pts.push(rootT, ribUpper, new THREE.Vector3(0, -28, 14), ribUpper, new THREE.Vector3(0, -28, -14), ribLower);
            }
        }
    }
    pts.push(new THREE.Vector3(0, 0, -12), new THREE.Vector3(0, -32, 0));
    pts.push(new THREE.Vector3(0, 0, 12), new THREE.Vector3(0, -32, 0));
    pts.push(new THREE.Vector3(-14, -28, 0), new THREE.Vector3(14, -28, 0));
    return new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(pts), createBlueprintLineMaterial());
}

function buildUltra3
