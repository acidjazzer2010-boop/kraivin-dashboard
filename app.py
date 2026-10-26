import streamlit as st

st.set_page_config(
    page_title="Архитектура Капитала // Финансовое Моделирование",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      #MainMenu, header, footer, .stDeployButton {
          visibility: hidden !important;
          display: none !important;
      }

      .block-container {
          padding: 0 !important;
          max-width: 100% !important;
          margin: 0 !important;
      }

      section.main {
          background-color: #070709 !important;
          padding: 0 !important;
      }

      body {
          overflow-x: hidden !important;
      }

      iframe[title="st.iframe"] {
          border: none !important;
          width: 100% !important;
          min-height: 100dvh !important;
          display: block !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

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
                gold: '#d4af37',
                vermilion: '#e63946',
                jade: '#2a9d8f',
            }
        }
    }
}
</script>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

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

* {
    box-sizing: border-box;
    border-color: var(--border-line);
}

html, body {
    width: 100%;
    min-height: 100%;
    margin: 0;
    padding: 0;
    overflow-x: hidden;
    background-color: var(--bg-space);
    color: var(--text-main);
    font-family: 'JetBrains Mono', monospace;
}

body {
    overflow-y: auto;
}

.film-grain {
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 999;
    opacity: var(--grain-opacity);
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
}

#preloader-stage {
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100dvh;
    background: radial-gradient(circle at center, #0a0b12 0%, #030306 100%);
    z-index: 900;
    overflow: hidden;
}

#preloader-webgl {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    z-index: 10;
    cursor: grab;
}

#preloader-webgl:active {
    cursor: grabbing;
}

.preloader-fixed-hud {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    z-index: 30;
    pointer-events: none;
    user-select: none;
}

#preloaderTitle {
    position: absolute;
    top: 48px;
    left: 50%;
    transform: translateX(-50%);
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-style: italic;
    font-size: clamp(28px, 3.5vw, 46px);
    font-weight: 700;
    letter-spacing: 0.28em;
    color: var(--accent-gold);
    opacity: 0;
    text-shadow: 0 0 45px rgba(212, 175, 55, 0.85);
    transition: opacity 1.8s cubic-bezier(0.16, 1, 0.3, 1);
    text-align: center;
    white-space: nowrap;
}

#preloaderTitle.locked-on {
    opacity: 1 !important;
}

.bottom-dock {
    position: absolute;
    bottom: 44px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: min(340px, 90vw);
    height: 56px;
}

#preloaderHUD {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    transition: opacity 0.4s ease;
}

.progress-bar-bg {
    width: min(280px, 80vw);
    height: 2px;
    background: rgba(255, 255, 255, 0.12);
    position: relative;
    overflow: hidden;
}

#loaderProgressBar {
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    width: 0%;
    background: var(--accent-gold);
    box-shadow: 0 0 10px var(--accent-gold);
    transition: width 0.1s linear;
}

#exploreBtnWrapper {
    position: absolute;
    opacity: 0;
    pointer-events: none;
    transition:
        opacity 0.6s cubic-bezier(0.19, 1, 0.22, 1),
        transform 0.6s cubic-bezier(0.19, 1, 0.22, 1);
    transform: translateY(8px);
}

#exploreBtnWrapper.active {
    opacity: 1;
    pointer-events: auto;
    transform: translateY(0);
}

.explore-btn {
    padding: 13px 46px;
    background: rgba(13, 13, 18, 0.9);
    border: 1px solid rgba(212, 175, 55, 0.95);
    color: #f4f1ea;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.38em;
    text-transform: uppercase;
    cursor: pointer;
    backdrop-filter: blur(14px);
    overflow: hidden;
    transition: all 0.3s ease;
    box-shadow:
        0 0 40px rgba(212, 175, 55, 0.35),
        inset 0 0 16px rgba(212, 175, 55, 0.18);
}

.explore-btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.45), transparent);
    transition: left 0.7s ease;
}

.explore-btn:hover {
    border-color: #ffd700;
    color: #ffd700;
    box-shadow:
        0 0 60px rgba(212, 175, 55, 0.7),
        inset 0 0 24px rgba(212, 175, 55, 0.35);
    transform: scale(1.05);
}

.explore-btn:hover::before {
    left: 100%;
}

#mainDashboardApp {
    display: none;
    position: relative;
    z-index: 10;
    min-height: 100dvh;
}

#mainDashboardApp.ready {
    display: flex;
}

#webgl-bg-canvas {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100dvh;
    z-index: 0;
    pointer-events: none;
    opacity: 0.35;
}

html:not(.dark) #webgl-bg-canvas {
    opacity: 0.18;
}

.alche-block {
    position: relative;
    background: var(--bg-panel);
    backdrop-filter: blur(20px);
    border-right: 1px solid var(--border-line);
    border-bottom: 1px solid var(--border-line);
}

.cross-tl::before {
    content: '+';
    position: absolute;
    top: -6px;
    left: -4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    line-height: 1;
    color: var(--accent-gold);
    pointer-events: none;
    z-index: 10;
}

.cross-br::after {
    content: '+';
    position: absolute;
    bottom: -6px;
    right: -4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    line-height: 1;
    color: var(--accent-gold);
    pointer-events: none;
    z-index: 10;
}

.tilt-card {
    position: relative;
    overflow: hidden;
    transform-style: preserve-3d;
    perspective: 1000px;
    transition:
        transform 0.25s cubic-bezier(0.2, 0, 0.2, 1),
        border-color 0.3s ease;
}

.tilt-card::before {
    content: '';
    position: absolute;
    inset: -1px;
    border: 1px solid transparent;
    background: radial-gradient(
        350px circle at var(--mouse-x, 0px) var(--mouse-y, 0px),
        var(--cursor-glow),
        transparent 75%
    );
    opacity: 0;
    transition: opacity 0.4s ease;
    pointer-events: none;
    z-index: 2;
}

.tilt-card:hover::before {
    opacity: 1;
}

.tab-view-enter {
    animation: tabEntrance 0.6s cubic-bezier(0.19, 1, 0.22, 1) forwards;
}

@keyframes tabEntrance {
    0% {
        opacity: 0;
        filter: blur(8px);
        transform: translateY(8px);
    }
    100% {
        opacity: 1;
        filter: blur(0);
        transform: translateY(0);
    }
}

input[type="range"] {
    -webkit-appearance: none;
    appearance: none;
    width: 100%;
    height: 2px;
    background: var(--border-line);
    outline: none;
}

input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 12px;
    height: 12px;
    background: var(--accent-gold);
    cursor: pointer;
    border: 1px solid var(--bg-space);
    transform: rotate(45deg);
    transition: transform 0.2s ease;
}

input[type="range"]::-webkit-slider-thumb:hover {
    transform: rotate(45deg) scale(1.4);
}

.mono-input {
    background: var(--input-bg);
    border: 1px solid var(--border-line);
    color: var(--text-main);
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    padding: 6px 9px;
    width: 100%;
    border-radius: 0;
    outline: none;
    transition: border-color 0.2s ease;
}

.mono-input:focus {
    border-color: var(--accent-gold);
    background: rgba(212, 175, 55, 0.06);
}

select.mono-input option {
    background-color: #0d0d12;
    color: #f4f1ea;
}

.hw-slider-track {
    position: relative;
    width: 130px;
    height: 28px;
    border: 1px solid var(--border-line);
    background: var(--input-bg);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 10px;
    cursor: pointer;
    user-select: none;
}

.hw-slider-thumb {
    position: absolute;
    top: 2px;
    bottom: 2px;
    width: 62px;
    background: var(--accent-gold);
    transition: transform 0.45s cubic-bezier(0.19, 1, 0.22, 1);
}

.pulse-dot {
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 9999px;
    background-color: var(--accent-gold);
    animation: pulseAnim 2s infinite ease-in-out;
}

@keyframes pulseAnim {
    0%, 100% {
        opacity: 0.4;
        transform: scale(0.9);
    }
    50% {
        opacity: 1;
        transform: scale(1.2);
    }
}

.table-scroll {
    width: 100%;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}

.table-scroll table {
    min-width: 900px;
    width: 100%;
}

::-webkit-scrollbar {
    width: 4px;
    height: 4px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: var(--border-line);
}

::-webkit-scrollbar-thumb:hover {
    background: var(--accent-gold);
}
</style>
</head>
<body class="selection:bg-[#d4af37] selection:text-black">
<div class="film-grain"></div>

<div id="preloader-stage">
    <canvas id="preloader-webgl"></canvas>

    <div class="preloader-fixed-hud">
        <div id="preloaderTitle">Архитектура финансов</div>

        <div class="bottom-dock">
            <div id="preloaderHUD">
                <div class="flex items-center gap-3 text-[#d4af37] text-[10px] tracking-[0.25em] uppercase font-mono">
                    <span class="pulse-dot"></span>
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
                <svg class="w-7 h-7 text-[#d4af37]" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.2">
                    <circle cx="16" cy="16" r="14" />
                    <rect x="6" y="6" width="20" height="20" />
                    <polygon points="16,2 30,26 2,26" stroke-width="0.8" stroke-dasharray="1 1"/>
                    <line x1="2" y1="16" x2="30" y2="16" stroke-dasharray="2 2"/>
                    <line x1="16" y1="2" x2="16" y2="30" stroke-dasharray="2 2"/>
                </svg>
                <div>
                    <div class="font-mono text-[9px] uppercase tracking-[0.25em] text-[#d4af37] opacity-80">
                        AUREA PROPORTIO // 1 : 1.618
                    </div>
                    <div class="font-serif italic text-lg lg:text-xl font-bold tracking-wide leading-none">
                        Архитектура Капитала и Ликвидности
                    </div>
                </div>
            </div>

            <div class="hidden xl:flex items-center gap-5 pl-5 border-l font-mono text-[10px] opacity-75">
                <span>[НАЛОГОВЫЙ КОДЕКС: 22% НДС]</span>
                <span id="telemetryRate">[КАПИТАЛ: 16.0% ГОДОВЫХ]</span>
                <span id="cursorCoordDisplay" class="text-[#d4af37]">X: 0000 / Y: 0000</span>
                <span id="telemetryClock">[15:00:00]</span>
            </div>
        </div>

        <div class="flex items-center gap-4">
            <button
                id="downloadReportBtn"
                onclick="exportDataToCsv()"
                type="button"
                class="px-3.5 py-1.5 border font-mono text-[10px] uppercase tracking-widest hover:border-[#d4af37] hover:bg-[#d4af37]/10 transition flex items-center gap-2"
            >
                <span>↓ Скачать отчет</span>
            </button>

            <div
                id="themeSlider"
                class="hw-slider-track"
                onclick="toggleTheme()"
                title="Переключить режим: Ночь / День"
            >
                <div id="sliderThumb" class="hw-slider-thumb" style="transform: translateX(0px);"></div>
                <span id="lblNight" class="relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold text-black">Ночь</span>
                <span id="lblDay" class="relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold opacity-70">День</span>
            </div>
        </div>
    </header>

    <div class="flex-1 grid grid-cols-1 lg:grid-cols-12">
        <aside class="lg:col-span-3 flex flex-col border-r">
            <div class="alche-block cross-tl px-5 py-3.5 flex items-center justify-between">
                <span class="font-mono text-[10px] uppercase tracking-[0.2em] text-[#d4af37] font-bold">
                    [00] Параметры Модели
                </span>
                <button
                    id="defaultResetBtn"
                    type="button"
                    onclick="resetDefaults()"
                    class="font-mono text-[9px] uppercase underline opacity-60 hover:opacity-100 transition"
                >
                    Сброс
                </button>
            </div>

            <form id="financialInputsForm" class="flex-1 flex flex-col" onsubmit="event.preventDefault();">
                <div class="alche-block p-5 space-y-4">
                    <div class="flex justify-between items-baseline">
                        <span class="font-serif italic text-base font-semibold">I. Временной горизонт и маржа</span>
                        <span class="font-mono text-[9px] opacity-40">01 // 04</span>
                    </div>

                    <div class="grid grid-cols-2 gap-2.5">
                        <div>
                            <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Месяц старта</label>
                            <select id="paramStartMonth" class="mono-input" onchange="playClickSound(); runCalculationDebounced();">
                                <option value="0">Январь</option>
                                <option value="1">Февраль</option>
                                <option value="2">Март</option>
                                <option value="3">Апрель</option>
                                <option value="4">Май</option>
                                <option value="5">Июнь</option>
                                <option value="6">Июль</option>
                                <option value="7">Август</option>
                                <option value="8">Сентябрь</option>
                                <option value="9" selected>Октябрь</option>
                                <option value="10">Ноябрь</option>
                                <option value="11">Декабрь</option>
                            </select>
                        </div>

                        <div>
                            <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Год старта</label>
                            <select id="paramStartYear" class="mono-input" onchange="playClickSound(); runCalculationDebounced();">
                                <option value="2026" selected>2026</option>
                                <option value="2027">2027</option>
                            </select>
                        </div>
                    </div>

                    <div class="grid grid-cols-2 gap-2.5">
                        <div>
                            <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Горизонт</label>
                            <select id="paramPeriod" class="mono-input" onchange="playClickSound(); runCalculationDebounced();">
                                <option value="6">6 месяцев</option>
                                <option value="12" selected>12 месяцев</option>
                                <option value="18">18 месяцев</option>
                                <option value="24">24 месяца</option>
                            </select>
                        </div>

                        <div>
                            <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Ставка НДС</label>
                            <select id="paramVatRate" class="mono-input" onchange="playClickSound(); runCalculationDebounced();">
                                <option value="22" selected>22%</option>
                                <option value="20">20%</option>
                                <option value="10">10%</option>
                                <option value="0">0%</option>
                            </select>
                        </div>
                    </div>

                    <div>
                        <div class="flex justify-between font-mono text-[10px] mb-1">
                            <span class="opacity-70">МАРЖИНАЛЬНОСТЬ ПРОДАЖ</span>
                            <span id="lblMarginVal" class="text-[#d4af37] font-bold">20%</span>
                        </div>
                        <input
                            type="range"
                            id="paramMargin"
                            min="10"
                            max="50"
                            step="1"
                            value="20"
                            oninput="runCalculationDebounced()"
                        >
                    </div>
                </div>

                <div class="alche-block p-5 space-y-4">
                    <div class="flex justify-between items-baseline">
                        <span class="font-serif italic text-base font-semibold">II. Партионный склад и кредитование</span>
                        <span class="font-mono text-[9px] opacity-40">02 // 04</span>
                    </div>

                    <div>
                        <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Стартовая закупка партии, ₽</label>
                        <input
                            type="text"
                            id="paramInitialPurchase"
                            value="25 000 000"
                            class="mono-input font-bold"
                            oninput="formatInput(this); runCalculationDebounced();"
                        >
                    </div>

                    <div class="grid grid-cols-3 gap-2">
                        <div>
                            <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Цикл, мес.</label>
                            <input
                                type="number"
                                id="paramBatchCycle"
                                value="5"
                                min="1"
                                max="12"
                                class="mono-input text-center"
                                oninput="runCalculationDebounced()"
                            >
                        </div>

                        <div>
                            <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">ЦБ РФ, %</label>
                            <input
                                type="number"
                                id="paramCbRate"
                                value="14.0"
                                step="0.5"
                                class="mono-input text-center font-bold text-[#d4af37]"
                                oninput="runCalculationDebounced()"
                            >
                        </div>

                        <div>
                            <label class="block font-mono text-[8px] uppercase opacity-70 mb-1" title="Коммерческая наценка кредитора">
                                Комиссия, %
                            </label>
                            <input
                                type="number"
                                id="paramCommMargin"
                                value="2.0"
                                step="0.5"
                                class="mono-input text-center"
                                oninput="runCalculationDebounced()"
                            >
                        </div>
                    </div>

                    <div
                        class="p-3 border space-y-3"
                        style="border-color: rgba(212, 175, 55, 0.25); background: rgba(212, 175, 55, 0.02);"
                    >
                        <div class="font-mono text-[8px] uppercase tracking-widest text-[#d4af37] font-bold">
                            [УСЛОВИЯ ПОСТАВЩИКА]
                        </div>

                        <div>
                            <div class="flex justify-between font-mono text-[9px] mb-1">
                                <span class="opacity-70">ПРЕДОПЛАТА ПОСТАВЩИКУ</span>
                                <span id="lblSupplierPrepVal" class="text-[#d4af37] font-bold">50%</span>
                            </div>
                            <input
                                type="range"
                                id="paramSupplierPrepay"
                                min="0"
                                max="100"
                                step="10"
                                value="50"
                                oninput="runCalculationDebounced()"
                            >
                        </div>

                        <div>
                            <div class="flex justify-between font-mono text-[9px] mb-1">
                                <span class="opacity-70">ОТСРОЧКА ОСТАТКА</span>
                                <span id="lblSupplierDelayVal" class="text-[#d4af37] font-bold">1 мес.</span>
                            </div>
                            <input
                                type="range"
                                id="paramSupplierDelay"
                                min="0"
                                max="6"
                                step="1"
                                value="1"
                                oninput="runCalculationDebounced()"
                            >
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
                            <input
                                type="text"
                                id="paramAov"
                                value="150 000"
                                class="mono-input font-bold"
                                oninput="formatInput(this); runCalculationDebounced();"
                            >
                        </div>

                        <div>
                            <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Заказов в 1-й мес.</label>
                            <input
                                type="number"
                                id="paramStartOrders"
                                value="40"
                                min="1"
                                max="2000"
                                class="mono-input text-center font-bold"
                                oninput="runCalculationDebounced()"
                            >
                        </div>
                    </div>

                    <div>
                        <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Логика прироста</label>
                        <div class="grid grid-cols-2 border">
                            <button
                                type="button"
                                id="btnModeAbs"
                                onclick="setGrowthMode('abs')"
                                class="py-1 font-mono text-[9px] uppercase tracking-wider bg-[#d4af37] text-black font-bold transition"
                            >
                                В штуках
                            </button>
                            <button
                                type="button"
                                id="btnModePct"
                                onclick="setGrowthMode('pct')"
                                class="py-1 font-mono text-[9px] uppercase tracking-wider opacity-60 hover:opacity-100 transition"
                            >
                                В процентах
                            </button>
                        </div>
                    </div>

                    <div>
                        <div class="flex justify-between font-mono text-[10px] mb-1">
                            <span id="lblGrowthModeTitle" class="opacity-70">ПРИРОСТ В МЕСЯЦ</span>
                            <span id="lblGrowthVal" class="text-[#d4af37] font-bold">+5 шт.</span>
                        </div>
                        <input
                            type="range"
                            id="paramGrowthSlider"
                            min="0"
                            max="100"
                            step="1"
                            value="5"
                            oninput="runCalculationDebounced()"
                        >
                    </div>

                    <div>
                        <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">
                            Потолок продаж в месяц, шт.
                        </label>
                        <input
                            type="number"
                            id="paramMaxOrdersCap"
                            value="300"
                            min="10"
                            step="10"
                            class="mono-input text-center"
                            oninput="runCalculationDebounced()"
                        >
                    </div>
                </div>

                <div class="alche-block p-5 space-y-4 flex-1">
                    <div class="flex justify-between items-baseline">
                        <span class="font-serif italic text-base font-semibold">IV. Постоянные затраты и факторинг</span>
                        <span class="font-mono text-[9px] opacity-40">04 // 04</span>
                    </div>

                    <div class="grid grid-cols-3 gap-2">
                        <div>
                            <label class="block font-mono text-[8px] uppercase opacity-70 mb-1">ФОТ, ₽</label>
                            <input
                                type="text"
                                id="paramFot"
                                value="500 000"
                                class="mono-input"
                                oninput="formatInput(this); runCalculationDebounced();"
                            >
                        </div>

                        <div>
                            <label class="block font-mono text-[8px] uppercase opacity-70 mb-1">Склад, ₽</label>
                            <input
                                type="text"
                                id="paramWh"
                                value="200 000"
                                class="mono-input"
                                oninput="formatInput(this); runCalculationDebounced();"
                            >
                        </div>

                        <div>
                            <label class="block font-mono text-[8px] uppercase opacity-70 mb-1">Офис, ₽</label>
                            <input
                                type="text"
                                id="paramOffice"
                                value="150 000"
                                class="mono-input"
                                oninput="formatInput(this); runCalculationDebounced();"
                            >
                        </div>
                    </div>

                    <div class="pt-1">
                        <div class="flex justify-between font-mono text-[9px] mb-1">
                            <span class="opacity-70">ДОЛЯ ФАКТОРИНГА В ВЫРУЧКЕ</span>
                            <span id="lblFactShareVal" class="text-[#d4af37] font-bold">50%</span>
                        </div>
                        <input
                            type="range"
                            id="paramFactoringShare"
                            min="0"
                            max="100"
                            step="10"
                            value="50"
                            oninput="runCalculationDebounced()"
                        >
                    </div>
                </div>
            </form>
        </aside>

        <section class="lg:col-span-9 flex flex-col">
            <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 border-b">
                <div class="alche-block tilt-card p-5" onmouseenter="scrambleTitle(this)">
                    <div class="flex justify-between items-center opacity-60 mb-1">
                        <span class="metric-title font-mono text-[9px] uppercase tracking-widest" data-original="[01] Выручка">[01] Выручка</span>
                    </div>
                    <div id="kpiRev" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#f4f1ea]">0 ₽</div>
                    <div id="kpiRevSub" class="font-mono text-[9px] text-[#d4af37] mt-1.5 opacity-90">Маржа: 20%</div>
                </div>

                <div class="alche-block tilt-card p-5" onmouseenter="scrambleTitle(this)">
                    <div class="flex justify-between items-center opacity-60 mb-1">
                        <span class="metric-title font-mono text-[9px] uppercase tracking-widest" data-original="[02] Дефицит">[02] Дефицит</span>
                    </div>
                    <div id="kpiInjections" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#e63946]">0 ₽</div>
                    <div class="font-mono text-[9px] text-[#e63946] mt-1.5 opacity-90">Внешние дотации</div>
                </div>

                <div class="alche-block tilt-card p-5" onmouseenter="scrambleTitle(this)">
                    <div class="flex justify-between items-center opacity-60 mb-1">
                        <span class="metric-title font-mono text-[9px] uppercase tracking-widest" data-original="[03] Проценты">[03] Проценты</span>
                    </div>
                    <div id="kpiInterest" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#d4af37]">0 ₽</div>
                    <div id="kpiRateSub" class="font-mono text-[9px] text-[#d4af37] mt-1.5 opacity-90">Ставка 16.0%</div>
                </div>

                <div class="alche-block tilt-card p-5" onmouseenter="scrambleTitle(this)">
                    <div class="flex justify-between items-center opacity-60 mb-1">
                        <span class="metric-title font-mono text-[9px] uppercase tracking-widest" data-original="[04] Пиковый долг">[04] Пиковый долг</span>
                    </div>
                    <div id="kpiMaxDebt" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#f4f1ea]">0 ₽</div>
                    <div class="font-mono text-[9px] opacity-60 mt-1.5">Максимум тела</div>
                </div>

                <div class="alche-block tilt-card p-5 col-span-2 sm:col-span-1" onmouseenter="scrambleTitle(this)">
                    <div class="flex justify-between items-center opacity-60 mb-1">
                        <span class="metric-title font-mono text-[9px] uppercase tracking-widest" data-original="[05] Прибыль">[05] Прибыль</span>
                    </div>
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

                    <div class="alche-block border table-scroll">
                        <table class="w-full text-left font-mono text-[11px]">
                            <thead class="border-b" style="background-color: var(--table-header-bg);">
                                <tr class="text-[9px] uppercase tracking-widest text-[#d4af37]">
                                    <th class="p-3">Период</th>
                                    <th class="p-3">Дотация (вход)</th>
                                    <th class="p-3">Проценты</th>
                                    <th class="p-3">Погашение долга</th>
                                    <th class="p-3">Остаток долга</th>
                                    <th class="p-3">Свободный остаток</th>
                                </tr>
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
/* ============================ УТИЛИТЫ ============================ */

function debounce(fn, delay = 140) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => fn.apply(this, args), delay);
    };
}

function parseCleanNum(value, fallback = 0) {
    if (value === null || value === undefined) return fallback;

    const normalized = String(value)
        .replace(/\u00a0/g, '')
        .replace(/\s/g, '')
        .replace(/,/g, '.')
        .trim();

    const parsed = Number(normalized);
    return Number.isFinite(parsed) ? parsed : fallback;
}

function safeNumber(value, fallback = 0) {
    return Number.isFinite(value) ? value : fallback;
}

function formatSpaced(num) {
    return Math.round(safeNumber(num)).toLocaleString('ru-RU').replace(/,/g, ' ');
}

function formatInput(input) {
    input.value = formatSpaced(parseCleanNum(input.value));
}

/* ============================ ЗВУК ============================ */

const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

function playClickSound(freq = 1200, duration = 0.02) {
    try {
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
    } catch (error) {}
}

/* ======================== ПРЕЛОАДЕР ======================== */

let preloaderDismissed = false;

function dismissPreloader() {
    if (preloaderDismissed) return;
    preloaderDismissed = true;

    const stage = document.getElementById('preloader-stage');
    const app = document.getElementById('mainDashboardApp');

    document.documentElement.style.overflow = 'auto';
    document.body.style.overflow = 'auto';

    if (app) {
        app.classList.add('ready');
        void app.offsetWidth;
        app.classList.remove('opacity-0');
        app.classList.add('opacity-100');
    }

    setTimeout(() => {
        if (stage) stage.style.display = 'none';
    }, 600);
}

const PRELOADER_TOTAL_TIME = 9000;
const preloaderStartTime = performance.now();

setTimeout(() => {
    const title = document.getElementById('preloaderTitle');
    if (title) title.classList.add('locked-on');
}, 900);

let drawingCompleted = false;

function updatePreloaderProgress(now) {
    if (preloaderDismissed) return;

    const elapsed = now - preloaderStartTime;
    const progress = Math.min(elapsed / PRELOADER_TOTAL_TIME, 1);

    const bar = document.getElementById('loaderProgressBar');
    const percent = document.getElementById('loaderPercent');

    if (bar) bar.style.width = `${(progress * 100).toFixed(0)}%`;
    if (percent) percent.textContent = `${Math.floor(progress * 100)}%`;

    if (progress >= 0.96 && !drawingCompleted) {
        drawingCompleted = true;

        const hud = document.getElementById('preloaderHUD');
        const button = document.getElementById('exploreBtnWrapper');

        if (hud) hud.style.opacity = '0';
        if (button) button.classList.add('active');
    }

    if (progress < 1) requestAnimationFrame(updatePreloaderProgress);
}

requestAnimationFrame(updatePreloaderProgress);

/* =========================================================================
   ВАШ THREE.JS ПРЕЛОАДЕР
   Вставьте сюда весь ваш существующий код:
   от const preCanvas = document.getElementById('preloader-webgl');
   до конца функции animatePreloader() и её первого вызова.
   ========================================================================= */

/* >>> НАЧАЛО ВАШЕГО СУЩЕСТВУЮЩЕГО THREE.JS ПРЕЛОАДЕРА <<< */

/* <<< КОНЕЦ ВАШЕГО СУЩЕСТВУЮЩЕГО THREE.JS ПРЕЛОАДЕРА >>> */

/* ===================== ФОНОВЫЙ THREE.JS ===================== */

const dashCanvas = document.getElementById('webgl-bg-canvas');
const dashScene = new THREE.Scene();
const dashCamera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 2000);
dashCamera.position.z = 160;

const dashRenderer = new THREE.WebGLRenderer({
    canvas: dashCanvas,
    alpha: true,
    antialias: false,
    powerPreference: 'low-power'
});

dashRenderer.setSize(window.innerWidth, window.innerHeight);
dashRenderer.setPixelRatio(1);

const dashArmillary = new THREE.Group();
dashScene.add(dashArmillary);

let ringColor = 0x00aaff;
const dashRingMat = new THREE.MeshBasicMaterial({
    color: ringColor,
    wireframe: true,
    transparent: true,
    opacity: 0.15
});

const dashRings = [];

[65, 88, 110].forEach((radius, i) => {
    const geometry = new THREE.TorusGeometry(radius, 8 - i * 2, 14, 100);
    const ring = new THREE.Mesh(geometry, dashRingMat);

    if (i === 0) ring.rotation.x = Math.PI / 2;
    if (i === 1) ring.rotation.y = Math.PI / 3;
    if (i === 2) ring.rotation.z = Math.PI / 4;

    dashArmillary.add(ring);
    dashRings.push(ring);
});

dashRenderer.render(dashScene, dashCamera);

let dashTurnProgress = 1.0;
let dashStartRot = [0, 0, 0];
let dashTargetRot = [0, 0, 0];
let dashAnimFrameId = null;

function triggerDashRingTurn() {
    dashStartRot = [
        dashRings[0].rotation.y,
        dashRings[1].rotation.x,
        dashRings[2].rotation.z
    ];

    dashTargetRot = [
        dashStartRot[0] + Math.PI / 2.618,
        dashStartRot[1] - Math.PI / 3.141,
        dashStartRot[2] + Math.PI / 4.0
    ];

    dashTurnProgress = 0.0;

    if (dashAnimFrameId) cancelAnimationFrame(dashAnimFrameId);
    animateDashTurn();
}

function animateDashTurn() {
    dashTurnProgress += 0.025;
    const p = Math.min(dashTurnProgress, 1.0);
    const ease = p < 0.5
        ? 4 * p * p * p
        : 1 - Math.pow(-2 * p + 2, 3) / 2;

    dashRings[0].rotation.y = dashStartRot[0] + (dashTargetRot[0] - dashStartRot[0]) * ease;
    dashRings[1].rotation.x = dashStartRot[1] + (dashTargetRot[1] - dashStartRot[1]) * ease;
    dashRings[2].rotation.z = dashStartRot[2] + (dashTargetRot[2] - dashStartRot[2]) * ease;

    dashRenderer.render(dashScene, dashCamera);

    if (p < 1.0) {
        dashAnimFrameId = requestAnimationFrame(animateDashTurn);
    } else {
        dashAnimFrameId = null;
    }
}

document.addEventListener('mousemove', (event) => {
    const coord = document.getElementById('cursorCoordDisplay');
    if (coord) {
        coord.textContent = `X: ${String(event.clientX).padStart(4, '0')} / Y: ${String(event.clientY).padStart(4, '0')}`;
    }
});

document.querySelectorAll('.tilt-card').forEach((card) => {
    card.addEventListener('mousemove', (event) => {
        const rect = card.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        card.style.setProperty('--mouse-x', `${x}px`);
        card.style.setProperty('--mouse-y', `${y}px`);

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = ((y - centerY) / centerY) * -6;
        const rotateY = ((x - centerX) / centerX) * 6;

        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-3px)`;
    });

    card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)';
    });
});

window.addEventListener('resize', () => {
    if (typeof preCamera !== 'undefined' && typeof preRenderer !== 'undefined') {
        preCamera.aspect = window.innerWidth / window.innerHeight;
        preCamera.updateProjectionMatrix();
        preRenderer.setSize(window.innerWidth, window.innerHeight);
    }

    dashCamera.aspect = window.innerWidth / window.innerHeight;
    dashCamera.updateProjectionMatrix();
    dashRenderer.setSize(window.innerWidth, window.innerHeight);
    dashRenderer.render(dashScene, dashCamera);
});

/* ========================== ТЕМА ========================== */

let isDark = true;

function toggleTheme() {
    isDark = !isDark;
    document.documentElement.classList.toggle('dark', isDark);

    const thumb = document.getElementById('sliderThumb');
    const lblNight = document.getElementById('lblNight');
    const lblDay = document.getElementById('lblDay');

    if (isDark) {
        thumb.style.transform = 'translateX(0px)';
        lblNight.className = 'relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold text-black';
        lblDay.className = 'relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold opacity-70';

        dashRingMat.color.setHex(0x00aaff);
        if (typeof megaRingWireMat !== 'undefined') megaRingWireMat.color.setHex(0x00c3ff);
        if (typeof secondaryWireMat !== 'undefined') secondaryWireMat.color.setHex(0x0077aa);
    } else {
        thumb.style.transform = 'translateX(58px)';
        lblDay.className = 'relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold text-white';
        lblNight.className = 'relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold opacity-70';

        dashRingMat.color.setHex(0x0055aa);
        if (typeof megaRingWireMat !== 'undefined') megaRingWireMat.color.setHex(0x0066cc);
        if (typeof secondaryWireMat !== 'undefined') secondaryWireMat.color.setHex(0x004488);
    }

    playClickSound(900, 0.03);
    dashRenderer.render(dashScene, dashCamera);
    runCalculationDebounced();
}

/* ====================== ТЕКСТОВЫЕ ЭФФЕКТЫ ====================== */

const CYRILLIC_GLYPHS = 'АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЭЮЯ0123456789!';
const NUMERIC_GLYPHS = '0123456789';

function scrambleElementText(element, finalText, duration = 460, useAlphabet = true) {
    if (!element) return;

    const glyphs = useAlphabet ? CYRILLIC_GLYPHS : NUMERIC_GLYPHS;
    const start = performance.now();
    const length = finalText.length;

    if (element.scrambleTimer) cancelAnimationFrame(element.scrambleTimer);

    function update(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const revealIndex = Math.floor(progress * length);

        let output = '';

        for (let i = 0; i < length; i++) {
            const char = finalText[i];

            if (i < revealIndex || char === ' ' || char === '.' || char === ',' || char === '₽') {
                output += char;
            } else {
                output += glyphs[Math.floor(Math.random() * glyphs.length)];
            }
        }

        element.textContent = output;

        if (progress < 1) {
            element.scrambleTimer = requestAnimationFrame(update);
        } else {
            element.scrambleTimer = null;
        }
    }

    element.scrambleTimer = requestAnimationFrame(update);
}

function scrambleNumber(element, finalString, duration = 400) {
    scrambleElementText(element, finalString, duration, false);
}

function scrambleTitle(card) {
    playClickSound(1600, 0.015);

    const titleElement = card.querySelector('.metric-title');
    if (!titleElement) return;

    const original = titleElement.getAttribute('data-original') || titleElement.textContent;
    titleElement.setAttribute('data-original', original);
    scrambleElementText(titleElement, original, 380, true);
}

/* ========================== ВКЛАДКИ ========================== */

const TAB_TITLES = [
    '[01] ОБСЛУЖИВАНИЕ КАПИТАЛА',
    '[02] СКЛАДСКОЙ ЦИКЛ',
    '[03] ДЕНЕЖНЫЙ ПОТОК',
    '[04] ЭКОНОМИКА И ЗАКАЗЫ'
];

function selectTab(index) {
    playClickSound(1400, 0.025);
    triggerDashRingTurn();

    const buttons = document.querySelectorAll('#navTabsContainer .tab-btn');

    buttons.forEach((button, idx) => {
        if (idx === index) {
            button.className = 'tab-btn px-4 py-1.5 font-mono text-[10px] uppercase tracking-widest bg-[#d4af37] text-black font-bold transition shadow-md';
            scrambleElementText(button, TAB_TITLES[idx], 400, true);
        } else {
            button.className = 'tab-btn px-4 py-1.5 font-mono text-[10px] uppercase tracking-widest opacity-70 hover:opacity-100 transition';
            button.textContent = TAB_TITLES[idx];
        }
    });

    for (let i = 0; i < 4; i++) {
        const view = document.getElementById(`viewTab${i}`);

        if (i === index) {
            view.classList.remove('hidden');
            view.classList.remove('tab-view-enter');
            void view.offsetWidth;
            view.classList.add('tab-view-enter');
        } else {
            view.classList.add('hidden');
        }
    }
}

/* ====================== ПАРАМЕТРЫ МОДЕЛИ ====================== */

let growthMode = 'abs';

function setGrowthMode(mode) {
    playClickSound(950, 0.02);
    growthMode = mode;

    const buttonAbs = document.getElementById('btnModeAbs');
    const buttonPct = document.getElementById('btnModePct');
    const title = document.getElementById('lblGrowthModeTitle');
    const slider = document.getElementById('paramGrowthSlider');

    if (mode === 'abs') {
        buttonAbs.className = 'py-1 font-mono text-[9px] uppercase tracking-wider bg-[#d4af37] text-black font-bold transition';
        buttonPct.className = 'py-1 font-mono text-[9px] uppercase tracking-wider opacity-60 hover:opacity-100 transition';
        title.textContent = 'ПРИРОСТ В МЕСЯЦ';
        slider.max = 100;
        slider.value = 5;
    } else {
        buttonPct.className = 'py-1 font-mono text-[9px] uppercase tracking-wider bg-[#d4af37] text-black font-bold transition';
        buttonAbs.className = 'py-1 font-mono text-[9px] uppercase tracking-wider opacity-60 hover:opacity-100 transition';
        title.textContent = 'ПРИРОСТ В МЕСЯЦ, %';
        slider.max = 50;
        slider.value = 10;
    }

    runCalculationDebounced();
}

/* ====================== ФИНАНСОВАЯ МОДЕЛЬ ====================== */

let chartDebtInstance = null;
let chartStockInstance = null;
let chartCFInstance = null;
let chartOrdersInstance = null;
let chartPieInstance = null;
let latestCalculatedData = null;

function runCalculation() {
    const startMonth = parseInt(document.getElementById('paramStartMonth').value, 10) || 0;
    const startYear = parseInt(document.getElementById('paramStartYear').value, 10) || 2026;
    const period = parseInt(document.getElementById('paramPeriod').value, 10) || 12;
    const vatRate = safeNumber(parseFloat(document.getElementById('paramVatRate').value), 22);
    const vatMultiplier = 1 + vatRate / 100;

    const marginPct = safeNumber(parseFloat(document.getElementById('paramMargin').value), 20);
    document.getElementById('lblMarginVal').textContent = `${marginPct}%`;

    const initialPurchase = safeNumber(parseCleanNum(document.getElementById('paramInitialPurchase').value), 0);
    const batchCycle = Math.max(1, parseInt(document.getElementById('paramBatchCycle').value, 10) || 5);
    const cbRate = safeNumber(parseFloat(document.getElementById('paramCbRate').value), 14);
    const commMargin = safeNumber(parseFloat(document.getElementById('paramCommMargin').value), 2);

    const totalRateAnnual = cbRate + commMargin;
    const monthlyRate = totalRateAnnual / 100 / 12;

    document.getElementById('telemetryRate').textContent = `[КАПИТАЛ: ${totalRateAnnual.toFixed(1)}% ГОДОВЫХ]`;
    document.getElementById('kpiRateSub').textContent = `Ставка ${totalRateAnnual.toFixed(1)}%`;

    const supplierPrepayPct = safeNumber(parseFloat(document.getElementById('paramSupplierPrepay').value), 50);
    document.getElementById('lblSupplierPrepVal').textContent = `${supplierPrepayPct}%`;

    const supplierDelay = Math.max(0, parseInt(document.getElementById('paramSupplierDelay').value, 10) || 0);
    document.getElementById('lblSupplierDelayVal').textContent = `${supplierDelay} мес.`;

    const aov = safeNumber(parseCleanNum(document.getElementById('paramAov').value), 0);
    const startOrders = Math.max(1, parseInt(document.getElementById('paramStartOrders').value, 10) || 40);

    const growthValue = safeNumber(parseFloat(document.getElementById('paramGrowthSlider').value), 0);
    document.getElementById('lblGrowthVal').textContent = growthMode === 'abs'
        ? `+${growthValue} шт.`
        : `+${growthValue}%`;

    const maxOrdersCap = Math.max(1, parseInt(document.getElementById('paramMaxOrdersCap').value, 10) || 300);

    const fot = safeNumber(parseCleanNum(document.getElementById('paramFot').value), 0);
    const warehouse = safeNumber(parseCleanNum(document.getElementById('paramWh').value), 0);
    const office = safeNumber(parseCleanNum(document.getElementById('paramOffice').value), 0);

    const factoringShare = safeNumber(parseFloat(document.getElementById('paramFactoringShare').value), 50);
    document.getElementById('lblFactShareVal').textContent = `${factoringShare}%`;

    const factoringAdvance = 0.8;

    const shortMonths = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'];
    const xLabels = [];
    const orders = [];
    const revenue = [];

    for (let i = 0; i < period; i++) {
        const monthIndex = (startMonth + i) % 12;
        const yearOffset = Math.floor((startMonth + i) / 12);

        xLabels.push(`${shortMonths[monthIndex]} ${startYear + yearOffset}`);

        let currentOrders = i === 0
            ? startOrders
            : growthMode === 'abs'
                ? orders[i - 1] + growthValue
                : orders[i - 1] * (1 + growthValue / 100);

        currentOrders = Math.min(currentOrders, maxOrdersCap);

        orders.push(currentOrders);
        revenue.push(currentOrders * aov);
    }

    const cogsPercent = 1 - marginPct / 100;
    const cogsVat = revenue.map((value) => value * cogsPercent * vatMultiplier);

    const cogsPayments = new Array(period).fill(0);
    const inventoryDeliveries = new Array(period).fill(0);

    cogsPayments[0] += initialPurchase * (supplierPrepayPct / 100);
    inventoryDeliveries[0] += initialPurchase;

    const firstDelayMonth = supplierDelay;
    if (firstDelayMonth < period) {
        cogsPayments[firstDelayMonth] += initialPurchase * ((100 - supplierPrepayPct) / 100);
    }

    for (let batchStart = batchCycle; batchStart < period; batchStart += batchCycle) {
        const batchEnd = Math.min(batchStart + batchCycle, period);
        let batchTotal = 0;

        for (let k = batchStart; k < batchEnd; k++) {
            batchTotal += cogsVat[k];
        }

        inventoryDeliveries[batchStart] += batchTotal;
        cogsPayments[batchStart] += batchTotal * (supplierPrepayPct / 100);

        const secondTrancheMonth = batchStart + supplierDelay;
        if (secondTrancheMonth < period) {
            cogsPayments[secondTrancheMonth] += batchTotal * ((100 - supplierPrepayPct) / 100);
        }
    }

    const inventoryBalance = [];
    let currentStock = 0;

    for (let i = 0; i < period; i++) {
        currentStock += inventoryDeliveries[i] - cogsVat[i];
        inventoryBalance.push(Math.max(currentStock, 0));
    }

    const inflows = new Array(period).fill(0);

    for (let i = 0; i < period; i++) {
        const invoiceVat = revenue[i] * vatMultiplier;

        inflows[i] += invoiceVat * (factoringShare / 100) * factoringAdvance;

        const deferredMonth = i + 2;
        if (deferredMonth < period) {
            inflows[deferredMonth] += invoiceVat * (1 - factoringShare / 100);
            inflows[deferredMonth] += invoiceVat * (factoringShare / 100) * (1 - factoringAdvance);
        }
    }

    const operatingExpenses = [];
    const taxes = revenue.map((value) => value * 0.05);
    const baseOperatingCost = 150000 + warehouse + office + fot;

    for (let i = 0; i < period; i++) {
        operatingExpenses.push(i >= 6 ? baseOperatingCost * 1.2 : baseOperatingCost);
    }

    const baseOutflows = [];

    for (let i = 0; i < period; i++) {
        baseOutflows.push(cogsPayments[i] + operatingExpenses[i] + taxes[i]);
    }

    const monthlyInvestments = new Array(period).fill(0);
    const interestPayments = new Array(period).fill(0);
    const debtRepayments = new Array(period).fill(0);
    const debtBalance = new Array(period).fill(0);
    const cashBalance = new Array(period).fill(0);

    let currentDebt = 0;
    let currentCash = 0;

    for (let i = 0; i < period; i++) {
        const interestDue = currentDebt * monthlyRate;
        interestPayments[i] = interestDue;

        const netBeforeFinancing = inflows[i] - baseOutflows[i] - interestDue;
        const potentialCash = currentCash + netBeforeFinancing;

        if (potentialCash < 0) {
            const needed = Math.abs(potentialCash);
            monthlyInvestments[i] = needed;
            currentDebt += needed;
            currentCash = 0;
            debtRepayments[i] = 0;
        } else {
            monthlyInvestments[i] = 0;
            const repayment = Math.min(potentialCash, currentDebt);

            debtRepayments[i] = repayment;
            currentDebt -= repayment;
            currentCash = potentialCash - repayment;
        }

        debtBalance[i] = currentDebt;
        cashBalance[i] = currentCash;
    }

    const totalRevenue = revenue.reduce((sum, value) => sum + value, 0);
    const totalInvestments = monthlyInvestments.reduce((sum, value) => sum + value, 0);
    const totalInterest = interestPayments.reduce((sum, value) => sum + value, 0);
    const maxDebt = Math.max(...debtBalance, 0);
    const totalOperatingExpenses = operatingExpenses.reduce((sum, value) => sum + value, 0);
    const totalTaxes = taxes.reduce((sum, value) => sum + value, 0);

    const netProfit = totalRevenue * (marginPct / 100)
        - totalOperatingExpenses
        - totalTaxes
        - totalInterest;

    const roi = totalRevenue > 0 ? (netProfit / totalRevenue) * 100 : 0;

    latestCalculatedData = {
        xLabels,
        monthlyInvestments,
        interestPayments,
        debtRepayments,
        debtBalance,
        cashBalance,
        totalRevenue,
        netProfit,
        roi
    };

    scrambleNumber(document.getElementById('kpiRev'), formatSpaced(totalRevenue));
    document.getElementById('kpiRevSub').textContent = `Маржа: ${marginPct}%`;

    scrambleNumber(document.getElementById('kpiInjections'), formatSpaced(totalInvestments));
    scrambleNumber(document.getElementById('kpiInterest'), formatSpaced(totalInterest));
    scrambleNumber(document.getElementById('kpiMaxDebt'), formatSpaced(maxDebt));
    scrambleNumber(document.getElementById('kpiProfit'), formatSpaced(netProfit));

    document.getElementById('kpiRoiSub').textContent = `Рентабельность: ${roi.toFixed(1)}%`;

    const tableBody = document.getElementById('tableDebtBody');
    tableBody.innerHTML = '';

    for (let i = 0; i < period; i++) {
        const row = document.createElement('tr');
        row.className = 'hover:bg-[var(--bg-cell-hover)] transition';

        row.innerHTML = `
            <td class="p-3 font-bold">${xLabels[i]}</td>
            <td class="p-3 text-[#e63946]">${formatSpaced(monthlyInvestments[i])}</td>
            <td class="p-3 text-[#d4af37]">${formatSpaced(interestPayments[i])}</td>
            <td class="p-3 text-[#2a9d8f]">${formatSpaced(debtRepayments[i])}</td>
            <td class="p-3 font-bold">${formatSpaced(debtBalance[i])}</td>
            <td class="p-3">${formatSpaced(cashBalance[i])}</td>
        `;

        tableBody.appendChild(row);
    }

    const chartText = isDark ? '#8e8a80' : '#6b665c';
    const chartGrid = isDark ? 'rgba(212, 175, 55, 0.08)' : 'rgba(184, 134, 11, 0.12)';

    updateChart('debt', 'chartDebt', {
        type: 'bar',
        data: {
            labels: xLabels,
            datasets: [
                {
                    label: 'Проценты',
                    data: interestPayments,
                    backgroundColor: '#d4af37',
                    order: 2
                },
                {
                    label: 'Остаток долга',
                    data: debtBalance,
                    type: 'line',
                    borderColor: '#e63946',
                    backgroundColor: '#e63946',
                    borderWidth: 2.5,
                    yAxisID: 'y1',
                    tension: 0.3,
                    order: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { color: chartText, font: { family: 'JetBrains Mono', size: 10 } }
                },
                y: {
                    grid: { color: chartGrid },
                    ticks: { color: chartText, font: { family: 'JetBrains Mono', size: 10 } }
                },
                y1: {
                    position: 'right',
                    grid: { display: false },
                    ticks: { color: '#e63946', font: { family: 'JetBrains Mono', size: 10 } }
                }
            },
            plugins: {
                legend: {
                    labels: { color: chartText, font: { family: 'JetBrains Mono', size: 11 } }
                }
            }
        }
    });

    updateChart('stock', 'chartStock', {
        type: 'bar',
        data: {
            labels: xLabels,
            datasets: [
                {
                    label: 'Закупки',
                    data: cogsPayments,
                    backgroundColor: isDark ? '#52525b' : '#cbd5e1',
                    order: 2
                },
                {
                    label: 'Остаток на складе',
                    data: inventoryBalance,
                    type: 'line',
                    borderColor: '#d4af37',
                    borderWidth: 2.5,
                    yAxisID: 'y1',
                    tension: 0.3,
                    order: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { color: chartText, font: { family: 'JetBrains Mono', size: 10 } }
                },
                y: {
                    grid: { color: chartGrid },
                    ticks: { color: chartText, font: { family: 'JetBrains Mono', size: 10 } }
                },
                y1: {
                    position: 'right',
                    grid: { display: false },
                    ticks: { color: '#d4af37', font: { family: 'JetBrains Mono', size: 10 } }
                }
            },
            plugins: {
                legend: {
                    labels: { color: chartText, font: { family: 'JetBrains Mono', size: 11 } }
                }
            }
        }
    });

    const totalOutflows = baseOutflows.map((value, index) => value + interestPayments[index]);

    updateChart('cashflow', 'chartCF', {
        type: 'bar',
        data: {
            labels: xLabels,
            datasets: [
                {
                    label: 'Поступления',
                    data: inflows,
                    backgroundColor: '#2a9d8f'
                },
                {
                    label: 'Выплаты',
                    data: totalOutflows.map((value) => -value),
                    backgroundColor: '#e63946'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { color: chartText, font: { family: 'JetBrains Mono', size: 10 } }
                },
                y: {
                    grid: { color: chartGrid },
                    ticks: { color: chartText, font: { family: 'JetBrains Mono', size: 10 } }
                }
            },
            plugins: {
                legend: {
                    labels: { color: chartText, font: { family: 'JetBrains Mono', size: 11 } }
                }
            }
        }
    });

    updateChart('orders', 'chartOrders', {
        type: 'bar',
        data: {
            labels: xLabels,
            datasets: [
                {
                    label: 'Заказы, шт.',
                    data: orders,
                    backgroundColor: '#d4af37'
                },
                {
                    label: 'Выручка, ₽',
                    data: revenue,
                    type: 'line',
                    borderColor: '#2a9d8f',
                    yAxisID: 'y1',
                    borderWidth: 2.5,
                    tension: 0.3
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { color: chartText, font: { family: 'JetBrains Mono', size: 10 } }
                },
                y: {
                    grid: { color: chartGrid },
                    ticks: { color: chartText, font: { family: 'JetBrains Mono', size: 10 } }
                },
                y1: {
                    position: 'right',
                    grid: { display: false },
                    ticks: { color: '#2a9d8f', font: { family: 'JetBrains Mono', size: 10 } }
                }
            },
            plugins: {
                legend: {
                    labels: { color: chartText, font: { family: 'JetBrains Mono', size: 11 } }
                }
            }
        }
    });

    const totalPurchases = cogsPayments.reduce((sum, value) => sum + value, 0);

    updateChart('pie', 'chartPie', {
        type: 'doughnut',
        data: {
            labels: ['Склад', 'Офис', 'ФОТ', 'Налоги', 'Закупки', 'Проценты'],
            datasets: [{
                data: [
                    warehouse * period,
                    office * period,
                    fot * period,
                    totalTaxes,
                    totalPurchases,
                    totalInterest
                ],
                backgroundColor: [
                    '#52525b',
                    '#71717a',
                    '#d4af37',
                    '#e63946',
                    '#2a9d8f',
                    '#457b9d'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: chartText,
                        font: { family: 'JetBrains Mono', size: 10 }
                    }
                }
            }
        }
    });
}

/* ===================== ОПТИМИЗАЦИЯ ГРАФИКОВ ===================== */

const chartRegistry = {};

function updateChart(chartKey, canvasId, config) {
    const canvas = document.getElementById(canvasId);
    if (!canvas || typeof Chart === 'undefined') return;

    if (chartRegistry[chartKey]) {
        chartRegistry[chartKey].data = config.data;
        chartRegistry[chartKey].options = config.options;
        chartRegistry[chartKey].update('none');
        return;
    }

    chartRegistry[chartKey] = new Chart(canvas.getContext('2d'), config);
}

const runCalculationDebounced = debounce(runCalculation, 140);

/* ========================= CSV-ЭКСПОРТ ========================= */

function exportDataToCsv() {
    playClickSound(1600, 0.05);

    if (!latestCalculatedData) {
        runCalculation();
    }

    if (!latestCalculatedData) return;

    const {
        xLabels,
        monthlyInvestments,
        interestPayments,
        debtRepayments,
        debtBalance,
        cashBalance
    } = latestCalculatedData;

    let csvContent = '\uFEFFПериод;Дотация;Проценты;Погашение долга;Остаток долга;Свободный остаток\n';

    for (let i = 0; i < xLabels.length; i++) {
        csvContent += [
            xLabels[i],
            Math.round(monthlyInvestments[i]),
            Math.round(interestPayments[i]),
            Math.round(debtRepayments[i]),
            Math.round(debtBalance[i]),
            Math.round(cashBalance[i])
        ].join(';') + '\n';
    }

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'FinansovayaModelKapital.csv';

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(link.href);
}

/* ========================= ЧАСЫ ========================= */

setInterval(() => {
    const clock = document.getElementById('telemetryClock');
    if (clock) {
        clock.textContent = `[${new Date().toLocaleTimeString('ru-RU')}]`;
    }
}, 1000);

/* ========================= СБРОС ========================= */

function resetDefaults() {
    playClickSound(600, 0.05);
    document.getElementById('financialInputsForm').reset();
    runCalculationDebounced();
}

/* ========================= СТАРТ ========================= */

window.addEventListener('load', () => {
    runCalculation();
});
</script>
</body>
</html>
"""

st.iframe(
    html_code,
    width="stretch",
    height="stretch",
)
