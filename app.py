import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Архитектура Капитала // Финансовое Моделирование",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Скрываем системные элементы Streamlit для кинематографичного монолита
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

html_code = """<!DOCTYPE html>
<html lang="ru" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Архитектура Капитала // Финансовое Моделирование</title>

  <!-- Типографика: Cormorant Garamond, JetBrains Mono, Inter -->
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

  <!-- Three.js & Chart.js -->
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
      --cursor-glow: rgba(212, 175, 55, 0.18);
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

    body {
      background-color: var(--bg-space);
      color: var(--text-main);
      font-family: 'JetBrains Mono', monospace;
      overflow-x: hidden;
      margin: 0;
      padding: 0;
      transition: background-color 0.5s cubic-bezier(0.16, 1, 0.3, 1), color 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Архитектурный аналоговый шум кинопленки (Film Grain) */
    .film-grain {
      position: fixed;
      inset: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      z-index: 50;
      opacity: var(--grain-opacity);
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
    }

    #webgl-bg-canvas {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: 0;
      pointer-events: none;
      opacity: 0.45;
      transition: opacity 0.5s ease;
    }
    html:not(.dark) #webgl-bg-canvas {
      opacity: 0.18;
    }

    .alche-block {
      position: relative;
      background: var(--bg-panel);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-right: 1px solid var(--border-line);
      border-bottom: 1px solid var(--border-line);
      transition: background-color 0.3s ease, border-color 0.3s ease;
    }

    /* Координатные перекрестия сетки */
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

    /* Рельефная оптика через SVG feSpecularLighting */
    .specular-emboss {
      filter: url(#specular-glass-filter);
      transition: filter 0.2s ease, transform 0.3s ease;
    }
    .specular-emboss:hover {
      transform: scale(1.08) rotate(4deg);
    }

    /* 3D Tilt Карточки с динамическим курсорным бликом */
    .tilt-card {
      position: relative;
      overflow: hidden;
      transform-style: preserve-3d;
      perspective: 900px;
      transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.3s ease;
    }
    .tilt-card::before {
      content: '';
      position: absolute;
      inset: 0;
      border: 1px solid transparent;
      background: radial-gradient(350px circle at var(--mouse-x, 0px) var(--mouse-y, 0px), var(--cursor-glow), transparent 70%);
      opacity: 0;
      transition: opacity 0.35s ease;
      pointer-events: none;
      z-index: 2;
    }
    .tilt-card:hover::before {
      opacity: 1;
    }

    /* Двухфазное раскрытие вкладок */
    @keyframes alcheTabEntrance {
      0% {
        opacity: 0;
        filter: blur(14px);
        transform: translateY(12px) scale(0.992);
        clip-path: inset(0 0 100% 0);
      }
      45% {
        opacity: 0.85;
        clip-path: inset(0 0 0% 0);
      }
      100% {
        opacity: 1;
        filter: blur(0px);
        transform: translateY(0) scale(1);
        clip-path: inset(0 0 0% 0);
      }
    }
    .tab-view-enter {
      animation: alcheTabEntrance 0.72s cubic-bezier(0.19, 1, 0.22, 1) forwards;
      will-change: transform, opacity, filter, clip-path;
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
      transition: transform 0.2s ease, background-color 0.2s ease;
    }
    input[type="range"]::-webkit-slider-thumb:hover {
      transform: rotate(45deg) scale(1.35);
    }

    .mono-input {
      background: var(--input-bg);
      border: 1px solid var(--border-line);
      color: var(--text-main);
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      padding: 7px 10px;
      width: 100%;
      border-radius: 0;
      transition: border-color 0.2s ease, background 0.2s ease;
    }
    .mono-input:focus {
      outline: none;
      border-color: var(--accent-gold);
      background: rgba(212, 175, 55, 0.06);
    }
    select.mono-input option {
      background-color: #0d0d12;
      color: #f4f1ea;
    }
    html:not(.dark) select.mono-input option {
      background-color: #f4f1ea;
      color: #141416;
    }

    /* Тактильный тумблер */
    .hw-slider-track {
      position: relative;
      width: 140px;
      height: 30px;
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
      width: 66px;
      background: var(--accent-gold);
      transition: transform 0.45s cubic-bezier(0.19, 1, 0.22, 1), background-color 0.3s ease;
    }

    /* Индикатор пульса телеметрии */
    .pulse-dot {
      display: inline-block;
      width: 6px;
      height: 6px;
      border-radius: 9999px;
      background-color: var(--accent-gold);
      animation: pulseAnim 2s infinite ease-in-out;
    }
    @keyframes pulseAnim {
      0%, 100% { opacity: 0.4; transform: scale(0.9); }
      50% { opacity: 1; transform: scale(1.2); }
    }

    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--border-line); }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent-gold); }
  </style>
</head>
<body class="selection:bg-[#d4af37] selection:text-black">

  <!-- КИНЕМАТОГРАФИЧНЫЙ ВИТРУВИАНСКИЙ ПРЕЛОАДЕР (РОVНО 3 СЕКУНДЫ + 1 СЕКУНДА РАСФОКУСА) -->
  <div id="alche-preloader" class="fixed inset-0 z-50 flex flex-col items-center justify-center bg-[#070709] select-none pointer-events-auto" style="transition: opacity 1.0s cubic-bezier(0.19, 1, 0.22, 1), filter 1.0s cubic-bezier(0.19, 1, 0.22, 1), transform 1.0s cubic-bezier(0.19, 1, 0.22, 1);">
    
    <!-- Фоновые сакральные сетки -->
    <div class="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(212,175,55,0.08)_0%,transparent_70%)] pointer-events-none"></div>

    <div class="relative flex flex-col items-center max-w-xl mx-auto px-6 text-center">
      
      <!-- Контейнер гравюры с вращающимися астрономическими кругами -->
      <div class="relative w-72 h-72 sm:w-80 sm:h-80 mb-6 flex items-center justify-center">
        <!-- Внешние вращающиеся геометрические орбиты -->
        <div class="absolute -inset-4 border border-[#d4af37]/25 rounded-full animate-[spin_24s_linear_infinite] pointer-events-none"></div>
        <div class="absolute -inset-8 border border-dashed border-[#d4af37]/20 rounded-full animate-[spin_40s_linear_infinite_reverse] pointer-events-none"></div>
        <div class="absolute -inset-12 border border-[#d4af37]/10 rounded-full animate-[spin_60s_linear_infinite] pointer-events-none"></div>

        <!-- Перекрестия сакральных осей -->
        <div class="absolute inset-x-0 top-1/2 h-[1px] bg-gradient-to-r from-transparent via-[#d4af37]/30 to-transparent pointer-events-none"></div>
        <div class="absolute inset-y-0 left-1/2 w-[1px] bg-gradient-to-b from-transparent via-[#d4af37]/30 to-transparent pointer-events-none"></div>

        <!-- Карточка гравюры Витрувианского человека -->
        <div class="relative w-64 h-64 sm:w-72 sm:h-72 border border-[#d4af37]/40 rounded-sm overflow-hidden bg-[#0d0d12] shadow-[0_0_50px_rgba(212,175,55,0.2)]">
          <img src="data:image/jpeg;base64,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" alt="Витрувианский человек Леонардо да Винчи" class="w-full h-full object-cover object-center filter contrast-125 brightness-95 opacity-90 transition-transform duration-[3000ms] ease-out scale-100 hover:scale-105" id="vitruvian-artwork" />
          
          <!-- Сканирующий лазерный луч (Laser Scanline) -->
          <div class="absolute inset-x-0 h-1.5 bg-gradient-to-r from-transparent via-[#d4af37] to-transparent opacity-75 shadow-[0_0_15px_#d4af37] animate-[scanLaser_3s_ease-in-out_infinite] pointer-events-none"></div>
          
          <!-- Виньетка по краям изображения -->
          <div class="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_45%,rgba(7,7,9,0.85)_100%)] pointer-events-none"></div>
        </div>
      </div>

      <!-- Текстовый блок инициализации -->
      <div class="space-y-2.5 z-10">
        <div class="font-mono text-[9px] uppercase tracking-[0.35em] text-[#d4af37] opacity-85">
          [САКРАЛЬНАЯ ГЕОМЕТРИЯ // AUREA PROPORTIO 1 : 1.618]
        </div>
        <h2 class="font-serif italic text-2xl sm:text-3xl font-bold tracking-wider text-[#f4f1ea]">
          Витрувианский Канон
        </h2>
        <p class="font-mono text-[10px] text-[#8e8a80] max-w-sm mx-auto tracking-wide">
          «Пропорции человеческого тела упорядочены природой согласно законам высшей гармонии»
        </p>

        <!-- Прогресс-бар и счетчик ровно на 3 секунды -->
        <div class="pt-3 w-64 mx-auto space-y-1.5">
          <div class="flex justify-between items-center font-mono text-[9px]">
            <span class="text-[#8e8a80] uppercase tracking-wider flex items-center gap-1.5">
              <span class="pulse-dot"></span> ИНИЦИАЛИЗАЦИЯ
            </span>
            <span id="preloader-pct" class="text-[#d4af37] font-bold">0%</span>
          </div>
          <div class="w-full h-[2px] bg-[#d4af37]/20 rounded-full overflow-hidden">
            <div id="preloader-bar" class="h-full bg-gradient-to-r from-[#d4af37] via-[#f4f1ea] to-[#d4af37] w-0 transition-all duration-[75ms] ease-linear"></div>
          </div>
        </div>

      </div>

    </div>
  </div>

  <style>
    @keyframes scanLaser {
      0% { top: -5%; opacity: 0; }
      15% { opacity: 0.9; }
      85% { opacity: 0.9; }
      100% { top: 105%; opacity: 0; }
    }
  </style>

  <div class="film-grain"></div>

  <!-- Оптический стеклянно-металлический фильтр SVG feSpecularLighting -->
  <svg width="0" height="0" class="absolute pointer-events-none" style="position: fixed;">
    <defs>
      <filter id="specular-glass-filter" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur in="SourceAlpha" stdDeviation="2.2" result="blurMap" />
        <feDiffuseLighting in="blurMap" surfaceScale="3" diffuseConstant="1.1" lighting-color="#ffffff" result="diffuseLight">
          <fePointLight id="svgCursorLightDiff" x="120" y="40" z="50" />
        </feDiffuseLighting>
        <feSpecularLighting in="blurMap" surfaceScale="4.5" specularConstant="1.4" specularExponent="24" lighting-color="#d4af37" result="specularGlare">
          <fePointLight id="svgCursorLightSpec" x="120" y="40" z="70" />
        </feSpecularLighting>
        <feComposite in="SourceGraphic" in2="diffuseLight" operator="arithmetic" k1="0" k2="1" k3="0.35" k4="0" result="litGraphic" />
        <feComposite in="specularGlare" in2="SourceGraphic" operator="in" result="glareMasked" />
        <feBlend in="glareMasked" in2="litGraphic" mode="screen" />
      </filter>
    </defs>
  </svg>

  <canvas id="webgl-bg-canvas"></canvas>

  <div class="relative z-10 min-h-screen flex flex-col border-t border-l" style="border-color: var(--border-line);">

    <!-- ВЕРХНИЙ HUD И ПАНЕЛЬ ТЕЛЕМЕТРИИ -->
    <header class="alche-block px-5 lg:px-8 py-3 flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center gap-6">
        <div class="flex items-center gap-3">
          <svg class="w-7 h-7 text-[#d4af37] specular-emboss cursor-pointer" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.2">
            <circle cx="16" cy="16" r="14" />
            <rect x="6" y="6" width="20" height="20" />
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
        <!-- Кнопка мгновенного скачивания отчета (без перезагрузки страницы) -->
        <button id="downloadReportBtn" onclick="exportDataToCsv()" type="button" class="px-3.5 py-1.5 border font-mono text-[10px] uppercase tracking-widest hover:border-[#d4af37] hover:bg-[#d4af37]/10 transition flex items-center gap-2">
          <span>↓ Скачать отчет</span>
        </button>

        <!-- Аппаратный ползунок "День / Ночь" -->
        <div id="themeSlider" class="hw-slider-track" onclick="toggleTheme()" title="Переключить режим: Ночь / День">
          <div id="sliderThumb" class="hw-slider-thumb" style="transform: translateX(0px);"></div>
          <span id="lblNight" class="relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold text-black">Ночь</span>
          <span id="lblDay" class="relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold opacity-70">День</span>
        </div>
      </div>
    </header>

    <!-- Основная рабочая сетка -->
    <div class="flex-1 grid grid-cols-1 lg:grid-cols-12">

      <!-- ЛЕВАЯ ПАНЕЛЬ ПАРАМЕТРОВ -->
      <aside class="lg:col-span-3 flex flex-col">
        <div class="alche-block cross-tl px-5 py-3.5 flex items-center justify-between">
          <span class="font-mono text-[10px] uppercase tracking-[0.2em] text-[#d4af37] font-bold">[00] Параметры Модели</span>
          <button id="defaultResetBtn" type="button" onclick="resetDefaults()" class="font-mono text-[9px] uppercase underline opacity-60 hover:opacity-100 transition">Сброс</button>
        </div>

        <form id="financialInputsForm" class="flex-1 flex flex-col" onsubmit="event.preventDefault();">
          <!-- Секция I: Горизонт и маржинальность -->
          <div class="alche-block p-5 space-y-4">
            <div class="flex justify-between items-baseline">
              <span class="font-serif italic text-base font-semibold">I. Временной горизонт и маржа</span>
              <span class="font-mono text-[9px] opacity-40">01 // 04</span>
            </div>

            <div class="grid grid-cols-2 gap-2.5">
              <div>
                <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Месяц старта</label>
                <select id="paramStartMonth" class="mono-input" onchange="playClickSound(); runCalculation();">
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
                <select id="paramStartYear" class="mono-input" onchange="playClickSound(); runCalculation();">
                  <option value="2026" selected>2026</option>
                  <option value="2027">2027</option>
                </select>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-2.5">
              <div>
                <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Горизонт</label>
                <select id="paramPeriod" class="mono-input" onchange="playClickSound(); runCalculation();">
                  <option value="6">6 месяцев</option>
                  <option value="12" selected>12 месяцев</option>
                  <option value="18">18 месяцев</option>
                  <option value="24">24 месяца</option>
                </select>
              </div>
              <div>
                <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Ставка НДС</label>
                <select id="paramVatRate" class="mono-input" onchange="playClickSound(); runCalculation();">
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
              <input type="range" id="paramMargin" min="10" max="50" step="1" value="20" oninput="runCalculation()">
            </div>
          </div>

          <!-- Секция II: Партионный склад и кредитная ставка -->
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

          <!-- Секция III: Масштабирование заказов -->
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
              <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Логика прироста</label>
              <div class="grid grid-cols-2 border" style="border-color: var(--border-line);">
                <button type="button" id="btnModeAbs" onclick="setGrowthMode('abs')" class="py-1 font-mono text-[9px] uppercase tracking-wider bg-[#d4af37] text-black font-bold transition">В штуках</button>
                <button type="button" id="btnModePct" onclick="setGrowthMode('pct')" class="py-1 font-mono text-[9px] uppercase tracking-wider opacity-60 hover:opacity-100 transition">В процентах</button>
              </div>
            </div>

            <div>
              <div class="flex justify-between font-mono text-[10px] mb-1">
                <span id="lblGrowthModeTitle" class="opacity-70">ПРИРОСТ В МЕСЯЦ</span>
                <span id="lblGrowthVal" class="text-[#d4af37] font-bold">+5 шт.</span>
              </div>
              <input type="range" id="paramGrowthSlider" min="0" max="100" step="1" value="5" oninput="runCalculation()">
            </div>

            <div>
              <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Потолок продаж в месяц, шт.</label>
              <input type="number" id="paramMaxOrdersCap" value="300" min="10" step="10" class="mono-input text-center" oninput="runCalculation()">
            </div>
          </div>

          <!-- Секция IV: Постоянные затраты и факторинг -->
          <div class="alche-block p-5 space-y-4 flex-1">
            <div class="flex justify-between items-baseline">
              <span class="font-serif italic text-base font-semibold">IV. Постоянные затраты и факторинг</span>
              <span class="font-mono text-[9px] opacity-40">04 // 04</span>
            </div>

            <div class="grid grid-cols-3 gap-2">
              <div>
                <label class="block font-mono text-[8px] uppercase opacity-70 mb-1">ФОТ, ₽</label>
                <input type="text" id="paramFot" value="500 000" class="mono-input" oninput="formatInput(this); runCalculation();">
              </div>
              <div>
                <label class="block font-mono text-[8px] uppercase opacity-70 mb-1">Склад, ₽</label>
                <input type="text" id="paramWh" value="200 000" class="mono-input" oninput="formatInput(this); runCalculation();">
              </div>
              <div>
                <label class="block font-mono text-[8px] uppercase opacity-70 mb-1">Офис, ₽</label>
                <input type="text" id="paramOffice" value="150 000" class="mono-input" oninput="formatInput(this); runCalculation();">
              </div>
            </div>

            <div class="grid grid-cols-2 gap-3 pt-1">
              <div>
                <div class="flex justify-between font-mono text-[9px] mb-1">
                  <span class="opacity-70">ПРЕДОПЛАТА</span>
                  <span id="lblPrepVal">50%</span>
                </div>
                <input type="range" id="paramPrepaymentPct" min="0" max="100" step="10" value="50" oninput="runCalculation()">
              </div>
              <div>
                <div class="flex justify-between font-mono text-[9px] mb-1">
                  <span class="opacity-70">ФАКТОРИНГ</span>
                  <span id="lblFactShareVal">50%</span>
                </div>
                <input type="range" id="paramFactoringShare" min="0" max="100" step="10" value="50" oninput="runCalculation()">
              </div>
            </div>
          </div>
        </form>
      </aside>

      <!-- ПРАВАЯ ЧАСТЬ: ДАШБОРД И АНАЛИТИКА -->
      <section class="lg:col-span-9 flex flex-col">
        <!-- 5 Архитектурных KPI-карточек с 3D Tilt и спарклайнами -->
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 border-b" style="border-color: var(--border-line);">
          <div class="alche-block tilt-card p-5">
            <div class="flex justify-between items-center opacity-60 mb-1">
              <span class="font-mono text-[9px] uppercase tracking-widest">[01] Выручка</span>
              <svg class="w-8 h-3 text-[#d4af37]" viewBox="0 0 32 12" fill="none"><path d="M1 11L9 8L17 9L25 3L31 1" stroke="currentColor" stroke-width="1.2"/></svg>
            </div>
            <div id="kpiRev" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#f4f1ea]">0 ₽</div>
            <div class="font-mono text-[9px] text-[#d4af37] mt-1.5 opacity-90" id="kpiRevSub">Маржа: 20%</div>
          </div>

          <div class="alche-block tilt-card p-5">
            <div class="flex justify-between items-center opacity-60 mb-1">
              <span class="font-mono text-[9px] uppercase tracking-widest">[02] Дефицит</span>
              <svg class="w-8 h-3 text-[#e63946]" viewBox="0 0 32 12" fill="none"><path d="M1 2L9 2L17 8L25 10L31 11" stroke="currentColor" stroke-width="1.2"/></svg>
            </div>
            <div id="kpiInjections" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#e63946]">0 ₽</div>
            <div class="font-mono text-[9px] text-[#e63946] mt-1.5 opacity-90">Внешние дотации</div>
          </div>

          <div class="alche-block tilt-card p-5">
            <div class="flex justify-between items-center opacity-60 mb-1">
              <span class="font-mono text-[9px] uppercase tracking-widest">[03] Проценты</span>
              <span class="pulse-dot"></span>
            </div>
            <div id="kpiInterest" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#d4af37]">0 ₽</div>
            <div id="kpiRateSub" class="font-mono text-[9px] text-[#d4af37] mt-1.5 opacity-90">Ставка 19.0%</div>
          </div>

          <div class="alche-block tilt-card p-5">
            <div class="flex justify-between items-center opacity-60 mb-1">
              <span class="font-mono text-[9px] uppercase tracking-widest">[04] Пиковый долг</span>
            </div>
            <div id="kpiMaxDebt" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#f4f1ea]">0 ₽</div>
            <div class="font-mono text-[9px] opacity-60 mt-1.5">Максимум тела</div>
          </div>

          <div class="alche-block tilt-card p-5 col-span-2 sm:col-span-1">
            <div class="flex justify-between items-center opacity-60 mb-1">
              <span class="font-mono text-[9px] uppercase tracking-widest">[05] Прибыль</span>
              <svg class="w-8 h-3 text-[#2a9d8f]" viewBox="0 0 32 12" fill="none"><path d="M1 10L10 9L18 6L24 5L31 1" stroke="currentColor" stroke-width="1.2"/></svg>
            </div>
            <div id="kpiProfit" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#2a9d8f]">0 ₽</div>
            <div id="kpiRoiSub" class="font-mono text-[9px] text-[#2a9d8f] mt-1.5 opacity-90">Рентабельность: 0%</div>
          </div>
        </div>

        <!-- Навигационные вкладки -->
        <div class="alche-block px-5 py-2.5 flex items-center justify-between border-b" style="border-color: var(--border-line);">
          <div class="flex flex-wrap items-center gap-1.5" id="navTabsContainer">
            <button type="button" onclick="selectTab(0)" class="tab-btn px-4 py-1.5 font-mono text-[10px] uppercase tracking-widest bg-[#d4af37] text-black font-bold transition shadow-md">[01] ОБСЛУЖИВАНИЕ КАПИТАЛА</button>
            <button type="button" onclick="selectTab(1)" class="tab-btn px-4 py-1.5 font-mono text-[10px] uppercase tracking-widest opacity-70 hover:opacity-100 transition">[02] СКЛАДСКОЙ ЦИКЛ</button>
            <button type="button" onclick="selectTab(2)" class="tab-btn px-4 py-1.5 font-mono text-[10px] uppercase tracking-widest opacity-70 hover:opacity-100 transition">[03] ДЕНЕЖНЫЙ ПОТОК</button>
            <button type="button" onclick="selectTab(3)" class="tab-btn px-4 py-1.5 font-mono text-[10px] uppercase tracking-widest opacity-70 hover:opacity-100 transition">[04] ЭКОНОМИКА И ЗАКАЗЫ</button>
          </div>
          <div class="hidden md:flex items-center gap-2 font-mono text-[9px] text-[#d4af37]">
            <span class="pulse-dot"></span>
            <span>THREE.JS & SVG LIGHTING</span>
          </div>
        </div>

        <!-- Динамические секции -->
        <div class="flex-1 p-5 lg:p-7 space-y-6">
          <!-- Секция 01: Долг и проценты -->
          <div id="viewTab0" class="tab-view-enter space-y-6">
            <div class="alche-block p-5 border">
              <div class="flex justify-between items-center mb-4">
                <div>
                  <h3 class="font-serif text-xl font-bold tracking-wide italic">График обслуживания долга и начисления процентов</h3>
                  <p class="font-mono text-[10px] opacity-60">Ежемесячные проценты по ставке кредитора (столбцы) и динамика тела долга (кривая)</p>
                </div>
              </div>
              <div class="h-[360px] relative">
                <canvas id="chartDebt"></canvas>
              </div>
            </div>

            <!-- Таблица долговой ведомости -->
            <div class="alche-block border overflow-x-auto">
              <table class="w-full text-left font-mono text-[11px]">
                <thead class="border-b" style="background-color: var(--table-header-bg); border-color: var(--border-line);">
                  <tr class="text-[9px] uppercase tracking-widest text-[#d4af37]">
                    <th class="p-3">Период</th>
                    <th class="p-3">Дотация (вход)</th>
                    <th class="p-3">Проценты</th>
                    <th class="p-3">Погашение долга</th>
                    <th class="p-3">Остаток долга</th>
                    <th class="p-3">Свободный остаток</th>
                  </tr>
                </thead>
                <tbody id="tableDebtBody" class="divide-y" style="border-color: var(--border-line);"></tbody>
              </table>
            </div>
          </div>

          <!-- Секция 02: Складской цикл -->
          <div id="viewTab1" class="hidden space-y-6">
            <div class="alche-block p-5 border">
              <div class="flex justify-between items-center mb-4">
                <div>
                  <h3 class="font-serif text-xl font-bold tracking-wide italic">Партионные закупки и истощение склада</h3>
                  <p class="font-mono text-[10px] opacity-60">Закупка дискретными циклами каждые N месяцев без ежемесячного задвоения</p>
                </div>
              </div>
              <div class="h-[400px] relative">
                <canvas id="chartStock"></canvas>
              </div>
            </div>
          </div>

          <!-- Секция 03: Денежный поток -->
          <div id="viewTab2" class="hidden space-y-6">
            <div class="alche-block p-5 border">
              <div class="flex justify-between items-center mb-4">
                <div>
                  <h3 class="font-serif text-xl font-bold tracking-wide italic">Структура помесячного денежного потока</h3>
                  <p class="font-mono text-[10px] opacity-60">Сопоставление входящей выручки и совокупных выплат (закупки, аренда, ФОТ и налоги)</p>
                </div>
              </div>
              <div class="h-[400px] relative">
                <canvas id="chartCF"></canvas>
              </div>
            </div>
          </div>

          <!-- Секция 04: Заказы и структура затрат -->
          <div id="viewTab3" class="hidden space-y-6">
            <div class="grid grid-cols-1 xl:grid-cols-2 gap-6">
              <div class="alche-block p-5 border">
                <h3 class="font-serif text-xl font-bold tracking-wide italic mb-1">Динамика заказов и выручки</h3>
                <p class="font-mono text-[10px] opacity-60 mb-4">Рост клиентской базы и масштабирование объемов отгрузок</p>
                <div class="h-[320px] relative">
                  <canvas id="chartOrders"></canvas>
                </div>
              </div>

              <div class="alche-block p-5 border">
                <h3 class="font-serif text-xl font-bold tracking-wide italic mb-1">Структура совокупных затрат</h3>
                <p class="font-mono text-[10px] opacity-60 mb-4">Доли расходов с учетом себестоимости, инфраструктуры и процентов по долгу</p>
                <div class="h-[320px] relative">
                  <canvas id="chartPie"></canvas>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>

  <script>
    // --- 0. АУДИОСИНТЕЗАТОР ТАКТИЛЬНЫХ КЛИКОВ (Web Audio API) ---
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    function playClickSound(freq = 1200, duration = 0.02) {
      try {
        if (audioCtx.state === 'suspended') audioCtx.resume();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(300, audioCtx.currentTime + duration);
        gain.gain.setValueAtTime(0.04, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
      } catch (e) {}
    }

    // --- 1. THREE.JS RENAISSANCE ARMILLARY SPHERE ---
    const canvas = document.getElementById('webgl-bg-canvas');
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 24;

    const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    const armillaryGroup = new THREE.Group();
    scene.add(armillaryGroup);

    let ringColor = 0xd4af37;
    const ringMat = new THREE.MeshBasicMaterial({ color: ringColor, wireframe: true, transparent: true, opacity: 0.32 });

    const rings = [
      new THREE.Mesh(new THREE.TorusGeometry(8.5, 0.04, 16, 120), ringMat),
      new THREE.Mesh(new THREE.TorusGeometry(10.5, 0.03, 16, 120), ringMat),
      new THREE.Mesh(new THREE.TorusGeometry(12.5, 0.025, 16, 120), ringMat),
      new THREE.Mesh(new THREE.IcosahedronGeometry(4.8, 1), ringMat)
    ];

    rings[0].rotation.x = Math.PI / 4;
    rings[1].rotation.y = Math.PI / 3;
    rings[2].rotation.z = Math.PI / 6;

    rings.forEach(r => armillaryGroup.add(r));

    let mouseX = 0, mouseY = 0;
    const lightDiff = document.getElementById('svgCursorLightDiff');
    const lightSpec = document.getElementById('svgCursorLightSpec');

    document.addEventListener('mousemove', (e) => {
      mouseX = (e.clientX - window.innerWidth / 2) * 0.0006;
      mouseY = (e.clientY - window.innerHeight / 2) * 0.0006;
      document.getElementById('cursorCoordDisplay').textContent = `X: ${e.clientX.toString().padStart(4, '0')} / Y: ${e.clientY.toString().padStart(4, '0')}`;

      // Динамическое смещение луча в SVG feSpecularLighting
      if (lightDiff && lightSpec) {
        const lx = e.clientX % 320;
        const ly = e.clientY % 220;
        lightDiff.setAttribute('x', lx);
        lightDiff.setAttribute('y', ly);
        lightSpec.setAttribute('x', lx);
        lightSpec.setAttribute('y', ly);
      }
    });

    // 3D Tilt Карточки с магнитным наклоном
    document.querySelectorAll('.tilt-card').forEach(card => {
      card.addEventListener('mousemove', e => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        card.style.setProperty('--mouse-x', `${x}px`);
        card.style.setProperty('--mouse-y', `${y}px`);
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = ((y - centerY) / centerY) * -5;
        const rotateY = ((x - centerX) / centerX) * 5;
        card.style.transform = `perspective(900px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-2px)`;
      });
      card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(900px) rotateX(0deg) rotateY(0deg) translateY(0px)';
      });
    });

    const camPresets = [
      { z: 24, rx: 0.2, ry: 0.3 },
      { z: 19, rx: -0.4, ry: 1.1 },
      { z: 27, rx: 0.5, ry: -0.6 },
      { z: 18, rx: 0.1, ry: 2.2 }
    ];
    let currentCamPreset = camPresets[0];

    function animate() {
      requestAnimationFrame(animate);
      armillaryGroup.rotation.x += 0.002 + (mouseY - armillaryGroup.rotation.x) * 0.04;
      armillaryGroup.rotation.y += 0.003 + (mouseX - armillaryGroup.rotation.y) * 0.04;
      camera.position.z += (currentCamPreset.z - camera.position.z) * 0.05;
      renderer.render(scene, camera);
    }
    animate();

    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });

    // --- 2. HARDWARE DAY / NIGHT SWITCH ---
    let isDark = true;
    function toggleTheme() {
      playClickSound(800, 0.04);
      isDark = !isDark;
      document.documentElement.classList.toggle('dark', isDark);
      const thumb = document.getElementById('sliderThumb');
      const lblNight = document.getElementById('lblNight');
      const lblDay = document.getElementById('lblDay');

      if (isDark) {
        thumb.style.transform = 'translateX(0px)';
        lblNight.className = 'relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold text-black';
        lblDay.className = 'relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold opacity-70';
        ringMat.color.setHex(0xd4af37);
      } else {
        thumb.style.transform = 'translateX(62px)';
        lblDay.className = 'relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold text-white';
        lblNight.className = 'relative z-10 font-mono text-[9px] uppercase tracking-widest font-bold opacity-70';
        ringMat.color.setHex(0x1d756b);
      }
      runCalculation();
    }

    // --- 3. MATRIX CIPHER / ПОДБОР БУКВ И ЦИФР ДЛЯ СЛОЖЕНИЯ СЛОВА ---
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
          if (i < revealIdx || char === ' ' || char === '₽' || char === '%' || char === '.' || char === ',' || char === '(' || char === ')' || char === '/' || char === '[' || char === ']' || char === ':') {
            out += char;
          } else {
            out += glyphs[Math.floor(Math.random() * glyphs.length)];
          }
        }
        el.textContent = out;
        if (progress < 1) {
          el._scrambleTimer = requestAnimationFrame(update);
        } else {
          el.textContent = finalText;
          el._scrambleTimer = null;
        }
      }
      el._scrambleTimer = requestAnimationFrame(update);
    }

    function scrambleNumber(el, finalStr, duration = 400) {
      scrambleElementText(el, finalStr, duration, false);
    }

    // --- 4. TAB CONTROLLER WITH CINEMATIC REVEAL & CIPHER SCRAMBLE ---
    const TAB_TITLES = [
      '[01] ОБСЛУЖИВАНИЕ КАПИТАЛА',
      '[02] СКЛАДСКОЙ ЦИКЛ',
      '[03] ДЕНЕЖНЫЙ ПОТОК',
      '[04] ЭКОНОМИКА И ЗАКАЗЫ'
    ];

    function selectTab(index) {
      playClickSound(1400, 0.025);
      currentCamPreset = camPresets[index];
      const buttons = document.querySelectorAll('#navTabsContainer .tab-btn');
      buttons.forEach((btn, idx) => {
        if (idx === index) {
          btn.className = 'tab-btn px-4 py-1.5 font-mono text-[10px] uppercase tracking-widest bg-[#d4af37] text-black font-bold transition shadow-md';
          scrambleElementText(btn, TAB_TITLES[idx], 420, true);
        } else {
          btn.className = 'tab-btn px-4 py-1.5 font-mono text-[10px] uppercase tracking-widest opacity-70 hover:opacity-100 transition';
          btn.textContent = TAB_TITLES[idx];
        }
      });

      for (let i = 0; i < 4; i++) {
        const view = document.getElementById(`viewTab${i}`);
        if (i === index) {
          view.classList.remove('hidden');
          view.classList.remove('tab-view-enter');
          void view.offsetWidth; // trigger reflow
          view.classList.add('tab-view-enter');

          const headerTitles = view.querySelectorAll('h3');
          headerTitles.forEach(h => {
            const orig = h.getAttribute('data-original-text') || h.textContent;
            h.setAttribute('data-original-text', orig);
            scrambleElementText(h, orig, 520, true);
          });
        } else {
          view.classList.add('hidden');
        }
      }
    }

    // --- 5. FINANCIAL MODEL CORE ENGINE ---
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
        title.textContent = 'ПРИРОСТ В МЕСЯЦ';
        slider.max = 100;
        slider.value = 5;
      } else {
        btnPct.className = 'py-1 font-mono text-[9px] uppercase tracking-wider bg-[#d4af37] text-black font-bold transition';
        btnAbs.className = 'py-1 font-mono text-[9px] uppercase tracking-wider opacity-60 hover:opacity-100 transition';
        title.textContent = 'ПРИРОСТ В %';
        slider.max = 50;
        slider.value = 10;
      }
      runCalculation();
    }

    function parseCleanNum(val) {
      if (typeof val === 'number') return val;
      return parseFloat(String(val).replace(/[^\d.-]/g, '')) || 0;
    }

    function formatSpaced(num) {
      return Math.round(num).toLocaleString('ru-RU').replace(/,/g, ' ');
    }

    function formatInput(input) {
      const val = parseCleanNum(input.value);
      input.value = formatSpaced(val);
    }

    let chartDebtInstance = null;
    let chartStockInstance = null;
    let chartCFInstance = null;
    let chartOrdersInstance = null;
    let chartPieInstance = null;

    let latestCalculatedData = null;

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
      const xLabels = [];
      const orders = [];
      const rev = [];

      for (let i = 0; i < period; i++) {
        const mIdx = (startMonth + i) % 12;
        const yOff = Math.floor((startMonth + i) / 12);
        xLabels.push(`${shortMonths[mIdx]} ${startYear + yOff}`);

        let curOrders = 0;
        if (i === 0) {
          curOrders = startOrders;
        } else {
          curOrders = growthMode === 'abs' ? orders[i - 1] + growthVal : orders[i - 1] * (1 + growthVal / 100);
        }
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

      const opex = [];
      for (let i = 0; i < period; i++) {
        const base = 150000 + wh + office + fot;
        opex.push(i >= 6 ? base * 1.2 : base);
      }
      const taxes = rev.map(r => r * 0.05);

      const baseOutflows = [];
      for (let i = 0; i < period; i++) {
        baseOutflows.push(cogsPayments[i] + opex[i] + taxes[i]);
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

      const sumRev = rev.reduce((a, b) => a + b, 0);
      const sumInvestments = monthlyInvestments.reduce((a, b) => a + b, 0);
      const sumInterest = interestPayments.reduce((a, b) => a + b, 0);
      const maxDebt = Math.max(...debtBalance);
      const sumOpex = opex.reduce((a, b) => a + b, 0);
      const sumTaxes = taxes.reduce((a, b) => a + b, 0);
      const netProfit = sumRev * (marginPct / 100) - sumOpex - sumTaxes - sumInterest;
      const roi = sumRev > 0 ? (netProfit / sumRev) * 100 : 0;

      latestCalculatedData = {
        xLabels, monthlyInvestments, interestPayments, debtRepayments, debtBalance, cashBalance, sumRev, netProfit, roi
      };

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
        tr.innerHTML = `
          <td class="p-3 font-bold">${xLabels[i]}</td>
          <td class="p-3 text-[#e63946]">${formatSpaced(monthlyInvestments[i])} ₽</td>
          <td class="p-3 text-[#d4af37]">${formatSpaced(interestPayments[i])} ₽</td>
          <td class="p-3 text-[#2a9d8f]">${formatSpaced(debtRepayments[i])} ₽</td>
          <td class="p-3 font-bold">${formatSpaced(debtBalance[i])} ₽</td>
          <td class="p-3">${formatSpaced(cashBalance[i])} ₽</td>
        `;
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
          responsive: true, maintainAspectRatio: false,
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
          responsive: true, maintainAspectRatio: false,
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
          responsive: true, maintainAspectRatio: false,
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
          responsive: true, maintainAspectRatio: false,
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
          responsive: true, maintainAspectRatio: false,
          plugins: { legend: { position: 'bottom', labels: { color: chartText, font: { family: 'JetBrains Mono', size: 10 } } } }
        }
      });
    }

    // Мгновенный экспорт в CSV прямо в браузере без обращения к бэкенду
    function exportDataToCsv() {
      playClickSound(1600, 0.05);
      if (!latestCalculatedData) return;
      const { xLabels, monthlyInvestments, interestPayments, debtRepayments, debtBalance, cashBalance } = latestCalculatedData;
      
      let csvContent = "data:text/csv;charset=utf-8,﻿";
      csvContent += "Период;Дотация (дефицит);Проценты по долгу;Погашение долга;Остаток тела долга;Свободный остаток счета\n";

      for (let i = 0; i < xLabels.length; i++) {
        csvContent += `${xLabels[i]};${Math.round(monthlyInvestments[i])};${Math.round(interestPayments[i])};${Math.round(debtRepayments[i])};${Math.round(debtBalance[i])};${Math.round(cashBalance[i])}\n`;
      }

      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", "Finansovaya_Model_Kapital.csv");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }

    // Часы в HUD
    setInterval(() => {
      const now = new Date();
      document.getElementById('telemetryClock').textContent = `[${now.toTimeString().split(' ')[0]}]`;
    }, 1000);

    function resetDefaults() {
      playClickSound(600, 0.05);
      document.getElementById('financialInputsForm').reset();
      runCalculation();
    }

    
    // --- ПРЕЛОАДЕР: РОВНО 3 СЕКУНДЫ АКТИВНОСТИ + ПРЕМИАЛЬНЫЙ РАСФОКУС ---
    (function runVitruvianIntro() {
      const preloader = document.getElementById('alche-preloader');
      const pctEl = document.getElementById('preloader-pct');
      const barEl = document.getElementById('preloader-bar');
      const artwork = document.getElementById('vitruvian-artwork');
      if (!preloader) return;

      const TOTAL_DURATION = 3000; // Ровно 3 секунды показа заставки
      const startTime = performance.now();

      function updateProgress(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / TOTAL_DURATION, 1.0);
        const percentVal = Math.floor(progress * 100);

        if (pctEl) pctEl.textContent = `${percentVal}%`;
        if (barEl) barEl.style.width = `${progress * 100}%`;

        if (progress < 1.0) {
          requestAnimationFrame(updateProgress);
        } else {
          // Ровно через 3.0 секунды запускается кинематографичный расфокус и растворение
          if (pctEl) pctEl.textContent = '100%';
          if (barEl) barEl.style.width = '100%';

          setTimeout(() => {
            // Звук завершения калибровки
            playClickSound(1800, 0.06);

            // Плавный расфокус, масштабирование и растворение за 1 секунду
            preloader.style.opacity = '0';
            preloader.style.filter = 'blur(22px)';
            preloader.style.transform = 'scale(1.06)';

            setTimeout(() => {
              preloader.style.display = 'none';
            }, 1000);
          }, 150);
        }
      }

      requestAnimationFrame(updateProgress);
    })();

    window.onload = () => {
      runCalculation();
    };
  </script>
</body>
</html>"""

components.html(html_code, height=1350, scrolling=True)
