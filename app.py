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

def get_image_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            ext = path.split('.')[-1].lower()
            mime = "image/jpeg" if ext in ["jpg", "jpeg"] else f"image/{ext}"
            return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"
    return ""

img_1 = get_image_b64("1000400438.jpg")
img_2 = get_image_b64("genio2.webp")
img_3 = get_image_b64("genio3.png")

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
<meta name="viewport" content="width=device-width, initial-scale=1.0">
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
html,body{width:100%;height:100%;margin:0;padding:0;overflow:hidden;background:var(--bg-space);color:var(--text-main);font-family:'JetBrains Mono',monospace}
:focus-visible{outline:2px solid var(--accent-gold);outline-offset:2px}
button:focus:not(:focus-visible){outline:none}
.film-grain{position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;z-index:999;opacity:var(--grain-opacity);background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
#preloader-stage{position:fixed;top:0;left:0;width:100vw;height:100vh;background:radial-gradient(circle at center,#0a0b12 0%,#030306 100%);z-index:900;overflow:hidden}
#preloader-webgl{position:absolute;inset:0;width:100%;height:100%;z-index:10;cursor:grab}
#preloader-webgl:active{cursor:grabbing}
.preloader-fixed-hud{position:absolute;inset:0;width:100%;height:100%;z-index:30;pointer-events:none;user-select:none}
#preloaderTitle{position:absolute;top:44px;left:50%;transform:translateX(-50%);font-family:'Cormorant Garamond',Georgia,serif;font-style:italic;font-size:clamp(22px,3.4vw,46px);font-weight:700;letter-spacing:.28em;color:var(--accent-gold);opacity:0;text-shadow:0 0 45px rgba(212,175,55,.85);transition:opacity 1.8s cubic-bezier(.16,1,.3,1);text-align:center;white-space:nowrap}
#preloaderTitle.locked-on{opacity:1!important}
.bottom-dock{position:absolute;bottom:40px;left:50%;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;justify-content:center;width:340px;height:56px}
#preloaderHUD{display:flex;flex-direction:column;align-items:center;gap:8px;transition:opacity .4s}
.progress-bar-bg{width:280px;height:2px;background:rgba(255,255,255,.12);position:relative;overflow:hidden}
#loaderProgressBar{position:absolute;left:0;top:0;height:100%;width:0;background:var(--accent-gold);box-shadow:0 0 10px var(--accent-gold);transition:width .1s linear}
#exploreBtnWrapper{position:absolute;opacity:0;pointer-events:none;transition:opacity .6s cubic-bezier(.19,1,.22,1),transform .6s cubic-bezier(.19,1,.22,1);transform:translateY(8px)}
#exploreBtnWrapper.active{opacity:1;pointer-events:auto;transform:translateY(0)}
.explore-btn{padding:13px 46px;background:rgba(13,13,18,.9);border:1px solid rgba(212,175,55,.95);color:#f4f1ea;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.38em;text-transform:uppercase;cursor:pointer;backdrop-filter:blur(14px);overflow:hidden;transition:all .3s;box-shadow:0 0 40px rgba(212,175,55,.35),inset 0 0 16px rgba(212,175,55,.18)}
.explore-btn::before{content:'';position:absolute;top:0;left:-100%;width:100%;height:100%;background:linear-gradient(90deg,transparent,rgba(212,175,55,.45),transparent);transition:left .7s}
.explore-btn:hover{border-color:#ffd700;color:#ffd700;box-shadow:0 0 60px rgba(212,175,55,.7),inset 0 0 24px rgba(212,175,55,.35);transform:scale(1.05)}
.explore-btn:hover::before{left:100%}
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
                <div class="progress-bar-bg mt-1"><div id="loaderProgressBar"></div></div>
            </div>
            <div id="exploreBtnWrapper">
                <button id="exploreBtn" onclick="triggerLiquidTransition(event)" class="explore-btn">Исследовать</button>
            </div>
        </div>
    </div>
</div>

<canvas id="webgl-bg-canvas"></canvas>

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

const USER_IMAGES = {
    img1: "__IMG_1__",
    img2: "__IMG_2__",
    img3: "__IMG_3__"
};

let audioCtx = null;
function playClickSound(freq = 1200, duration = 0.02) {
    try {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        if (audioCtx.state === 'suspended') audioCtx.resume();
        const osc = audioCtx.createOscillator(), gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(320, audioCtx.currentTime + duration);
        gain.gain.setValueAtTime(0.035, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(); osc.stop(audioCtx.currentTime + duration);
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
        app.classList.add('ready'); void app.offsetWidth;
        app.classList.remove('opacity-0'); app.classList.add('opacity-100');
    }
    setTimeout(() => {
        if (stage) stage.style.display = 'none';
        try {
            preScene.traverse(o => {
                if (o.geometry) o.geometry.dispose();
                if (o.material) { Array.isArray(o.material) ? o.material.forEach(m => m.dispose()) : o.material.dispose(); }
            });
            preRenderer.dispose(); preRenderer.forceContextLoss();
            snapshotTarget.dispose();
        } catch (e) {}
    }, 1350);
}

const PRELOADER_TOTAL_TIME = REDUCE_MOTION ? 1200 : 9000;
const preloaderStartTime = performance.now();

setTimeout(() => { const pt = document.getElementById('preloaderTitle'); if (pt) pt.classList.add('locked-on'); }, 900);

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

const megaRingWireMat = new THREE.MeshBasicMaterial({ color: 0x00c3ff, wireframe: true, transparent: true, opacity: 0.38 });
const secondaryWireMat = new THREE.MeshBasicMaterial({ color: 0x0077aa, wireframe: true, transparent: true, opacity: 0.22 });

function createCyclopeanTrussRing(mainRadius, tubeWidth, tubeDepth, segments) {
    const group = new THREE.Group();
    group.add(new THREE.Mesh(new THREE.TorusGeometry(mainRadius, tubeWidth * 0.45, 12, segments), megaRingWireMat));
    const linePts = [];
    const rOuter = mainRadius + tubeWidth, rInner = mainRadius - tubeWidth, zOffset = tubeDepth;
    for (let i = 0; i < segments; i++) {
        const a1 = (i / segments) * Math.PI * 2, a2 = ((i + 1) / segments) * Math.PI * 2;
        const p1_topOut = new THREE.Vector3(Math.cos(a1) * rOuter, Math.sin(a1) * rOuter, zOffset);
        const p2_topOut = new THREE.Vector3(Math.cos(a2) * rOuter, Math.sin(a2) * rOuter, zOffset);
        const p1_botOut = new THREE.Vector3(Math.cos(a1) * rOuter, Math.sin(a1) * rOuter, -zOffset);
        const p2_botOut = new THREE.Vector3(Math.cos(a2) * rOuter, Math.sin(a2) * rOuter, -zOffset);
        const p1_topIn = new THREE.Vector3(Math.cos(a1) * rInner, Math.sin(a1) * rInner, zOffset);
        const p2_topIn = new THREE.Vector3(Math.cos(a2) * rInner, Math.sin(a2) * rInner, zOffset);
        const p1_botIn = new THREE.Vector3(Math.cos(a1) * rInner, Math.sin(a1) * rInner, -zOffset);
        const p2_botIn = new THREE.Vector3(Math.cos(a2) * rInner, Math.sin(a2) * rInner, -zOffset);
        linePts.push(p1_topOut, p2_topOut, p1_botOut, p2_botOut, p1_topIn, p2_topIn, p1_botIn, p2_botIn, p1_topOut, p1_botOut, p1_topIn, p1_botIn, p1_topOut, p1_topIn, p1_botOut, p2_botIn);
        if (i % 2 === 0) linePts.push(p1_topOut, p2_botOut, p1_topIn, p2_botIn, p1_topOut, p2_topIn);
        if (i % 3 === 0) {
            const toothR = rOuter + tubeWidth * 0.42;
            const pTooth = new THREE.Vector3(Math.cos(a1) * toothR, Math.sin(a1) * toothR, 0);
            linePts.push(p1_topOut, pTooth, pTooth, p1_botOut);
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
    { group: aRing1, sx: 0.00045, sy: 0.00065, sz: 0.00025, px: 0.2, py: 1.1 },
    { group: aRing2, sx: -0.00055, sy: 0.00040, sz: -0.00045, px: 2.3, py: 0.7 },
    { group: aRing3, sx: 0.00060, sy: -0.00050, sz: 0.00035, px: 1.5, py: 3.2 }
);

function createBlueprintLineMaterial() {
    return new THREE.ShaderMaterial({
        uniforms: { uHover: { value: 0.0 }, uTime: { value: 0.0 } },
        vertexShader: `varying vec3 vPos;void main(){vPos=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}`,
        fragmentShader: `uniform float uHover;uniform float uTime;varying vec3 vPos;void main(){float wave=sin((vPos.x+vPos.y+vPos.z)*0.2-uTime*3.5)*0.5+0.5;vec3 baseGold=vec3(0.85,0.71,0.25);vec3 brightGlow=vec3(1.0,0.96,0.82);vec3 col=mix(baseGold,brightGlow,wave*0.4+uHover*0.6);float alpha=clamp(0.70+wave*0.30+uHover*0.30,0.0,1.0);gl_FragColor=vec4(col,alpha);}`,
        transparent: true, depthWrite: false
    });
}

/* 3D-чертежи */
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
            pts.push(new THREE.Vector3(Math.cos(a1) * r, -h/2, Math.sin(a1) * r), new THREE.Vector3(Math.cos(a2) * r, -h/2, Math.sin(a2) * r));
            if (r === 38 && i % 2 === 0) {
                pts.push(new THREE.Vector3(Math.cos(a1) * r, -h/2, Math.sin(a1) * r), new THREE.Vector3(Math.cos(a1) * (r + 4), -h/2, Math.sin(a1) * (r + 4)));
            }
        }
    }
    return new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(pts), createBlueprintLineMaterial());
}

function buildUltra3DClockworkGears() {
    const pts = [];
    function buildVolumetricGear(cx, cy, cz, radius, thickness, teeth, spokes) {
        const z1 = cz - thickness / 2, z2 = cz + thickness / 2;
        for (let i = 0; i < teeth * 2; i++) {
            const a1 = (i / (teeth * 2)) * Math.PI * 2;
            const a2 = ((i + 1) / (teeth * 2)) * Math.PI * 2;
            const r1 = (i % 2 === 0) ? radius + 3.0 : radius - 1.5;
            const r2 = ((i + 1) % 2 === 0) ? radius + 3.0 : radius - 1.5;
            const pF1 = new THREE.Vector3(cx + Math.cos(a1) * r1, cy + Math.sin(a1) * r1, z1);
            const pF2 = new THREE.Vector3(cx + Math.cos(a2) * r2, cy + Math.sin(a2) * r2, z1);
            const pB1 = new THREE.Vector3(cx + Math.cos(a1) * r1, cy + Math.sin(a1) * r1, z2);
            const pB2 = new THREE.Vector3(cx + Math.cos(a2) * r2, cy + Math.sin(a2) * r2, z2);
            pts.push(pF1, pF2, pB1, pB2, pF1, pB1);
        }
        for (let s = 0; s < spokes; s++) {
            const sa = (s / spokes) * Math.PI * 2;
            pts.push(new THREE.Vector3(cx, cy, z1), new THREE.Vector3(cx + Math.cos(sa) * radius, cy + Math.sin(sa) * radius, z1));
            pts.push(new THREE.Vector3(cx, cy, z2), new THREE.Vector3(cx + Math.cos(sa) * radius, cy + Math.sin(sa) * radius, z2));
            pts.push(
                new THREE.Vector3(cx + Math.cos(sa) * radius * 0.5, cy + Math.sin(sa) * radius * 0.5, z1),
                new THREE.Vector3(cx + Math.cos(sa + 0.3) * radius * 0.8, cy + Math.sin(sa + 0.3) * radius * 0.8, z2)
            );
        }
    }
    buildVolumetricGear(-16, 8, -6, 26, 6, 28, 6);
    buildVolumetricGear(18, -12, 6, 18, 5, 20, 5);
    buildVolumetricGear(16, 22, 0, 11, 4, 12, 4);
    for (let i = 0; i < 12; i++) {
        const a = (i / 12) * Math.PI * 2;
        pts.push(new THREE.Vector3(-16 + Math.cos(a) * 3, 8 + Math.sin(a) * 3, -24), new THREE.Vector3(-16 + Math.cos(a) * 3, 8 + Math.sin(a) * 3, 24));
        pts.push(new THREE.Vector3(18 + Math.cos(a) * 2.5, -12 + Math.sin(a) * 2.5, -20), new THREE.Vector3(18 + Math.cos(a) * 2.5, -12 + Math.sin(a) * 2.5, 20));
    }
    const b = 42;
    pts.push(new THREE.Vector3(-b, -b, 0), new THREE.Vector3(b, -b, 0), new THREE.Vector3(b, -b, 0), new THREE.Vector3(b, b, 0), new THREE.Vector3(b, b, 0), new THREE.Vector3(-b, b, 0), new THREE.Vector3(-b, b, 0), new THREE.Vector3(-b, -b, 0));
    for (let c = -b; c <= b; c += 7) {
        pts.push(new THREE.Vector3(c, -b, 0), new THREE.Vector3(c, -b + 2, 0), new THREE.Vector3(-b, c, 0), new THREE.Vector3(-b + 2, c, 0));
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
        pts.push(sparTop[i], sparTop[i + 1], sparBot[i], sparBot[i + 1], sparTop[i], sparBot[i], sparTop[i], sparBot[i + 1]);
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
            if (prevUpper) { pts.push(prevUpper, ribUpper, prevLower, ribLower, ribUpper, ribLower); }
            prevUpper = ribUpper; prevLower = ribLower;
            if (s === 6) {
                pts.push(rootT, ribUpper, new THREE.Vector3(0, -28, 14), ribUpper, new THREE.Vector3(0, -28, -14), ribLower);
            }
        }
    }
    pts.push(new THREE.Vector3(0, 0, -12), new THREE.Vector3(0, -32, 0), new THREE.Vector3(0, 0, 12), new THREE.Vector3(0, -32, 0), new THREE.Vector3(-14, -28, 0), new THREE.Vector3(14, -28, 0));
    return new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(pts), createBlueprintLineMaterial());
}

function buildUltra3DVitruvian() {
    const pts = [];
    const r = 36;
    for (let axis = 0; axis < 3; axis++) {
        for (let i = 0; i < 72; i++) {
            const a1 = (i / 72) * Math.PI * 2, a2 = ((i + 1) / 72) * Math.PI * 2;
            if (axis === 0) pts.push(new THREE.Vector3(Math.cos(a1) * r, Math.sin(a1) * r, 0), new THREE.Vector3(Math.cos(a2) * r, Math.sin(a2) * r, 0));
            else if (axis === 1) pts.push(new THREE.Vector3(Math.cos(a1) * r, 0, Math.sin(a1) * r), new THREE.Vector3(Math.cos(a2) * r, 0, Math.sin(a2) * r));
            else pts.push(new THREE.Vector3(0, Math.cos(a1) * r, Math.sin(a1) * r), new THREE.Vector3(0, Math.cos(a2) * r, Math.sin(a2) * r));
        }
    }
    const s = 28;
    const boxPts = [
        new THREE.Vector3(-s, -s, -s), new THREE.Vector3(s, -s, -s),
        new THREE.Vector3(s, s, -s), new THREE.Vector3(-s, s, -s),
        new THREE.Vector3(-s, -s, s), new THREE.Vector3(s, -s, s),
        new THREE.Vector3(s, s, s), new THREE.Vector3(-s, s, s)
    ];
    const edges = [[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7],[0,6],[1,7],[2,4],[3,5]];
    edges.forEach(e => pts.push(boxPts[e[0]], boxPts[e[1]]));

    let prevFib = new THREE.Vector3(0, 0, 0);
    for (let i = 1; i <= 80; i++) {
        const theta = i * 0.20, rad = 0.9 * Math.exp(0.06 * theta);
        const fibPt = new THREE.Vector3(Math.cos(theta) * rad, Math.sin(theta) * rad, Math.sin(theta * 2) * 6);
        pts.push(prevFib, fibPt); prevFib = fibPt;
    }
    pts.push(new THREE.Vector3(0, 24, 0), new THREE.Vector3(0, -20, 0), new THREE.Vector3(-28, 14, 4), new THREE.Vector3(28, 14, 4), new THREE.Vector3(-26, 26, -4), new THREE.Vector3(26, 26, -4), new THREE.Vector3(0, -20, 0), new THREE.Vector3(-18, -34, 5), new THREE.Vector3(0, -20, 0), new THREE.Vector3(18, -34, 5), new THREE.Vector3(0, -20, 0), new THREE.Vector3(-28, -26, -5), new THREE.Vector3(0, -20, 0), new THREE.Vector3(28, -26, -5));
    return new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(pts), createBlueprintLineMaterial());
}

function createWireframeFromImage(dataUriOrUrl, fallbackMesh) {
    const group = new THREE.Group();
    group.add(fallbackMesh);
    if (!dataUriOrUrl) return group;

    const img = new Image();
    img.crossOrigin = "anonymous";
    img.onload = () => {
        try {
            const canvas = document.createElement('canvas');
            canvas.width = 64; canvas.height = 64;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, 64, 64);
            const data = ctx.getImageData(0, 0, 64, 64).data;
            const detected = [];
            for (let y = 0; y < 64; y += 2) {
                for (let x = 0; x < 64; x += 2) {
                    const idx = (y * 64 + x) * 4;
                    const bright = 0.299 * data[idx] + 0.587 * data[idx + 1] + 0.114 * data[idx + 2];
                    if (bright < 165 || (bright > 60 && bright < 195)) {
                        detected.push(new THREE.Vector3(((x / 64) - 0.5) * 64, -((y / 64) - 0.5) * 64, ((bright / 255) - 0.5) * 12.0));
                    }
                }
            }
            if (detected.length > 50) {
                const linePts = [];
                for (let i = 0; i < detected.length; i += 2) {
                    const p1 = detected[i];
                    for (let j = i + 1; j < Math.min(i + 8, detected.length); j++) {
                        const p2 = detected[j];
                        if (p1.distanceTo(p2) > 1.2 && p1.distanceTo(p2) < 11.0) linePts.push(p1, p2);
                    }
                }
                if (linePts.length > 80) {
                    group.remove(fallbackMesh);
                    group.add(new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(linePts), createBlueprintLineMaterial()));
                }
            }
        } catch (e) {}
    };
    img.src = dataUriOrUrl;
    return group;
}

const floatingInventions = [
    { group: createWireframeFromImage(USER_IMAGES.img1, buildUltra3DAerialScrew()), basePos: new THREE.Vector3(-105, 28, 50), rotSpeed: new THREE.Vector3(0.0016, 0.0014, -0.0008) },
    { group: createWireframeFromImage(USER_IMAGES.img2, buildUltra3DClockworkGears()), basePos: new THREE.Vector3(110, -24, -45), rotSpeed: new THREE.Vector3(0.0012, 0.0018, 0.0010) },
    { group: createWireframeFromImage(USER_IMAGES.img3, buildUltra3DOrnithopter()), basePos: new THREE.Vector3(88, 34, 75), rotSpeed: new THREE.Vector3(-0.0014, 0.0016, 0.0009) },
    { group: createWireframeFromImage("", buildUltra3DVitruvian()), basePos: new THREE.Vector3(-30, -36, -35), rotSpeed: new THREE.Vector3(0.0008, 0.0012, 0.0006) }
];

const hoverTargets = [];
floatingInventions.forEach((item) => {
    item.group.position.copy(item.basePos);
    preGroup.add(item.group);

    const hitGeo = new THREE.SphereGeometry(44, 16, 16);
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

const raycaster = new THREE.Raycaster();
const mouseVec = new THREE.Vector2(-999, -999);
let currentHovered = null;

window.addEventListener('mousemove', (e) => {
    mouseVec.x = (e.clientX / window.innerWidth) * 2 - 1;
    mouseVec.y = -(e.clientY / window.innerHeight) * 2 + 1;
});

function checkRaycastHover() {
    if (preloaderDismissed) return;
    raycaster.setFromCamera(mouseVec, preCamera);
    const hitMeshes = hoverTargets.map(h => h.hitMesh);
    const intersects = raycaster.intersectObjects(hitMeshes, false);

    hoverTargets.forEach(item => {
        item.isHovered = false;
        item.targetScale = 1.0;
        item.targetZ = item.basePos.z;
        item.group.traverse(child => {
            if (child.isLineSegments && child.material && child.material.uniforms && child.material.uniforms.uHover) {
                child.material.uniforms.uHover.value = THREE.MathUtils.lerp(child.material.uniforms.uHover.value, 0.0, 0.08);
            }
        });
    });

    if (intersects.length > 0) {
        const hit = intersects[0].object;
        const found = hoverTargets.find(h => h.hitMesh === hit);
        if (found) {
            found.isHovered = true;
            found.targetScale = 1.35;
            found.targetZ = 135;

            const objPos = found.group.position;
            targetCamPos.set(objPos.x * 0.95, objPos.y * 0.95, objPos.z + 55);
            targetLookTarget.set(objPos.x, objPos.y, objPos.z - 10);

            found.group.traverse(child => {
                if (child.isLineSegments && child.material && child.material.uniforms && child.material.uniforms.uHover) {
                    child.material.uniforms.uHover.value = THREE.MathUtils.lerp(child.material.uniforms.uHover.value, 1.0, 0.22);
                }
            });

            if (currentHovered !== found) {
                playClickSound(1800, 0.015);
                currentHovered = found;
            }
        }
    } else {
        currentHovered = null;
        targetCamPos.set(0, 0, baseCamZ);
        targetLookTarget.set(0, 0, 0);
    }
}

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

    const hud = document.querySelector('.preloader-fixed-hud');
    if (hud) { hud.style.transition = 'opacity 0.35s ease'; hud.style.opacity = '0'; }

    preRenderer.setRenderTarget(snapshotTarget);
    preRenderer.clear();
    preRenderer.render(preScene, preCamera);
    preRenderer.setRenderTarget(null);

    rippleScene = new THREE.Scene();
    rippleCamera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);

    rippleMaterial = new THREE.ShaderMaterial({
        uniforms: {
            tDiffuse: { value: snapshotTarget.texture },
            uCenter: { value: new THREE.Vector2(clickX, clickY) },
            uProgress: { value: 0.0 },
            uAspect: { value: window.innerWidth / window.innerHeight }
        },
        vertexShader: `varying vec2 vUv;void main(){vUv=uv;gl_Position=vec4(position,1.0);}`,
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
                float waveRadius = uProgress * 2.5;
                float waveWidth = 0.40;
                float waveFactor = smoothstep(waveRadius - waveWidth, waveRadius, dist) * smoothstep(waveRadius + waveWidth, waveRadius, dist);
                float wave = sin((dist - waveRadius) * 36.0) * waveFactor * (1.0 - uProgress);
                vec2 dir = normalize(aspectAdjustedUV - aspectAdjustedCenter + 0.0001);
                vec2 offsetR = dir * wave * 0.09;
                vec2 offsetG = dir * wave * 0.07;
                vec2 offsetB = dir * wave * 0.05;
                float r = texture2D(tDiffuse, uv + offsetR).r;
                float g = texture2D(tDiffuse, uv + offsetG).g;
                float b = texture2D(tDiffuse, uv + offsetB).b;
                float fadeOut = smoothstep(0.0, 0.95, uProgress);
                gl_FragColor = vec4(r, g, b, (1.0 - fadeOut));
            }
        `,
        transparent: true
    });

    rippleScene.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), rippleMaterial));
}

function animatePreloader() {
    if (preloaderDismissed) return;
    requestAnimationFrame(animatePreloader);

    const elapsed = performance.now() - preloaderStartTime;
    const t = elapsed * 0.001;

    if (isRippling) {
        rippleTime += 0.016;
        const ripProgress = Math.min(rippleTime / 1.3, 1.0);
        rippleMaterial.uniforms.uProgress.value = ripProgress;
        preRenderer.clear();
        preRenderer.render(rippleScene, rippleCamera);
        if (ripProgress >= 1.0) dismissPreloader();
        return;
    }

    astrolabeRings.forEach(item => {
        item.group.rotation.x += item.sx + Math.sin(t * 0.25 + item.px) * 0.0004;
        item.group.rotation.y += item.sy + Math.cos(t * 0.20 + item.py) * 0.0005;
        item.group.rotation.z += item.sz + Math.sin(t * 0.15) * 0.0003;
    });

    checkRaycastHover();

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
            if (child.isLineSegments && child.material && child.material.uniforms && child.material.uniforms.uTime) {
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
animatePreloader();

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

# Безопасная подстановка без конфликтов с JS-синтаксисом
HTML = (
    HTML_TEMPLATE
    .replace("__IMG_1__", img_1)
    .replace("__IMG_2__", img_2)
    .replace("__IMG_3__", img_3)
)

components.html(HTML, height=940, scrolling=False)
