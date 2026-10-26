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

img_files = [
    "1793030578548.jpg",
    "1793030581888.jpg",
    "1793030587821.jpg",
    "1793030589564.jpg",
    "1793030590445.jpg"
]
b64_images = [get_image_b64(f) for f in img_files]
json_images_payload = json.dumps(b64_images)

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

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="ru" class="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Архитектура Капитала</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600;1,700&family=JetBrains+Mono:ital,wght@0,300;0,400;0,500;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com/3.4.1"></script>
<script>tailwind.config={darkMode:'class',theme:{extend:{fontFamily:{serif:['"Cormorant Garamond"','Georgia','serif'],mono:['"JetBrains Mono"','monospace'],sans:['"Inter"','system-ui','sans-serif']},colors:{obsidian:'#070709',obsidianCard:'#0d0d12',alabaster:'#f4f1ea',gold:'#d4af37',vermilion:'#e63946',jade:'#2a9d8f'}}}}</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
:root{--bg-space:#070709;--bg-panel:rgba(13,13,18,.85);--bg-cell-hover:rgba(24,24,34,.95);--text-main:#f4f1ea;--text-muted:#8e8a80;--border-line:rgba(212,175,55,.16);--border-accent:rgba(212,175,55,.6);--accent-gold:#d4af37;--accent-vermilion:#e63946;--accent-jade:#2a9d8f;--input-bg:rgba(255,255,255,.025);--cursor-glow:rgba(212,175,55,.2);--table-header-bg:rgba(13,13,18,.98);--grain-opacity:.035}
html:not(.dark){--bg-space:#f4f1ea;--bg-panel:rgba(255,255,255,.92);--bg-cell-hover:rgba(246,243,235,.98);--text-main:#141416;--text-muted:#6b665c;--border-line:rgba(184,134,11,.22);--border-accent:rgba(184,134,11,.75);--accent-gold:#b8860b;--accent-vermilion:#c5221f;--accent-jade:#1d756b;--input-bg:rgba(0,0,0,.03);--cursor-glow:rgba(184,134,11,.15);--table-header-bg:rgba(244,241,234,.98);--grain-opacity:.02}
*{box-sizing:border-box;border-color:var(--border-line);margin:0;padding:0;scrollbar-width:thin;scrollbar-color:var(--border-line) transparent}
html,body{width:100%;height:100%;margin:0;padding:0;overflow:hidden;background:var(--bg-space);color:var(--text-main);font-family:'JetBrains Mono',monospace;-webkit-tap-highlight-color:transparent}
:focus-visible{outline:2px solid var(--accent-gold);outline-offset:2px}
button:focus:not(:focus-visible){outline:none}
.film-grain{position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;z-index:999;opacity:var(--grain-opacity);background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}

#shutter-flash{
    position:fixed;
    inset:0;
    width:100vw;
    height:100vh;
    background:#f4f1ea;
    z-index:950;
    pointer-events:none;
    opacity:0;
}

#preloader-stage{position:fixed;top:0;left:0;width:100vw;height:100vh;background:radial-gradient(circle at center,#0d0e17 0%,#030306 100%);z-index:900;overflow:hidden;touch-action:none}
#preloader-webgl{position:absolute;inset:0;width:100%;height:100%;z-index:10;cursor:grab}
#preloader-webgl:active{cursor:grabbing}

.preloader-fixed-hud{position:absolute;inset:0;width:100%;height:100%;z-index:30;pointer-events:none;user-select:none;transition:opacity 0.6s ease}
#preloaderTitle{position:absolute;top:26px;left:50%;transform:translateX(-50%);font-family:'Cormorant Garamond',Georgia,serif;font-style:italic;font-size:clamp(20px,3.2vw,44px);font-weight:700;letter-spacing:.26em;color:var(--accent-gold);opacity:0;text-shadow:0 0 45px rgba(212,175,55,.85);transition:opacity 1.8s cubic-bezier(.16,1,.3,1);text-align:center;white-space:nowrap}
#preloaderTitle.locked-on{opacity:1!important}

#blueprintSubtitle{position:absolute;top:74px;left:50%;transform:translateX(-50%);font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:0.24em;text-transform:uppercase;color:rgba(212,175,55,0.85);opacity:0;transition:opacity 0.5s ease;text-align:center;white-space:nowrap;max-width:90vw}

.slider-ui-container{position:absolute;top:50%;left:0;width:100%;transform:translateY(-50%);display:flex;justify-content:space-between;align-items:center;padding:0 18px;pointer-events:none;z-index:40}
.slide-nav-btn{width:48px;height:48px;border-radius:50%;background:rgba(13,13,18,0.8);border:1px solid rgba(212,175,55,0.5);color:var(--accent-gold);display:flex;align-items:center;justify-content:center;font-size:24px;cursor:pointer;pointer-events:auto;backdrop-filter:blur(10px);transition:all .25s ease}
.slide-nav-btn:hover{background:rgba(212,175,55,0.3);border-color:var(--accent-gold);transform:scale(1.08)}
.slide-nav-btn:active{transform:scale(0.96)}

.slide-dots{position:absolute;bottom:102px;left:50%;transform:translateX(-50%);display:flex;gap:12px;pointer-events:auto;z-index:40}
.slide-dot{width:9px;height:9px;border-radius:50%;border:1px solid var(--accent-gold);background:transparent;cursor:pointer;transition:all .3s ease}
.slide-dot.active{background:var(--accent-gold);box-shadow:0 0 12px var(--accent-gold);transform:scale(1.35)}

.bottom-dock{position:absolute;bottom:30px;left:50%;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;justify-content:center;width:400px;height:64px}
#preloaderHUD{display:flex;flex-direction:column;align-items:center;gap:8px;transition:opacity .4s}
.progress-bar-bg{width:290px;height:2px;background:rgba(255,255,255,.12);position:relative;overflow:hidden}
#loaderProgressBar{position:absolute;left:0;top:0;height:100%;width:0;background:var(--accent-gold);box-shadow:0 0 10px var(--accent-gold);transition:width .1s linear}

#exploreBtnWrapper{position:absolute;opacity:0;pointer-events:none;transition:opacity .6s cubic-bezier(.19,1,.22,1),transform .6s cubic-bezier(.19,1,.22,1);transform:translateY(8px);display:flex;gap:12px}
#exploreBtnWrapper.active{opacity:1;pointer-events:auto;transform:translateY(0)}
.explore-btn{padding:12px 34px;background:rgba(13,13,18,.9);border:1px solid rgba(212,175,55,.95);color:#f4f1ea;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.32em;text-transform:uppercase;cursor:pointer;backdrop-filter:blur(14px);overflow:hidden;transition:all .3s;box-shadow:0 0 40px rgba(212,175,55,.35),inset 0 0 16px rgba(212,175,55,.18)}
.explore-btn:hover{border-color:#ffd700;color:#ffd700;box-shadow:0 0 60px rgba(212,175,55,.7),inset 0 0 24px rgba(212,175,55,.35);transform:scale(1.04)}

.preset-btn{padding:12px 20px;background:rgba(212,175,55,0.12);border:1px solid var(--accent-gold);color:var(--accent-gold);font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:0.2em;text-transform:uppercase;cursor:pointer;backdrop-filter:blur(10px);transition:all .3s}
.preset-btn:hover{background:var(--accent-gold);color:#070709}

#mainDashboardApp{display:none;position:relative;z-index:10;min-height:100vh}
#mainDashboardApp.ready{display:flex}

.camera-obscura-reveal {
    animation: developNegative 2.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes developNegative {
    0% {
        opacity: 0.95;
        filter: invert(1) grayscale(1) contrast(1.7) brightness(1.2);
        transform: scale(1.015);
    }
    35% {
        opacity: 1;
        filter: invert(0.85) sepia(0.6) contrast(1.4) brightness(1.1);
    }
    70% {
        filter: invert(0.2) sepia(0.25) contrast(1.1) brightness(1.02);
    }
    100% {
        opacity: 1;
        filter: invert(0) sepia(0) contrast(1) brightness(1);
        transform: scale(1);
    }
}

#webgl-bg-canvas{position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:0;pointer-events:none;opacity:.35}
html:not(.dark) #webgl-bg-canvas{opacity:.18}
.alche-block{position:relative;background:var(--bg-panel);backdrop-filter:blur(20px);border-right:1px solid var(--border-line);border-bottom:1px solid var(--border-line)}
.cross-tl::before{content:'+';position:absolute;top:-6px;left:-4px;font-family:'JetBrains Mono',monospace;font-size:10px;line-height:1;color:var(--accent-gold);pointer-events:none;z-index:10}
.cross-br::after{content:'+';position:absolute;bottom:-6px;right:-4px;font-family:'JetBrains Mono',monospace;font-size:10px;line-height:1;color:var(--accent-gold);pointer-events:none;z-index:10}
.tilt-card{position:relative;overflow:hidden;transform-style:preserve-3d;perspective:1000px;transition:transform .25s cubic-bezier(.2,0,.2,1),border-color .3s}
.tilt-card::before{content:'';position:absolute;inset:-1px;border:1px solid transparent;background:radial-gradient(350px circle at var(--mouse-x,0) var(--mouse-y,0),var(--cursor-glow),transparent 75%);opacity:0;transition:opacity .4s;pointer-events:none;z-index:2}
.tilt-card:hover::before{opacity:1}
.tab-view-enter{animation:tabEntrance .6s cubic-bezier(.19,1,.22,1) forwards}
@keyframes tabEntrance{0%{opacity:0;filter:blur(8px);transform:translateY(8px)}100%{opacity:1;filter:blur(0);transform:translateY(0)}}
input[type="range"]{-webkit-appearance:none;appearance:none;width:100%;height:2px;background:var(--border-line);outline:none}
input[type="range"]::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:12px;height:12px;background:var(--accent-gold);cursor:pointer;border:1px solid var(--bg-space);transform:rotate(45deg);transition:transform .2s}
input[type="range"]::-webkit-slider-thumb:hover{transform:rotate(45deg) scale(1.4)}
.mono-input{background:var(--input-bg);border:1px solid var(--border-line);color:var(--text-main);font-family:'JetBrains Mono',monospace;font-size:11px;padding:6px 9px;width:100%;border-radius:0;outline:none;transition:border-color .2s}
.mono-input:focus{border-color:var(--accent-gold);background:rgba(212,175,55,.06)}
select.mono-input option{background:#0d0d12;color:#f4f1ea}
.hw-slider-track{position:relative;width:130px;height:28px;border:1px solid var(--border-line);background:var(--input-bg);display:flex;align-items:center;justify-content:space-between;padding:0 10px;cursor:pointer;user-select:none}
.hw-slider-thumb{position:absolute;top:2px;bottom:2px;width:62px;background:var(--accent-gold);transition:transform .45s cubic-bezier(.19,1,.22,1)}
.pulse-dot{display:inline-block;width:6px;height:6px;border-radius:9999px;background:var(--accent-gold);animation:pulseAnim 2s infinite ease-in-out}
@keyframes pulseAnim{0%,100%{opacity:.4;transform:scale(.9)}50%{opacity:1;transform:scale(1.2)}}
::-webkit-scrollbar{width:4px;height:4px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--border-line)}
::-webkit-scrollbar-thumb:hover{background:var(--accent-gold)}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}
</style>
</head>
<body class="selection:bg-[#d4af37] selection:text-black">
<div class="film-grain" aria-hidden="true"></div>
<div id="shutter-flash"></div>

<!-- ПРЕЛОАДЕР -->
<div id="preloader-stage">
    <canvas id="preloader-webgl"></canvas>
    
    <div class="preloader-fixed-hud">
        <div id="preloaderTitle">Архитектура финансов</div>
        <div id="blueprintSubtitle">Воздушный винт // Тяга и масштабирование</div>
        
        <div class="slider-ui-container">
            <button class="slide-nav-btn" onclick="prevSlide()" aria-label="Предыдущее изобретение">‹</button>
            <button class="slide-nav-btn" onclick="nextSlide()" aria-label="Следующее изобретение">›</button>
        </div>

        <div class="slide-dots">
            <button class="slide-dot active" onclick="goToSlide(0)"></button>
            <button class="slide-dot" onclick="goToSlide(1)"></button>
            <button class="slide-dot" onclick="goToSlide(2)"></button>
            <button class="slide-dot" onclick="goToSlide(3)"></button>
            <button class="slide-dot" onclick="goToSlide(4)"></button>
        </div>

        <div class="bottom-dock">
            <div id="preloaderHUD">
                <div class="flex items-center gap-3 text-[#d4af37] text-[10px] tracking-[0.25em] uppercase font-mono">
                    <span class="pulse-dot" aria-hidden="true"></span>
                    <span id="loaderStatusText">Изучите 5 механизмов Да Винчи...</span>
                    <span id="loaderPercent" class="font-bold">0%</span>
                </div>
                <div class="progress-bar-bg mt-1"><div id="loaderProgressBar"></div></div>
            </div>
            <div id="exploreBtnWrapper">
                <button id="applyPresetBtn" onclick="applySelectedPresetAndEnter(event)" class="preset-btn">Применить модель</button>
                <button id="exploreBtn" onclick="triggerCameraObscuraTransition(event)" class="explore-btn">Исследовать</button>
            </div>
        </div>
    </div>
</div>

<canvas id="webgl-bg-canvas"></canvas>

<!-- ДАШБОРД -->
<div id="mainDashboardApp" class="flex-col border-t border-l">
    <header class="alche-block px-5 lg:px-8 py-3 flex flex-wrap items-center justify-between gap-4 border-b">
        <div class="flex items-center gap-6">
            <div class="flex items-center gap-3 cursor-pointer" onclick="playClickSound(1500,0.04)">
                <svg class="w-7 h-7 text-[#d4af37]" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true">
                    <circle cx="16" cy="16" r="14"/><rect x="6" y="6" width="20" height="20"/>
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
            <button id="toggleAudioBtn" onclick="toggleRenaissanceAmbient()" type="button" class="px-3 py-1.5 border border-[#d4af37]/60 text-[#d4af37] font-mono text-[10px] uppercase tracking-widest hover:bg-[#d4af37]/15 transition flex items-center gap-2" title="Включить / заглушить соборный эмбиент">
                <span id="audioStatusDot" class="pulse-dot"></span>
                <span id="audioBtnLabel">ЗВУК: ВЫСОКИЙ ХОР</span>
            </button>
            <button id="downloadExecutiveMemoBtn" onclick="generateExecutiveMemo()" type="button" class="px-3.5 py-1.5 border border-[#d4af37]/60 text-[#d4af37] font-mono text-[10px] uppercase tracking-widest hover:bg-[#d4af37]/15 transition flex items-center gap-2"><span>★ Меморандум (PDF)</span></button>
            <button id="downloadReportBtn" onclick="exportDataToCsv()" type="button" class="px-3.5 py-1.5 border font-mono text-[10px] uppercase tracking-widest hover:border-[#d4af37] hover:bg-[#d4af37]/10 transition flex items-center gap-2"><span>↓ Скачать отчет</span></button>
            <div id="themeSlider" class="hw-slider-track" onclick="toggleTheme()" role="switch" aria-checked="true" aria-label="Переключить режим: Ночь / День" tabindex="0" title="Переключить режим: Ночь / День">
                <div id="sliderThumb" class="hw-slider-thumb" style="transform: translateX(0)"></div>
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
            <form id="financialInputsForm" class="flex-1 flex flex-col" onsubmit="event.preventDefault()">
                <div class="alche-block p-5 space-y-4">
                    <div class="flex justify-between items-baseline"><span class="font-serif italic text-base font-semibold">I. Временной горизонт и маржа</span><span class="font-mono text-[9px] opacity-40" aria-hidden="true">01 // 04</span></div>
                    <div class="grid grid-cols-2 gap-2.5">
                        <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Месяц старта</label>
                            <select id="paramStartMonth" class="mono-input" onchange="playClickSound();runCalculation();">
                                <option value="0">Январь</option><option value="1">Февраль</option><option value="2">Март</option><option value="3">Апрель</option>
                                <option value="4">Май</option><option value="5">Июнь</option><option value="6">Июль</option><option value="7">Август</option>
                                <option value="8">Сентябрь</option><option value="9" selected>Октябрь</option><option value="10">Ноябрь</option><option value="11">Декабрь</option>
                            </select>
                        </div>
                        <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Год старта</label>
                            <select id="paramStartYear" class="mono-input" onchange="playClickSound();runCalculation();">
                                <option value="2026" selected>2026</option><option value="2027">2027</option>
                            </select>
                        </div>
                    </div>
                    <div class="grid grid-cols-2 gap-2.5">
                        <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Горизонт</label>
                            <select id="paramPeriod" class="mono-input" onchange="playClickSound();runCalculation();">
                                <option value="6">6 месяцев</option><option value="12" selected>12 месяцев</option><option value="18">18 месяцев</option><option value="24">24 месяца</option>
                            </select>
                        </div>
                        <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Ставка НДС</label>
                            <select id="paramVatRate" class="mono-input" onchange="playClickSound();runCalculation();">
                                <option value="22" selected>22%</option><option value="20">20%</option><option value="10">10%</option><option value="0">0%</option>
                            </select>
                        </div>
                    </div>
                    <div>
                        <div class="flex justify-between font-mono text-[10px] mb-1"><span class="opacity-70">МАРЖИНАЛЬНОСТЬ ПРОДАЖ</span><span id="lblMarginVal" class="text-[#d4af37] font-bold">20%</span></div>
                        <input type="range" id="paramMargin" min="10" max="50" step="1" value="20" oninput="scheduleCalc()">
                    </div>
                </div>
                <div class="alche-block p-5 space-y-4">
                    <div class="flex justify-between items-baseline"><span class="font-serif italic text-base font-semibold">II. Партионный склад и кредитование</span><span class="font-mono text-[9px] opacity-40" aria-hidden="true">02 // 04</span></div>
                    <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Стартовая закупка партии, ₽</label><input type="text" id="paramInitialPurchase" value="25 000 000" class="mono-input font-bold" inputmode="numeric" oninput="formatInput(this);scheduleCalc();"></div>
                    <div class="grid grid-cols-3 gap-2">
                        <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Цикл, мес.</label><input type="number" id="paramBatchCycle" value="5" min="1" max="12" class="mono-input text-center" oninput="scheduleCalc()"></div>
                        <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">ЦБ РФ, %</label><input type="number" id="paramCbRate" value="14.0" step="0.5" class="mono-input text-center font-bold text-[#d4af37]" oninput="scheduleCalc()"></div>
                        <div><label class="block font-mono text-[8px] uppercase opacity-70 mb-1" title="Коммерческая наценка кредитора">Комиссия, %</label><input type="number" id="paramCommMargin" value="2.0" step="0.5" class="mono-input text-center" oninput="scheduleCalc()"></div>
                    </div>
                    <div class="p-3 border space-y-3" style="border-color:rgba(212,175,55,.25);background:rgba(212,175,55,.02)">
                        <div class="font-mono text-[8px] uppercase tracking-widest text-[#d4af37] font-bold">[УСЛОВИЯ ПОСТАВЩИКА]</div>
                        <div>
                            <div class="flex justify-between font-mono text-[9px] mb-1"><span class="opacity-70">ПРЕДОПЛАТА ПОСТАВЩИКУ</span><span id="lblSupplierPrepVal" class="text-[#d4af37] font-bold">50%</span></div>
                            <input type="range" id="paramSupplierPrepay" min="0" max="100" step="10" value="50" oninput="scheduleCalc()">
                        </div>
                        <div>
                            <div class="flex justify-between font-mono text-[9px] mb-1"><span class="opacity-70">ОТСРОЧКА ОСТАТКА</span><span id="lblSupplierDelayVal" class="text-[#d4af37] font-bold">1 мес.</span></div>
                            <input type="range" id="paramSupplierDelay" min="0" max="6" step="1" value="1" oninput="scheduleCalc()">
                        </div>
                    </div>
                </div>
                <div class="alche-block p-5 space-y-4">
                    <div class="flex justify-between items-baseline"><span class="font-serif italic text-base font-semibold">III. Масштабирование заказов</span><span class="font-mono text-[9px] opacity-40" aria-hidden="true">03 // 04</span></div>
                    <div class="grid grid-cols-2 gap-2.5">
                        <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Средний чек, ₽</label><input type="text" id="paramAov" value="150 000" class="mono-input font-bold" inputmode="numeric" oninput="formatInput(this);scheduleCalc();"></div>
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
                        <div><label class="block font-mono text-[8px] uppercase opacity-70 mb-1">ФОТ, ₽</label><input type="text" id="paramFot" value="500 000" class="mono-input" inputmode="numeric" oninput="formatInput(this);scheduleCalc();"></div>
                        <div><label class="block font-mono text-[8px] uppercase opacity-70 mb-1">Склад, ₽</label><input type="text" id="paramWh" value="200 000" class="mono-input" inputmode="numeric" oninput="formatInput(this);scheduleCalc();"></div>
                        <div><label class="block font-mono text-[8px] uppercase opacity-70 mb-1">Офис, ₽</label><input type="text" id="paramOffice" value="150 000" class="mono-input" inputmode="numeric" oninput="formatInput(this);scheduleCalc();"></div>
                    </div>
                    <div class="pt-1">
                        <div>
                            <div class="flex justify-between font-mono text-[9px] mb-1"><span class="opacity-70">ДОЛЯ ФАКТОРИНГА В ВЫРУЧКЕ</span><span id="lblFactShareVal" class="text-[#d4af37] font-bold">50%</span></div>
                            <input type="range" id="paramFactoringShare" min="0" max="100" step="10" value="50" oninput="scheduleCalc()">
                        </div>
                    </div>
                </div>
            </form>
        </aside>

        <section class="lg:col-span-9 flex flex-col">
            <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 border-b">
                <div class="alche-block tilt-card p-5" onmouseenter="scrambleTitle(this)"><div class="flex justify-between items-center opacity-60 mb-1"><span class="metric-title font-mono text-[9px] uppercase tracking-widest" data-original="[01] Выручка">[01] Выручка</span></div><div id="kpiRev" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#f4f1ea]">0 ₽</div><div class="font-mono text-[9px] text-[#d4af37] mt-1.5 opacity-90" id="kpiRevSub">Маржа: 20%</div></div>
                <div class="alche-block tilt-card p-5" onmouseenter="scrambleTitle(this)"><div class="flex justify-between items-center opacity-60 mb-1"><span class="metric-title font-mono text-[9px] uppercase tracking-widest" data-original="[02] Дефицит">[02] Дефицит</span></div><div id="kpiInjections" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#e63946]">0 ₽</div><div class="font-mono text-[9px] text-[#e63946] mt-1.5 opacity-90">Внешние дотации</div></div>
                <div class="alche-block tilt-card p-5" onmouseenter="scrambleTitle(this)"><div class="flex justify-between items-center opacity-60 mb-1"><span class="metric-title font-mono text-[9px] uppercase tracking-widest" data-original="[03] Проценты">[03] Проценты</span></div><div id="kpiInterest" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#d4af37]">0 ₽</div><div id="kpiRateSub" class="font-mono text-[9px] text-[#d4af37] mt-1.5 opacity-90">Ставка 16.0%</div></div>
                <div class="alche-block tilt-card p-5" onmouseenter="scrambleTitle(this)"><div class="flex justify-between items-center opacity-60 mb-1"><span class="metric-title font-mono text-[9px] uppercase tracking-widest" data-original="[04] Пиковый долг">[04] Пиковый долг</span></div><div id="kpiMaxDebt" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#f4f1ea]">0 ₽</div><div class="font-mono text-[9px] opacity-60 mt-1.5">Максимум тела</div></div>
                <div class="alche-block tilt-card p-5 col-span-2 sm:col-span-1" onmouseenter="scrambleTitle(this)"><div class="flex justify-between items-center opacity-60 mb-1"><span class="metric-title font-mono text-[9px] uppercase tracking-widest" data-original="[05] Прибыль">[05] Прибыль</span></div><div id="kpiProfit" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#2a9d8f]">0 ₽</div><div id="kpiRoiSub" class="font-mono text-[9px] text-[#2a9d8f] mt-1.5 opacity-90">Рентабельность: 0%</div></div>
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
                        <div class="flex justify-between items-center mb-4"><div><h3 class="font-serif text-xl font-bold tracking-wide italic">График обслуживания долга и начисления процентов</h3><p class="font-mono text-[10px] opacity-60">Ежемесячные проценты по совокупной ставке кредитора (столбцы) и динамика тела долга (кривая)</p></div></div>
                        <div class="h-[360px] relative"><canvas id="chartDebt"></canvas></div>
                    </div>
                    <div class="alche-block border overflow-x-auto">
                        <table class="w-full text-left font-mono text-[11px]">
                            <thead class="border-b" style="background:var(--table-header-bg)"><tr class="text-[9px] uppercase tracking-widest text-[#d4af37]"><th class="p-3">Период</th><th class="p-3">Дотация (вход)</th><th class="p-3">Проценты</th><th class="p-3">Погашение долга</th><th class="p-3">Остаток долга</th><th class="p-3">Свободный остаток</th></tr></thead>
                            <tbody id="tableDebtBody" class="divide-y"></tbody>
                        </table>
                    </div>
                </div>
                <div id="viewTab1" class="hidden space-y-6">
                    <div class="alche-block p-5 border">
                        <div class="flex justify-between items-center mb-4"><div><h3 class="font-serif text-xl font-bold tracking-wide italic">Партионные закупки и истощение склада</h3><p class="font-mono text-[10px] opacity-60">Закупка дискретными циклами с учетом предоплаты и отсрочки поставщика</p></div></div>
                        <div class="h-[400px] relative"><canvas id="chartStock"></canvas></div>
                    </div>
                </div>
                <div id="viewTab2" class="hidden space-y-6">
                    <div class="alche-block p-5 border">
                        <div class="flex justify-between items-center mb-4"><div><h3 class="font-serif text-xl font-bold tracking-wide italic">Структура помесячного денежного потока</h3><p class="font-mono text-[10px] opacity-60">Сопоставление входящей выручки и совокупных выплат (закупки, аренда, ФОТ и налоги)</p></div></div>
                        <div class="h-[400px] relative"><canvas id="chartCF"></canvas></div>
                    </div>
                </div>
                <div id="viewTab3" class="hidden space-y-6">
                    <div class="grid grid-cols-1 xl:grid-cols-2 gap-6">
                        <div class="alche-block p-5 border">
                            <h3 class="font-serif text-xl font-bold tracking-wide italic mb-1">Динамика заказов и выручки</h3><p class="font-mono text-[10px] opacity-60 mb-4">Рост клиентской базы и масштабирование объемов отгрузок</p>
                            <div class="h-[320px] relative"><canvas id="chartOrders"></canvas></div>
                        </div>
                        <div class="alche-block p-5 border">
                            <h3 class="font-serif text-xl font-bold tracking-wide italic mb-1">Структура совокупных затрат</h3><p class="font-mono text-[10px] opacity-60 mb-4">Доли расходов с учетом себестоимости, инфраструктуры и процентов по долгу</p>
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
window.onerror = function(msg, url, line) {
    console.error("Critical Runtime Error:", msg, "line:", line);
    return false;
};

const REDUCE_MOTION = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const USER_IMAGES = __JSON_IMAGES_PAYLOAD__;

/* =========================================================================
   ИЗОБРЕТЕНИЯ ДА ВИНЧИ И ФИНАНСОВЫЕ СТРАТЕГИИ
   ========================================================================= */
const DA_VINCI_BLUEPRINTS = [
    {
        id: 0,
        invention: "Воздушный винт (Helix Pteron)",
        name: "Тяга и масштабирование",
        subtitle: "Сверхбыстрый прирост заказов (+15 шт./мес)",
        apply: () => {
            setGrowthMode('abs');
            document.getElementById('paramGrowthSlider').value = 15;
            document.getElementById('paramMargin').value = 25;
            document.getElementById('paramStartOrders').value = 50;
        }
    },
    {
        id: 1,
        invention: "Арочный мост (Ponte Autoportante)",
        name: "Механика оборачиваемости",
        subtitle: "Самонесущая система: короткий 3-мес. складской цикл",
        apply: () => {
            document.getElementById('paramBatchCycle').value = 3;
            document.getElementById('paramSupplierPrepay').value = 30;
            document.getElementById('paramSupplierDelay').value = 2;
        }
    },
    {
        id: 2,
        invention: "Гидравлический шлюз (Chiusa Idraulica)",
        name: "Купирование кассовых разрывов",
        subtitle: "Факторинг 80% для сброса пикового дефицита",
        apply: () => {
            document.getElementById('paramFactoringShare').value = 80;
            document.getElementById('paramMargin').value = 22;
        }
    },
    {
        id: 3,
        invention: "Витрувианский человек (Canone delle Proporzioni)",
        name: "Золотая пропорция (Канон)",
        subtitle: "Сбалансированная модель 1 : 1.618 и маржа 20%",
        apply: () => {
            document.getElementById('paramMargin').value = 20;
            document.getElementById('paramFactoringShare').value = 50;
            document.getElementById('paramBatchCycle').value = 5;
        }
    },
    {
        id: 4,
        invention: "Бронированная колесница (Carro Armato)",
        name: "Защита резервов и баланс",
        subtitle: "Минимизация заёмного плеча и лимит отгрузок",
        apply: () => {
            document.getElementById('paramSupplierPrepay').value = 20;
            document.getElementById('paramSupplierDelay').value = 3;
            document.getElementById('paramMaxOrdersCap').value = 180;
        }
    }
];

/* =========================================================================
   АВТОНОМНЫЙ ЗВУКОВОЙ ДВИЖОК: RENAISSANCE CATHEDRAL SOUNDSCAPE
   ========================================================================= */
class RenaissanceSoundscapeEngine {
    constructor() {
        this.ctx = null;
        this.isPlaying = false;
        this.timer = null;
        this.masterGain = null;
        this.scale = [146.83, 164.81, 174.61, 196.00, 220.00, 246.94, 261.63, 293.66, 329.63, 440.00];
    }

    init() {
        if (this.ctx) return;
        const AudioContextClass = window.AudioContext || window.webkitAudioContext;
        this.ctx = new AudioContextClass();

        this.masterGain = this.ctx.createGain();
        this.masterGain.gain.setValueAtTime(0.26, this.ctx.currentTime);
        this.masterGain.connect(this.ctx.destination);

        this.warmthFilter = this.ctx.createBiquadFilter();
        this.warmthFilter.type = 'lowpass';
        this.warmthFilter.frequency.setValueAtTime(1100, this.ctx.currentTime);
        this.warmthFilter.Q.setValueAtTime(1.15, this.ctx.currentTime);

        this.convolver = this.ctx.createConvolver();
        this.convolver.buffer = this.buildCathedralImpulse(5.5, 2.0);

        this.warmthFilter.connect(this.convolver);
        this.convolver.connect(this.masterGain);

        const dryGain = this.ctx.createGain();
        dryGain.gain.setValueAtTime(0.35, this.ctx.currentTime);
        this.warmthFilter.connect(dryGain);
        dryGain.connect(this.masterGain);
    }

    buildCathedralImpulse(duration, decay) {
        const rate = this.ctx.sampleRate;
        const length = rate * duration;
        const impulse = this.ctx.createBuffer(2, length, rate);
        const left = impulse.getChannelData(0);
        const right = impulse.getChannelData(1);

        for (let i = 0; i < length; i++) {
            const factor = Math.exp(-i / (rate * (decay * 0.45)));
            left[i] = (Math.random() * 2 - 1) * factor;
            right[i] = (Math.random() * 2 - 1) * factor;
        }
        return impulse;
    }

    startCathedralDrone() {
        const roots = [73.42, 110.00];
        roots.forEach(freq => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(freq, this.ctx.currentTime);

            const lfo = this.ctx.createOscillator();
            const lfoGain = this.ctx.createGain();
            lfo.frequency.setValueAtTime(0.18, this.ctx.currentTime);
            lfoGain.gain.setValueAtTime(0.015, this.ctx.currentTime);
            lfo.connect(lfoGain);
            lfoGain.connect(gain.gain);

            gain.gain.setValueAtTime(0.05, this.ctx.currentTime);

            osc.connect(gain);
            gain.connect(this.warmthFilter);
            osc.start();
            lfo.start();
        });
    }

    playPolyphonicVoice(freq, duration = 6.5) {
        if (!this.ctx || this.ctx.state === 'suspended') return;
        const now = this.ctx.currentTime;

        const osc1 = this.ctx.createOscillator();
        const osc2 = this.ctx.createOscillator();
        const voiceGain = this.ctx.createGain();

        osc1.type = 'sine';
        osc1.frequency.setValueAtTime(freq, now);

        osc2.type = 'triangle';
        osc2.frequency.setValueAtTime(freq * 1.0016, now);

        voiceGain.gain.setValueAtTime(0.0001, now);
        voiceGain.gain.exponentialRampToValueAtTime(0.075, now + 2.2);
        voiceGain.gain.exponentialRampToValueAtTime(0.0001, now + duration);

        osc1.connect(voiceGain);
        osc2.connect(voiceGain);
        voiceGain.connect(this.warmthFilter);

        osc1.start(now);
        osc2.start(now);
        osc1.stop(now + duration + 0.1);
        osc2.stop(now + duration + 0.1);

        // Устранение утечки памяти Web Audio
        osc1.onended = () => {
            try {
                osc1.disconnect();
                osc2.disconnect();
                voiceGain.disconnect();
            } catch (_) {}
        };
    }

    start() {
        this.init();
        if (this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
        if (this.isPlaying) return;
        this.isPlaying = true;

        this.startCathedralDrone();

        const scheduleVoice = () => {
            if (!this.isPlaying) return;
            const note = this.scale[Math.floor(Math.random() * this.scale.length)];
            const duration = 5.0 + Math.random() * 4.0;
            this.playPolyphonicVoice(note, duration);

            if (Math.random() > 0.55) {
                setTimeout(() => {
                    if (this.isPlaying) this.playPolyphonicVoice(note * 1.5, duration * 0.9);
                }, 1300);
            }

            const nextIn = 3200 + Math.random() * 3800;
            this.timer = setTimeout(scheduleVoice, nextIn);
        };

        scheduleVoice();
    }

    toggle() {
        if (!this.isPlaying) {
            this.start();
            return true;
        } else {
            this.stop();
            return false;
        }
    }

    stop() {
        this.isPlaying = false;
        if (this.timer) clearTimeout(this.timer);
        if (this.ctx && this.masterGain) {
            this.masterGain.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + 1.2);
            setTimeout(() => {
                if (!this.isPlaying && this.ctx) this.ctx.suspend();
            }, 1300);
        }
    }
}

const renaissanceAudio = new RenaissanceSoundscapeEngine();

function attemptAutoStartAudio() {
    renaissanceAudio.start();
}

['click', 'touchstart', 'keydown', 'mousemove'].forEach(evt => {
    window.addEventListener(evt, () => {
        if (renaissanceAudio.ctx && renaissanceAudio.ctx.state === 'suspended') {
            renaissanceAudio.ctx.resume();
        } else if (!renaissanceAudio.isPlaying) {
            renaissanceAudio.start();
        }
    }, { once: true });
});

attemptAutoStartAudio();

function toggleRenaissanceAmbient() {
    const active = renaissanceAudio.toggle();
    const dot = document.getElementById('audioStatusDot');
    const label = document.getElementById('audioBtnLabel');
    if (active) {
        dot.style.display = 'inline-block';
        label.textContent = 'ЗВУК: ВЫСОКИЙ ХОР';
    } else {
        dot.style.display = 'none';
        label.textContent = 'ЗВУК: ТИШИНА';
    }
}

function playClickSound(freq = 1200, duration = 0.02) {
    try {
        if (!renaissanceAudio.ctx) renaissanceAudio.init();
        const ctx = renaissanceAudio.ctx;
        if (ctx.state === 'suspended') ctx.resume();
        const osc = ctx.createOscillator(), gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(320, ctx.currentTime + duration);
        gain.gain.setValueAtTime(0.035, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + duration);
        osc.connect(gain); gain.connect(ctx.destination);
        osc.start(); osc.stop(ctx.currentTime + duration);
        osc.onended = () => { osc.disconnect(); gain.disconnect(); };
    } catch (e) {}
}

function playGearSpinUpSound(duration = 3.2) {
    try {
        if (!renaissanceAudio.ctx) renaissanceAudio.init();
        const ctx = renaissanceAudio.ctx;
        if (ctx.state === 'suspended') ctx.resume();
        const osc = ctx.createOscillator(), gain = ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(50, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(260, ctx.currentTime + duration);
        gain.gain.setValueAtTime(0.015, ctx.currentTime);
        gain.gain.linearRampToValueAtTime(0.07, ctx.currentTime + duration * 0.85);
        gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + duration);
        osc.connect(gain); gain.connect(ctx.destination);
        osc.start(); osc.stop(ctx.currentTime + duration);
        osc.onended = () => { osc.disconnect(); gain.disconnect(); };
    } catch (e) {}
}

function playApertureSnapSound() {
    try {
        if (!renaissanceAudio.ctx) renaissanceAudio.init();
        const ctx = renaissanceAudio.ctx;
        if (ctx.state === 'suspended') ctx.resume();
        
        const osc = ctx.createOscillator(), gain = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(750, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(30, ctx.currentTime + 0.15);
        gain.gain.setValueAtTime(0.4, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.15);
        osc.connect(gain); gain.connect(ctx.destination);
        osc.start(); osc.stop(ctx.currentTime + 0.15);
        osc.onended = () => { osc.disconnect(); gain.disconnect(); };

        const bufferSize = ctx.sampleRate * 0.09;
        const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) data[i] = Math.random() * 2 - 1;
        const noise = ctx.createBufferSource();
        noise.buffer = buffer;
        const noiseGain = ctx.createGain();
        noiseGain.gain.setValueAtTime(0.25, ctx.currentTime);
        noiseGain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.09);
        noise.connect(noiseGain);
        noiseGain.connect(ctx.destination);
        noise.start();
        noise.onended = () => { noise.disconnect(); noiseGain.disconnect(); };
    } catch (e) {}
}

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
    document.documentElement.style.overflow = 'auto';
    document.body.style.overflow = 'auto';
    
    if (app) {
        app.classList.add('ready');
        app.classList.add('camera-obscura-reveal');
    }
    
    setTimeout(() => {
        if (stage) stage.style.display = 'none';
        try {
            preScene.traverse(o => {
                if (o.geometry) o.geometry.dispose();
                if (o.material) { Array.isArray(o.material) ? o.material.forEach(m => m.dispose()) : o.material.dispose(); }
            });
            preRenderer.dispose(); preRenderer.forceContextLoss();
        } catch (e) {}
    }, 1200);
}

const PRELOADER_TOTAL_TIME = REDUCE_MOTION ? 1200 : 9000;
const preloaderStartTime = performance.now();

setTimeout(() => { const pt = document.getElementById('preloaderTitle'); if (pt) pt.classList.add('locked-on'); }, 800);

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

/* THREE.JS ПРЕЛОАДЕР */
const preCanvas = document.getElementById('preloader-webgl');
const preRenderer = new THREE.WebGLRenderer({ canvas: preCanvas, alpha: true, antialias: true, powerPreference: "high-performance" });
preRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
preRenderer.setSize(window.innerWidth, window.innerHeight);

const preScene = new THREE.Scene();
const preCamera = new THREE.PerspectiveCamera(46, window.innerWidth / window.innerHeight, 1, 6000);
const baseCamZ = 390;
let targetCamPos = new THREE.Vector3(0, 0, baseCamZ);
let currentLookTarget = new THREE.Vector3(0, 0, 0);
let targetLookTarget = new THREE.Vector3(0, 0, 0);
preCamera.position.copy(targetCamPos);

const preGroup = new THREE.Group();
preScene.add(preGroup);

/* ЗОЛОТАЯ ВЗВЕСЬ ЧАСТИЦ */
const particleCount = 450;
const particleGeo = new THREE.BufferGeometry();
const particlePos = new Float32Array(particleCount * 3);
for (let i = 0; i < particleCount * 3; i += 3) {
    particlePos[i] = (Math.random() - 0.5) * 600;
    particlePos[i + 1] = (Math.random() - 0.5) * 450;
    particlePos[i + 2] = (Math.random() - 0.5) * 400;
}
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePos, 3));
const particleMat = new THREE.PointsMaterial({
    color: 0xd4af37,
    size: 2.2,
    transparent: true,
    opacity: 0.38,
    blending: THREE.AdditiveBlending
});
const dustParticles = new THREE.Points(particleGeo, particleMat);
preGroup.add(dustParticles);

const megaRingWireMat = new THREE.MeshBasicMaterial({ color: 0x00c3ff, wireframe: true, transparent: true, opacity: 0.38 });
const secondaryWireMat = new THREE.MeshBasicMaterial({ color: 0x0077aa, wireframe: true, transparent: true, opacity: 0.22 });

function createCyclopeanTrussRing(mainRadius, tubeWidth, tubeDepth, segments) {
    const group = new THREE.Group();
    group.add(new THREE.Mesh(new THREE.TorusGeometry(mainRadius, tubeWidth * 0.45, 12, segments), megaRingWireMat));
    const linePts = [];
    const rOuter = mainRadius + tubeWidth, rInner = mainRadius - tubeWidth, zOffset = tubeDepth;
    
    for (let i = 0; i < segments; i++) {
        const nextIdx = (i + 1) % segments;
        const a1 = (i / segments) * Math.PI * 2;
        const a2 = (nextIdx / segments) * Math.PI * 2;

        const p1_topOut = new THREE.Vector3(Math.cos(a1) * rOuter, Math.sin(a1) * rOuter, zOffset);
        const p2_topOut = new THREE.Vector3(Math.cos(a2) * rOuter, Math.sin(a2) * rOuter, zOffset);
        const p1_botOut = new THREE.Vector3(Math.cos(a1) * rOuter, Math.sin(a1) * rOuter, -zOffset);
        const p2_botOut = new THREE.Vector3(Math.cos(a2) * rOuter, Math.sin(a2) * rOuter, -zOffset);

        const p1_topIn = new THREE.Vector3(Math.cos(a1) * rInner, Math.sin(a1) * rInner, zOffset);
        const p2_topIn = new THREE.Vector3(Math.cos(a2) * rInner, Math.sin(a2) * rInner, zOffset);
        const p1_botIn = new THREE.Vector3(Math.cos(a1) * rInner, Math.sin(a1) * rInner, -zOffset);
        const p2_botIn = new THREE.Vector3(Math.cos(a2) * rInner, Math.sin(a2) * rInner, -zOffset);

        linePts.push(p1_topOut, p2_topOut);
        linePts.push(p1_botOut, p2_botOut);
        linePts.push(p1_topIn, p2_topIn);
        linePts.push(p1_botIn, p2_botIn);

        linePts.push(p1_topOut, p1_botOut);
        linePts.push(p1_topIn, p1_botIn);
        linePts.push(p1_topOut, p1_topIn);
        linePts.push(p1_botOut, p1_botIn);

        if (i % 2 === 0) {
            linePts.push(p1_topOut, p2_botOut);
            linePts.push(p1_topIn, p2_botIn);
            linePts.push(p1_topOut, p2_topIn);
        } else {
            linePts.push(p1_botOut, p2_topOut);
            linePts.push(p1_botIn, p2_botIn);
            linePts.push(p1_botOut, p2_botIn);
        }

        if (i % 3 === 0) {
            const toothR = rOuter + tubeWidth * 0.42;
            const pTooth = new THREE.Vector3(Math.cos(a1) * toothR, Math.sin(a1) * toothR, 0);
            linePts.push(p1_topOut, pTooth);
            linePts.push(pTooth, p1_botOut);
        }
    }
    group.add(new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(linePts), megaRingWireMat));
    group.add(new THREE.Mesh(new THREE.TorusGeometry(mainRadius - tubeWidth * 1.6, tubeWidth * 0.18, 8, Math.floor(segments * 0.75)), secondaryWireMat));
    return group;
}

const astrolabeRings = [];
const aRing1 = createCyclopeanTrussRing(340, 18.0, 12.0, 180);
const aRing2 = createCyclopeanTrussRing(255, 14.0, 10.0, 150);
const aRing3 = createCyclopeanTrussRing(175, 11.0, 8.0, 130);
aRing2.rotation.x = Math.PI / 3.4; aRing2.rotation.z = Math.PI / 6.0; aRing3.rotation.y = Math.PI / 3.0;
preGroup.add(aRing1); preGroup.add(aRing2); preGroup.add(aRing3);
astrolabeRings.push(
    { group: aRing1, sx: 0.00045, sy: 0.00065, sz: 0.00025, px: 0.2, py: 1.1, dir: 1.0 },
    { group: aRing2, sx: -0.00055, sy: 0.00040, sz: -0.00045, px: 2.3, py: 0.7, dir: -1.0 },
    { group: aRing3, sx: 0.00060, sy: -0.00050, sz: 0.00035, px: 1.5, py: 3.2, dir: 1.15 }
);

function createDaVinciHoloMaterial(texture) {
    return new THREE.ShaderMaterial({
        uniforms: {
            uTex: { value: texture },
            uHover: { value: 0.0 },
            uTime: { value: 0.0 }
        },
        vertexShader: `
            varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
        fragmentShader: `
            uniform sampler2D uTex;
            uniform float uHover;
            uniform float uTime;
            varying vec2 vUv;
            void main() {
                vec4 tex = texture2D(uTex, vUv);
                float lum = dot(tex.rgb, vec3(0.299, 0.587, 0.114));
                float stroke = smoothstep(0.10, 0.60, lum);
                if (lum > 0.88) stroke = 1.0 - stroke;
                
                vec3 baseGold = vec3(0.85, 0.71, 0.25);
                vec3 highlight = vec3(1.0, 0.95, 0.78);
                float wave = sin((vUv.x + vUv.y) * 12.0 - uTime * 4.0) * 0.5 + 0.5;
                vec3 finalColor = mix(baseGold, highlight, wave * 0.4 + uHover * 0.6);
                
                float alpha = stroke * (0.65 + uHover * 0.35);
                gl_FragColor = vec4(finalColor, alpha);
            }
        `,
        transparent: true,
        side: THREE.DoubleSide,
        depthWrite: false
    });
}

function createBlueprintWireMaterial() {
    return new THREE.ShaderMaterial({
        uniforms: { uHover: { value: 0.0 }, uTime: { value: 0.0 } },
        vertexShader: `varying vec3 vPos;void main(){vPos=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}`,
        fragmentShader: `uniform float uHover;uniform float uTime;varying vec3 vPos;float wave=sin((vPos.x+vPos.y+vPos.z)*0.2-uTime*3.5)*0.5+0.5;vec3 baseGold=vec3(0.85,0.71,0.25);vec3 brightGlow=vec3(1.0,0.96,0.82);vec3 col=mix(baseGold,brightGlow,wave*0.4+uHover*0.6);float alpha=clamp(0.70+wave*0.30+uHover*0.30,0.0,1.0);gl_FragColor=vec4(col,alpha);`,
        transparent: true, depthWrite: false
    });
}

function createFallbackDaVinciCanvas(typeIdx) {
    const canvas = document.createElement('canvas');
    canvas.width = 512; canvas.height = 512;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#0d0e17'; ctx.fillRect(0, 0, 512, 512);
    ctx.strokeStyle = '#d4af37'; ctx.lineWidth = 2.5;

    // Векторные чертежи механизмов Да Винчи
    if (typeIdx === 0) { // Воздушный винт
        ctx.beginPath(); ctx.arc(256, 256, 180, 0, Math.PI * 2); ctx.stroke();
        for (let r = 20; r < 180; r += 24) {
            ctx.beginPath(); ctx.arc(256, 256, r, 0, Math.PI * 1.5); ctx.stroke();
        }
        ctx.beginPath(); ctx.moveTo(256, 40); ctx.lineTo(256, 472); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(40, 256); ctx.lineTo(472, 256); ctx.stroke();
    } else if (typeIdx === 1) { // Арочный мост
        ctx.beginPath(); ctx.arc(256, 380, 200, Math.PI, 0); ctx.stroke();
        ctx.beginPath(); ctx.arc(256, 380, 230, Math.PI, 0); ctx.stroke();
        for (let a = Math.PI; a <= 2 * Math.PI; a += 0.2) {
            ctx.moveTo(256 + Math.cos(a) * 200, 380 + Math.sin(a) * 200);
            ctx.lineTo(256 + Math.cos(a) * 230, 380 + Math.sin(a) * 230);
        }
        ctx.stroke();
    } else if (typeIdx === 2) { // Гидравлический шлюз
        ctx.strokeRect(90, 80, 332, 352);
        ctx.beginPath(); ctx.moveTo(256, 80); ctx.lineTo(170, 256); ctx.lineTo(256, 432); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(256, 80); ctx.lineTo(342, 256); ctx.lineTo(256, 432); ctx.stroke();
        for (let y = 120; y <= 390; y += 30) {
            ctx.moveTo(90, y); ctx.lineTo(422, y);
        }
        ctx.stroke();
    } else if (typeIdx === 3) { // Витрувианский канон
        ctx.beginPath(); ctx.arc(256, 256, 190, 0, Math.PI * 2); ctx.stroke();
        ctx.strokeRect(66, 66, 380, 380);
        ctx.beginPath(); ctx.moveTo(256, 66); ctx.lineTo(256, 446); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(66, 256); ctx.lineTo(446, 256); ctx.stroke();
    } else { // Бронированная колесница
        ctx.beginPath(); ctx.ellipse(256, 280, 200, 100, 0, 0, Math.PI * 2); ctx.stroke();
        ctx.beginPath(); ctx.arc(256, 220, 70, Math.PI, 0); ctx.stroke();
        for (let x = 80; x <= 432; x += 32) {
            ctx.moveTo(x, 280); ctx.lineTo(x, 340);
        }
        ctx.stroke();
    }
    return new THREE.CanvasTexture(canvas);
}

function createSafeVolumetricBlueprintCard(b64Image, typeIdx) {
    const cardGroup = new THREE.Group();
    const w = 58, h = 58, d = 26;
    const pts = [];

    const corners = [
        new THREE.Vector3(-w/2, -h/2, -d/2), new THREE.Vector3(w/2, -h/2, -d/2),
        new THREE.Vector3(w/2, h/2, -d/2), new THREE.Vector3(-w/2, h/2, -d/2),
        new THREE.Vector3(-w/2, -h/2, d/2), new THREE.Vector3(w/2, -h/2, d/2),
        new THREE.Vector3(w/2, h/2, d/2), new THREE.Vector3(-w/2, h/2, d/2)
    ];
    const boxEdges = [
        [0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],
        [0,4],[1,5],[2,6],[3,7],[0,6],[1,7],[2,4],[3,5]
    ];
    boxEdges.forEach(e => pts.push(corners[e[0]], corners[e[1]]));

    for (let x = -w/2; x <= w/2; x += 11.6) {
        pts.push(new THREE.Vector3(x, -h/2, 0), new THREE.Vector3(x, h/2, 0));
        pts.push(new THREE.Vector3(x, -h/2, -d/2), new THREE.Vector3(x, -h/2, d/2));
    }
    for (let y = -h/2; y <= h/2; y += 11.6) {
        pts.push(new THREE.Vector3(-w/2, y, 0), new THREE.Vector3(w/2, y, 0));
        pts.push(new THREE.Vector3(-w/2, y, -d/2), new THREE.Vector3(-w/2, y, d/2));
    }

    const rLimb = 32;
    for (let i = 0; i < 48; i++) {
        const nextI = (i + 1) % 48;
        const a1 = (i / 48) * Math.PI * 2, a2 = (nextI / 48) * Math.PI * 2;
        pts.push(new THREE.Vector3(Math.cos(a1)*rLimb, Math.sin(a1)*rLimb, 0), new THREE.Vector3(Math.cos(a2)*rLimb, Math.sin(a2)*rLimb, 0));
        if (i % 4 === 0) {
            pts.push(new THREE.Vector3(Math.cos(a1)*(rLimb-3), Math.sin(a1)*(rLimb-3), 0), new THREE.Vector3(Math.cos(a1)*(rLimb+3), Math.sin(a1)*(rLimb+3), 0));
            pts.push(new THREE.Vector3(0, 0, 0), new THREE.Vector3(Math.cos(a1)*rLimb*0.5, Math.sin(a1)*rLimb*0.5, (i%8===0?4:-4)));
        }
    }

    const wireframeMesh = new THREE.LineSegments(
        new THREE.BufferGeometry().setFromPoints(pts),
        createBlueprintWireMaterial()
    );
    cardGroup.add(wireframeMesh);

    // Добавление плоскости чертежа
    const planeGeo = new THREE.PlaneGeometry(50, 50);
    let planeMat;

    if (typeof b64Image === 'string' && b64Image.length > 50 && b64Image.startsWith('data:image')) {
        try {
            const imgEl = new Image();
            imgEl.onload = function() {
                const texture = new THREE.Texture(imgEl);
                texture.needsUpdate = true;
                planeMat = createDaVinciHoloMaterial(texture);
                const planeMesh = new THREE.Mesh(planeGeo, planeMat);
                planeMesh.position.z = 0;
                cardGroup.add(planeMesh);
            };
            imgEl.src = b64Image;
        } catch (e) {
            const fbTex = createFallbackDaVinciCanvas(typeIdx);
            planeMat = createDaVinciHoloMaterial(fbTex);
            const planeMesh = new THREE.Mesh(planeGeo, planeMat);
            cardGroup.add(planeMesh);
        }
    } else {
        const fbTex = createFallbackDaVinciCanvas(typeIdx);
        planeMat = createDaVinciHoloMaterial(fbTex);
        const planeMesh = new THREE.Mesh(planeGeo, planeMat);
        cardGroup.add(planeMesh);
    }

    return cardGroup;
}

/* 5 ИЗОБРЕТЕНИЙ РАЗВЁРНУТЫ ПО ВЕРТИКАЛЬНО-ГОРИЗОНТАЛЬНОЙ ДУГЕ ПЕРЕД КАМЕРОЙ (БЕЗ ПУСТЫХ ЭКРАНОВ) */
const floatingInventions = [
    { group: createSafeVolumetricBlueprintCard(USER_IMAGES[0], 0), basePos: new THREE.Vector3(-125,  35,  25), rotSpeed: new THREE.Vector3(0.0016, 0.0014, -0.0008) },
    { group: createSafeVolumetricBlueprintCard(USER_IMAGES[1], 1), basePos: new THREE.Vector3( -60, -32,  45), rotSpeed: new THREE.Vector3(0.0012, 0.0018,  0.0010) },
    { group: createSafeVolumetricBlueprintCard(USER_IMAGES[2], 2), basePos: new THREE.Vector3(   0,  38,  65), rotSpeed: new THREE.Vector3(-0.0014, 0.0016, 0.0009) },
    { group: createSafeVolumetricBlueprintCard(USER_IMAGES[3], 3), basePos: new THREE.Vector3(  60, -32,  45), rotSpeed: new THREE.Vector3(0.0008, 0.0012,  0.0006) },
    { group: createSafeVolumetricBlueprintCard(USER_IMAGES[4], 4), basePos: new THREE.Vector3( 125,  35,  25), rotSpeed: new THREE.Vector3(-0.0012, 0.0015, -0.0007) }
];

const hoverTargets = [];
floatingInventions.forEach((item) => {
    item.group.position.copy(item.basePos);
    preGroup.add(item.group);

    const hitGeo = new THREE.SphereGeometry(46, 16, 16);
    const hitMat = new THREE.MeshBasicMaterial({ visible: false });
    const hitMesh = new THREE.Mesh(hitGeo, hitMat);
    hitMesh.position.copy(item.basePos);
    preGroup.add(hitMesh);

    item.hitMesh = hitMesh;
    item.targetZ = item.basePos.z;
    item.targetScale = 1.0;
    item.isHovered = false;
    hoverTargets.push(item);
});

preRenderer.render(preScene, preCamera);

let currentSlideIndex = -1;

function updateSlideDots() {
    const dots = document.querySelectorAll('.slide-dot');
    dots.forEach((d, idx) => {
        if (idx === currentSlideIndex) d.classList.add('active');
        else d.classList.remove('active');
    });
}

function focusSlide(idx) {
    if (idx < 0 || idx >= hoverTargets.length) return;
    currentSlideIndex = idx;
    
    if (navigator.vibrate) {
        try { navigator.vibrate(12); } catch (_) {}
    }
    
    playClickSound(1800, 0.015);
    updateSlideDots();

    hoverTargets.forEach((item, i) => {
        const isCurrent = (i === idx);
        item.isHovered = isCurrent;
        item.targetScale = isCurrent ? 1.35 : 1.0;
        item.targetZ = isCurrent ? (item.basePos.z + 55) : item.basePos.z;

        item.group.traverse(child => {
            if (child.material && child.material.uniforms && child.material.uniforms.uHover) {
                child.material.uniforms.uHover.value = isCurrent ? 1.0 : 0.0;
            }
        });
    });

    const target = hoverTargets[idx];
    const objPos = target.basePos;
    const isMobile = window.innerWidth < 768;
    const zOffset = isMobile ? 120 : 95;
    
    // Плавное наведение камеры с идеальным фронтальным ракурсом на выбранный чертеж
    targetCamPos.set(objPos.x * 0.75, objPos.y * 0.75, objPos.z + zOffset);
    targetLookTarget.set(objPos.x, objPos.y, objPos.z);

    const preset = DA_VINCI_BLUEPRINTS[idx];
    const status = document.getElementById('loaderStatusText');
    const sub = document.getElementById('blueprintSubtitle');
    if (status && preset) {
        status.textContent = `[${idx + 1}/5] ${preset.name}`;
    }
    if (sub && preset) {
        sub.textContent = `${preset.invention} — ${preset.subtitle}`;
        sub.style.opacity = '1';
    }
}

window.nextSlide = function() {
    let next = currentSlideIndex + 1;
    if (next >= hoverTargets.length) next = 0;
    focusSlide(next);
};

window.prevSlide = function() {
    let prev = currentSlideIndex - 1;
    if (prev < 0) prev = hoverTargets.length - 1;
    focusSlide(prev);
};

window.goToSlide = function(idx) {
    focusSlide(idx);
};

window.applySelectedPresetAndEnter = function(e) {
    if (currentSlideIndex >= 0 && DA_VINCI_BLUEPRINTS[currentSlideIndex]) {
        DA_VINCI_BLUEPRINTS[currentSlideIndex].apply();
        runCalculation();
    }
    triggerCameraObscuraTransition(e);
};

let touchStartX = 0, touchStartY = 0;
window.addEventListener('touchstart', (e) => {
    if (e.touches.length > 0) {
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
    }
}, { passive: true });

window.addEventListener('touchend', (e) => {
    if (e.changedTouches.length > 0) {
        const diffX = e.changedTouches[0].clientX - touchStartX;
        const diffY = e.changedTouches[0].clientY - touchStartY;
        if (Math.abs(diffX) > 40 && Math.abs(diffX) > Math.abs(diffY)) {
            if (diffX < 0) nextSlide();
            else prevSlide();
        }
    }
}, { passive: true });

const raycaster = new THREE.Raycaster();
const mouseVec = new THREE.Vector2(-999, -999);

window.addEventListener('mousemove', (e) => {
    mouseVec.x = (e.clientX / window.innerWidth) * 2 - 1;
    mouseVec.y = -(e.clientY / window.innerHeight) * 2 + 1;
    checkRaycastHover();
});

function checkRaycastHover() {
    if (preloaderDismissed || isObscuraTransition || window.innerWidth < 768) return;
    raycaster.setFromCamera(mouseVec, preCamera);
    const hitMeshes = hoverTargets.map(h => h.hitMesh);
    const intersects = raycaster.intersectObjects(hitMeshes, false);

    if (intersects.length > 0) {
        const hit = intersects[0].object;
        const idx = hoverTargets.findIndex(h => h.hitMesh === hit);
        if (idx !== -1 && idx !== currentSlideIndex) {
            focusSlide(idx);
        }
    }
}

/* =========================================================================
   МЕДЛЕННЫЙ ТРАНЗИШН: ВЫРАВНИВАНИЕ В ПЛОСКОСТЬ И СУЖЕНИЕ ДИАФРАГМЫ ОБСКУРЫ
   ========================================================================= */
let isObscuraTransition = false;
let obscuraStartTime = 0;
const OBSCURA_DURATION = 3.4; // Увеличенное время для грациозного кинематографичного перехода

function triggerCameraObscuraTransition(event) {
    if (isObscuraTransition) return;
    isObscuraTransition = true;
    obscuraStartTime = performance.now();
    
    playGearSpinUpSound(OBSCURA_DURATION);

    const hud = document.querySelector('.preloader-fixed-hud');
    if (hud) hud.style.opacity = '0';

    targetCamPos.set(0, 0, baseCamZ);
    targetLookTarget.set(0, 0, 0);

    // Запоминаем текущие углы колец для плавного выравнивания в плоскость
    astrolabeRings.forEach(ring => {
        ring.startRotX = ring.group.rotation.x;
        ring.startRotY = ring.group.rotation.y;
        ring.startRotZ = ring.group.rotation.z;
    });
}

function triggerShutterBlink() {
    playApertureSnapSound();
    const flash = document.getElementById('shutter-flash');
    if (!flash) return;

    flash.style.transition = 'none';
    flash.style.opacity = '1';

    setTimeout(() => {
        flash.style.opacity = '0.35';
        setTimeout(() => {
            flash.style.opacity = '0.9';
            dismissPreloader();
            setTimeout(() => {
                flash.style.transition = 'opacity 0.75s cubic-bezier(0.16, 1, 0.3, 1)';
                flash.style.opacity = '0';
            }, 60);
        }, 35);
    }, 45);
}

function animatePreloader() {
    if (preloaderDismissed) return;
    requestAnimationFrame(animatePreloader);

    const now = performance.now();
    const elapsed = now - preloaderStartTime;
    const t = elapsed * 0.001;

    if (isObscuraTransition) {
        const obsElapsed = (now - obscuraStartTime) * 0.001;
        const progress = Math.min(obsElapsed / OBSCURA_DURATION, 1.0);

        
