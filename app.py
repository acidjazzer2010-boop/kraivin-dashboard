import streamlit as st
import streamlit.components.v1 as components

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

html_code = """<!DOCTYPE html>
<html lang="ru" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Архитектура Капитала // Финансовое Моделирование</title>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600;1,700&family=JetBrains+Mono:ital,wght@0,300;0,400;0,500;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">

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

    .film-grain {
      position: fixed;
      inset: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      z-index: 999;
      opacity: var(--grain-opacity);
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
    }

    #preloader-stage {
      position: fixed;
      inset: 0;
      background: #060608;
      z-index: 900;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      transition: opacity 1.1s cubic-bezier(0.19, 1, 0.22, 1), transform 1.1s cubic-bezier(0.19, 1, 0.22, 1);
    }

    #preloader-stage.fade-out {
      opacity: 0;
      transform: scale(1.035);
      pointer-events: none;
    }

    .draw-circle {
      stroke-dasharray: 1300;
      stroke-dashoffset: 1300;
      animation: drawLineAnim 2.2s cubic-bezier(0.4, 0, 0.2, 1) 0.2s forwards;
    }
    .draw-square {
      stroke-dasharray: 1400;
      stroke-dashoffset: 1400;
      animation: drawLineAnim 2.2s cubic-bezier(0.4, 0, 0.2, 1) 1.0s forwards;
    }
    .draw-axis {
      stroke-dasharray: 600;
      stroke-dashoffset: 600;
      animation: drawLineAnim 1.6s cubic-bezier(0.4, 0, 0.2, 1) 1.8s forwards;
    }
    .draw-anatomy-primary {
      stroke-dasharray: 3800;
      stroke-dashoffset: 3800;
      animation: drawLineAnim 4.2s cubic-bezier(0.25, 0.1, 0.25, 1) 2.2s forwards;
    }
    .draw-anatomy-spread {
      stroke-dasharray: 3200;
      stroke-dashoffset: 3200;
      animation: drawLineAnim 3.8s cubic-bezier(0.25, 0.1, 0.25, 1) 2.8s forwards;
    }
    .draw-anatomy-hatch {
      stroke-dasharray: 1600;
      stroke-dashoffset: 1600;
      animation: drawLineAnim 2.8s ease-out 3.6s forwards;
    }

    @keyframes drawLineAnim {
      to {
        stroke-dashoffset: 0;
      }
    }

    @keyframes quillFollowsDrawing {
      0%   { transform: translate(300px, 95px) rotate(-18deg); opacity: 0; }
      4%   { transform: translate(300px, 95px) rotate(-22deg); opacity: 1; }
      18%  { transform: translate(500px, 300px) rotate(-10deg); }
      32%  { transform: translate(100px, 300px) rotate(-35deg); }
      48%  { transform: translate(300px, 160px) rotate(-25deg); }
      60%  { transform: translate(180px, 225px) rotate(-30deg); }
      72%  { transform: translate(430px, 225px) rotate(-15deg); }
      84%  { transform: translate(250px, 420px) rotate(-20deg); }
      92%  { transform: translate(350px, 420px) rotate(-18deg); opacity: 1; }
      100% { transform: translate(300px, 300px) rotate(-15deg); opacity: 0; }
    }

    .animated-quill {
      position: absolute;
      top: 0;
      left: 0;
      pointer-events: none;
      animation: quillFollowsDrawing 6.8s cubic-bezier(0.35, 0.1, 0.25, 1) forwards;
      filter: drop-shadow(0 0 12px rgba(212, 175, 55, 0.55));
    }

    .nib-spark {
      animation: sparkFlicker 0.25s infinite alternate;
    }
    @keyframes sparkFlicker {
      0% { opacity: 0.55; transform: scale(0.8); }
      100% { opacity: 1; transform: scale(1.3); }
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

  <div class="film-grain"></div>

  <div id="preloader-stage">
    <div class="relative w-[340px] h-[340px] sm:w-[480px] sm:h-[480px] lg:w-[540px] lg:h-[540px] flex items-center justify-center">
      
      <svg id="vitruvianSvg" viewBox="0 0 600 600" class="w-full h-full text-[#d4af37] overflow-visible">
        <defs>
          <radialGradient id="goldGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#d4af37" stop-opacity="0.18"/>
            <stop offset="100%" stop-color="#d4af37" stop-opacity="0"/>
          </radialGradient>
        </defs>

        <circle cx="300" cy="300" r="235" fill="url(#goldGlow)" />

        <circle cx="300" cy="300" r="202" fill="none" stroke="#d4af37" stroke-width="1.3" class="draw-circle" />
        <circle cx="300" cy="300" r="208" fill="none" stroke="#d4af37" stroke-opacity="0.3" stroke-width="0.7" class="draw-circle" stroke-dasharray="3 3" />

        <rect x="125" y="125" width="350" height="350" fill="none" stroke="#d4af37" stroke-width="1.3" class="draw-square" />
        <rect x="120" y="120" width="360" height="360" fill="none" stroke="#d4af37" stroke-opacity="0.3" stroke-width="0.6" class="draw-square" stroke-dasharray="2 3" />

        <g stroke="#d4af37" stroke-width="0.7" stroke-dasharray="3 3" opacity="0.55" class="draw-axis">
          <line x1="300" y1="45" x2="300" y2="555" />
          <line x1="45" y1="300" x2="555" y2="300" />
          <line x1="125" y1="125" x2="475" y2="475" />
          <line x1="125" y1="475" x2="475" y2="125" />
          <line x1="125" y1="210" x2="475" y2="210" stroke-opacity="0.35" />
          <line x1="125" y1="345" x2="475" y2="345" stroke-opacity="0.35" />
          <circle cx="125" cy="225" r="2.5" fill="#d4af37" />
          <circle cx="475" cy="225" r="2.5" fill="#d4af37" />
          <circle cx="157" cy="157" r="2.5" fill="#d4af37" />
          <circle cx="443" cy="157" r="2.5" fill="#d4af37" />
          <circle cx="185" cy="450" r="2.5" fill="#d4af37" />
          <circle cx="415" cy="450" r="2.5" fill="#d4af37" />
        </g>

        <!-- АНАТОМИЧЕСКИЙ РЕЛЬЕФНЫЙ СИЛУЭТ ЧЕЛОВЕКА (КОНТУРЫ ДА ВИНЧИ) -->
        <!-- 1. Основная анатомическая фигура: Голова, рельефный торс, горизонтальные руки и сомкнутые ноги -->
        <g fill="none" stroke="#d4af37" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" class="draw-anatomy-primary">
          <!-- Голова и черты лица с волосами -->
          <path d="M293 162 C291 150 309 150 307 162 C312 165 310 178 307 184 C304 188 301 190 300 190 C299 190 296 188 293 184 C290 178 288 165 293 162 Z" />
          <path d="M288 160 C294 153 306 153 312 160 C315 168 312 176 312 176 M288 160 C285 168 288 176 288 176" stroke-width="0.8" />
          <path d="M296 170 Q300 172 304 170 M298 175 Q300 177 302 175 M297 181 Q300 183 303 181" stroke-width="0.7" />
          
          <!-- Шея и ключицы -->
          <path d="M294 188 C294 195 289 198 284 202 M306 188 C306 195 311 198 316 202" />
          <path d="M284 202 C292 205 300 205 300 206 C300 205 308 205 316 202" stroke-width="0.9" />

          <!-- Мускулатура груди и пресс -->
          <path d="M284 204 C278 214 278 226 287 232 C295 233 300 231 300 231 C300 231 305 233 313 232 C322 226 322 214 316 204" />
          <line x1="300" y1="206" x2="300" y2="288" stroke-width="0.8" />
          <path d="M290 242 C296 244 300 244 300 244 C300 244 304 244 310 242" stroke-width="0.8" />
          <path d="M291 256 C296 258 300 258 300 258 C300 258 304 258 309 256" stroke-width="0.8" />
          <circle cx="300" cy="272" r="1.8" fill="#d4af37" />

          <!-- Контур торса и таза -->
          <path d="M283 204 C276 220 280 240 283 258 C285 268 287 278 285 288 C287 296 295 302 300 302 C305 302 313 296 315 288 C313 278 315 268 317 258 C320 240 324 220 317 204" />

          <!-- Левая горизонтальная рука: плечо, бицепс, предплечье, пальцы -->
          <path d="M283 204 C268 205 248 207 230 209 C212 211 192 212 174 213 C155 214 138 216 126 217 C122 217 122 223 125 224 C132 226 148 224 165 222 C184 221 204 220 226 219 C248 218 268 217 282 220" />
          <path d="M125 217 C120 216 116 218 116 221 C116 224 121 225 125 225" stroke-width="0.8" />

          <!-- Правая горизонтальная рука -->
          <path d="M317 204 C332 205 352 207 370 209 C388 211 408 212 426 213 C445 214 462 216 474 217 C478 217 478 223 475 224 C468 226 452 224 435 222 C416 221 396 220 374 219 C352 218 332 217 318 220" />
          <path d="M475 217 C480 216 484 218 484 221 C484 224 479 225 475 225" stroke-width="0.8" />

          <!-- Левая прямая нога: бедро, колено, икра, ступня к основанию квадрата -->
          <path d="M287 296 C283 318 283 346 284 374 C284 382 282 390 284 398 C287 420 285 450 285 474 C280 475 272 475 272 473 C275 471 282 467 283 458 C286 440 287 416 288 396 C290 380 292 360 293 340 C295 322 296 306 298 300" />

          <!-- Правая прямая нога -->
          <path d="M313 296 C317 318 317 346 316 374 C316 382 318 390 316 398 C313 420 315 450 315 474 C320 475 328 475 328 473 C325 471 318 467 317 458 C314 440 313 416 312 396 C310 380 308 360 307 340 C305 322 304 306 302 300" />
        </g>

        <!-- 2. Вторая стойка в круге: Поднятые руки к ободу круга и расставленные ноги -->
        <g fill="none" stroke="#d4af37" stroke-width="1.05" stroke-linecap="round" stroke-linejoin="round" class="draw-anatomy-spread">
          <!-- Левая поднятая рука (к верхнему сектору круга) -->
          <path d="M282 206 C262 192 238 180 214 168 C192 158 174 148 155 138 C151 136 148 141 151 144 C167 156 186 170 208 182 C230 194 254 204 278 216" stroke-dasharray="8 2" />
          <path d="M152 137 C147 134 144 137 146 141 C149 144 153 144 156 142" stroke-width="0.8" />

          <!-- Правая поднятая рука (к верхнему сектору круга) -->
          <path d="M318 206 C338 192 362 180 386 168 C408 158 426 148 445 138 C449 136 452 141 449 144 C433 156 414 170 392 182 C370 194 346 204 322 216" stroke-dasharray="8 2" />
          <path d="M448 137 C453 134 456 137 454 141 C451 144 447 144 444 142" stroke-width="0.8" />

          <!-- Левая расставленная нога к нижнему сектору круга -->
          <path d="M285 298 C270 326 248 358 226 390 C206 420 188 448 176 462 C172 466 176 468 181 465 C196 452 216 426 238 396 C260 364 282 330 294 304" stroke-dasharray="9 2" />

          <!-- Правая расставленная нога к нижнему сектору круга -->
          <path d="M315 298 C330 326 352 358 374 390 C394 420 412 448 424 462 C428 466 424 468 419 465 C404 452 384 426 362 396 C340 364 318 330 306 304" stroke-dasharray="9 2" />
        </g>

        <!-- 3. Аутентичная манускриптная штриховка мышц и анатомических теней -->
        <g fill="none" stroke="#d4af37" stroke-opacity="0.38" stroke-width="0.65" class="draw-anatomy-hatch">
          <line x1="285" y1="212" x2="295" y2="210" />
          <line x1="285" y1="217" x2="295" y2="215" />
          <line x1="305" y1="210" x2="315" y2="212" />
          <line x1="305" y1="215" x2="315" y2="217" />
          <line x1="286" y1="234" x2="294" y2="231" />
          <line x1="287" y1="247" x2="295" y2="244" />
          <line x1="306" y1="231" x2="314" y2="234" />
          <line x1="305" y1="244" x2="313" y2="247" />
          <line x1="145" y1="130" x2="220" y2="130" />
          <line x1="145" y1="136" x2="200" y2="136" />
          <line x1="380" y1="130" x2="455" y2="130" />
          <line x1="400" y1="136" x2="455" y2="136" />
          <line x1="145" y1="466" x2="225" y2="466" />
          <line x1="375" y1="466" x2="455" y2="466" />
        </g>

        <text x="300" y="525" text-anchor="middle" fill="#d4af37" font-family="'Cormorant Garamond', serif" font-style="italic" font-size="12" letter-spacing="3" opacity="0.85">
          HOMO VITRUVIANUS
        </text>
      </svg>

      <div id="quillPen" class="animated-quill">
        <svg width="42" height="42" viewBox="0 0 64 64" fill="none">
          <circle cx="4" cy="4" r="3.5" fill="#ffffff" class="nib-spark" />
          <circle cx="4" cy="4" r="6.5" fill="#d4af37" opacity="0.4" class="nib-spark" />
          
          <path d="M4 4 L14 10 L18 8 L8 2 Z" fill="#ffffff" />
          <path d="M8 2 L18 8 L42 22 C52 28 58 40 60 52 C50 48 40 40 32 30 L14 10 Z" fill="url(#quillGrad)" stroke="#d4af37" stroke-width="0.8" />
          <path d="M14 10 L44 32" stroke="#4a3b10" stroke-width="0.7" />
          
          <defs>
            <linearGradient id="quillGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#fff4cc" />
              <stop offset="30%" stop-color="#d4af37" />
              <stop offset="100%" stop-color="#5a4510" />
            </linearGradient>
          </defs>
        </svg>
      </div>

    </div>

    <div class="mt-4 flex flex-col items-center gap-2 font-mono">
      <div class="flex items-center gap-3 text-[#d4af37] text-[11px] tracking-[0.25em] uppercase">
        <span class="pulse-dot"></span>
        <span id="loaderStatusText">Инициализация...</span>
        <span id="loaderPercent" class="font-bold">0%</span>
      </div>

      <div class="w-64 sm:w-80 h-[2px] bg-white/10 relative overflow-hidden mt-1">
        <div id="loaderProgressBar" class="absolute top-0 bottom-0 left-0 bg-[#d4af37] w-0 transition-all duration-100 ease-out"></div>
      </div>

      <button type="button" onclick="dismissPreloader()" class="mt-4 text-[9px] uppercase tracking-[0.2em] text-[#d4af37]/60 hover:text-[#d4af37] transition font-mono border border-transparent hover:border-[#d4af37]/30 px-3 py-1">
        [Пропустить Intro]
      </button>
    </div>
  </div>

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

  <div id="mainDashboardApp" class="relative z-10 min-h-screen flex flex-col border-t border-l opacity-0 transition-opacity duration-1000" style="border-color: var(--border-line);">

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

    <div class="flex-1 grid grid-cols-1 lg:grid-cols-12">

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

    let preloaderDismissed = false;
    function dismissPreloader() {
      if (preloaderDismissed) return;
      preloaderDismissed = true;
      const stage = document.getElementById('preloader-stage');
      const app = document.getElementById('mainDashboardApp');

      if (stage) stage.classList.add('fade-out');
      if (app) {
        app.classList.remove('opacity-0');
        app.classList.add('opacity-100');
      }

      setTimeout(() => {
        if (stage) stage.style.display = 'none';
      }, 1100);
    }

    const PRELOADER_TOTAL_TIME = 7000;
    const preloaderStartTime = performance.now();

    const statusSteps = [
      { t: 0.1, msg: "Калибровка циркуля и осей..." },
      { t: 0.25, msg: "Построение геометрии..." },
      { t: 0.45, msg: "Синтез фигуры Витрувия..." },
      { t: 0.70, msg: "Инициализация регистров..." },
      { t: 0.90, msg: "Финализация модели капитала..." }
    ];

    function updatePreloaderProgress(now) {
      if (preloaderDismissed) return;
      const elapsed = now - preloaderStartTime;
      const progress = Math.min(elapsed / PRELOADER_TOTAL_TIME, 1);
      
      const pBar = document.getElementById('loaderProgressBar');
      const pPct = document.getElementById('loaderPercent');
      const pTxt = document.getElementById('loaderStatusText');

      if (pBar) pBar.style.width = `${(progress * 100).toFixed(1)}%`;
      if (pPct) pPct.textContent = `${Math.floor(progress * 100)}%`;

      for (let s of statusSteps) {
        if (progress >= s.t) {
          if (pTxt && pTxt.textContent !== s.msg) pTxt.textContent = s.msg;
        }
      }

      if (progress < 1) {
        requestAnimationFrame(updatePreloaderProgress);
      } else {
        dismissPreloader();
      }
    }
    requestAnimationFrame(updatePreloaderProgress);

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

    function exportDataToCsv() {
      playClickSound(1600, 0.05);
      if (!latestCalculatedData) return;
      const { xLabels, monthlyInvestments, interestPayments, debtRepayments, debtBalance, cashBalance } = latestCalculatedData;
      
      let csvContent = "data:text/csv;charset=utf-8,\uFEFF";
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

    setInterval(() => {
      const now = new Date();
      document.getElementById('telemetryClock').textContent = `[${now.toTimeString().split(' ')[0]}]`;
    }, 1000);

    function resetDefaults() {
      playClickSound(600, 0.05);
      document.getElementById('financialInputsForm').reset();
      runCalculation();
    }

    window.onload = () => {
      runCalculation();
    };
  </script>
</body>
</html>"""

components.html(html_code, height=1350, scrolling=True)
