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
  
    
    /* ИСТИННАЯ CSS 3D АНИМАЦИЯ: 3 ПЛОСКОСТИ + ПРИБЛИЖЕНИЕ И УДАЛЕНИЕ */
    #alche-preloader {
      perspective: 1200px;
      overflow: hidden;
    }
    
    .camera-dolly {
      transform-style: preserve-3d;
      animation: dollyZoom 5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
      position: relative;
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    
    /* Анимация камеры: наезд на фигуру и отдаление */
    @keyframes dollyZoom {
      0% { transform: translateZ(-600px) scale(0.6); opacity: 0; }
      20% { opacity: 1; }
      50% { transform: translateZ(300px) scale(1.3); } /* Максимальное приближение */
      90% { transform: translateZ(0px) scale(1.0); opacity: 1; filter: blur(0px); }
      100% { transform: translateZ(100px) scale(1.1); opacity: 0; filter: blur(20px); }
    }

    .astrolabe-group {
      position: relative;
      width: 320px;
      height: 320px;
      transform-style: preserve-3d;
      animation: globalSpin 20s linear infinite;
    }

    @keyframes globalSpin {
      0% { transform: rotateY(0deg) rotateX(10deg); }
      100% { transform: rotateY(360deg) rotateX(10deg); }
    }

    .astro-ring {
      position: absolute;
      inset: 0;
      border-radius: 50%;
      transform-style: preserve-3d;
      pointer-events: none;
    }

    /* Кольцо 1: Экватор (ось X) */
    .ring-1 {
      border: 3px solid rgba(212, 175, 55, 0.85);
      border-left: 3px dashed rgba(212, 175, 55, 0.4);
      animation: spinX 8s linear infinite;
      box-shadow: 0 0 25px rgba(212, 175, 55, 0.4), inset 0 0 15px rgba(212, 175, 55, 0.2);
    }
    .ring-1::before {
      content: ''; position: absolute; top: -5px; left: 50%; width: 10px; height: 10px; background: #d4af37; border-radius: 50%; box-shadow: 0 0 15px #d4af37;
    }

    /* Кольцо 2: Меридиан (ось Y) */
    .ring-2 {
      border: 2px solid rgba(244, 241, 234, 0.7);
      border-top: 2px dotted rgba(212, 175, 55, 0.9);
      animation: spinY 12s linear infinite;
      transform: scale(1.15);
    }
    .ring-2::after {
      content: ''; position: absolute; bottom: -4px; left: 50%; width: 8px; height: 8px; background: #f4f1ea; border-radius: 50%; box-shadow: 0 0 10px #f4f1ea;
    }

    /* Кольцо 3: Эклиптика (ось Z и диагональ) */
    .ring-3 {
      border: 4px groove rgba(212, 175, 55, 0.6);
      animation: spinZ 15s linear infinite;
      transform: scale(1.3) rotateX(45deg);
    }

    @keyframes spinX { 100% { transform: rotateX(360deg); } }
    @keyframes spinY { 100% { transform: scale(1.15) rotateY(-360deg); } }
    @keyframes spinZ { 100% { transform: scale(1.3) rotateX(45deg) rotateZ(360deg); } }

    /* Центральная фигура Витрувианского человека */
    .vitruvian-core {
      position: absolute;
      top: 50%;
      left: 50%;
      width: 240px;
      height: 240px;
      margin-top: -120px;
      margin-left: -120px;
      border: 1px solid rgba(212, 175, 55, 0.6);
      background: rgba(13, 13, 18, 0.9);
      box-shadow: 0 0 50px rgba(212, 175, 55, 0.5);
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      transform: translateZ(0px); /* Anchor in 3D space */
    }

  </style>
</head>
<body class="selection:bg-[#d4af37] selection:text-black">

  <!-- ПРЕЛОАДЕР: АУТЕНТИЧНАЯ ГРАВЮРА ВИТРУВИАНСКОГО ЧЕЛОВЕКА С ТРЕХМЕРНО ВРАЩАЮЩЕЙСЯ АСТРОЛЯБИЕЙ (3 СЕКУНДЫ) -->
  
  <!-- ЭКРАН ЗАГРУЗКИ: 3D АНИМАЦИЯ НА PURE CSS (5 СЕКУНД) -->
  <!-- ПРЕЛОАДЕР: 3D АРМИЛЛЯРНАЯ СФЕРА С ВРАЩЕНИЕМ КОЛЕЦ В 3 ПЛОСКОСТЯХ И СТАТИЧНЫМ ВИТРУВИАНСКИМ ЧЕЛОВЕКОМ (5 СЕКУНД) -->
  <div id="alche-preloader" class="fixed inset-0 z-50 flex flex-col items-center justify-center bg-[#070709] select-none" style="transition: opacity 1.0s cubic-bezier(0.19, 1, 0.22, 1), filter 1.0s cubic-bezier(0.19, 1, 0.22, 1);">
    
    <!-- 3D WebGL Canvas для колец астролябии -->
    <canvas id="preloader-3d-canvas" class="absolute inset-0 w-full h-full pointer-events-none"></canvas>

    <!-- СТАТИЧНЫЙ ВИТРУВИАНСКИЙ ЧЕЛОВЕК (БЕЗ ПЕРГАМЕНТА, ПРОЗРАЧНЫЙ) -->
    <div class="absolute z-10 flex items-center justify-center pointer-events-none">
      <div class="relative w-64 h-64 sm:w-80 sm:h-80 flex items-center justify-center">
        <img src="data:image/png;base64,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" alt="Витрувианский человек" class="w-full h-full object-contain filter drop-shadow-[0_0_25px_rgba(212,175,55,0.45)] opacity-95" />
      </div>
    </div>

    <!-- Финансовая телеметрия и прогресс заставки -->
    <div class="absolute bottom-12 z-20 flex flex-col items-center text-center w-full px-6 pointer-events-none">
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

    
    // --- ПРЕЛОАДЕР: 3D THREE.JS АРМИЛЛЯРНЫЕ КОЛЬЦА + ЗУМ (5 СЕКУНД) ---
    (function initReferencePreloader() {
      const preloader = document.getElementById('alche-preloader');
      const canvas3d = document.getElementById('preloader-3d-canvas');
      const pctEl = document.getElementById('preloader-pct');
      const barEl = document.getElementById('preloader-bar');
      if (!preloader || !canvas3d) return;

      let renderer, scene, camera, ringGroup;
      let ringX, ringY, ringZ;
      let animId = null;

      try {
        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 24;

        renderer = new THREE.WebGLRenderer({ canvas: canvas3d, alpha: true, antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

        ringGroup = new THREE.Group();
        scene.add(ringGroup);

        // Цвета как на референсе: золотое, бирюзовое, бордовое/красное кольца в 3 плоскостях
        const matX = new THREE.MeshBasicMaterial({ color: 0xd4af37, wireframe: true, transparent: true, opacity: 0.85 });
        const matY = new THREE.MeshBasicMaterial({ color: 0x2a9d8f, wireframe: true, transparent: true, opacity: 0.85 });
        const matZ = new THREE.MeshBasicMaterial({ color: 0xe63946, wireframe: true, transparent: true, opacity: 0.85 });

        // БОЛЬШИЕ КОЛЬЦА В 3 ПЛОСКОСТЯХ (как на референсном GIF)
        ringX = new THREE.Mesh(new THREE.TorusGeometry(7.5, 0.08, 16, 100), matX);
        ringX.rotation.x = Math.PI / 2;
        ringGroup.add(ringX);

        ringY = new THREE.Mesh(new THREE.TorusGeometry(6.2, 0.08, 16, 100), matY);
        ringY.rotation.y = Math.PI / 2;
        ringGroup.add(ringY);

        ringZ = new THREE.Mesh(new THREE.TorusGeometry(5.0, 0.08, 16, 100), matZ);
        ringGroup.add(ringZ);

      } catch (e) {
        console.warn("WebGL preloader failed:", e);
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
        preloader.style.filter = 'blur(20px)';
        preloader.style.pointerEvents = 'none';

        setTimeout(() => {
          preloader.style.display = 'none';
          if (animId) cancelAnimationFrame(animId);
          if (renderer) renderer.dispose();
          // ГАРАНТИРОВАННЫЙ ЗАПУСК ДАШБОРДА ПОСЛЕ ЗАСТАВКИ
          try {
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
