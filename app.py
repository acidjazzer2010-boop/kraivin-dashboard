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
  
    /* ТРЕХМЕРНАЯ АСТРОЛЯБИЯ ДА ВИНЧИ: ВРАЩЕНИЕ В 3D ПЛОСКОСТЯХ (X, Y, Z) */
    .astrolabe-3d-stage {
      position: relative;
      perspective: 1200px;
      transform-style: preserve-3d;
    }

    @keyframes rotate3D_Ring1 {
      0% { transform: rotateX(68deg) rotateY(18deg) rotateZ(0deg); }
      100% { transform: rotateX(68deg) rotateY(18deg) rotateZ(360deg); }
    }
    @keyframes rotate3D_Ring2 {
      0% { transform: rotateX(-42deg) rotateY(65deg) rotateZ(0deg); }
      100% { transform: rotateX(-42deg) rotateY(65deg) rotateZ(-360deg); }
    }
    @keyframes rotate3D_Ring3 {
      0% { transform: rotateX(25deg) rotateY(-58deg) rotateZ(360deg); }
      100% { transform: rotateX(25deg) rotateY(-58deg) rotateZ(0deg); }
    }
    @keyframes rotate3D_Ring4 {
      0% { transform: rotateX(80deg) rotateY(-20deg) rotateZ(0deg); }
      100% { transform: rotateX(80deg) rotateY(-20deg) rotateZ(360deg); }
    }

    .ring-3d-1 {
      position: absolute;
      inset: -28px;
      border: 1.5px solid rgba(212, 175, 55, 0.7);
      border-radius: 50%;
      transform-style: preserve-3d;
      animation: rotate3D_Ring1 16s linear infinite;
      box-shadow: 0 0 20px rgba(212, 175, 55, 0.3), inset 0 0 15px rgba(212, 175, 55, 0.15);
      pointer-events: none;
    }
    .ring-3d-1::after {
      content: '';
      position: absolute;
      top: -4px;
      left: 50%;
      width: 9px;
      height: 9px;
      background: #d4af37;
      border-radius: 50%;
      box-shadow: 0 0 14px #d4af37;
    }

    .ring-3d-2 {
      position: absolute;
      inset: -52px;
      border: 1.5px dashed rgba(212, 175, 55, 0.55);
      border-radius: 50%;
      transform-style: preserve-3d;
      animation: rotate3D_Ring2 24s linear infinite;
      pointer-events: none;
    }
    .ring-3d-2::after {
      content: '';
      position: absolute;
      bottom: -5px;
      left: 50%;
      width: 10px;
      height: 10px;
      background: #f4f1ea;
      border-radius: 50%;
      box-shadow: 0 0 14px #d4af37;
    }

    .ring-3d-3 {
      position: absolute;
      inset: -74px;
      border: 1px solid rgba(212, 175, 55, 0.4);
      border-radius: 50%;
      transform-style: preserve-3d;
      animation: rotate3D_Ring3 34s linear infinite;
      pointer-events: none;
    }
    .ring-3d-3::before {
      content: '';
      position: absolute;
      top: 50%;
      right: -4px;
      width: 8px;
      height: 8px;
      background: #d4af37;
      border-radius: 50%;
      box-shadow: 0 0 10px #d4af37;
    }

    .ring-3d-4 {
      position: absolute;
      inset: -12px;
      border: 1px dotted rgba(212, 175, 55, 0.75);
      border-radius: 50%;
      transform-style: preserve-3d;
      animation: rotate3D_Ring4 20s linear infinite;
      pointer-events: none;
    }

  </style>
</head>
<body class="selection:bg-[#d4af37] selection:text-black">

  <!-- ПРЕЛОАДЕР: АУТЕНТИЧНАЯ ГРАВЮРА ВИТРУВИАНСКОГО ЧЕЛОВЕКА С ТРЕХМЕРНО ВРАЩАЮЩЕЙСЯ АСТРОЛЯБИЕЙ (3 СЕКУНДЫ) -->
  <!-- ПРЕЛОАДЕР: 3D АСТРОЛЯБИЯ С БОЛЬШИМИ КОЛЬЦАМИ В 3 ПЛОСКОСТЯХ, ПРИБЛИЖЕНИЕМ И УДАЛЕНИЕМ (5 СЕКУНД) -->
  <div id="alche-preloader" class="fixed inset-0 z-50 flex flex-col items-center justify-center bg-[#070709] select-none" style="transition: opacity 1.0s cubic-bezier(0.19, 1, 0.22, 1), filter 1.0s cubic-bezier(0.19, 1, 0.22, 1), transform 1.0s cubic-bezier(0.19, 1, 0.22, 1);">
    
    <!-- 3D Canvas для полноэкранного рендеринга трехмерной астролябии -->
    <canvas id="preloader-3d-canvas" class="absolute inset-0 w-full h-full pointer-events-none"></canvas>

    <!-- Центральный контейнер гравюры и финансовой телеметрии -->
    <div class="relative z-10 flex flex-col items-center max-w-xl mx-auto px-6 text-center pointer-events-none">
      
      <!-- Рама с оригинальной гравюрой Витрувианского человека да Винчи -->
      <div class="relative w-64 h-64 sm:w-72 sm:h-72 mb-6 border border-[#d4af37]/70 rounded-sm overflow-hidden bg-[#0d0d12]/80 backdrop-blur-md shadow-[0_0_60px_rgba(212,175,55,0.4)] flex items-center justify-center">
        <img src="data:image/jpeg;base64,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" alt="Витрувианский человек Леонардо да Винчи" class="w-full h-full object-cover object-center filter contrast-125 brightness-95 opacity-90 transition-transform duration-[5000ms] ease-out scale-100" id="vitruvian-artwork" />
        
        <!-- Лазерный сканирующий луч -->
        <div class="absolute inset-x-0 h-1 bg-gradient-to-r from-transparent via-[#d4af37] to-transparent opacity-90 shadow-[0_0_15px_#d4af37] laser-scanner-line pointer-events-none"></div>
        
        <!-- Виньетка -->
        <div class="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_50%,rgba(7,7,9,0.75)_100%)] pointer-events-none"></div>
      </div>

      <!-- Деловой финансовый статус -->
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

    
    // --- ПРЕЛОАДЕР: 3D WEBGL СЦЕНА С БОЛЬШИМИ КОЛЬЦАМИ В 3 ПЛОСКОСТЯХ И ЗУМОМ (5 СЕКУНД) ---
    (function init3DPreloader() {
      const preloader = document.getElementById('alche-preloader');
      const canvas3d = document.getElementById('preloader-3d-canvas');
      const pctEl = document.getElementById('preloader-pct');
      const barEl = document.getElementById('preloader-bar');
      if (!preloader || !canvas3d) return;

      let pRenderer, pScene, pCamera;
      let ring1, ring2, ring3, ring4, ringGroup;
      let animFrameId = null;

      try {
        pScene = new THREE.Scene();
        pCamera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
        pCamera.position.z = 25;

        pRenderer = new THREE.WebGLRenderer({ canvas: canvas3d, alpha: true, antialias: true });
        pRenderer.setSize(window.innerWidth, window.innerHeight);
        pRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

        ringGroup = new THREE.Group();
        pScene.add(ringGroup);

        const goldMat = new THREE.MeshBasicMaterial({ color: 0xd4af37, wireframe: true, transparent: true, opacity: 0.45 });
        const brightGoldMat = new THREE.MeshBasicMaterial({ color: 0xf4f1ea, wireframe: true, transparent: true, opacity: 0.65 });
        const solidGold = new THREE.MeshBasicMaterial({ color: 0xd4af37 });

        // БОЛЬШИЕ КОЛЬЦА АСТРОЛЯБИИ В 3 РАЗНЫХ ПЛОСКОСТЯХ:
        // Кольцо 1: Огромный внешний лимб (радиус 7.2), наклон в плоскости X/Y
        ring1 = new THREE.Mesh(new THREE.TorusGeometry(7.2, 0.06, 16, 120), goldMat);
        ring1.rotation.x = Math.PI / 3;
        ringGroup.add(ring1);

        // Кольцо 2: Экваториально-эклиптическое кольцо (радиус 5.8), наклон в плоскости Y/Z
        ring2 = new THREE.Mesh(new THREE.TorusGeometry(5.8, 0.08, 16, 120), brightGoldMat);
        ring2.rotation.y = Math.PI / 4;
        ringGroup.add(ring2);

        // Кольцо 3: Высотно-азимутальное кольцо (радиус 4.5), наклон в плоскости X/Z
        ring3 = new THREE.Mesh(new THREE.TorusGeometry(4.5, 0.07, 16, 100), goldMat);
        ring3.rotation.z = Math.PI / 6;
        ringGroup.add(ring3);

        // Кольцо 4: Дополнительное прецизионное наклонное кольцо (радиус 8.5)
        ring4 = new THREE.Mesh(new THREE.TorusGeometry(8.5, 0.04, 16, 120), goldMat);
        ring4.rotation.x = -Math.PI / 4;
        ring4.rotation.y = Math.PI / 6;
        ringGroup.add(ring4);

        // Спутниковые узловые точки на кольцах
        const nodeGeo = new THREE.SphereGeometry(0.18, 16, 16);
        const node1 = new THREE.Mesh(nodeGeo, solidGold); node1.position.set(7.2, 0, 0); ring1.add(node1);
        const node2 = new THREE.Mesh(nodeGeo, solidGold); node2.position.set(0, 5.8, 0); ring2.add(node2);
        const node3 = new THREE.Mesh(nodeGeo, solidGold); node3.position.set(0, 0, 4.5); ring3.add(node3);

      } catch (e) {
        console.warn("Preloader WebGL initialization fallback:", e);
      }

      const TOTAL_DURATION = 5000; // Ровно 5 секунд (5000 мс)
      const startTime = performance.now();
      let dismissed = false;

      function dismiss() {
        if (dismissed) return;
        dismissed = true;
        if (pctEl) pctEl.textContent = '100%';
        if (barEl) barEl.style.width = '100%';

        preloader.style.opacity = '0';
        preloader.style.filter = 'blur(24px)';
        preloader.style.transform = 'scale(1.08)';
        preloader.style.pointerEvents = 'none';

        setTimeout(() => {
          preloader.style.display = 'none';
          if (animFrameId) cancelAnimationFrame(animFrameId);
          if (pRenderer) pRenderer.dispose();
        }, 1000);
      }

      function renderFrame(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / TOTAL_DURATION, 1.0);
        const p = Math.floor(progress * 100);

        if (pctEl) pctEl.textContent = `${p}%`;
        if (barEl) barEl.style.width = `${p}%`;

        // АНИМАЦИЯ 3D КОЛЕЦ В 3 ПЛОСКОСТЯХ И ПРИБЛИЖЕНИЕ/УДАЛЕНИЕ К КАМЕРЕ:
        if (ringGroup && pCamera) {
          const t = elapsed * 0.001;

          // Вращение в трех плоскостях вокруг центра
          ring1.rotation.x += 0.014;
          ring1.rotation.y += 0.008;

          ring2.rotation.y += 0.018;
          ring2.rotation.z -= 0.012;

          ring3.rotation.z += 0.016;
          ring3.rotation.x -= 0.01;

          ring4.rotation.x += 0.006;
          ring4.rotation.y -= 0.009;

          ringGroup.rotation.y += 0.005;

          // КИНЕМАТОГРАФИЧНЫЙ 3D ЗУМ: ПРИБЛИЖЕНИЕ И УДАЛЕНИЕ К КАМЕРЕ (DOLLY EFFECT)
          // За 5 секунд камера сначала приближается с расстояния 26 -> 16 (крупный план Витрувианского человека и колец),
          // затем плавно отдаляется до 21, сохраняя объемную глубину!
          pCamera.position.z = 21.0 + Math.cos(t * 1.5) * 5.0;
          pCamera.position.y = Math.sin(t * 1.2) * 0.6;

          pRenderer.render(pScene, pCamera);
        }

        if (progress < 1.0) {
          animFrameId = requestAnimationFrame(renderFrame);
        } else {
          dismiss();
        }
      }

      animFrameId = requestAnimationFrame(renderFrame);

      // Аварийная страховка на 5.2с
      setTimeout(dismiss, 5200);

      window.addEventListener('resize', () => {
        if (!pCamera || !pRenderer) return;
        pCamera.aspect = window.innerWidth / window.innerHeight;
        pCamera.updateProjectionMatrix();
        pRenderer.setSize(window.innerWidth, window.innerHeight);
      });
    })();

    runCalculation();
  </script>
</body>
</html>"""

components.html(html_code, height=1350, scrolling=True)
