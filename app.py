import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Архитектура Капитала // Финансовое Моделирование",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Скрываем системные элементы Streamlit для чистого отображения монолита
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
  
    
    
    /* РЕФЕРЕНСНАЯ 3D АРМИЛЛЯРНАЯ СФЕРА (PURE CSS 3D - БЕЗ ВНЕШНИХ ЗАВИСИМОСТЕЙ) */
    #alche-preloader {
      perspective: 1400px;
      overflow: hidden;
    }

    .armillary-stage {
      position: relative;
      width: 320px;
      height: 320px;
      transform-style: preserve-3d;
      animation: sceneRotate 24s linear infinite;
    }

    @keyframes sceneRotate {
      0% { transform: rotateX(25deg) rotateY(0deg); }
      100% { transform: rotateX(25deg) rotateY(360deg); }
    }

    .arm-ring {
      position: absolute;
      inset: 0;
      border-radius: 50%;
      transform-style: preserve-3d;
      pointer-events: none;
    }

    /* Кольцо 1: Золотое (горизонтальное / экваториальное, как на референсе) */
    .ring-gold {
      border: 6px solid #d4af37;
      box-shadow: 0 0 20px rgba(212, 175, 55, 0.6), inset 0 0 10px rgba(212, 175, 55, 0.4);
      transform: rotateX(90deg);
      animation: spinRingGold 8s linear infinite;
    }
    .ring-gold::after {
      content: '';
      position: absolute;
      right: -8px;
      top: 50%;
      margin-top: -6px;
      width: 12px;
      height: 12px;
      background: #f4f1ea;
      border-radius: 50%;
      box-shadow: 0 0 12px #ffffff;
    }

    /* Кольцо 2: Бирюзовое/Тиловое (вертикальное меридиональное) */
    .ring-teal {
      border: 6px solid #2a9d8f;
      box-shadow: 0 0 20px rgba(42, 157, 143, 0.6), inset 0 0 10px rgba(42, 157, 143, 0.4);
      transform: rotateY(90deg);
      animation: spinRingTeal 12s linear infinite;
    }

    /* Кольцо 3: Красное/Бордовое (диагональное эклиптическое) */
    .ring-red {
      border: 6px solid #e63946;
      box-shadow: 0 0 20px rgba(230, 57, 70, 0.6), inset 0 0 10px rgba(230, 57, 70, 0.4);
      transform: rotateX(45deg) rotateY(45deg);
      animation: spinRingRed 10s linear infinite;
    }

    @keyframes spinRingGold {
      0% { transform: rotateX(90deg) rotateZ(0deg); }
      100% { transform: rotateX(90deg) rotateZ(360deg); }
    }
    @keyframes spinRingTeal {
      0% { transform: rotateY(90deg) rotateZ(0deg); }
      100% { transform: rotateY(90deg) rotateZ(360deg); }
    }
    @keyframes spinRingRed {
      0% { transform: rotateX(45deg) rotateY(45deg) rotateZ(0deg); }
      100% { transform: rotateX(45deg) rotateY(45deg) rotateZ(360deg); }
    }

    /* Статичный Витрувианский человек в центре (без пергамента) */
    .vitruvian-static-core {
      position: absolute;
      top: 50%;
      left: 50%;
      width: 190px;
      height: 190px;
      margin-top: -95px;
      margin-left: -95px;
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 10;
      pointer-events: none;
      transform: translateZ(0px);
    }

  </style>
</head>
<body class="selection:bg-[#d4af37] selection:text-black">

  <!-- ПРЕЛОАДЕР: АУТЕНТИЧНАЯ ГРАВЮРА ВИТРУВИАНСКОГО ЧЕЛОВЕКА С ТРЕХМЕРНО ВРАЩАЮЩЕЙСЯ АСТРОЛЯБИЕЙ (3 СЕКУНДЫ) -->
  
  <!-- ЭКРАН ЗАГРУЗКИ: 3D АНИМАЦИЯ НА PURE CSS (5 СЕКУНД) -->
  <!-- ПРЕЛОАДЕР: 3D АРМИЛЛЯРНАЯ СФЕРА С ВРАЩЕНИЕМ КОЛЕЦ В 3 ПЛОСКОСТЯХ И СТАТИЧНЫМ ВИТРУВИАНСКИМ ЧЕЛОВЕКОМ (5 СЕКУНД) -->
  <!-- ПРЕЛОАДЕР: АРМИЛЛЯРНАЯ СФЕРА (РЕФЕРЕНС 1000400440.GIF) + СТАТИЧНЫЙ ВИТРУВИАНСКИЙ ЧЕЛОВЕК (5 СЕКУНД) -->
  <div id="alche-preloader" class="fixed inset-0 z-50 flex flex-col items-center justify-center bg-[#070709] select-none" style="transition: opacity 1.0s cubic-bezier(0.19, 1, 0.22, 1), filter 1.0s cubic-bezier(0.19, 1, 0.22, 1);">
    
    <div class="relative flex flex-col items-center justify-center w-full h-full">
      
      <!-- 3D Сцена армиллярных колец по референсу -->
      <div class="armillary-stage mb-8">
        
        <!-- 3 независимых кольца в трех плоскостях (Золотое, Тиловое, Красное) -->
        <div class="arm-ring ring-gold"></div>
        <div class="arm-ring ring-teal"></div>
        <div class="arm-ring ring-red"></div>
        
        <!-- Абсолютно статичная фигура Витрувианского человека в центре (без пергамента) -->
        <div class="vitruvian-static-core">
          <img src="data:image/png;base64,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" alt="Витрувианский человек" class="w-full h-full object-contain filter drop-shadow-[0_0_20px_rgba(212,175,55,0.6)] opacity-95" />
        </div>
      </div>

      <!-- Финансовый статус и прогресс заставки -->
      <div class="absolute bottom-16 z-20 flex flex-col items-center text-center w-full px-6 pointer-events-none">
        <div class="space-y-2">
          <div class="font-mono text-[9px] uppercase tracking-[0.3em] text-[#d4af37] opacity-90">
            [ФИНАНСОВОЕ МОДЕЛИРОВАНИЕ // СИСТЕМА 2026]
          </div>
          <h2 class="font-serif italic text-2xl sm:text-3xl font-bold tracking-wider text-[#f4f1ea]">
            Архитектура Капитала
          </h2>
          <p class="font-mono text-[10px] text-[#8e8a80] max-w-sm mx-auto tracking-wide">
            Моделирование денежных потоков, партионных закупок и кредитной нагрузки
          </p>

          <!-- Прогресс-бар ровно на 5 секунд -->
          <div class="pt-3 w-64 mx-auto space-y-1.5">
            <div class="flex justify-between items-center font-mono text-[9px]">
              <span class="text-[#8e8a80] uppercase tracking-wider flex items-center gap-1.5">
                <span class="pulse-dot"></span> КАЛИБРОВКА МОДЕЛИ
              </span>
              <span id="preloader-pct" class="text-[#d4af37] font-bold">0%</span>
            </div>
            <div class="w-full h-[2px] bg-[#d4af37]/20 rounded-full overflow-hidden">
              <div id="preloader-bar" class="h-full bg-gradient-to-r from-[#d4af37] via-[#f4f1ea] to-[#d4af37] w-0 transition-all duration-[30ms] ease-linear"></div>
            </div>
          </div>
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

    // АБСОЛЮТНАЯ СТРАХОВКА: Этот блок выполнится самым первым и гарантированно снимет заставку, даже если дальше будет фатальная ошибка JS!
    (function absoluteFailsafe() {
      setTimeout(() => {
        try {
          const preloader = document.getElementById('alche-preloader');
          if (preloader && preloader.style.display !== 'none') {
             preloader.style.opacity = '0';
             preloader.style.pointerEvents = 'none';
             setTimeout(() => preloader.style.display = 'none', 1000);
          }
        } catch(e) {}
      }, 5500);
    })();

    // --- 0. АУДИОСИНТЕЗАТОР ТАКТИЛЬНЫХ КЛИКОВ (Web Audio API) ---
    let audioCtx = null;
    function playClickSound(freq = 1200, duration = 0.02) {
      try {
        if (!audioCtx) {
          const AudioCtor = window.AudioContext || window.webkitAudioContext;
          if (!AudioCtor) return;
          audioCtx = new AudioCtor();
        }
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
    let scene, camera, renderer, armillaryGroup;
    try {
      const canvas = document.getElementById('webgl-bg-canvas');
      scene = new THREE.Scene();
      camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 1000);
      camera.position.z = 24;

      renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

      armillaryGroup = new THREE.Group();
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
      if (!scene || !renderer || !camera || !armillaryGroup) return;
      requestAnimationFrame(animate);
      armillaryGroup.rotation.x += 0.002 + (mouseY - armillaryGroup.rotation.x) * 0.04;
      armillaryGroup.rotation.y += 0.003 + (mouseX - armillaryGroup.rotation.y) * 0.04;
      camera.position.z += (currentCamPreset.z - camera.position.z) * 0.05;
      renderer.render(scene, camera);
    }
    animate();

    window.addEventListener('resize', () => {
      if (!camera || !renderer) return;
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });
    } catch(e) { console.warn("WebGL BG failed:", e); }

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

    
    // --- ПРЕЛОАДЕР: 3D THREE.JS АРМИЛЛЯРНЫЕ КОЛЬЦА + ЗУМ (5 СЕКУНД) ---
    // --- ПРЕЛОАДЕР: РОВНО 5 СЕКУНД + ГАРАНТИРОВАННЫЙ ЗАПУСК ДАШБОРДА ---
    (function runPureCSSPreloader() {
      const preloader = document.getElementById('alche-preloader');
      const pctEl = document.getElementById('preloader-pct');
      const barEl = document.getElementById('preloader-bar');
      if (!preloader) return;

      const DURATION = 5000; // Ровно 5 секунд (5000 мс)
      const startTime = performance.now();
      let dismissed = false;

      function dismissPreloader() {
        if (dismissed) return;
        dismissed = true;
        if (pctEl) pctEl.textContent = '100%';
        if (barEl) barEl.style.width = '100%';

        preloader.style.opacity = '0';
        preloader.style.filter = 'blur(20px)';
        preloader.style.pointerEvents = 'none';

        setTimeout(() => {
          preloader.style.display = 'none';
          // ГАРАНТИРОВАННЫЙ ЗАПУСК РАСЧЕТА И ДАШБОРДА ПОСЛЕ ПРЕЛОАДЕРА
          try {
            runCalculation();
          } catch(e) {
            console.error("Dashboard init error:", e);
          }
        }, 900);
      }

      function tick(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / DURATION, 1.0);
        const p = Math.floor(progress * 100);

        if (pctEl) pctEl.textContent = `${p}%`;
        if (barEl) barEl.style.width = `${p}%`;

        if (progress < 1.0) {
          requestAnimationFrame(tick);
        } else {
          dismissPreloader();
        }
      }

      requestAnimationFrame(tick);

      // Железобетонная страховка скрытия на 5.3с
      setTimeout(() => {
        if (!dismissed) dismissPreloader();
      }, 5300);
    })();

    runCalculation();
          } catch(err) {
            console.error("Run calculation error:", err);
          }
        }, 900);
      }

      function loop(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / TOTAL_DURATION, 1.0);
        const p = Math.floor(progress * 100);

        if (pctEl) pctEl.textContent = `${p}%`;
        if (barEl) barEl.style.width = `${p}%`;

        if (ringGroup && camera) {
          const t = elapsed * 0.001;

          // Независимое вращение колец в трех плоскостях
          if (ringX) ringX.rotation.z += 0.015;
          if (ringY) ringY.rotation.x += 0.02;
          if (ringZ) ringZ.rotation.y += 0.012;

          ringGroup.rotation.y += 0.004;

          // Приближение и удаление к камере (Dolly zoom / Zoom in & Zoom out за 5 секунд)
          camera.position.z = 20.0 + Math.sin(t * 1.3) * 6.0;
          
          renderer.render(scene, camera);
        }

        if (progress < 1.0) {
          animId = requestAnimationFrame(loop);
        } else {
          dismiss();
        }
      }

      animId = requestAnimationFrame(loop);

      // Аварийная страховка на 5.3с для гарантированного показа дашборда
      setTimeout(() => {
        if (!dismissed) dismiss();
      }, 5300);

      window.addEventListener('resize', () => {
        if (!camera || !renderer) return;
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
      });
    })();

    runCalculation();
  </script>
</body>
</html>"""

components.html(html_code, height=1350, scrolling=True)
