"""Архитектура Капитала // Финансовое Моделирование — Streamlit runner."""
import os
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
    # Проверяем как в текущей директории, так и в родительских/вложенных
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
                    return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"
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

#preloader-stage{position:fixed;top:0;left:0;width:100vw;height:100vh;background:radial-gradient(circle at center,#0d0e17 0%,#030306 100%);z-index:900;overflow:hidden;touch-action:none}
#preloader-webgl{position:absolute;inset:0;width:100%;height:100%;z-index:10;cursor:grab}
#preloader-webgl:active{cursor:grabbing}

.preloader-fixed-hud{position:absolute;inset:0;width:100%;height:100%;z-index:30;pointer-events:none;user-select:none}
#preloaderTitle{position:absolute;top:28px;left:50%;transform:translateX(-50%);font-family:'Cormorant Garamond',Georgia,serif;font-style:italic;font-size:clamp(20px,3.2vw,44px);font-weight:700;letter-spacing:.26em;color:var(--accent-gold);opacity:0;text-shadow:0 0 45px rgba(212,175,55,.85);transition:opacity 1.8s cubic-bezier(.16,1,.3,1);text-align:center;white-space:nowrap}
#preloaderTitle.locked-on{opacity:1!important}

#blueprintSubtitle{position:absolute;top:76px;left:50%;transform:translateX(-50%);font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:0.32em;text-transform:uppercase;color:rgba(212,175,55,0.7);opacity:0;transition:opacity 0.6s ease;text-align:center;white-space:nowrap}

.slider-ui-container{position:absolute;top:50%;left:0;width:100%;transform:translateY(-50%);display:flex;justify-content:space-between;align-items:center;padding:0 14px;pointer-events:none;z-index:40}
.slide-nav-btn{width:46px;height:46px;border-radius:50%;background:rgba(13,13,18,0.75);border:1px solid rgba(212,175,55,0.4);color:var(--accent-gold);display:flex;align-items:center;justify-content:center;font-size:22px;cursor:pointer;pointer-events:auto;backdrop-filter:blur(10px);transition:all .25s ease}
.slide-nav-btn:hover{background:rgba(212,175,55,0.25);border-color:var(--accent-gold);transform:scale(1.1)}
.slide-nav-btn:active{transform:scale(0.95)}

.slide-dots{position:absolute;bottom:102px;left:50%;transform:translateX(-50%);display:flex;gap:10px;pointer-events:auto;z-index:40}
.slide-dot{width:8px;height:8px;border-radius:50%;border:1px solid var(--accent-gold);background:transparent;cursor:pointer;transition:all .3s ease}
.slide-dot.active{background:var(--accent-gold);box-shadow:0 0 10px var(--accent-gold);transform:scale(1.35)}

.bottom-dock{position:absolute;bottom:30px;left:50%;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;justify-content:center;width:380px;height:62px}
#preloaderHUD{display:flex;flex-direction:column;align-items:center;gap:8px;transition:opacity .4s}
.progress-bar-bg{width:280px;height:2px;background:rgba(255,255,255,.12);position:relative;overflow:hidden}
#loaderProgressBar{position:absolute;left:0;top:0;height:100%;width:0;background:var(--accent-gold);box-shadow:0 0 10px var(--accent-gold);transition:width .1s linear}

#exploreBtnWrapper{position:absolute;opacity:0;pointer-events:none;transition:opacity .6s cubic-bezier(.19,1,.22,1),transform .6s cubic-bezier(.19,1,.22,1);transform:translateY(8px);display:flex;gap:10px}
#exploreBtnWrapper.active{opacity:1;pointer-events:auto;transform:translateY(0)}
.explore-btn{padding:12px 34px;background:rgba(13,13,18,.9);border:1px solid rgba(212,175,55,.95);color:#f4f1ea;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.32em;text-transform:uppercase;cursor:pointer;backdrop-filter:blur(14px);overflow:hidden;transition:all .3s;box-shadow:0 0 40px rgba(212,175,55,.35),inset 0 0 16px rgba(212,175,55,.18)}
.explore-btn:hover{border-color:#ffd700;color:#ffd700;box-shadow:0 0 60px rgba(212,175,55,.7),inset 0 0 24px rgba(212,175,55,.35);transform:scale(1.04)}

.preset-btn{padding:12px 18px;background:rgba(212,175,55,0.12);border:1px solid var(--accent-gold);color:var(--accent-gold);font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:0.2em;text-transform:uppercase;cursor:pointer;backdrop-filter:blur(10px);transition:all .3s}
.preset-btn:hover{background:var(--accent-gold);color:#070709}

#mainDashboardApp{display:none;position:relative;z-index:10;min-height:100vh}
#mainDashboardApp.ready{display:flex}
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

<!-- ПРЕЛОАДЕР -->
<div id="preloader-stage">
    <canvas id="preloader-webgl"></canvas>
    
    <div class="preloader-fixed-hud">
        <div id="preloaderTitle">Архитектура финансов</div>
        <div id="blueprintSubtitle">Тяга и масштабирование выручки</div>
        
        <div class="slider-ui-container">
            <button class="slide-nav-btn" onclick="prevSlide()" aria-label="Предыдущий чертеж">‹</button>
            <button class="slide-nav-btn" onclick="nextSlide()" aria-label="Следующий чертеж">›</button>
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
                    <span id="loaderStatusText">Листайте 3D-чертежи Да Винчи...</span>
                    <span id="loaderPercent" class="font-bold">0%</span>
                </div>
                <div class="progress-bar-bg mt-1"><div id="loaderProgressBar"></div></div>
            </div>
            <div id="exploreBtnWrapper">
                <button id="applyPresetBtn" onclick="applySelectedPresetAndEnter(event)" class="preset-btn">Применить пресет</button>
                <button id="exploreBtn" onclick="triggerIrisShutterTransition(event)" class="explore-btn">Исследовать</button>
            </div>
        </div>
    </div>
</div>

<canvas id="webgl-bg-canvas"></canvas>

<!-- ДАШБОРД -->
<div id="mainDashboardApp" class="flex-col border-t border-l opacity-0 transition-opacity duration-1000">
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
const REDUCE_MOTION = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const USER_IMAGES = [
    "__IMG_0__",
    "__IMG_1__",
    "__IMG_2__",
    "__IMG_3__",
    "__IMG_4__"
];

/* БЕЗОПАСНАЯ ГЕНЕРАЦИЯ ОБЪЕМНЫХ КАРТОЧЕК С 3D-ЧЕРТЕЖОМ */
function createSafeVolumetricBlueprintCard(b64Image, typeIdx) {
    const cardGroup = new THREE.Group();
    const w = 58, h = 58, d = 26;
    const pts = [];

    // 1. Пространственный каркас куба
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

    // 2. Сетка пересечений по горизонтали и вертикали
    for (let x = -w/2; x <= w/2; x += 11.6) {
        pts.push(new THREE.Vector3(x, -h/2, 0), new THREE.Vector3(x, h/2, 0));
        pts.push(new THREE.Vector3(x, -h/2, -d/2), new THREE.Vector3(x, -h/2, d/2));
    }
    for (let y = -h/2; y <= h/2; y += 11.6) {
        pts.push(new THREE.Vector3(-w/2, y, 0), new THREE.Vector3(w/2, y, 0));
        pts.push(new THREE.Vector3(-w/2, y, -d/2), new THREE.Vector3(-w/2, y, d/2));
    }

    // 3. Кинематические кольца и спицы
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

    // 4. Безопасная загрузка изображения с Luma-Keying
    if (typeof b64Image === 'string' && b64Image.length > 50 && b64Image.startsWith('data:image')) {
        try {
            const loader = new THREE.TextureLoader();
            loader.load(
                b64Image,
                (texture) => {
                    texture.generateMipmaps = true;
                    texture.minFilter = THREE.LinearMipmapLinearFilter;
                    const planeGeo = new THREE.PlaneGeometry(50, 50);
                    const planeMat = createDaVinciHoloMaterial(texture);
                    const planeMesh = new THREE.Mesh(planeGeo, planeMat);
                    planeMesh.position.z = 0;
                    cardGroup.add(planeMesh);
                },
                undefined,
                (err) => {
                    // Изолируем ошибку, чтобы каркас оставался рабочим
                    console.warn("Image load fallback for index:", typeIdx);
                }
            );
        } catch (e) {
            console.warn("Texture exception caught:", e);
        }
    }

    return cardGroup;
}

const floatingInventions = [
    { group: createSafeVolumetricBlueprintCard(USER_IMAGES[0], 0), basePos: new THREE.Vector3(-110, 34, 45), rotSpeed: new THREE.Vector3(0.0016, 0.0014, -0.0008), name: "Чертёж I" },
    { group: createSafeVolumetricBlueprintCard(USER_IMAGES[1], 1), basePos: new THREE.Vector3(115, -28, -40), rotSpeed: new THREE.Vector3(0.0012, 0.0018, 0.0010), name: "Чертёж II" },
    { group: createSafeVolumetricBlueprintCard(USER_IMAGES[2], 2), basePos: new THREE.Vector3(90, 36, 75), rotSpeed: new THREE.Vector3(-0.0014, 0.0016, 0.0009), name: "Чертёж III" },
    { group: createSafeVolumetricBlueprintCard(USER_IMAGES[3], 3), basePos: new THREE.Vector3(-36, -42, -35), rotSpeed: new THREE.Vector3(0.0008, 0.0012, 0.0006), name: "Чертёж IV" },
    { group: createSafeVolumetricBlueprintCard(USER_IMAGES[4], 4), basePos: new THREE.Vector3(-85, -25, 80), rotSpeed: new THREE.Vector3(-0.0012, 0.0015, -0.0007), name: "Чертёж V" }
];

const hoverTargets = [];
floatingInventions.forEach((item) => {
    item.group.position.copy(item.basePos);
    preGroup.add(item.group);

    const hitGeo = new THREE.SphereGeometry(48, 16, 16);
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

// ПЕРВЫЙ ПРИНУДИТЕЛЬНЫЙ РЕНДЕР КАДРА ДЛЯ ИСКЛЮЧЕНИЯ ЧЕРНОГО ЭКРАНА
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
    playGearDroneSound();
    
    updateSlideDots();

    hoverTargets.forEach((item, i) => {
        const isCurrent = (i === idx);
        item.isHovered = isCurrent;
        item.targetScale = isCurrent ? 1.35 : 1.0;
        item.targetZ = isCurrent ? 120 : item.basePos.z;

        item.group.traverse(child => {
            if (child.material && child.material.uniforms && child.material.uniforms.uHover) {
                child.material.uniforms.uHover.value = isCurrent ? 1.0 : 0.0;
            }
        });
    });

    const target = hoverTargets[idx];
    const objPos = target.group.position;
    const isMobile = window.innerWidth < 768;
    const zOffset = isMobile ? 125 : 105;
    targetCamPos.set(objPos.x * 0.72, objPos.y * 0.72, objPos.z + zOffset);
    targetLookTarget.set(objPos.x, objPos.y, objPos.z);

    const preset = BLUEPRINT_PRESETS[idx];
    const status = document.getElementById('loaderStatusText');
    const sub = document.getElementById('blueprintSubtitle');
    if (status && preset) {
        status.textContent = `[${idx + 1}/5] ${preset.name}`;
    }
    if (sub && preset) {
        sub.textContent = preset.subtitle;
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
    if (currentSlideIndex >= 0 && BLUEPRINT_PRESETS[currentSlideIndex]) {
        BLUEPRINT_PRESETS[currentSlideIndex].apply();
        runCalculation();
    }
    triggerIrisShutterTransition(e);
};

/* TOUCH SWIPE */
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

/* ДЕСКТОПНЫЙ РАЙКАСТЕР */
const raycaster = new THREE.Raycaster();
const mouseVec = new THREE.Vector2(-999, -999);

window.addEventListener('mousemove', (e) => {
    mouseVec.x = (e.clientX / window.innerWidth) * 2 - 1;
    mouseVec.y = -(e.clientY / window.innerHeight) * 2 + 1;
    checkRaycastHover();
});

function checkRaycastHover() {
    if (preloaderDismissed || window.innerWidth < 768) return;
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

/* МЕХАНИЧЕСКАЯ ИРИСОВАЯ ДИАФРАГМА */
let isIrisTransition = false;
let irisScene, irisCamera, irisMaterial, irisTime = 0;
const snapshotTarget = new THREE.WebGLRenderTarget(window.innerWidth, window.innerHeight);

function triggerIrisShutterTransition(event) {
    if (isIrisTransition) return;
    isIrisTransition = true;
    
    playGearDroneSound();
    playIrisShutterSound();

    const hud = document.querySelector('.preloader-fixed-hud');
    if (hud) { 
        hud.style.transition = 'opacity 0.25s ease'; 
        hud.style.opacity = '0'; 
    }

    preRenderer.setRenderTarget(snapshotTarget);
    preRenderer.clear();
    preRenderer.render(preScene, preCamera);
    preRenderer.setRenderTarget(null);

    irisScene = new THREE.Scene();
    irisCamera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);

    irisMaterial = new THREE.ShaderMaterial({
        uniforms: {
            tDiffuse: { value: snapshotTarget.texture },
            uProgress: { value: 0.0 },
            uAspect: { value: window.innerWidth / window.innerHeight },
            uTime: { value: 0.0 }
        },
        vertexShader: `varying vec2 vUv; void main() { vUv = uv; gl_Position = vec4(position, 1.0); }`,
        fragmentShader: `
            uniform sampler2D tDiffuse;
            uniform float uProgress;
            uniform float uAspect;
            uniform float uTime;
            varying vec2 vUv;

            #define BLADES 12.0
            #define PI 3.14159265359

            void main() {
                vec2 p = vUv - 0.5;
                p.x *= uAspect;
                float r = length(p);
                float theta = atan(p.y, p.x);

                float closeProgress = smoothstep(0.0, 0.72, uProgress);
                float flashProgress = smoothstep(0.72, 1.0, uProgress);

                float twist = theta + closeProgress * 2.8;
                float bladePattern = cos(twist * BLADES);
                
                float aperture = (1.0 - closeProgress) * 1.35;
                float bladeEdge = aperture + bladePattern * 0.08 * (1.0 - closeProgress);

                vec4 sceneCol = texture2D(tDiffuse, vUv);

                vec3 brassDark = vec3(0.08, 0.07, 0.04);
                vec3 brassGold = vec3(0.85, 0.71, 0.25);
                vec3 brassEdge = vec3(1.0, 0.92, 0.65);

                float rib = smoothstep(0.85, 0.98, sin(twist * BLADES * 2.0));
                vec3 bladeColor = mix(brassDark, brassGold, 0.25 + rib * 0.35);

                float edgeGlow = smoothstep(bladeEdge - 0.02, bladeEdge, r) * smoothstep(bladeEdge + 0.02, bladeEdge, r);

                vec3 col;
                float alpha = 1.0;

                if (r > bladeEdge) {
                    col = bladeColor + edgeGlow * brassEdge * 1.5;
                } else {
                    col = sceneCol.rgb;
                    col += edgeGlow * brassEdge * 2.0;
                }

                if (uProgress > 0.65 && uProgress < 0.85) {
                    float burst = 1.0 - abs(uProgress - 0.75) / 0.10;
                    col += vec3(1.0, 0.95, 0.75) * burst * 2.2;
                }

                alpha = 1.0 - flashProgress;
                gl_FragColor = vec4(col, alpha);
            }
        `,
        transparent: true
    });

    irisScene.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), irisMaterial));
}

function animatePreloader() {
    if (preloaderDismissed) return;
    requestAnimationFrame(animatePreloader);

    const elapsed = performance.now() - preloaderStartTime;
    const t = elapsed * 0.001;

    if (isIrisTransition) {
        irisTime += 0.016;
        const transProgress = Math.min(irisTime / 1.35, 1.0);
        irisMaterial.uniforms.uProgress.value = transProgress;
        irisMaterial.uniforms.uTime.value = t;

        preGroup.scale.multiplyScalar(0.96);
        astrolabeRings.forEach(item => {
            item.group.rotation.x += item.sx * 6.0;
            item.group.rotation.y += item.sy * 6.0;
        });

        preRenderer.clear();
        preRenderer.render(irisScene, irisCamera);

        if (transProgress >= 1.0) {
            dismissPreloader();
        }
        return;
    }

    dustParticles.rotation.y = t * 0.02;
    dustParticles.rotation.x = Math.sin(t * 0.015) * 0.1;

    const isFocused = currentSlideIndex !== -1;
    const ringTargetOpacity = isFocused ? 0.12 : 0.38;
    megaRingWireMat.opacity = THREE.MathUtils.lerp(megaRingWireMat.opacity, ringTargetOpacity, 0.05);

    astrolabeRings.forEach(item => {
        item.group.rotation.x += item.sx + Math.sin(t * 0.25 + item.px) * 0.0004;
        item.group.rotation.y += item.sy + Math.cos(t * 0.20 + item.py) * 0.0005;
        item.group.rotation.z += item.sz + Math.sin(t * 0.15) * 0.0003;
    });

    hoverTargets.forEach((item, idx) => {
        if (!item.isHovered) {
            item.group.position.y = item.basePos.y + Math.sin(t * 1.1 + idx * 1.5) * 7.5;
            item.group.position.x = item.basePos.x + Math.cos(t * 0.75 + idx * 1.2) * 5.0;
            item.group.rotation.x += item.rotSpeed.x;
            item.group.rotation.y += item.rotSpeed.y;
            item.group.rotation.z += item.rotSpeed.z;
        } else {
            item.group.rotation.y += 0.006;
            item.group.rotation.x = THREE.MathUtils.lerp(item.group.rotation.x, 0.1, 0.05);
        }

        item.group.position.z = THREE.MathUtils.lerp(item.group.position.z, item.targetZ, 0.08);
        item.hitMesh.position.copy(item.group.position);

        const sc = THREE.MathUtils.lerp(item.group.scale.x, item.targetScale, 0.1);
        item.group.scale.set(sc, sc, sc);

        item.group.traverse(child => {
            if (child.material && child.material.uniforms && child.material.uniforms.uTime) {
                child.material.uniforms.uTime.value = t;
            }
        });
    });

    preCamera.position.lerp(targetCamPos, 0.05);
    currentLookTarget.lerp(targetLookTarget, 0.05);
    preCamera.lookAt(currentLookTarget);

    preRenderer.clear();
    preRenderer.render(preScene, preCamera);
}

// ЗАПУСК ЦИКЛА АНИМАЦИИ
animatePreloader();

setTimeout(() => {
    if (!preloaderDismissed && currentSlideIndex === -1) {
        focusSlide(0);
    }
}, 1200);

/* ДЕКОДЕР ГЛИФОВ */
const CYRILLIC_GLYPHS = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ0123456789§$%*#@!/[]:;';
const NUMERIC_GLYPHS = '0123456789 ';
function scrambleElementText(el, finalText, duration = 460, useAlphabet = true) {
    if (!el) return;
    const glyphs = useAlphabet ? CYRILLIC_GLYPHS : NUMERIC_GLYPHS;
    const start = performance.now(), len = finalText.length;
    if (el._scrambleTimer) cancelAnimationFrame(el._scrambleTimer);
    function update(now) {
        const elapsed = now - start, progress = Math.min(elapsed / duration, 1);
        const revealIdx = Math.floor(progress * len);
        let out = '';
        for (let i = 0; i < len; i++) {
            const char = finalText[i];
            if (i < revealIdx || ' ₽%.,()/[]:'.includes(char)) out += char;
            else out += glyphs[Math.floor(Math.random() * glyphs.length)];
        }
        el.textContent = out;
        if (progress < 1) el._scrambleTimer = requestAnimationFrame(update);
        else el._scrambleTimer = null;
    }
    el._scrambleTimer = requestAnimationFrame(update);
}
function scrambleNumber(el, finalStr, duration = 400) { scrambleElementText(el, finalStr, duration, false); }
function scrambleTitle(card) {
    playClickSound(1600, 0.015);
    const titleEl = card.querySelector('.metric-title');
    if (!titleEl) return;
    const orig = titleEl.getAttribute('data-original') || titleEl.textContent;
    titleEl.setAttribute('data-original', orig);
    scrambleElementText(titleEl, orig, 380, true);
}

function selectTab(index) {
    playClickSound(1400, 0.025);
    triggerDashRingTurn();
    const buttons = document.querySelectorAll('#navTabsContainer .tab-btn');
    buttons.forEach((btn, idx) => {
        if (idx === index) { btn.className = 'tab-btn px-4 py-1.5 font-mono text-[10px] uppercase tracking-widest bg-[#d4af37] text-black font-bold transition shadow-md'; scrambleElementText(btn, TAB_TITLES[idx], 400, true); }
        else { btn.className = 'tab-btn px-4 py-1.5 font-mono text-[10px] uppercase tracking-widest opacity-70 hover:opacity-100 transition'; btn.textContent = TAB_TITLES[idx]; }
    });
    for (let i = 0; i < 4; i++) {
        const view = document.getElementById(`viewTab${i}`);
        if (i === index) { view.classList.remove('hidden'); view.classList.remove('tab-view-enter'); void view.offsetWidth; view.classList.add('tab-view-enter'); }
        else view.classList.add('hidden');
    }
}

const TAB_TITLES = ['[01] ОБСЛУЖИВАНИЕ КАПИТАЛА', '[02] СКЛАДСКОЙ ЦИКЛ', '[03] ДЕНЕЖНЫЙ ПОТОК', '[04] ЭКОНОМИКА И ЗАКАЗЫ'];
let growthMode = 'abs';
function setGrowthMode(mode) {
    playClickSound(950, 0.02); growthMode = mode;
    const btnAbs = document.getElementById('btnModeAbs'), btnPct = document.getElementById('btnModePct');
    const title = document.getElementById('lblGrowthModeTitle'), slider = document.getElementById('paramGrowthSlider');
    if (mode === 'abs') { btnAbs.className = 'py-1 font-mono text-[9px] uppercase tracking-wider bg-[#d4af37] text-black font-bold transition'; btnPct.className = 'py-1 font-mono text-[9px] uppercase tracking-wider opacity-60 hover:opacity-100 transition'; title.textContent = 'ПРИРОСТ В МЕСЯЦ'; slider.max = 100; slider.value = 5; }
    else { btnPct.className = 'py-1 font-mono text-[9px] uppercase tracking-wider bg-[#d4af37] text-black font-bold transition'; btnAbs.className = 'py-1 font-mono text-[9px] uppercase tracking-wider opacity-60 hover:opacity-100 transition'; title.textContent = 'ПРИРОСТ В %'; slider.max = 50; slider.value = 10; }
    runCalculation();
}

function parseCleanNum(val) { return typeof val === 'number' ? val : parseFloat(String(val).replace(/[^\d.-]/g, '')) || 0; }
function formatSpaced(num) { return Math.round(num).toLocaleString('ru-RU').replace(/,/g, ' '); }
function formatInput(input) {
    const el = input, cursorPos = el.selectionStart ?? el.value.length;
    const digitsBefore = el.value.slice(0, cursorPos).replace(/\D/g, '').length;
    el.value = formatSpaced(parseCleanNum(el.value));
    let newPos = 0, seen = 0;
    while (newPos < el.value.length && seen < digitsBefore) {
        if (/\d/.test(el.value[newPos])) seen++;
        newPos++;
    }
    try { el.setSelectionRange(newPos, newPos); } catch (_) {}
}

let chartDebtInstance = null, chartStockInstance = null, chartCFInstance = null, chartOrdersInstance = null, chartPieInstance = null, latestCalculatedData = null;

function runCalculation() {
    const startMonth = parseInt(document.getElementById('paramStartMonth').value);
    const startYear = parseInt(document.getElementById('paramStartYear').value);
    const period = parseInt(document.getElementById('paramPeriod').value);
    const vatRate = parseFloat(document.getElementById('paramVatRate').value);
    const vatMultiplier = 1 + (vatRate / 100);
    const marginPct = parseFloat(document.getElementById('paramMargin').value);
    document.getElementById('lblMarginVal').textContent = `${marginPct}%`;
    document.getElementById('kpiRevSub').textContent = `Маржа: ${marginPct}%`;
    const initialPurchase = parseCleanNum(document.getElementById('paramInitialPurchase').value);
    const batchCycle = parseInt(document.getElementById('paramBatchCycle').value) || 5;
    const cbRate = parseFloat(document.getElementById('paramCbRate').value) || 14.0;
    const commMargin = parseFloat(document.getElementById('paramCommMargin').value) || 2.0;
    const totalRateAnnual = cbRate + commMargin;
    const monthlyRate = (totalRateAnnual / 100) / 12;
    document.getElementById('telemetryRate').textContent = `[КАПИТАЛ: ${totalRateAnnual.toFixed(1)}% ГОДОВЫХ]`;
    document.getElementById('kpiRateSub').textContent = `Ставка ${totalRateAnnual.toFixed(1)}%`;
    const supplierPrepayPct = parseFloat(document.getElementById('paramSupplierPrepay').value);
    document.getElementById('lblSupplierPrepVal').textContent = `${supplierPrepayPct}%`;
    const supplierDelay = parseInt(document.getElementById('paramSupplierDelay').value);
    document.getElementById('lblSupplierDelayVal').textContent = `${supplierDelay} мес.`;
    const aov = parseCleanNum(document.getElementById('paramAov').value);
    const startOrders = parseInt(document.getElementById('paramStartOrders').value) || 40;
    const growthVal = parseFloat(document.getElementById('paramGrowthSlider').value);
    document.getElementById('lblGrowthVal').textContent = growthMode === 'abs' ? `+${growthVal} шт.` : `+${growthVal}%`;
    const maxOrdersCap = parseInt(document.getElementById('paramMaxOrdersCap').value) || 300;
    const fot = parseCleanNum(document.getElementById('paramFot').value);
    const wh = parseCleanNum(document.getElementById('paramWh').value);
    const office = parseCleanNum(document.getElementById('paramOffice').value);
    const factShare = parseFloat(document.getElementById('paramFactoringShare').value);
    document.getElementById('lblFactShareVal').textContent = `${factShare}%`;
    const factAdvance = 0.8;

    const shortMonths = ['Янв','Фев','Мар','Апр','Май','Июн','Июл','Авг','Сен','Окт','Ноя','Дек'];
    const xLabels = [], orders = [], rev = [];
    for (let i = 0; i < period; i++) {
        const mIdx = (startMonth + i) % 12, yOff = Math.floor((startMonth + i) / 12);
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
    cogsPayments[0] += initialPurchase * (supplierPrepayPct / 100);
    if (supplierDelay < period) cogsPayments[supplierDelay] += initialPurchase * ((100 - supplierPrepayPct) / 100);
    inventoryDeliveries[0] = initialPurchase;
    for (let b = batchCycle; b < period; b += batchCycle) {
        const bEnd = Math.min(b + batchCycle, period);
        let batchTotal = 0;
        for (let k = b; k < bEnd; k++) batchTotal += cogsVat[k];
        inventoryDeliveries[b] = batchTotal;
        cogsPayments[b] += batchTotal * (supplierPrepayPct / 100);
        const secondTrancheMonth = b + supplierDelay;
        if (secondTrancheMonth < period) cogsPayments[secondTrancheMonth] += batchTotal * ((100 - supplierPrepayPct) / 100);
    }
    const inventoryBalance = [];
    let curStock = 0;
    for (let i = 0; i < period; i++) { curStock += inventoryDeliveries[i] - cogsVat[i]; inventoryBalance.push(Math.max(curStock, 0)); }
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
            monthlyInvestments[i] = needed; currentDebt += needed; currentCash = 0; debtRepayments[i] = 0;
        } else {
            monthlyInvestments[i] = 0;
            const repay = Math.min(potCash, currentDebt);
            debtRepayments[i] = repay; currentDebt -= repay; currentCash = potCash - repay;
        }
        debtBalance[i] = currentDebt; cashBalance[i] = currentCash;
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
    let rows = '';
    for (let i = 0; i < period; i++) {
        rows += `<tr class="hover:bg-[var(--bg-cell-hover)] transition"><td class="p-3 font-bold">${xLabels[i]}</td><td class="p-3 text-[#e63946]">${formatSpaced(monthlyInvestments[i])} ₽</td><td class="p-3 text-[#d4af37]">${formatSpaced(interestPayments[i])} ₽</td><td class="p-3 text-[#2a9d8f]">${formatSpaced(debtRepayments[i])} ₽</td><td class="p-3 font-bold">${formatSpaced(debtBalance[i])} ₽</td><td class="p-3">${formatSpaced(cashBalance[i])} ₽</td></tr>`;
    }
    tbody.innerHTML = rows;

    const chartText = isDark ? '#8e8a80' : '#6b665c';
    const chartGrid = isDark ? 'rgba(212,175,55,.08)' : 'rgba(184,134,11,.12)';
    const fontMono = { family: 'JetBrains Mono', size: 10 };

    if (chartDebtInstance) chartDebtInstance.destroy();
    chartDebtInstance = new Chart(document.getElementById('chartDebt').getContext('2d'), {
        type: 'bar',
        data: { labels: xLabels, datasets: [
            { label: 'Проценты за месяц', data: interestPayments, backgroundColor: '#d4af37', order: 2 },
            { label: 'Остаток тела долга', data: debtBalance, type: 'line', borderColor: '#e63946', backgroundColor: '#e63946', borderWidth: 2.5, yAxisID: 'y1', tension: 0.3, order: 1 }
        ]},
        options: { responsive: true, maintainAspectRatio: false, scales: {
            x: { grid: { display: false }, ticks: { color: chartText, font: fontMono } },
            y: { grid: { color: chartGrid }, ticks: { color: chartText, font: fontMono } },
            y1: { position: 'right', grid: { display: false }, ticks: { color: '#e63946', font: fontMono } }
        }, plugins: { legend: { labels: { color: chartText, font: { family: 'JetBrains Mono', size: 11 } } } } }
    });

    if (chartStockInstance) chartStockInstance.destroy();
    chartStockInstance = new Chart(document.getElementById('chartStock').getContext('2d'), {
        type: 'bar',
        data: { labels: xLabels, datasets: [
            { label: 'Оплата партии поставщику', data: cogsPayments, backgroundColor: isDark ? '#52525b' : '#cbd5e1', order: 2 },
            { label: 'Остаток склада', data: inventoryBalance, type: 'line', borderColor: '#d4af37', borderWidth: 2.5, yAxisID: 'y1', tension: 0.3, order: 1 }
        ]},
        options: { responsive: true, maintainAspectRatio: false, scales: {
            x: { grid: { display: false }, ticks: { color: chartText, font: fontMono } },
            y: { grid: { color: chartGrid }, ticks: { color: chartText, font: fontMono } },
            y1: { position: 'right', grid: { display: false }, ticks: { color: '#d4af37', font: fontMono } }
        }, plugins: { legend: { labels: { color: chartText, font: { family: 'JetBrains Mono', size: 11 } } } } }
    });

    const totalOutflows = baseOutflows.map((b, idx) => b + interestPayments[idx]);
    if (chartCFInstance) chartCFInstance.destroy();
    chartCFInstance = new Chart(document.getElementById('chartCF').getContext('2d'), {
        type: 'bar',
        data: { labels: xLabels, datasets: [
            { label: 'Притоки от продаж', data: inflows, backgroundColor: '#2a9d8f' },
            { label: 'Выплаты (закупки + OPEX + %)', data: totalOutflows.map(v => -v), backgroundColor: '#e63946' }
        ]},
        options: { responsive: true, maintainAspectRatio: false, scales: {
            x: { grid: { display: false }, ticks: { color: chartText, font: fontMono } },
            y: { grid: { color: chartGrid }, ticks: { color: chartText, font: fontMono } }
        }, plugins: { legend: { labels: { color: chartText, font: { family: 'JetBrains Mono', size: 11 } } } } }
    });

    if (chartOrdersInstance) chartOrdersInstance.destroy();
    chartOrdersInstance = new Chart(document.getElementById('chartOrders').getContext('2d'), {
        type: 'bar',
        data: { labels: xLabels, datasets: [
            { label: 'Заказы, шт.', data: orders, backgroundColor: '#d4af37' },
            { label: 'Выручка, ₽', data: rev, type: 'line', borderColor: '#2a9d8f', yAxisID: 'y1', borderWidth: 2.5 }
        ]},
        options: { responsive: true, maintainAspectRatio: false, scales: {
            x: { grid: { display: false }, ticks: { color: chartText, font: fontMono } },
            y: { grid: { color: chartGrid }, ticks: { color: chartText, font: fontMono } },
            y1: { position: 'right', grid: { display: false }, ticks: { color: '#2a9d8f', font: fontMono } }
        }, plugins: { legend: { labels: { color: chartText, font: { family: 'JetBrains Mono', size: 11 } } } } }
    });

    const sumPurchases = cogsPayments.reduce((a, b) => a + b, 0);
    if (chartPieInstance) chartPieInstance.destroy();
    chartPieInstance = new Chart(document.getElementById('chartPie').getContext('2d'), {
        type: 'doughnut',
        data: { labels: ['Склад', 'Офис', 'ФОТ', 'Налоги 5%', 'Закупки', 'Проценты по долгу'], datasets: [{
            data: [wh * period, office * period, fot * period, sumTaxes, sumPurchases, sumInterest],
            backgroundColor: ['#52525b', '#71717a', '#d4af37', '#e63946', '#2a9d8f', '#457b9d']
        }]},
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { color: chartText, font: fontMono } } } }
    });
}

function exportDataToCsv() {
    playClickSound(1600, 0.05);
    if (!latestCalculatedData) return;
    const { xLabels, monthlyInvestments, interestPayments, debtRepayments, debtBalance, cashBalance } = latestCalculatedData;
    let csv = '\uFEFF' + "Период;Дотация (дефицит);Проценты по долгу;Погашение долга;Остаток тела долга;Свободный остаток счета\n";
    for (let i = 0; i < xLabels.length; i++) csv += `${xLabels[i]};${Math.round(monthlyInvestments[i])};${Math.round(interestPayments[i])};${Math.round(debtRepayments[i])};${Math.round(debtBalance[i])};${Math.round(cashBalance[i])}\n`;
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url; link.download = 'Finansovaya_Model_Kapital.csv';
    document.body.appendChild(link); link.click(); link.remove();
    URL.revokeObjectURL(url);
}

function generateExecutiveMemo() {
    playClickSound(1800, 0.04);
    if (!latestCalculatedData) return;
    const { sumRev, netProfit, roi } = latestCalculatedData;
    const memoHtml = `
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Меморандум Капитала // Executive Summary</title>
        <style>
            body { background: #070709; color: #f4f1ea; font-family: 'Georgia', serif; padding: 40px; margin: 0; }
            .memo-card { max-width: 800px; margin: 0 auto; border: 1px solid rgba(212,175,55,0.4); padding: 40px; background: rgba(13,13,18,0.95); box-shadow: 0 0 50px rgba(0,0,0,0.8); }
            h1 { font-family: 'Cormorant Garamond', serif; color: #d4af37; font-style: italic; font-size: 32px; border-bottom: 1px solid rgba(212,175,55,0.3); padding-bottom: 15px; margin-top: 0; }
            .meta { font-family: 'Courier New', monospace; font-size: 11px; color: #8e8a80; margin-bottom: 30px; }
            .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 30px 0; }
            .metric { border: 1px solid rgba(212,175,55,0.2); padding: 15px; background: rgba(255,255,255,0.02); }
            .val { font-size: 24px; color: #d4af37; font-weight: bold; margin-top: 5px; }
            p { font-size: 14px; line-height: 1.8; color: #ccc; }
            @media print { body { background: white; color: black; } .memo-card { border: none; box-shadow: none; } }
        </style>
    </head>
    <body>
        <div class="memo-card">
            <div class="meta">AUREA PROPORTIO // ФИНАНСОВЫЙ МЕМОРАНДУМ // 1 : 1.618</div>
            <h1>Архитектура Капитала и Ликвидности</h1>
            <p>Настоящий меморандум фиксирует расчётные показатели финансовой модели оборотных средств, партионных поставок и факторингового плеча.</p>
            <div class="grid">
                <div class="metric"><div>СОВОКУПНАЯ ВЫРУЧКА</div><div class="val">${formatSpaced(sumRev)} ₽</div></div>
                <div class="metric"><div>ЧИСТАЯ ПРИБЫЛЬ</div><div class="val">${formatSpaced(netProfit)} ₽</div></div>
                <div class="metric"><div>РЕНТАБЕЛЬНОСТЬ (ROI)</div><div class="val">${roi.toFixed(1)}%</div></div>
            </div>
            <p>Модель учитывает дискретные закупки, отсрочки поставщиков, налог на добавленную стоимость и стоимость заёмного капитала. Сгенерировано автоматически в защищённом контуре моделирования.</p>
            <div style="margin-top: 40px; text-align: right;"><button onclick="window.print()" style="padding: 10px 24px; background: #d4af37; color: black; font-weight: bold; border: none; cursor: pointer;">Печать / Сохранить в PDF</button></div>
        </div>
    </body>
    </html>`;
    const win = window.open('', '_blank');
    win.document.write(memoHtml);
    win.document.close();
}

let isDark = true;
function toggleTheme() {
    isDark = !isDark;
    document.documentElement.classList.toggle('dark', isDark);
    const thumb = document.getElementById('sliderThumb'), lblNight = document.getElementById('lblNight'), lblDay = document.getElementById('lblDay');
    const themeSlider = document.getElementById('themeSlider');
    if (isDark) {
        thumb.style.transform = 'translateX(0px)';
        lblNight.className = 'relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold text-black';
        lblDay.className = 'relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold opacity-70';
        dashRingMat.color.setHex(0x00aaff); megaRingWireMat.color.setHex(0x00c3ff); secondaryWireMat.color.setHex(0x0077aa);
        themeSlider.setAttribute('aria-checked', 'true');
    } else {
        thumb.style.transform = 'translateX(58px)';
        lblDay.className = 'relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold text-white';
        lblNight.className = 'relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold opacity-70';
        dashRingMat.color.setHex(0x0055aa); megaRingWireMat.color.setHex(0x0066cc); secondaryWireMat.color.setHex(0x004488);
        themeSlider.setAttribute('aria-checked', 'false');
    }
    playClickSound(900, 0.03);
    dashRenderer.render(dashScene, dashCamera);
    runCalculation();
}

const dashCanvas = document.getElementById('webgl-bg-canvas');
const dashScene = new THREE.Scene();
const dashCamera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 2000);
dashCamera.position.z = 160;
const dashRenderer = new THREE.WebGLRenderer({ canvas: dashCanvas, alpha: true, antialias: false, powerPreference: "low-power" });
dashRenderer.setSize(window.innerWidth, window.innerHeight);
dashRenderer.setPixelRatio(1);
const dashArmillary = new THREE.Group();
dashScene.add(dashArmillary);
const dashRingMat = new THREE.MeshBasicMaterial({ color: 0x00aaff, wireframe: true, transparent: true, opacity: 0.15 });
const dashRings = [];
[65, 88, 110].forEach((radius, i) => {
    const geo = new THREE.TorusGeometry(radius, 8 + i * 2, 14, 100);
    const ring = new THREE.Mesh(geo, dashRingMat);
    if (i === 0) ring.rotation.x = Math.PI / 2;
    if (i === 1) ring.rotation.y = Math.PI / 3;
    if (i === 2) ring.rotation.z = Math.PI / 4;
    dashArmillary.add(ring); dashRings.push(ring);
});
dashRenderer.render(dashScene, dashCamera);
let dashTurnProgress = 1.0, dashStartRot = [0, 0, 0], dashTargetRot = [0, 0, 0], dashAnimFrameId = null;
function triggerDashRingTurn() {
    dashStartRot = [dashRings[0].rotation.y, dashRings[1].rotation.x, dashRings[2].rotation.z];
    dashTargetRot = [
        dashStartRot[0] + (Math.PI / 2.618),
        dashStartRot[1] - (Math.PI / 3.141),
        dashStartRot[2] + (Math.PI / 4.0)
    ];
    dashTurnProgress = 0.0;
    if (dashAnimFrameId) cancelAnimationFrame(dashAnimFrameId);
    animateDashTurn();
}
function animateDashTurn() {
    dashTurnProgress += 0.025;
    const p = Math.min(dashTurnProgress, 1.0);
    const ease = p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
    dashRings[0].rotation.y = dashStartRot[0] + (dashTargetRot[0] - dashStartRot[0]) * ease;
    dashRings[1].rotation.x = dashStartRot[1] + (dashTargetRot[1] - dashStartRot[1]) * ease;
    dashRings[2].rotation.z = dashStartRot[2] + (dashTargetRot[2] - dashStartRot[2]) * ease;
    dashRenderer.render(dashScene, dashCamera);
    if (p < 1.0) dashAnimFrameId = requestAnimationFrame(animateDashTurn);
    else dashAnimFrameId = null;
}

document.addEventListener('mousemove', (e) => {
    const coord = document.getElementById('cursorCoordDisplay');
    if (coord) coord.textContent = `X: ${e.clientX.toString().padStart(4, '0')} / Y: ${e.clientY.toString().padStart(4, '0')}`;
});

document.querySelectorAll('.tilt-card').forEach(card => {
    card.addEventListener('mousemove', e => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left, y = e.clientY - rect.top;
        card.style.setProperty('--mouse-x', `${x}px`);
        card.style.setProperty('--mouse-y', `${y}px`);
        const cx = rect.width / 2, cy = rect.height / 2;
        const rx = ((y - cy) / cy) * -6, ry = ((x - cx) / cx) * 6;
        card.style.transform = `perspective(1000px) rotateX(${rx}deg) rotateY(${ry}deg) translateY(-3px)`;
    });
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)';
    });
});

window.addEventListener('resize', () => {
    preCamera.aspect = window.innerWidth / window.innerHeight;
    preCamera.updateProjectionMatrix();
    preRenderer.setSize(window.innerWidth, window.innerHeight);
    dashCamera.aspect = window.innerWidth / window.innerHeight;
    dashCamera.updateProjectionMatrix();
    dashRenderer.setSize(window.innerWidth, window.innerHeight);
    dashRenderer.render(dashScene, dashCamera);
});

setInterval(() => {
    const clock = document.getElementById('telemetryClock');
    if (clock) clock.textContent = `[${new Date().toTimeString().split(' ')[0]}]`;
}, 1000);

function resetDefaults() { playClickSound(600, 0.05); document.getElementById('financialInputsForm').reset(); runCalculation(); }

document.getElementById('themeSlider').addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggleTheme(); }
});

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => runCalculation());
else runCalculation();
</script>
</body>
</html>"""

HTML = HTML_TEMPLATE
for idx in range(5):
    val = b64_images[idx] if idx < len(b64_images) else ""
    HTML = HTML.replace(f"__IMG_{idx}__", val)

components.html(HTML, height=940, scrolling=False)
