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


  /* СТИЛИ КИНЕМАТОГРАФИЧНОЙ ЗАСТАВКИ ДА ВИНЧИ (3 СЕКУНДЫ) */
  #alche-preloader {
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    z-index: 9999;
    background: #070709;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    transition: opacity 1.0s cubic-bezier(0.19, 1, 0.22, 1), filter 1.0s cubic-bezier(0.19, 1, 0.22, 1), transform 1.0s cubic-bezier(0.19, 1, 0.22, 1);
  }

  .vitruvian-orb {
    position: relative;
    width: 320px;
    height: 320px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  @media (min-width: 640px) {
    .vitruvian-orb {
      width: 400px;
      height: 400px;
    }
  }

  /* Вращающиеся концентрические кольца пропорций */
  .ring-orbit-1 {
    position: absolute;
    inset: -14px;
    border: 1px solid rgba(212, 175, 55, 0.35);
    border-radius: 50%;
    animation: spinClockwise 18s linear infinite;
  }
  .ring-orbit-2 {
    position: absolute;
    inset: -32px;
    border: 1px dashed rgba(212, 175, 55, 0.22);
    border-radius: 50%;
    animation: spinCounter 26s linear infinite;
  }
  .ring-orbit-3 {
    position: absolute;
    inset: -52px;
    border: 1px dotted rgba(212, 175, 55, 0.15);
    border-radius: 50%;
    animation: spinClockwise 36s linear infinite;
  }

  @keyframes spinClockwise {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
  @keyframes spinCounter {
    from { transform: rotate(360deg); }
    to { transform: rotate(0deg); }
  }

  /* Сканирующий световой луч */
  .scan-beam {
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, transparent 0%, rgba(212, 175, 55, 0.18) 50%, transparent 100%);
    opacity: 0.6;
    animation: scanVertical 2.2s ease-in-out infinite alternate;
    pointer-events: none;
    border-radius: 50%;
  }
  @keyframes scanVertical {
    0% { transform: translateY(-40%); }
    100% { transform: translateY(40%); }
  }

  .vitruvian-portrait {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
    border: 1px solid rgba(212, 175, 55, 0.4);
    box-shadow: 0 0 45px rgba(212, 175, 55, 0.25), inset 0 0 25px rgba(0, 0, 0, 0.8);
    filter: contrast(1.15) brightness(1.05);
  }

  /* Прогресс-бар */
  .progress-track {
    width: 260px;
    height: 2px;
    background: rgba(212, 175, 55, 0.15);
    margin-top: 24px;
    position: relative;
    overflow: hidden;
  }
  .progress-fill {
    position: absolute;
    top: 0; left: 0; bottom: 0;
    width: 0%;
    background: #d4af37;
    box-shadow: 0 0 10px #d4af37;
    transition: width 0.05s linear;
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

  <!-- ВИТРУВИАНСКИЙ КИНЕМАТОГРАФИЧНЫЙ ЭКРАН (3 СЕКУНДЫ) -->
  <div id="alche-preloader">
    <div class="relative flex flex-col items-center">
      <!-- Концентрические орбиты да Винчи -->
      <div class="vitruvian-orb">
        <div class="ring-orbit-1"></div>
        <div class="ring-orbit-2"></div>
        <div class="ring-orbit-3"></div>
        <div class="scan-beam"></div>
        
        <!-- Портрет Витрувианского человека да Винчи -->
        <img class="vitruvian-portrait" src="data:image/jpeg;base64,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" alt="Витрувианский человек Леонардо да Винчи" />
      </div>

      <!-- Архитектурная телеметрия загрузки -->
      <div class="text-center mt-7 space-y-2">
        <div class="font-mono text-[9px] uppercase tracking-[0.35em] text-[#d4af37] opacity-85">
          [САКРАЛЬНАЯ ГЕОМЕТРИЯ // AUREA PROPORTIO 1 : 1.618]
        </div>
        <div class="font-serif italic text-3xl sm:text-4xl font-bold tracking-wide text-[#f4f1ea]">
          Витрувианский Канон
        </div>
        
        <!-- Индикатор прогресса -->
        <div class="flex items-center justify-center gap-3 font-mono text-[10px] text-[#8e8a80] pt-2">
          <span class="pulse-dot"></span>
          <span id="splashStatusText">ИНИЦИАЛИЗАЦИЯ САКРАЛЬНОЙ ГЕОМЕТРИИ...</span>
          <span id="splashPctDisplay" class="text-[#d4af37] font-bold">000%</span>
        </div>

        <div class="progress-track mx-auto">
          <div id="splashProgressFill" class="progress-fill"></div>
        </div>
      </div>
    </div>
  </div>



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

    

    // --- ТОЧНЫЙ 3-СЕКУНДНЫЙ КИНЕМАТОГРАФИЧНЫЙ ПРЕЛОАДЕР ---
    (function initVitruvianSplash() {
      const preloader = document.getElementById('alche-preloader');
      const progressFill = document.getElementById('splashProgressFill');
      const statusText = document.getElementById('splashStatusText');
      const pctDisplay = document.getElementById('splashPctDisplay');
      if (!preloader) return;

      const DURATION = 3000; // Ровно 3.0 секунды
      const startTime = performance.now();

      const messages = [
        'ИНИЦИАЛИЗАЦИЯ САКРАЛЬНОЙ ГЕОМЕТРИИ...',
        'КАЛИБРОВКА КРЕДИТНОГО ПЛЕЧА И СТАВОК...',
        'ПОСТРОЕНИЕ СКЛАДСКИХ ТРАНШЕЙ...',
        'ГАРМОНИЗАЦИЯ ПОТОКОВ КАПИТАЛА...'
      ];

      function updateSplash(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / DURATION, 1);
        const pct = Math.floor(progress * 100);

        if (progressFill) progressFill.style.width = pct + '%';
        if (pctDisplay) pctDisplay.textContent = String(pct).padStart(3, '0') + '%';

        // Ротация статусов
        const msgIdx = Math.min(Math.floor(progress * messages.length), messages.length - 1);
        if (statusText) statusText.textContent = messages[msgIdx];

        if (progress < 1) {
          requestAnimationFrame(updateSplash);
        } else {
          // Ровно через 3 секунды запускаем расфокус и открываем дашборд
          if (statusText) statusText.textContent = 'КАНОН СФОРМИРОВАН';
          setTimeout(() => {
            preloader.style.filter = 'blur(28px)';
            preloader.style.transform = 'scale(1.09)';
            preloader.style.opacity = '0';
            setTimeout(() => {
              preloader.style.display = 'none';
              preloader.remove();
            }, 1000);
          }, 150);
        }
      }
      requestAnimationFrame(updateSplash);
    })();

    window.onload = () => {
      runCalculation();
    };
  </script>
</body>
</html>"""

components.html(html_code, height=1350, scrolling=True)
