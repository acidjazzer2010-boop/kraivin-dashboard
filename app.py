import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Архитектура Капитала // Финансовое Моделирование",
    page_icon="📊",
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

    /* Фоновый шум кинопленки */
    .film-grain {
      position: fixed;
      inset: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      z-index: 40;
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

    /* АСТРОЛЯБИЯ ДА ВИНЧИ: НЕЗАВИСИМОЕ ВРАЩЕНИЕ КОЛЕЦ */
    @keyframes spinClockwise {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    @keyframes spinCounterClockwise {
      0% { transform: rotate(360deg); }
      100% { transform: rotate(0deg); }
    }
    @keyframes laserVerticalScan {
      0% { top: -6%; opacity: 0; }
      15% { opacity: 0.9; }
      85% { opacity: 0.9; }
      100% { top: 104%; opacity: 0; }
    }

    .astrolabe-orbit-outer {
      animation: spinClockwise 20s linear infinite;
      transform-origin: 250px 250px;
      will-change: transform;
    }
    .astrolabe-orbit-middle {
      animation: spinCounterClockwise 28s linear infinite;
      transform-origin: 250px 250px;
      will-change: transform;
    }
    .astrolabe-orbit-inner {
      animation: spinClockwise 42s linear infinite;
      transform-origin: 250px 250px;
      will-change: transform;
    }
    .laser-scanner-line {
      animation: laserVerticalScan 3s ease-in-out infinite;
      will-change: top, opacity;
    }

    .specular-emboss {
      filter: url(#specular-glass-filter);
      transition: filter 0.2s ease, transform 0.3s ease;
    }
    .specular-emboss:hover {
      transform: scale(1.08) rotate(4deg);
    }

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

  <!-- ЭКРАН ЗАГРУЗКИ: ВИТРУВИАНСКИЙ ЧЕРТЕЖ ДА ВИНЧИ И НЕЗАВИСИМО ВРАЩАЮЩИЕСЯ КОЛЬЦА АСТРОЛЯБИИ (3 СЕКУНДЫ) -->
  <div id="alche-preloader" class="fixed inset-0 z-50 flex flex-col items-center justify-center bg-[#070709] select-none" style="transition: opacity 0.9s cubic-bezier(0.19, 1, 0.22, 1), filter 0.9s cubic-bezier(0.19, 1, 0.22, 1), transform 0.9s cubic-bezier(0.19, 1, 0.22, 1);">
    
    <div class="relative flex flex-col items-center max-w-xl mx-auto px-6 text-center">
      
      <!-- Контейнер гравюры с независимо вращающимися кольцами астролябии -->
      <div class="relative w-72 h-72 sm:w-80 sm:h-80 mb-6 flex items-center justify-center">
        
        <!-- АСТРОЛЯБИЯ ДА ВИНЧИ: 3 НЕЗАВИСИМО ВРАЩАЮЩИХСЯ КОЛЬЦА -->
        <div class="absolute -inset-10 sm:-inset-14 pointer-events-none flex items-center justify-center">
          
          <!-- КОЛЬЦО 1: Внешний лимб со шкалой румбов (по часовой стрелке, 20с) -->
          <svg class="absolute inset-0 w-full h-full text-[#d4af37] astrolabe-orbit-outer" viewBox="0 0 500 500" fill="none">
            <circle cx="250" cy="250" r="236" stroke="currentColor" stroke-width="1.2" class="opacity-60" />
            <circle cx="250" cy="250" r="226" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3 6" class="opacity-40" />
            <circle cx="250" cy="250" r="216" stroke="currentColor" stroke-width="0.6" class="opacity-30" />
            <g class="opacity-75" stroke="currentColor" stroke-width="1.5">
              <line x1="250" y1="14" x2="250" y2="34" />
              <line x1="250" y1="466" x2="250" y2="486" />
              <line x1="14" y1="250" x2="34" y2="250" />
              <line x1="466" y1="250" x2="486" y2="250" />
              <line x1="83" y1="83" x2="97" y2="97" />
              <line x1="403" y1="403" x2="417" y2="417" />
              <line x1="403" y1="97" x2="417" y2="83" />
              <line x1="83" y1="417" x2="97" y2="403" />
            </g>
            <circle cx="250" cy="14" r="5" fill="currentColor" class="filter drop-shadow-[0_0_10px_#d4af37]" />
            <circle cx="486" cy="250" r="4" fill="currentColor" class="opacity-80 filter drop-shadow-[0_0_6px_#d4af37]" />
            <circle cx="14" cy="250" r="4" fill="currentColor" class="opacity-80" />
            <circle cx="250" cy="486" r="4" fill="currentColor" class="opacity-80" />
            <circle cx="83" cy="83" r="3" fill="currentColor" class="opacity-90" />
            <circle cx="417" cy="417" r="3" fill="currentColor" class="opacity-90" />
          </svg>

          <!-- КОЛЬЦО 2: Эксцентрический зодиакальный круг (против часовой стрелки, 28с) -->
          <svg class="absolute inset-2 w-[calc(100%-16px)] h-[calc(100%-16px)] text-[#d4af37] astrolabe-orbit-middle" viewBox="0 0 500 500" fill="none">
            <ellipse cx="250" cy="235" rx="195" ry="175" stroke="currentColor" stroke-width="1.4" stroke-dasharray="16 8" class="opacity-70" />
            <circle cx="250" cy="250" r="185" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 8" class="opacity-50" />
            <polygon points="250,50 256,66 250,62 244,66" fill="currentColor" class="opacity-90 filter drop-shadow-[0_0_8px_#d4af37]" />
            <polygon points="435,235 419,241 423,235 419,229" fill="currentColor" class="opacity-90 filter drop-shadow-[0_0_8px_#d4af37]" />
            <polygon points="65,235 81,241 77,235 81,229" fill="currentColor" class="opacity-90 filter drop-shadow-[0_0_8px_#d4af37]" />
            <polygon points="250,410 256,394 250,398 244,394" fill="currentColor" class="opacity-90 filter drop-shadow-[0_0_8px_#d4af37]" />
            <circle cx="112" cy="112" r="4" fill="currentColor" class="opacity-80" />
            <circle cx="388" cy="358" r="4" fill="currentColor" class="opacity-80" />
          </svg>

          <!-- КОЛЬЦО 3: Внутреннее высотное кольцо альмукантаратов (по часовой стрелке, 42с) -->
          <svg class="absolute inset-6 w-[calc(100%-48px)] h-[calc(100%-48px)] text-[#d4af37] astrolabe-orbit-inner" viewBox="0 0 500 500" fill="none">
            <circle cx="250" cy="250" r="162" stroke="currentColor" stroke-width="1" class="opacity-50" />
            <circle cx="250" cy="250" r="152" stroke="currentColor" stroke-width="0.75" stroke-dasharray="4 6" class="opacity-60" />
            <path d="M250 88 A162 162 0 0 1 412 250" stroke="currentColor" stroke-width="1.2" stroke-dasharray="8 6" class="opacity-75" />
            <path d="M88 250 A162 162 0 0 1 250 412" stroke="currentColor" stroke-width="1.2" stroke-dasharray="8 6" class="opacity-75" />
            <circle cx="250" cy="88" r="4.5" fill="currentColor" class="filter drop-shadow-[0_0_10px_#d4af37]" />
            <circle cx="412" cy="250" r="4.5" fill="currentColor" class="filter drop-shadow-[0_0_10px_#d4af37]" />
            <circle cx="88" cy="250" r="3.5" fill="currentColor" class="opacity-80" />
            <circle cx="250" cy="412" r="3.5" fill="currentColor" class="opacity-80" />
          </svg>

        </div>

        <!-- Осевые координатные линии -->
        <div class="absolute inset-x-0 top-1/2 h-[1px] bg-gradient-to-r from-transparent via-[#d4af37]/40 to-transparent pointer-events-none"></div>
        <div class="absolute inset-y-0 left-1/2 w-[1px] bg-gradient-to-b from-transparent via-[#d4af37]/40 to-transparent pointer-events-none"></div>

        <!-- Центральный чертеж Витрувианского человека да Винчи -->
        <div class="relative w-64 h-64 sm:w-72 sm:h-72 border border-[#d4af37]/60 rounded-sm overflow-hidden bg-[#0d0d12] shadow-[0_0_50px_rgba(212,175,55,0.3)] flex items-center justify-center p-3">
          <svg class="w-full h-full text-[#d4af37] filter drop-shadow-[0_0_20px_rgba(212,175,55,0.45)]" viewBox="0 0 200 200" fill="none" stroke="currentColor">
            <circle cx="100" cy="100" r="92" stroke-width="1.2" stroke-dasharray="2 3" class="opacity-80" />
            <rect x="22" y="22" width="156" height="156" stroke-width="1" class="opacity-70" />
            <line x1="22" y1="22" x2="178" y2="178" stroke-width="0.5" stroke-dasharray="2 4" class="opacity-40" />
            <line x1="178" y1="22" x2="22" y2="178" stroke-width="0.5" stroke-dasharray="2 4" class="opacity-40" />
            <line x1="100" y1="8" x2="100" y2="192" stroke-width="0.8" stroke-dasharray="2 2" class="opacity-60" />
            <line x1="8" y1="100" x2="192" y2="100" stroke-width="0.8" stroke-dasharray="2 2" class="opacity-60" />

            <!-- Пропорции человека по чертежам Леонардо -->
            <circle cx="100" cy="45" r="11" stroke-width="1.5" />
            <path d="M100 56 L100 116" stroke-width="1.8" />
            <path d="M88 68 L112 68 L106 116 L94 116 Z" stroke-width="1.2" stroke-dasharray="3 2" class="opacity-75" />
            <path d="M24 70 L100 70 L176 70" stroke-width="1.6" />
            <path d="M38 36 L100 66 L162 36" stroke-width="1.5" />
            <path d="M94 116 L88 182 M106 116 L112 182" stroke-width="1.6" />
            <path d="M94 116 L48 170 M106 116 L152 170" stroke-width="1.5" />
          </svg>
          
          <!-- Сканирующий луч телеметрии -->
          <div class="absolute inset-x-0 h-1 bg-gradient-to-r from-transparent via-[#d4af37] to-transparent opacity-85 shadow-[0_0_15px_#d4af37] laser-scanner-line pointer-events-none"></div>
        </div>
      </div>

      <!-- Деловой финансовый статус -->
      <div class="space-y-2 z-10">
        <div class="font-mono text-[9px] uppercase tracking-[0.3em] text-[#d4af37] opacity-90">
          [ФИНАНСОВОЕ МОДЕЛИРОВАНИЕ // СИСТЕМА 2026]
        </div>
        <h2 class="font-serif italic text-2xl sm:text-3xl font-bold tracking-wider text-[#f4f1ea]">
          Архитектура Капитала
        </h2>
        <p class="font-mono text-[10px] text-[#8e8a80] max-w-sm mx-auto tracking-wide">
          Моделирование денежных потоков, партионных закупок и кредитной нагрузки
        </p>

        <!-- Прогресс-бар ровно на 3 секунды -->
        <div class="pt-3 w-64 mx-auto space-y-1.5">
          <div class="flex justify-between items-center font-mono text-[9px]">
            <span class="text-[#8e8a80] uppercase tracking-wider flex items-center gap-1.5">
              <span class="pulse-dot"></span> КАЛИБРОВКА
            </span>
            <span id="preloader-pct" class="text-[#d4af37] font-bold">0%</span>
          </div>
          <div class="w-full h-[2px] bg-[#d4af37]/20 rounded-full overflow-hidden">
            <div id="preloader-bar" class="h-full bg-gradient-to-r from-[#d4af37] via-[#f4f1ea] to-[#d4af37] w-0 transition-all duration-[50ms] ease-linear"></div>
          </div>
        </div>

      </div>

    </div>
  </div>

  <div class="film-grain"></div>

  <!-- Оптический фильтр SVG feSpecularLighting -->
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

    <!-- ВЕРХНЯЯ ПАНЕЛЬ ТЕЛЕМЕТРИИ -->
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
            <div class="font-mono text-[9px] uppercase tracking-[0.25em] text-[#d4af37] opacity-80">АНАЛИТИКА И УПРАВЛЕНИЕ ЛИКВИДНОСТЬЮ</div>
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

    <!-- Основная рабочая сетка -->
    <div class="flex-1 grid grid-cols-1 lg:grid-cols-12">

      <!-- ЛЕВАЯ ПАНЕЛЬ ПАРАМЕТРОВ -->
      <aside class="lg:col-span-3 flex flex-col">
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
                <select id="paramStartMonth" class="mono-input" onchange="runCalculation();">
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
                <select id="paramStartYear" class="mono-input" onchange="runCalculation();">
                  <option value="2026" selected>2026</option>
                  <option value="2027">2027</option>
                </select>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-2.5">
              <div>
                <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Горизонт</label>
                <select id="paramPeriod" class="mono-input" onchange="runCalculation();">
                  <option value="6">6 месяцев</option>
                  <option value="12" selected>12 месяцев</option>
                  <option value="18">18 месяцев</option>
                  <option value="24">24 месяца</option>
                </select>
              </div>
              <div>
                <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Ставка НДС</label>
                <select id="paramVatRate" class="mono-input" onchange="runCalculation();">
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

      <!-- ПРАВАЯ ЧАСТЬ: ДАШБОРД -->
      <section class="lg:col-span-9 flex flex-col">
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

        <!-- Вкладки -->
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
    // Безопасный аудио-синтезатор (не блокирует поток, если отключен звук)
    function playClickSound(freq = 1200, duration = 0.02) {
      try {
        const AudioCtor = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtor) return;
        const ctx = new AudioCtor();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, ctx.currentTime);
        gain.gain.setValueAtTime(0.03, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + duration);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + duration);
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

      if (lightDiff && lightSpec) {
        const lx = e.clientX % 320;
        const ly = e.clientY % 220;
        lightDiff.setAttribute('x', lx);
        lightDiff.setAttribute('y', ly);
        lightSpec.setAttribute('x', lx);
        lightSpec.setAttribute('y', ly);
      }
    });

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

    // --- 3. MATRIX CIPHER ---
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

    // --- 4. TAB CONTROLLER ---
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
          void view.offsetWidth;
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

    // --- 5. ФИНАНСОВЫЙ ДВИЖОК МОДЕЛИ ---
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
      return parseFloat(String(val).replace(/[^\\d.-]/g, '')) || 0;
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
      try {
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
              y: { grid: { color: chartGrid }, ticks: { color: chartText, font: { family: 'JetBrains Mono', size: 10 } } },
              y1: { position: 'right', grid: { display: false }, ticks: { color: '#e63946', font: { family: 'JetBrains Mono', size: 10 } } }
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
      } catch (err) {
        console.error("Calculation error:", err);
      }
    }

    // Мгновенный экспорт в CSV
    function exportDataToCsv() {
      playClickSound(1600, 0.05);
      if (!latestCalculatedData) return;
      const { xLabels, monthlyInvestments, interestPayments, debtRepayments, debtBalance, cashBalance } = latestCalculatedData;
      
      let csvContent = "data:text/csv;charset=utf-8,﻿";
      csvContent += "Период;Дотация (дефицит);Проценты по долгу;Погашение долга;Остаток тела долга;Свободный остаток счета\\n";

      for (let i = 0; i < xLabels.length; i++) {
        csvContent += `${xLabels[i]};${Math.round(monthlyInvestments[i])};${Math.round(interestPayments[i])};${Math.round(debtRepayments[i])};${Math.round(debtBalance[i])};${Math.round(cashBalance[i])}\\n`;
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

    // --- ПРЕЛОАДЕР: РОВНО 3.0 СЕКУНДЫ + ГАРАНТИРОВАННОЕ РАСТВОРЕНИЕ ---
    (function runPreloaderEngine() {
      const preloader = document.getElementById('alche-preloader');
      const pctEl = document.getElementById('preloader-pct');
      const barEl = document.getElementById('preloader-bar');
      if (!preloader) return;

      const DURATION = 3000;
      const start = performance.now();
      let dismissed = false;

      function dismiss() {
        if (dismissed) return;
        dismissed = true;
        if (pctEl) pctEl.textContent = '100%';
        if (barEl) barEl.style.width = '100%';
        
        preloader.style.opacity = '0';
        preloader.style.filter = 'blur(20px)';
        preloader.style.transform = 'scale(1.05)';
        preloader.style.pointerEvents = 'none';

        setTimeout(() => {
          preloader.style.display = 'none';
        }, 900);
      }

      function tick(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / DURATION, 1.0);
        const p = Math.floor(progress * 100);

        if (pctEl) pctEl.textContent = `${p}%`;
        if (barEl) barEl.style.width = `${p}%`;

        if (progress < 1.0) {
          requestAnimationFrame(tick);
        } else {
          dismiss();
        }
      }

      requestAnimationFrame(tick);

      // Аварийный сброс заставки через 3.2 сек на случай любых системных задержек
      setTimeout(dismiss, 3200);
    })();

    // Запуск модели сразу при инициализации
    runCalculation();
  </script>
</body>
</html>"""

components.html(html_code, height=1350, scrolling=True)
