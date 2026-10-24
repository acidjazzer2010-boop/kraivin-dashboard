import streamlit as st
import streamlit.components.v1 as components
import base64
import os
import io
from PIL import Image, ImageFilter

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

def get_blueprint_vitruvian(filename):
    if not os.path.exists(filename):
        return ""
    
    try:
        img = Image.open(filename).convert("L")
        smoothed = img.filter(ImageFilter.GaussianBlur(radius=0.6))
        edges = smoothed.filter(ImageFilter.FIND_EDGES)
        
        def extract_clean_strokes(p):
            if p < 35:
                return 0
            return int(min(255, (p - 35) * 3.2))
            
        alpha = edges.point(extract_clean_strokes)
        color_layer = Image.new("RGBA", img.size, (229, 193, 88, 255))
        color_layer.putalpha(alpha)
        
        buffered = io.BytesIO()
        color_layer.save(buffered, format="PNG")
        b64_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{b64_str}"
    except Exception as e:
        return ""

html_code = r"""<!DOCTYPE html>
<html lang="ru" class="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Архитектура Капитала // Финансовое Моделирование</title>

<!-- Типографика: Редакторская антиква + Инженерный моноширинный + Швейцарский гротеск -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600;1,700&family=JetBrains+Mono:ital,wght@0,300;0,400;0,500;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">

<!-- Библиотеки Awwwards стека: Tailwind, Three.js, Chart.js, GSAP + ScrollTrigger, Lenis -->
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

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script src="https://cdn.jsdelivr.net/gh/studio-freight/lenis@1.0.29/bundled/lenis.min.js"></script>

<style>
:root {
    --bg-space: #070709;
    --bg-panel: rgba(13, 13, 18, 0.78);
    --bg-cell-hover: rgba(24, 24, 34, 0.95);
    --text-main: #f4f1ea;
    --text-muted: #8e8a80;
    --border-line: rgba(212, 175, 55, 0.16);
    --border-accent: rgba(212, 175, 55, 0.6);
    --accent-gold: #d4af37;
    --accent-vermilion: #e63946;
    --accent-jade: #2a9d8f;
    --input-bg: rgba(255, 255, 255, 0.025);
    --cursor-glow: rgba(212, 175, 55, 0.22);
    --table-header-bg: rgba(13, 13, 18, 0.98);
    --grain-opacity: 0.038;
}
html:not(.dark) {
    --bg-space: #f4f1ea;
    --bg-panel: rgba(255, 255, 255, 0.88);
    --bg-cell-hover: rgba(246, 243, 235, 0.98);
    --text-main: #141416;
    --text-muted: #6b665c;
    --border-line: rgba(184, 134, 11, 0.22);
    --border-accent: rgba(184, 134, 11, 0.75);
    --accent-gold: #b8860b;
    --accent-vermilion: #c5221f;
    --accent-jade: #1d756b;
    --input-bg: rgba(0, 0, 0, 0.03);
    --cursor-glow: rgba(184, 134, 11, 0.18);
    --table-header-bg: rgba(244, 241, 234, 0.98);
    --grain-opacity: 0.022;
}

* { box-sizing: border-box; border-color: var(--border-line); }
html.lenis { height: auto; }
.lenis.lenis-smooth { scroll-behavior: auto !important; }
.lenis.lenis-smooth [data-lenis-prevent] { overscroll-behavior: contain; }
.lenis.lenis-stopped { overflow: hidden; }

body { 
    background-color: var(--bg-space); 
    color: var(--text-main); 
    font-family: 'JetBrains Mono', monospace; 
    overflow-x: hidden; 
    margin: 0; padding: 0; 
    transition: background-color 0.5s ease, color 0.5s ease;
}

/* Аналоговый пленочный шум (Film Grain) */
.film-grain {
    position: fixed; inset: 0; width: 100vw; height: 100vh;
    pointer-events: none; z-index: 999; opacity: var(--grain-opacity);
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
}

/* Кастомный реактивный курсор Alche */
#custom-cursor {
    position: fixed; top: 0; left: 0; width: 8px; height: 8px;
    background: var(--accent-gold); border-radius: 50%;
    pointer-events: none; z-index: 9999;
    transform: translate(-50%, -50%);
    transition: width 0.3s ease, height 0.3s ease, background-color 0.3s ease, opacity 0.3s ease;
}
#custom-cursor-follower {
    position: fixed; top: 0; left: 0; width: 34px; height: 34px;
    border: 1px solid var(--accent-gold); border-radius: 50%;
    pointer-events: none; z-index: 9998;
    transform: translate(-50%, -50%);
    opacity: 0.45;
    transition: width 0.3s ease, height 0.3s ease, border-color 0.3s ease, transform 0.15s ease-out;
}

/* ЗАСТАВКА */
#preloader-stage {
    position: fixed; inset: 0; background: #060608; z-index: 900;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
}
#preloader-canvas-container { position: absolute; inset: 0; width: 100vw; height: 100vh; display: flex; align-items: center; justify-content: center; z-index: 10; overflow: hidden; }

#quillPen {
    position: absolute; left: 0; top: 0; 
    margin-left: -4px; margin-top: -4px;
    pointer-events: none; z-index: 25; opacity: 0; 
    filter: drop-shadow(0 0 10px rgba(255, 215, 0, 0.8));
    will-change: transform, opacity;
    transition: opacity 0.5s ease;
}
.nib-spark { animation: sparkFlicker 0.15s infinite alternate; }
@keyframes sparkFlicker { 0% { opacity: 0.5; transform: scale(0.8); } 100% { opacity: 1; transform: scale(1.4); } }

#exploreBtnWrapper {
    position: absolute; bottom: 50px; left: 50%;
    transform: translateX(-50%); z-index: 40; opacity: 0; pointer-events: none;
    transition: opacity 1.2s cubic-bezier(0.19, 1, 0.22, 1), transform 1.2s cubic-bezier(0.19, 1, 0.22, 1);
}
#exploreBtnWrapper.active { opacity: 1; pointer-events: auto; transform: translateX(-50%) translateY(0); }
.explore-btn {
    position: relative; padding: 14px 44px;
    background: rgba(13, 13, 18, 0.65); border: 1px solid rgba(212, 175, 55, 0.7);
    color: #f4f1ea; font-family: 'JetBrains Mono', monospace; font-size: 11px;
    letter-spacing: 0.35em; text-transform: uppercase; cursor: pointer;
    backdrop-filter: blur(12px); overflow: hidden; transition: all 0.4s ease;
    box-shadow: 0 0 25px rgba(212, 175, 55, 0.15), inset 0 0 15px rgba(212, 175, 55, 0.08);
}
.explore-btn::before {
    content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.3), transparent);
    transition: left 0.7s ease;
}
.explore-btn:hover {
    border-color: #ffd700; color: #ffd700;
    box-shadow: 0 0 35px rgba(212, 175, 55, 0.4), inset 0 0 20px rgba(212, 175, 55, 0.25);
    transform: scale(1.04);
}
.explore-btn:hover::before { left: 100%; }

/* ФОН ОСНОВНОГО ПРИЛОЖЕНИЯ */
#webgl-bg-canvas { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 0; pointer-events: none; opacity: 0.5; transition: opacity 0.5s ease; }
html:not(.dark) #webgl-bg-canvas { opacity: 0.22; }

/* Архитектурные блоки с ренессансными засечками */
.alche-block {
    position: relative; background: var(--bg-panel); backdrop-filter: blur(20px);
    border-right: 1px solid var(--border-line); border-bottom: 1px solid var(--border-line);
    transition: background-color 0.3s ease, border-color 0.3s ease;
}
.cross-tl::before { content: '+'; position: absolute; top: -6px; left: -4px; font-family: 'JetBrains Mono', monospace; font-size: 10px; line-height: 1; color: var(--accent-gold); pointer-events: none; z-index: 10; }
.cross-br::after { content: '+'; position: absolute; bottom: -6px; right: -4px; font-family: 'JetBrains Mono', monospace; font-size: 10px; line-height: 1; color: var(--accent-gold); pointer-events: none; z-index: 10; }

/* Карточки с магнитным свечением границ (Cursor Glow + 3D Tilt) */
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

/* Боковой навигатор шагов скролла (HUD) */
#alcheScrollIndicator {
    position: fixed; right: 24px; top: 50%; transform: translateY(-50%);
    display: flex; flex-direction: column; gap: 14px; z-index: 80; pointer-events: auto;
}
.scroll-step-dot {
    position: relative; width: 6px; height: 6px; border: 1px solid var(--border-accent);
    background: transparent; cursor: pointer; transition: all 0.35s cubic-bezier(0.19, 1, 0.22, 1);
}
.scroll-step-dot.active {
    background: var(--accent-gold); transform: scale(2) rotate(45deg);
    box-shadow: 0 0 12px var(--accent-gold);
}
.scroll-step-dot::after {
    content: attr(data-label); position: absolute; right: 18px; top: 50%; transform: translateY(-50%);
    font-family: 'JetBrains Mono', monospace; font-size: 9px; text-transform: uppercase;
    letter-spacing: 0.2em; white-space: nowrap; color: var(--accent-gold); opacity: 0;
    pointer-events: none; transition: opacity 0.25s ease, transform 0.25s ease;
}
.scroll-step-dot:hover::after { opacity: 1; transform: translateY(-50%) translateX(-4px); }

/* Секции Scrollytelling с масками появления */
.scroll-section-step {
    opacity: 0.18;
    transform: translateY(28px) scale(0.985);
    filter: blur(5px);
    transition: opacity 0.7s cubic-bezier(0.19, 1, 0.22, 1), transform 0.7s cubic-bezier(0.19, 1, 0.22, 1), filter 0.7s ease;
    will-change: transform, opacity, filter;
}
.scroll-section-step.in-focus {
    opacity: 1;
    transform: translateY(0) scale(1);
    filter: blur(0px);
}

.reveal-mask {
    clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%);
    transition: clip-path 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

input[type="range"] { -webkit-appearance: none; appearance: none; width: 100%; height: 2px; background: var(--border-line); outline: none; }
input[type="range"]::-webkit-slider-thumb { -webkit-appearance: none; appearance: none; width: 12px; height: 12px; background: var(--accent-gold); cursor: pointer; border: 1px solid var(--bg-space); transform: rotate(45deg); transition: transform 0.2s ease, background-color 0.2s ease; }
input[type="range"]::-webkit-slider-thumb:hover { transform: rotate(45deg) scale(1.4); }

.mono-input { background: var(--input-bg); border: 1px solid var(--border-line); color: var(--text-main); font-family: 'JetBrains Mono', monospace; font-size: 12px; padding: 7px 10px; width: 100%; border-radius: 0; transition: border-color 0.2s ease, background 0.2s ease; }
.mono-input:focus { outline: none; border-color: var(--accent-gold); background: rgba(212, 175, 55, 0.08); }
select.mono-input option { background-color: #0d0d12; color: #f4f1ea; }
html:not(.dark) select.mono-input option { background-color: #f4f1ea; color: #141416; }

.hw-slider-track { position: relative; width: 140px; height: 30px; border: 1px solid var(--border-line); background: var(--input-bg); display: flex; align-items: center; justify-content: space-between; padding: 0 10px; cursor: pointer; user-select: none; }
.hw-slider-thumb { position: absolute; top: 2px; bottom: 2px; width: 66px; background: var(--accent-gold); transition: transform 0.45s cubic-bezier(0.19, 1, 0.22, 1), background-color 0.3s ease; }
.pulse-dot { display: inline-block; width: 6px; height: 6px; border-radius: 9999px; background-color: var(--accent-gold); animation: pulseAnim 2s infinite ease-in-out; }
@keyframes pulseAnim { 0%, 100% { opacity: 0.4; transform: scale(0.9); } 50% { opacity: 1; transform: scale(1.2); } }
::-webkit-scrollbar { width: 4px; height: 4px; } ::-webkit-scrollbar-track { background: transparent; } ::-webkit-scrollbar-thumb { background: var(--border-line); } ::-webkit-scrollbar-thumb:hover { background: var(--accent-gold); }
</style>
</head>
<body class="selection:bg-[#d4af37] selection:text-black">
<div class="film-grain"></div>

<!-- Кастомный курсор -->
<div id="custom-cursor"></div>
<div id="custom-cursor-follower"></div>

<!-- Боковой HUD-навигатор шагов скролла -->
<nav id="alcheScrollIndicator">
    <div class="scroll-step-dot active" data-step="0" data-label="[01] Сводка KPI" onclick="scrollToStep(0)"></div>
    <div class="scroll-step-dot" data-step="1" data-label="[02] Обслуживание капитала" onclick="scrollToStep(1)"></div>
    <div class="scroll-step-dot" data-step="2" data-label="[03] Складской цикл" onclick="scrollToStep(2)"></div>
    <div class="scroll-step-dot" data-step="3" data-label="[04] Денежный поток" onclick="scrollToStep(3)"></div>
    <div class="scroll-step-dot" data-step="4" data-label="[05] Юнит-экономика" onclick="scrollToStep(4)"></div>
</nav>

<!-- РЕНЕССАНСНЫЙ ПРЕЛОАДЕР С ВИТРУВИАНЦЕМ -->
<div id="preloader-stage">
    <div id="preloader-canvas-container">
        <canvas id="preloader-webgl"></canvas>
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
    
    <div id="preloaderTitle" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 mt-40 font-serif italic text-4xl md:text-5xl font-bold tracking-[0.1em] text-[#d4af37] opacity-0 transition-opacity duration-[1500ms] z-30 pointer-events-none drop-shadow-[0_0_15px_rgba(212,175,55,0.6)] text-center w-full">
        Архитектура финансов
    </div>

    <div id="preloaderHUD" class="absolute bottom-10 flex flex-col items-center gap-2 font-mono z-20 pointer-events-auto transition-opacity duration-500">
        <div class="flex items-center gap-3 text-[#d4af37] text-[11px] tracking-[0.25em] uppercase">
            <span class="pulse-dot"></span>
            <span id="loaderStatusText">Инициализация 3D среды...</span>
            <span id="loaderPercent" class="font-bold">0%</span>
        </div>
        <div class="w-64 sm:w-80 h-[2px] bg-white/10 relative overflow-hidden mt-1">
            <div id="loaderProgressBar" class="absolute top-0 bottom-0 left-0 bg-[#d4af37] w-0 transition-all duration-100 ease-out"></div>
        </div>
    </div>

    <div id="exploreBtnWrapper">
        <button id="exploreBtn" onclick="triggerLiquidTransition(event)" class="explore-btn">
            Исследовать
        </button>
    </div>
</div>

<canvas id="webgl-bg-canvas"></canvas>

<!-- Основное приложение -->
<div id="mainDashboardApp" class="relative z-10 min-h-screen flex flex-col border-t border-l opacity-0 transition-opacity duration-1000" style="border-color: var(--border-line);">
    <header class="sticky top-0 z-50 alche-block px-5 lg:px-8 py-3 flex flex-wrap items-center justify-between gap-4 border-b">
        <div class="flex items-center gap-6">
            <div class="flex items-center gap-3 cursor-pointer" onclick="playClickSound(1500, 0.04)">
                <svg class="w-7 h-7 text-[#d4af37]" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.2">
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
                <span id="telemetryRate">[КАПИТАЛ: 19.0% ГОДОВЫХ]</span>
                <span id="cursorCoordDisplay" class="text-[#d4af37]">X: 0000 / Y: 0000</span>
                <span id="telemetryClock">[15:00:00]</span>
            </div>
        </div>
        <div class="flex items-center gap-4">
            <button id="downloadReportBtn" onclick="exportDataToCsv()" type="button" class="px-3.5 py-1.5 border font-mono text-[10px] uppercase tracking-widest hover:border-[#d4af37] hover:bg-[#d4af37]/10 transition flex items-center gap-2">
                <span>↓ Скачать отчет</span>
            </button>
            <div id="themeSlider" class="hw-slider-track" onclick="toggleTheme()" title="Переключить режим: Ночь / День">
                <div id="sliderThumb" class="hw-slider-thumb" style="transform: translateX(0px);"></div>
                <span id="lblNight" class="relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold text-black">Ночь</span>
                <span id="lblDay" class="relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold opacity-70">День</span>
            </div>
        </div>
    </header>

    <div class="flex-1 grid grid-cols-1 lg:grid-cols-12 relative">
        <!-- ЛЕВАЯ ПАНЕЛЬ ПАРАМЕТРОВ (STICKY HUD) -->
        <aside class="lg:col-span-3 flex flex-col lg:sticky lg:top-[65px] lg:h-[calc(100vh-65px)] overflow-y-auto z-20 border-r" style="border-color: var(--border-line);">
            <div class="alche-block cross-tl px-5 py-3.5 flex items-center justify-between">
                <span class="font-mono text-[10px] uppercase tracking-[0.2em] text-[#d4af37] font-bold">[00] Параметры Модели</span>
                <button id="defaultResetBtn" type="button" onclick="resetDefaults()" class="font-mono text-[9px] uppercase underline opacity-60 hover:opacity-100 transition">Сброс</button>
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
                        <input type="range" id="paramMargin" min="10" max="50" step="1" value="20" oninput="runCalculation()">
                    </div>
                </div>
                <div class="alche-block p-5 space-y-4">
                    <div class="flex justify-between items-baseline"><span class="font-serif italic text-base font-semibold">II. Партионный склад и капитал</span><span class="font-mono text-[9px] opacity-40">02 // 04</span></div>
                    <div>
                        <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Стартовая закупка партии, ₽</label>
                        <input type="text" id="paramInitialPurchase" value="25 000 000" class="mono-input font-bold" oninput="formatInput(this); runCalculation();">
                    </div>
                    <div class="grid grid-cols-3 gap-2">
                        <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Цикл, мес.</label><input type="number" id="paramBatchCycle" value="5" min="1" max="12" class="mono-input text-center" oninput="runCalculation()"></div>
                        <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">ЦБ РФ, %</label><input type="number" id="paramCbRate" value="17.0" step="0.5" class="mono-input text-center" oninput="runCalculation()"></div>
                        <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Маржа, %</label><input type="number" id="paramCommMargin" value="2.0" step="0.5" class="mono-input text-center" oninput="runCalculation()"></div>
                    </div>
                </div>
                <div class="alche-block p-5 space-y-4">
                    <div class="flex justify-between items-baseline"><span class="font-serif italic text-base font-semibold">III. Масштабирование заказов</span><span class="font-mono text-[9px] opacity-40">03 // 04</span></div>
                    <div class="grid grid-cols-2 gap-2.5">
                        <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Средний чек, ₽</label><input type="text" id="paramAov" value="150 000" class="mono-input font-bold" oninput="formatInput(this); runCalculation();"></div>
                        <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Заказов в 1-й мес.</label><input type="number" id="paramStartOrders" value="40" min="1" max="2000" class="mono-input text-center font-bold" oninput="runCalculation()"></div>
                    </div>
                    <div>
                        <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Логика прироста</label>
                        <div class="grid grid-cols-2 border" style="border-color: var(--border-line);">
                            <button type="button" id="btnModeAbs" onclick="setGrowthMode('abs')" class="py-1 font-mono text-[9px] uppercase tracking-wider bg-[#d4af37] text-black font-bold transition">В штуках</button>
                            <button type="button" id="btnModePct" onclick="setGrowthMode('pct')" class="py-1 font-mono text-[9px] uppercase tracking-wider opacity-60 hover:opacity-100 transition">В процентах</button>
                        </div>
                    </div>
                    <div>
                        <div class="flex justify-between font-mono text-[10px] mb-1"><span id="lblGrowthModeTitle" class="opacity-70">ПРИРОСТ В МЕСЯЦ</span><span id="lblGrowthVal" class="text-[#d4af37] font-bold">+5 шт.</span></div>
                        <input type="range" id="paramGrowthSlider" min="0" max="100" step="1" value="5" oninput="runCalculation()">
                    </div>
                    <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Потолок продаж в месяц, шт.</label><input type="number" id="paramMaxOrdersCap" value="300" min="10" step="10" class="mono-input text-center" oninput="runCalculation()"></div>
                </div>
                <div class="alche-block p-5 space-y-4 flex-1">
                    <div class="flex justify-between items-baseline"><span class="font-serif italic text-base font-semibold">IV. Постоянные затраты и факторинг</span><span class="font-mono text-[9px] opacity-40">04 // 04</span></div>
                    <div class="grid grid-cols-3 gap-2">
                        <div><label class="block font-mono text-[8px] uppercase opacity-70 mb-1">ФОТ, ₽</label><input type="text" id="paramFot" value="500 000" class="mono-input" oninput="formatInput(this); runCalculation();"></div>
                        <div><label class="block font-mono text-[8px] uppercase opacity-70 mb-1">Склад, ₽</label><input type="text" id="paramWh" value="200 000" class="mono-input" oninput="formatInput(this); runCalculation();"></div>
                        <div><label class="block font-mono text-[8px] uppercase opacity-70 mb-1">Офис, ₽</label><input type="text" id="paramOffice" value="150 000" class="mono-input" oninput="formatInput(this); runCalculation();"></div>
                    </div>
                    <div class="grid grid-cols-2 gap-3 pt-1">
                        <div>
                            <div class="flex justify-between font-mono text-[9px] mb-1"><span class="opacity-70">ПРЕДОПЛАТА</span><span id="lblPrepVal">50%</span></div>
                            <input type="range" id="paramPrepaymentPct" min="0" max="100" step="10" value="50" oninput="runCalculation()">
                        </div>
                        <div>
                            <div class="flex justify-between font-mono text-[9px] mb-1"><span class="opacity-70">ФАКТОРИНГ</span><span id="lblFactShareVal">50%</span></div>
                            <input type="range" id="paramFactoringShare" min="0" max="100" step="10" value="50" oninput="runCalculation()">
                        </div>
                    </div>
                </div>
            </form>
        </aside>

        <!-- ПРАВАЯ ЧАСТЬ: ПОШАГОВЫЙ SCROLLYTELLING -->
        <section class="lg:col-span-9 flex flex-col">
            <!-- ЭТАП 0: СВОДКА KPI -->
            <div id="step-0" class="scroll-section-step in-focus p-4 lg:p-6">
                <div class="font-mono text-[10px] text-[#d4af37] tracking-[0.25em] uppercase mb-3 flex items-center gap-2">
                    <span class="pulse-dot"></span> [ШАГ 01 // КЛЮЧЕВЫЕ МЕТРИКИ КАПИТАЛА]
                </div>
                <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
                    <div class="alche-block tilt-card p-5 border">
                        <div class="flex justify-between items-center opacity-60 mb-1"><span class="font-mono text-[9px] uppercase tracking-widest">[01] Выручка</span></div>
                        <div id="kpiRev" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#f4f1ea]">0 ₽</div>
                        <div class="font-mono text-[9px] text-[#d4af37] mt-1.5 opacity-90" id="kpiRevSub">Маржа: 20%</div>
                    </div>
                    <div class="alche-block tilt-card p-5 border">
                        <div class="flex justify-between items-center opacity-60 mb-1"><span class="font-mono text-[9px] uppercase tracking-widest">[02] Дефицит</span></div>
                        <div id="kpiInjections" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#e63946]">0 ₽</div>
                        <div class="font-mono text-[9px] text-[#e63946] mt-1.5 opacity-90">Внешние дотации</div>
                    </div>
                    <div class="alche-block tilt-card p-5 border">
                        <div class="flex justify-between items-center opacity-60 mb-1"><span class="font-mono text-[9px] uppercase tracking-widest">[03] Проценты</span></div>
                        <div id="kpiInterest" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#d4af37]">0 ₽</div>
                        <div id="kpiRateSub" class="font-mono text-[9px] text-[#d4af37] mt-1.5 opacity-90">Ставка 19.0%</div>
                    </div>
                    <div class="alche-block tilt-card p-5 border">
                        <div class="flex justify-between items-center opacity-60 mb-1"><span class="font-mono text-[9px] uppercase tracking-widest">[04] Пиковый долг</span></div>
                        <div id="kpiMaxDebt" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#f4f1ea]">0 ₽</div>
                        <div class="font-mono text-[9px] opacity-60 mt-1.5">Максимум тела</div>
                    </div>
                    <div class="alche-block tilt-card p-5 border col-span-2 sm:col-span-1">
                        <div class="flex justify-between items-center opacity-60 mb-1"><span class="font-mono text-[9px] uppercase tracking-widest">[05] Прибыль</span></div>
                        <div id="kpiProfit" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#2a9d8f]">0 ₽</div>
                        <div id="kpiRoiSub" class="font-mono text-[9px] text-[#2a9d8f] mt-1.5 opacity-90">Рентабельность: 0%</div>
                    </div>
                </div>
            </div>

            <!-- ЭТАП 1: ОБСЛУЖИВАНИЕ ДОЛГА -->
            <div id="step-1" class="scroll-section-step p-4 lg:p-6 space-y-4">
                <div class="font-mono text-[10px] text-[#d4af37] tracking-[0.25em] uppercase flex items-center gap-2">
                    <span class="pulse-dot"></span> [ШАГ 02 // ГРАФИК ОБСЛУЖИВАНИЯ ДОЛГА И ПРОЦЕНТОВ]
                </div>
                <div class="alche-block p-5 border">
                    <div class="flex justify-between items-center mb-4">
                        <div>
                            <h3 class="font-serif text-xl font-bold tracking-wide italic">График обслуживания долга и начисления процентов</h3>
                            <p class="font-mono text-[10px] opacity-60">Ежемесячные проценты по ставке кредитора (столбцы) и динамика тела долга (кривая)</p>
                        </div>
                    </div>
                    <div class="h-[360px] relative"><canvas id="chartDebt"></canvas></div>
                </div>
                <div class="alche-block border overflow-x-auto">
                    <table class="w-full text-left font-mono text-[11px]">
                        <thead class="border-b" style="background-color: var(--table-header-bg); border-color: var(--border-line);">
                            <tr class="text-[9px] uppercase tracking-widest text-[#d4af37]"><th class="p-3">Период</th><th class="p-3">Дотация (вход)</th><th class="p-3">Проценты</th><th class="p-3">Погашение долга</th><th class="p-3">Остаток долга</th><th class="p-3">Свободный остаток</th></tr>
                        </thead>
                        <tbody id="tableDebtBody" class="divide-y" style="border-color: var(--border-line);"></tbody>
                    </table>
                </div>
            </div>

            <!-- ЭТАП 2: СКЛАДСКОЙ ЦИКЛ -->
            <div id="step-2" class="scroll-section-step p-4 lg:p-6 space-y-4">
                <div class="font-mono text-[10px] text-[#d4af37] tracking-[0.25em] uppercase flex items-center gap-2">
                    <span class="pulse-dot"></span> [ШАГ 03 // СКЛАДСКОЙ ЦИКЛ И ПАРТИОННЫЙ ЗАКАЗ]
                </div>
                <div class="alche-block p-5 border">
                    <div class="flex justify-between items-center mb-4">
                        <div>
                            <h3 class="font-serif text-xl font-bold tracking-wide italic">Партионные закупки и истощение склада</h3>
                            <p class="font-mono text-[10px] opacity-60">Закупка дискретными циклами каждые N месяцев без ежемесячного задвоения</p>
                        </div>
                    </div>
                    <div class="h-[380px] relative"><canvas id="chartStock"></canvas></div>
                </div>
            </div>

            <!-- ЭТАП 3: ДЕНЕЖНЫЙ ПОТОК -->
            <div id="step-3" class="scroll-section-step p-4 lg:p-6 space-y-4">
                <div class="font-mono text-[10px] text-[#d4af37] tracking-[0.25em] uppercase flex items-center gap-2">
                    <span class="pulse-dot"></span> [ШАГ 04 // СТРУКТУРА ДЕНЕЖНОГО ПОТОКА (CASH FLOW)]
                </div>
                <div class="alche-block p-5 border">
                    <div class="flex justify-between items-center mb-4">
                        <div>
                            <h3 class="font-serif text-xl font-bold tracking-wide italic">Структура помесячного денежного потока</h3>
                            <p class="font-mono text-[10px] opacity-60">Сопоставление входящей выручки и совокупных выплат (закупки, аренда, ФОТ и налоги)</p>
                        </div>
                    </div>
                    <div class="h-[380px] relative"><canvas id="chartCF"></canvas></div>
                </div>
            </div>

            <!-- ЭТАП 4: ЮНИТ-ЭКОНОМИКА -->
            <div id="step-4" class="scroll-section-step p-4 lg:p-6 space-y-4 mb-24">
                <div class="font-mono text-[10px] text-[#d4af37] tracking-[0.25em] uppercase flex items-center gap-2">
                    <span class="pulse-dot"></span> [ШАГ 05 // ЮНИТ-ЭКОНОМИКА И ДИАГРАММА ЗАТРАТ]
                </div>
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
        </section>
    </div>
</div>

<script>
/* ========================================================
   WEB AUDIO API: ТАКТИЛЬНЫЙ АКУСТИЧЕСКИЙ ОТКЛИК
   ======================================================== */
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
    } catch (e) {}
}

/* ========================================================
   КАСТОМНЫЙ МАГНИТНЫЙ КУРСОР
   ======================================================== */
const cursorDot = document.getElementById('custom-cursor');
const cursorFollower = document.getElementById('custom-cursor-follower');
let mouseX = window.innerWidth / 2, mouseY = window.innerHeight / 2;
let followerX = mouseX, followerY = mouseY;

document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    cursorDot.style.left = `${mouseX}px`;
    cursorDot.style.top = `${mouseY}px`;
    
    const coordEl = document.getElementById('cursorCoordDisplay');
    if (coordEl) coordEl.textContent = `X: ${mouseX.toString().padStart(4, '0')} / Y: ${mouseY.toString().padStart(4, '0')}`;
});

function updateCursorFollower() {
    followerX += (mouseX - followerX) * 0.18;
    followerY += (mouseY - followerY) * 0.18;
    cursorFollower.style.left = `${followerX}px`;
    cursorFollower.style.top = `${followerY}px`;
    requestAnimationFrame(updateCursorFollower);
}
requestAnimationFrame(updateCursorFollower);

// Интерактивное масштабирование курсора при ховере
document.querySelectorAll('button, a, input, select, .hw-slider-track, .scroll-step-dot').forEach(el => {
    el.addEventListener('mouseenter', () => {
        cursorDot.style.transform = 'translate(-50%, -50%) scale(2.2)';
        cursorFollower.style.transform = 'translate(-50%, -50%) scale(1.6)';
        cursorFollower.style.borderColor = '#ffd700';
    });
    el.addEventListener('mouseleave', () => {
        cursorDot.style.transform = 'translate(-50%, -50%) scale(1)';
        cursorFollower.style.transform = 'translate(-50%, -50%) scale(1)';
        cursorFollower.style.borderColor = 'var(--accent-gold)';
    });
});

/* ========================================================
   ПРЕЛОАДЕР: ВИТРУВИАНЕЦ + ЖИДКИЙ ПЕРЕХОД
   ======================================================== */
let preloaderDismissed = false;
function dismissPreloader() {
    if (preloaderDismissed) return;
    preloaderDismissed = true;
    const stage = document.getElementById('preloader-stage');
    const app = document.getElementById('mainDashboardApp');
    if (app) { app.classList.remove('opacity-0'); app.classList.add('opacity-100'); }
    setTimeout(() => { 
        if (stage) stage.style.display = 'none'; 
        initScrollytelling();
    }, 600);
}

const PRELOADER_TOTAL_TIME = 15000;
const preloaderStartTime = performance.now();

setTimeout(() => {
    const pt = document.getElementById('preloaderTitle');
    if(pt) pt.classList.replace('opacity-0', 'opacity-100');
}, 1800);

let drawingCompleted = false;

function updatePreloaderProgress(now) {
    if (preloaderDismissed) return;
    const elapsed = now - preloaderStartTime;
    const progress = Math.min(elapsed / PRELOADER_TOTAL_TIME, 1);
    
    if (document.getElementById('loaderProgressBar')) {
        document.getElementById('loaderProgressBar').style.width = `${(progress * 100).toFixed(1)}%`;
        document.getElementById('loaderPercent').textContent = `${Math.floor(progress * 100)}%`;
    }
    
    if (progress >= 0.95 && !drawingCompleted) {
        drawingCompleted = true;
        const hud = document.getElementById('preloaderHUD');
        const btn = document.getElementById('exploreBtnWrapper');
        if (hud) hud.style.opacity = '0';
        if (btn) btn.classList.add('active');
    }
    
    if (progress < 1) requestAnimationFrame(updatePreloaderProgress);
}
requestAnimationFrame(updatePreloaderProgress);

const preCanvas = document.getElementById('preloader-webgl');
const preRenderer = new THREE.WebGLRenderer({ canvas: preCanvas, alpha: true, antialias: true, preserveDrawingBuffer: true });
preRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
preRenderer.setClearColor(0x000000, 0);
preRenderer.autoClear = false;

const preScene = new THREE.Scene();
const preCamera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 2000);
preCamera.position.z = 100;

const preArmillary = new THREE.Group();
preScene.add(preArmillary);

const preBlueMat = new THREE.MeshBasicMaterial({ color: 0x00aaff, wireframe: true, transparent: true, opacity: 0.25 });
const ringRadiuses = [35, 55, 75];
const rings = [];

ringRadiuses.forEach((radius, i) => {
    const geo = new THREE.TorusGeometry(radius, 6 + i*1.5, 40, 250);
    const ring = new THREE.Mesh(geo, preBlueMat);
    if (i === 0) ring.rotation.x = Math.PI / 2;
    if (i === 1) ring.rotation.y = Math.PI / 3;
    if (i === 2) ring.rotation.z = Math.PI / 4;
    preArmillary.add(ring);
    rings.push(ring);
});

const orthoScene = new THREE.Scene();
const orthoCamera = new THREE.OrthographicCamera(
    -window.innerWidth / 2, window.innerWidth / 2,
    window.innerHeight / 2, -window.innerHeight / 2,
    -100, 100
);

const maskTarget = new THREE.WebGLRenderTarget(1024, 1024, {
    minFilter: THREE.LinearFilter, magFilter: THREE.LinearFilter, format: THREE.RGBAFormat
});
preRenderer.setRenderTarget(maskTarget);
preRenderer.clear();
preRenderer.setRenderTarget(null);

const maskScene = new THREE.Scene();
const maskCamera = new THREE.OrthographicCamera(-0.5, 0.5, 0.5, -0.5, 0.1, 10);
maskCamera.position.z = 1;

const brushGeo = new THREE.PlaneGeometry(0.045, 0.045); 
const brushMat = new THREE.ShaderMaterial({
    transparent: true, depthWrite: false,
    vertexShader: `varying vec2 vUv; void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `varying vec2 vUv; void main() { 
        float d = distance(vUv, vec2(0.5)); 
        gl_FragColor = vec4(1.0, 1.0, 1.0, smoothstep(0.5, 0.05, d) * 0.45); 
    }`
});
const brushMesh = new THREE.Mesh(brushGeo, brushMat);
maskScene.add(brushMesh);

const vitruvianImg = new Image();
vitruvianImg.crossOrigin = "Anonymous"; 
vitruvianImg.src = "VITRUVIAN_IMAGE_SRC_PLACEHOLDER";
let vitruvianPlane = null, aspect = 1.0, drawPlaneWidth = 0, drawPlaneHeight = 0;

vitruvianImg.onload = () => {
    const canvasTexture = new THREE.Texture(vitruvianImg);
    canvasTexture.needsUpdate = true;
    aspect = vitruvianImg.height / vitruvianImg.width;
    
    const planeMaterial = new THREE.ShaderMaterial({
        uniforms: { 
            tDiffuse: { value: canvasTexture },
            tMask: { value: maskTarget.texture }
        },
        vertexShader: `varying vec2 vUv; void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
        fragmentShader: `
            uniform sampler2D tDiffuse;
            uniform sampler2D tMask;
            varying vec2 vUv;
            void main() {
                vec4 tex = texture2D(tDiffuse, vUv);
                vec4 mask = texture2D(tMask, vUv);
                tex.a *= mask.r; 
                gl_FragColor = tex;
            }
        `,
        transparent: true, depthWrite: false, side: THREE.DoubleSide
    });
    
    vitruvianPlane = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), planeMaterial);
    orthoScene.add(vitruvianPlane);
    resizePreloader(); 
};

function resizePreloader() {
    preRenderer.setSize(window.innerWidth, window.innerHeight);
    preCamera.aspect = window.innerWidth / window.innerHeight;
    preCamera.updateProjectionMatrix();
    
    orthoCamera.left = -window.innerWidth / 2;
    orthoCamera.right = window.innerWidth / 2;
    orthoCamera.top = window.innerHeight / 2;
    orthoCamera.bottom = -window.innerHeight / 2;
    orthoCamera.updateProjectionMatrix();
    
    if (vitruvianPlane) {
        drawPlaneHeight = window.innerHeight * 0.72;
        drawPlaneWidth = drawPlaneHeight / aspect;
        vitruvianPlane.scale.set(drawPlaneWidth, drawPlaneHeight, 1);
    }
}
window.addEventListener('resize', resizePreloader);

let isRippling = false;
let rippleScene, rippleCamera, rippleMaterial, rippleTime = 0;
const snapshotTarget = new THREE.WebGLRenderTarget(window.innerWidth, window.innerHeight);

function triggerLiquidTransition(event) {
    if (isRippling) return;
    isRippling = true;
    playClickSound(800, 0.08);

    const rect = event.target.getBoundingClientRect();
    const clickX = (rect.left + rect.width / 2) / window.innerWidth;
    const clickY = 1.0 - ((rect.top + rect.height / 2) / window.innerHeight);

    document.getElementById('exploreBtnWrapper').style.transition = 'opacity 0.3s ease';
    document.getElementById('exploreBtnWrapper').style.opacity = '0';
    document.getElementById('preloaderTitle').style.transition = 'opacity 0.4s ease';
    document.getElementById('preloaderTitle').style.opacity = '0';

    preRenderer.setRenderTarget(snapshotTarget);
    preRenderer.clear();
    preRenderer.render(preScene, preCamera);
    preRenderer.clearDepth();
    preRenderer.render(orthoScene, orthoCamera);
    preRenderer.setRenderTarget(null);

    rippleScene = new THREE.Scene();
    rippleCamera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);

    const quadGeo = new THREE.PlaneGeometry(2, 2);
    rippleMaterial = new THREE.ShaderMaterial({
        uniforms: {
            tDiffuse: { value: snapshotTarget.texture },
            uCenter: { value: new THREE.Vector2(clickX, clickY) },
            uProgress: { value: 0.0 },
            uAspect: { value: window.innerWidth / window.innerHeight }
        },
        vertexShader: `varying vec2 vUv; void main() { vUv = uv; gl_Position = vec4(position, 1.0); }`,
        fragmentShader: `
            uniform sampler2D tDiffuse;
            uniform vec2 uCenter;
            uniform float uProgress;
            uniform float uAspect;
            varying vec2 vUv;

            void main() {
                vec2 uv = vUv;
                vec2 aspectAdjustedUV = vec2(uv.x * uAspect, uv.y);
                vec2 aspectAdjustedCenter = vec2(uCenter.x * uAspect, uCenter.y);
                float dist = distance(aspectAdjustedUV, aspectAdjustedCenter);
                float waveRadius = uProgress * 2.2;
                float waveWidth = 0.35;
                float waveFactor = smoothstep(waveRadius - waveWidth, waveRadius, dist) * smoothstep(waveRadius + waveWidth, waveRadius, dist);
                float wave = sin((dist - waveRadius) * 35.0) * waveFactor * (1.0 - uProgress);
                vec2 dir = normalize(aspectAdjustedUV - aspectAdjustedCenter + 0.0001);
                
                vec2 offsetR = dir * wave * 0.085;
                vec2 offsetG = dir * wave * 0.070;
                vec2 offsetB = dir * wave * 0.055;
                
                float r = texture2D(tDiffuse, uv + offsetR).r;
                float g = texture2D(tDiffuse, uv + offsetG).g;
                float b = texture2D(tDiffuse, uv + offsetB).b;
                float fadeOut = smoothstep(0.0, 0.95, uProgress);
                gl_FragColor = vec4(r, g, b, (1.0 - fadeOut));
            }
        `,
        transparent: true
    });

    const quad = new THREE.Mesh(quadGeo, rippleMaterial);
    rippleScene.add(quad);
}

let drawStep = 0;
const penEl = document.getElementById('quillPen');

function animatePreloader() {
    if (preloaderDismissed) return;
    requestAnimationFrame(animatePreloader);
    
    const elapsed = performance.now() - preloaderStartTime;
    const t = elapsed * 0.001;
    const progress = Math.min(elapsed / PRELOADER_TOTAL_TIME, 1.0);
    
    if (isRippling) {
        rippleTime += 0.016;
        const ripProgress = Math.min(rippleTime / 1.3, 1.0);
        rippleMaterial.uniforms.uProgress.value = ripProgress;
        preRenderer.clear();
        preRenderer.render(rippleScene, rippleCamera);
        if (ripProgress >= 1.0) dismissPreloader();
        return;
    }
    
    rings[0].rotation.y += 0.0015 + Math.sin(t * 0.4) * 0.001;
    rings[0].rotation.x += 0.0005;
    rings[1].rotation.x -= 0.001 + Math.cos(t * 0.5) * 0.001;
    rings[1].rotation.z += 0.002;
    rings[2].rotation.z -= 0.0005 + Math.sin(t * 0.3) * 0.0015;
    rings[2].rotation.y += 0.0015;
    
    preCamera.position.z = 100 - (progress * 50);
    preCamera.position.x = Math.sin(progress * Math.PI) * 10;
    preCamera.position.y = Math.cos(progress * Math.PI * 1.5) * 8;
    preCamera.lookAt(0, 0, -20);
    
    if (vitruvianPlane) {
        let px = 0, py = 0;
        if (progress <= 0.86) {
            for (let sub = 0; sub < 4; sub++) {
                drawStep += 0.016;
                const pTime = drawStep * 1.8;
                px = Math.sin(pTime) * 0.28 + Math.sin(pTime * 3.7) * 0.12;
                py = Math.cos(pTime * 0.85) * 0.34 + Math.sin(pTime * 2.1) * 0.09;
                brushMesh.position.set(px, py, 0);
                preRenderer.setRenderTarget(maskTarget);
                preRenderer.render(maskScene, maskCamera);
                preRenderer.setRenderTarget(null);
            }
        } else {
            brushMesh.scale.set(30, 30, 1);
            brushMesh.position.set(0, 0, 0);
            preRenderer.setRenderTarget(maskTarget);
            preRenderer.render(maskScene, maskCamera);
            preRenderer.setRenderTarget(null);
        }
        
        if (progress < 0.88) {
            penEl.style.opacity = 1;
            const penX = window.innerWidth / 2 + (px * drawPlaneWidth);
            const penY = window.innerHeight / 2 - (py * drawPlaneHeight);
            penEl.style.transform = `translate3d(${penX}px, ${penY}px, 0) rotate(${Math.sin(drawStep * 6) * 18 - 12}deg)`;
        } else {
            penEl.style.opacity = 0; 
        }
    }
    
    preRenderer.clear();
    preRenderer.render(preScene, preCamera);
    preRenderer.clearDepth(); 
    preRenderer.render(orthoScene, orthoCamera);
}
animatePreloader();

/* ========================================================
   ОСНОВНОЙ ФОН: THREE.JS С ПРИВЯЗКОЙ К СКРОЛЛУ
   ======================================================== */
const canvas = document.getElementById('webgl-bg-canvas');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 2000);
camera.position.z = 150;

const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

const armillaryGroup = new THREE.Group();
scene.add(armillaryGroup);

let ringColor = 0x00aaff;
const ringMat = new THREE.MeshBasicMaterial({ color: ringColor, wireframe: true, transparent: true, opacity: 0.14 });

const mainRings = [];
ringRadiuses.forEach((radius, i) => {
    const geo = new THREE.TorusGeometry(radius + 20, 8 + i*2, 40, 250);
    const ring = new THREE.Mesh(geo, ringMat);
    if (i === 0) ring.rotation.x = Math.PI / 2;
    if (i === 1) ring.rotation.y = Math.PI / 3;
    if (i === 2) ring.rotation.z = Math.PI / 4;
    armillaryGroup.add(ring);
    mainRings.push(ring);
});

let scrollProgressTarget = 0;
let currentScrollProgress = 0;

// Магнитный эффект 3D-наклона карточек за мышью
document.querySelectorAll('.tilt-card').forEach(card => {
    card.addEventListener('mousemove', e => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        card.style.setProperty('--mouse-x', `${x}px`);
        card.style.setProperty('--mouse-y', `${y}px`);
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = ((y - centerY) / centerY) * -6;
        const rotateY = ((x - centerX) / centerX) * 6;
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-3px) scale(1.01)`;
    });
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px) scale(1)';
    });
});

function animate() {
    requestAnimationFrame(animate);
    currentScrollProgress += (scrollProgressTarget - currentScrollProgress) * 0.06;
    
    mainRings[0].rotation.y += 0.001;
    mainRings[1].rotation.x -= 0.0015;
    mainRings[2].rotation.z += 0.0008;

    armillaryGroup.rotation.y = currentScrollProgress * Math.PI * 1.6;
    armillaryGroup.rotation.x = currentScrollProgress * 0.75;
    
    const t = performance.now() * 0.0002;
    const normX = (mouseX - window.innerWidth / 2) * 0.0006;
    const normY = (mouseY - window.innerHeight / 2) * 0.0006;
    
    const baseX = Math.sin(t) * 70 + (currentScrollProgress * 50);
    const baseY = Math.sin(t * 0.8) * 45 - (currentScrollProgress * 70);
    const baseZ = 150 - (currentScrollProgress * 40);
    
    camera.position.x += (baseX + normX * 35 - camera.position.x) * 0.05;
    camera.position.y += (baseY - normY * 35 - camera.position.y) * 0.05;
    camera.position.z += (baseZ - camera.position.z) * 0.05;
    camera.lookAt(scene.position);
    renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

/* ========================================================
   LENIS + SCROLLTRIGGER: SCROLLYTELLING ALCHE STUDIO
   ======================================================== */
let lenisInstance = null;

function initScrollytelling() {
    gsap.registerPlugin(ScrollTrigger);

    lenisInstance = new Lenis({
        duration: 1.3,
        easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
        smooth: true,
        direction: 'vertical'
    });

    lenisInstance.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((time) => {
        lenisInstance.raf(time * 1000);
    });
    gsap.ticker.lagSmoothing(0);

    const steps = [
        document.getElementById('step-0'),
        document.getElementById('step-1'),
        document.getElementById('step-2'),
        document.getElementById('step-3'),
        document.getElementById('step-4')
    ];

    steps.forEach((step, idx) => {
        if (!step) return;

        ScrollTrigger.create({
            trigger: step,
            start: "top 72%",
            end: "bottom 28%",
            onEnter: () => activateStep(idx),
            onEnterBack: () => activateStep(idx),
            onUpdate: (self) => {
                if (self.isActive) {
                    scrollProgressTarget = (idx + self.progress) / steps.length;
                }
            }
        });
    });

    ScrollTrigger.create({
        start: 0,
        end: "max",
        onUpdate: (self) => {
            scrollProgressTarget = self.progress;
        }
    });
}

function activateStep(index) {
    playClickSound(1600 - index * 120, 0.02);
    
    document.querySelectorAll('.scroll-step-dot').forEach((dot, i) => {
        dot.classList.toggle('active', i === index);
    });

    for (let i = 0; i <= 4; i++) {
        const el = document.getElementById(`step-${i}`);
        if (!el) continue;
        if (i === index) {
            el.classList.add('in-focus');
            const headings = el.querySelectorAll('h3');
            headings.forEach(h => {
                const orig = h.getAttribute('data-original-text') || h.textContent;
                h.setAttribute('data-original-text', orig);
                scrambleElementText(h, orig, 460, true);
            });
        } else {
            el.classList.remove('in-focus');
        }
    }
}

function scrollToStep(stepIndex) {
    const target = document.getElementById(`step-${stepIndex}`);
    if (target && lenisInstance) {
        lenisInstance.scrollTo(target, { offset: -85, duration: 1.4 });
    }
}

/* ========================================================
   ТЕМА И СТИЛИЗАЦИЯ
   ======================================================== */
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
        ringMat.color.setHex(0x00aaff);
        preBlueMat.color.setHex(0x00aaff);
    } else {
        thumb.style.transform = 'translateX(62px)';
        lblDay.className = 'relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold text-white';
        lblNight.className = 'relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold opacity-70';
        ringMat.color.setHex(0x0055aa);
        preBlueMat.color.setHex(0x0055aa);
    }
    playClickSound(900, 0.03);
    runCalculation();
}

/* ========================================================
   ГЛИФ-ДЕКОДЕР (SCRAMBLE EFFECT)
   ======================================================== */
const CYRILLIC_GLYPHS = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ0123456789§$%*#@!/[]:;';
const NUMERIC_GLYPHS = '0123456789 ';
function scrambleElementText(el, finalText, duration = 460, useAlphabet = true) {
    if (!el) return;
    const glyphs = useAlphabet ? CYRILLIC_GLYPHS : NUMERIC_GLYPHS;
    const start = performance.now();
    const len = finalText.length;
    if (el._scrambleTimer) cancelAnimationFrame(el._scrambleTimer);
    function update(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const revealIdx = Math.floor(progress * len);
        let out = '';
        for (let i = 0; i < len; i++) {
            const char = finalText[i];
            if (i < revealIdx || char === ' ' || char === '₽' || char === '%' || char === '.' || char === ',' || char === '(' || char === ')' || char === '/' || char === '[' || char === ']' || char === ':') out += char;
            else out += glyphs[Math.floor(Math.random() * glyphs.length)];
        }
        el.textContent = out;
        if (progress < 1) el._scrambleTimer = requestAnimationFrame(update);
        else el._scrambleTimer = null;
    }
    el._scrambleTimer = requestAnimationFrame(update);
}
function scrambleNumber(el, finalStr, duration = 400) { scrambleElementText(el, finalStr, duration, false); }

let growthMode = 'abs';
function setGrowthMode(mode) {
    playClickSound(950, 0.02);
    growthMode = mode;
    const btnAbs = document.getElementById('btnModeAbs');
    const btnPct = document.getElementById('btnModePct');
    const title = document.getElementById('lblGrowthModeTitle');
    const slider = document.getElementById('paramGrowthSlider');
    if (mode === 'abs') {
        btnAbs.className = 'py-1 font-mono text-[9px] uppercase tracking-wider bg-[#d4af37] text-black font-bold transition';
        btnPct.className = 'py-1 font-mono text-[9px] uppercase tracking-wider opacity-60 hover:opacity-100 transition';
        title.textContent = 'ПРИРОСТ В МЕСЯЦ'; slider.max = 100; slider.value = 5;
    } else {
        btnPct.className = 'py-1 font-mono text-[9px] uppercase tracking-wider bg-[#d4af37] text-black font-bold transition';
        btnAbs.className = 'py-1 font-mono text-[9px] uppercase tracking-wider opacity-60 hover:opacity-100 transition';
        title.textContent = 'ПРИРОСТ В %'; slider.max = 50; slider.value = 10;
    }
    runCalculation();
}

function parseCleanNum(val) { return typeof val === 'number' ? val : parseFloat(String(val).replace(/[^\d.-]/g, '')) || 0; }
function formatSpaced(num) { return Math.round(num).toLocaleString('ru-RU').replace(/,/g, ' '); }
function formatInput(input) { input.value = formatSpaced(parseCleanNum(input.value)); }

let chartDebtInstance = null, chartStockInstance = null, chartCFInstance = null, chartOrdersInstance = null, chartPieInstance = null, latestCalculatedData = null;

function runCalculation() {
    const startMonth = parseInt(document.getElementById('paramStartMonth').value);
    const startYear = parseInt(document.getElementById('paramStartYear').value);
    const period = parseInt(document.getElementById('paramPeriod').value);
    const vatRate = parseFloat(document.getElementById('paramVatRate').value);
    const vatMultiplier = 1 + (vatRate / 100);
    const marginPct = parseFloat(document.getElementById('paramMargin').value);
    document.getElementById('lblMarginVal').textContent = `${marginPct}%`;
    const initialPurchase = parseCleanNum(document.getElementById('paramInitialPurchase').value);
    const batchCycle = parseInt(document.getElementById('paramBatchCycle').value) || 5;
    const cbRate = parseFloat(document.getElementById('paramCbRate').value) || 17;
    const commMargin = parseFloat(document.getElementById('paramCommMargin').value) || 2;
    const totalRateAnnual = cbRate + commMargin;
    const monthlyRate = (totalRateAnnual / 100) / 12;
    document.getElementById('telemetryRate').textContent = `[КАПИТАЛ: ${totalRateAnnual.toFixed(1)}% ГОДОВЫХ]`;
    document.getElementById('kpiRateSub').textContent = `Ставка ${totalRateAnnual.toFixed(1)}%`;
    const aov = parseCleanNum(document.getElementById('paramAov').value);
    const startOrders = parseInt(document.getElementById('paramStartOrders').value) || 40;
    const growthVal = parseFloat(document.getElementById('paramGrowthSlider').value);
    document.getElementById('lblGrowthVal').textContent = growthMode === 'abs' ? `+${growthVal} шт.` : `+${growthVal}%`;
    const maxOrdersCap = parseInt(document.getElementById('paramMaxOrdersCap').value) || 300;
    const fot = parseCleanNum(document.getElementById('paramFot').value);
    const wh = parseCleanNum(document.getElementById('paramWh').value);
    const office = parseCleanNum(document.getElementById('paramOffice').value);
    const prepPct = parseFloat(document.getElementById('paramPrepaymentPct').value);
    document.getElementById('lblPrepVal').textContent = `${prepPct}%`;
    const factShare = parseFloat(document.getElementById('paramFactoringShare').value);
    document.getElementById('lblFactShareVal').textContent = `${factShare}%`;
    const factAdvance = 0.8;
    const shortMonths = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'];
    const xLabels = [], orders = [], rev = [];
    
    for (let i = 0; i < period; i++) {
        const mIdx = (startMonth + i) % 12;
        const yOff = Math.floor((startMonth + i) / 12);
        xLabels.push(`${shortMonths[mIdx]} ${startYear + yOff}`);
        let curOrders = i === 0 ? startOrders : (growthMode === 'abs' ? orders[i - 1] + growthVal : orders[i - 1] * (1 + growthVal / 100));
        curOrders = Math.min(curOrders, maxOrdersCap);
        orders.push(curOrders);
        rev.push(curOrders * aov);
    }
    
    const cogsPct = 1 - (marginPct / 100);
    const cogsVat = rev.map(r => r * cogsPct * vatMultiplier);
    const cogsPayments = new Array(period).fill(0);
    const inventoryDeliveries = new Array(period).fill(0);
    cogsPayments[0] += initialPurchase * (prepPct / 100);
    if (1 < period) cogsPayments[1] += initialPurchase * ((100 - prepPct) / 100);
    inventoryDeliveries[0] = initialPurchase;
    
    for (let b = batchCycle; b < period; b += batchCycle) {
        const bEnd = Math.min(b + batchCycle, period);
        let batchTotal = 0;
        for (let k = b; k < bEnd; k++) batchTotal += cogsVat[k];
        inventoryDeliveries[b] = batchTotal;
        cogsPayments[b] += batchTotal * (prepPct / 100);
        if (b + 1 < period) cogsPayments[b + 1] += batchTotal * ((100 - prepPct) / 100);
    }
    
    const inventoryBalance = [];
    let curStock = 0;
    for (let i = 0; i < period; i++) {
        curStock += inventoryDeliveries[i] - cogsVat[i];
        inventoryBalance.push(Math.max(curStock, 0));
    }
    
    const inflows = new Array(period).fill(0);
    for (let i = 0; i < period; i++) {
        const invVat = rev[i] * vatMultiplier;
        inflows[i] += invVat * (factShare / 100) * factAdvance;
        const targetM = i + 2;
        if (targetM < period) {
            inflows[targetM] += invVat * ((100 - factShare) / 100);
            inflows[targetM] += invVat * (factShare / 100) * (1 - factAdvance);
        }
    }
    
    const opex = [], taxes = rev.map(r => r * 0.05), baseOutflows = [];
    for (let i = 0; i < period; i++) {
        const base = 150000 + wh + office + fot;
        opex.push(i >= 6 ? base * 1.2 : base);
        baseOutflows.push(cogsPayments[i] + opex[i] + taxes[i]);
    }
    
    const monthlyInvestments = new Array(period).fill(0), interestPayments = new Array(period).fill(0), debtRepayments = new Array(period).fill(0), debtBalance = new Array(period).fill(0), cashBalance = new Array(period).fill(0);
    let currentDebt = 0, currentCash = 0;
    for (let i = 0; i < period; i++) {
        const interestDue = currentDebt * monthlyRate;
        interestPayments[i] = interestDue;
        const netBeforeFin = inflows[i] - (baseOutflows[i] + interestDue);
        const potCash = currentCash + netBeforeFin;
        if (potCash < 0) {
            const needed = Math.abs(potCash);
            monthlyInvestments[i] = needed;
            currentDebt += needed;
            currentCash = 0;
            debtRepayments[i] = 0;
        } else {
            monthlyInvestments[i] = 0;
            const repay = Math.min(potCash, currentDebt);
            debtRepayments[i] = repay;
            currentDebt -= repay;
            currentCash = potCash - repay;
        }
        debtBalance[i] = currentDebt;
        cashBalance[i] = currentCash;
    }
    
    const sumRev = rev.reduce((a, b) => a + b, 0), sumInvestments = monthlyInvestments.reduce((a, b) => a + b, 0), sumInterest = interestPayments.reduce((a, b) => a + b, 0), maxDebt = Math.max(...debtBalance), sumOpex = opex.reduce((a, b) => a + b, 0), sumTaxes = taxes.reduce((a, b) => a + b, 0);
    const netProfit = sumRev * (marginPct / 100) - sumOpex - sumTaxes - sumInterest;
    const roi = sumRev > 0 ? (netProfit / sumRev) * 100 : 0;
    
    latestCalculatedData = { xLabels, monthlyInvestments, interestPayments, debtRepayments, debtBalance, cashBalance, sumRev, netProfit, roi };
    
    scrambleNumber(document.getElementById('kpiRev'), `${formatSpaced(sumRev)} ₽`);
    scrambleNumber(document.getElementById('kpiInjections'), `${formatSpaced(sumInvestments)} ₽`);
    scrambleNumber(document.getElementById('kpiInterest'), `${formatSpaced(sumInterest)} ₽`);
    scrambleNumber(document.getElementById('kpiMaxDebt'), `${formatSpaced(maxDebt)} ₽`);
    scrambleNumber(document.getElementById('kpiProfit'), `${formatSpaced(netProfit)} ₽`);
    document.getElementById('kpiRoiSub').textContent = `Рентабельность: ${roi.toFixed(1)}%`;
    
    const tbody = document.getElementById('tableDebtBody');
    tbody.innerHTML = '';
    for (let i = 0; i < period; i++) {
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-[var(--bg-cell-hover)] transition';
        tr.innerHTML = `<td class="p-3 font-bold">${xLabels[i]}</td><td class="p-3 text-[#e63946]">${formatSpaced(monthlyInvestments[i])} ₽</td><td class="p-3 text-[#d4af37]">${formatSpaced(interestPayments[i])} ₽</td><td class="p-3 text-[#2a9d8f]">${formatSpaced(debtRepayments[i])} ₽</td><td class="p-3 font-bold">${formatSpaced(debtBalance[i])} ₽</td><td class="p-3">${formatSpaced(cashBalance[i])} ₽</td>`;
        tbody.appendChild(tr);
    }
    
    const chartText = isDark ? '#8e8a80' : '#6b665c';
    const chartGrid = isDark ? 'rgba(212, 175, 55, 0.08)' : 'rgba(184, 134, 11, 0.12)';
    
    if (chartDebtInstance) chartDebtInstance.destroy();
    chartDebtInstance = new Chart(document.getElementById('chartDebt').getContext('2d'), {
        type: 'bar',
        data: {
            labels: xLabels,
            datasets: [
                { label: 'Проценты за месяц', data: interestPayments, backgroundColor: '#d4af37', order: 2 },
                { label: 'Остаток тела долга', data: debtBalance, type: 'line', borderColor: '#e63946', backgroundColor: '#e63946', borderWidth: 2.5, yAxisID: 'y1', tension: 0.3, order: 1 }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { grid: { display: false }, ticks: { color: chartText, font: { family: 'JetBrains Mono', size: 10 } } },
                y: { grid: { color: chartGrid }, ticks: { color: chartText, font: { family: 'JetBrains Mono', size: 10 } } },
                y1: { position: 'right', grid: { display: false }, ticks: { color: '#e63946', font: { family: 'JetBrains Mono', size: 10 } } }
            },
            plugins: { legend: { labels: { color: chartText, font: { family: 'JetBrains Mono', size: 11 } } } }
        }
    });

    if (chartStockInstance) chartStockInstance.destroy();
    chartStockInstance = new Chart(document.getElementById('chartStock').getContext('2d'), {
        type: 'bar',
        data: {
            labels: xLabels,
            datasets: [
                { label: 'Оплата партии поставщику', data: cogsPayments, backgroundColor: isDark ? '#52525b' : '#cbd5e1', order: 2 },
                { label: 'Остаток склада', data: inventoryBalance, type: 'line', borderColor: '#d4af37', borderWidth: 2.5, yAxisID: 'y1', tension: 0.3, order: 1 }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { grid: { display: false }, ticks: { color: chartText, font: { family: 'JetBrains Mono', size: 10 } } },
                y: { grid: { color: chartGrid }, ticks: { color: chartText, font: { family: 'JetBrains Mono', size: 10 } } },
                y1: { position: 'right', grid: { display: false }, ticks: { color: '#d4af37', font: { family: 'JetBrains Mono', size: 10 } } }
            },
            plugins: { legend: { labels: { color: chartText, font: { family: 'JetBrains Mono', size: 11 } } } }
        }
    });

    const totalOutflows = baseOutflows.map((b, idx) => b + interestPayments[idx]);
    if (chartCFInstance) chartCFInstance.destroy();
    chartCFInstance = new Chart(document.getElementById('chartCF').getContext('2d'), {
        type: 'bar',
        data: {
            labels: xLabels,
            datasets: [
                { label: 'Притоки от продаж', data: inflows, backgroundColor: '#2a9d8f' },
                { label: 'Выплаты (закупки + OPEX + %)', data: totalOutflows.map(v => -v), backgroundColor: '#e63946' }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { grid: { display: false }, ticks: { color: chartText, font: { family: 'JetBrains Mono', size: 10 } } },
                y: { grid: { color: chartGrid }, ticks: { color: chartText, font: { family: 'JetBrains Mono', size: 10 } } }
            },
            plugins: { legend: { labels: { color: chartText, font: { family: 'JetBrains Mono', size: 11 } } } }
        }
    });

    if (chartOrdersInstance) chartOrdersInstance.destroy();
    chartOrdersInstance = new Chart(document.getElementById('chartOrders').getContext('2d'), {
        type: 'bar',
        data: {
            labels: xLabels,
            datasets: [
                { label: 'Заказы, шт.', data: orders, backgroundColor: '#d4af37' },
                { label: 'Выручка, ₽', data: rev, type: 'line', borderColor: '#2a9d8f', yAxisID: 'y1', borderWidth: 2.5 }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { grid: { display: false }, ticks: { color: chartText, font: { family: 'JetBrains Mono', size: 10 } } },
                y: { grid: { color: chartGrid }, ticks: { color: chartText, font: { family: 'JetBrains Mono', size: 10 } } },
                y1: { position: 'right', grid: { display: false }, ticks: { color: '#2a9d8f', font: { family: 'JetBrains Mono', size: 10 } } }
            },
            plugins: { legend: { labels: { color: chartText, font: { family: 'JetBrains Mono', size: 11 } } } }
        }
    });

    const sumPurchases = cogsPayments.reduce((a, b) => a + b, 0);
    if (chartPieInstance) chartPieInstance.destroy();
    chartPieInstance = new Chart(document.getElementById('chartPie').getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: ['Склад', 'Офис', 'ФОТ', 'Налоги 5%', 'Закупки', 'Проценты по долгу'],
            datasets: [{
                data: [wh * period, office * period, fot * period, sumTaxes, sumPurchases, sumInterest],
                backgroundColor: ['#52525b', '#71717a', '#d4af37', '#e63946', '#2a9d8f', '#457b9d']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom', labels: { color: chartText, font: { family: 'JetBrains Mono', size: 10 } } } }
        }
    });
}

function exportDataToCsv() {
    playClickSound(1600, 0.05);
    if (!latestCalculatedData) return;
    const { xLabels, monthlyInvestments, interestPayments, debtRepayments, debtBalance, cashBalance } = latestCalculatedData;
    let csvContent = "data:text/csv;charset=utf-8,\uFEFF";
    csvContent += "Период;Дотация (дефицит);Проценты по долгу;Погашение долга;Остаток тела долга;Свободный остаток счета\n";
    for (let i = 0; i < xLabels.length; i++) csvContent += `${xLabels[i]};${Math.round(monthlyInvestments[i])};${Math.round(interestPayments[i])};${Math.round(debtRepayments[i])};${Math.round(debtBalance[i])};${Math.round(cashBalance[i])}\n`;
    const link = document.createElement("a"); link.setAttribute("href", encodeURI(csvContent)); link.setAttribute("download", "Finansovaya_Model_Kapital.csv"); document.body.appendChild(link); link.click(); document.body.removeChild(link);
}

setInterval(() => { 
    const clock = document.getElementById('telemetryClock');
    if (clock) clock.textContent = `[${new Date().toTimeString().split(' ')[0]}]`; 
}, 1000);

function resetDefaults() { playClickSound(600, 0.05); document.getElementById('financialInputsForm').reset(); runCalculation(); }
window.onload = () => runCalculation();
</script>
</body>
</html>"""

img_src = get_blueprint_vitruvian("1000400438.jpg")
html_code = html_code.replace("VITRUVIAN_IMAGE_SRC_PLACEHOLDER", img_src)

components.html(html_code, height=1350, scrolling=True)
