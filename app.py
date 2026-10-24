import streamlit as st
import streamlit.components.v1 as components
import base64
import os

st.set_page_config(
    page_title="Архитектура Капитала // Финансовое Моделирование",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Скрываем элементы Streamlit
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

# Инъекция локального изображения напрямую в HTML для обхода CORS-ограничений браузера
def get_local_image_b64(filename):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/jpeg;base64,{b64}"
    # Фолбэк, если файл не найден в директории запуска
    return "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Da_Vinci_Vitruve_Luc_Viatour.jpg/800px-Da_Vinci_Vitruve_Luc_Viatour.jpg"

vitruvian_src = get_local_image_b64("1000400438_2.jpg")

html_code = """<!DOCTYPE html>
<html lang="ru" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Архитектура Капитала // Финансовое Моделирование</title>

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
          }
        }
      }
    }
  </script>

  <!-- Three.js и контроллер свободной камеры -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <style>
    :root {
      --bg-space: #070709;
      --bg-panel: rgba(13, 13, 18, 0.85);
      --bg-cell-hover: rgba(24, 24, 34, 0.95);
      --text-main: #f4f1ea;
      --border-line: rgba(212, 175, 55, 0.16);
      --accent-gold: #d4af37;
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
      --border-line: rgba(184, 134, 11, 0.22);
      --accent-gold: #b8860b;
      --input-bg: rgba(0, 0, 0, 0.03);
      --cursor-glow: rgba(184, 134, 11, 0.15);
      --table-header-bg: rgba(244, 241, 234, 0.98);
      --grain-opacity: 0.02;
    }

    * { box-sizing: border-box; border-color: var(--border-line); }

    body {
      background-color: var(--bg-space);
      color: var(--text-main);
      font-family: 'JetBrains Mono', monospace;
      overflow-x: hidden;
      margin: 0; padding: 0;
      transition: background-color 0.5s ease, color 0.5s ease;
    }

    .film-grain {
      position: fixed; inset: 0;
      pointer-events: none; z-index: 999;
      opacity: var(--grain-opacity);
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
    }

    #preloader-stage {
      position: fixed; inset: 0;
      background: #060608; z-index: 900;
      display: flex; flex-direction: column;
      align-items: center; justify-content: center;
      transition: opacity 1.1s cubic-bezier(0.19, 1, 0.22, 1), transform 1.1s cubic-bezier(0.19, 1, 0.22, 1);
    }
    #preloader-stage.fade-out { opacity: 0; transform: scale(1.05); pointer-events: none; }

    #preloader-canvas-container {
      position: absolute; inset: 0;
      width: 100vw; height: 100vh;
      display: flex; align-items: center; justify-content: center;
      cursor: grab; z-index: 10;
    }
    #preloader-canvas-container:active { cursor: grabbing; }

    #preloader-webgl { width: 100% !important; height: 100% !important; outline: none; }

    .quill-overlay-nib {
      position: absolute; top: 0; left: 0;
      pointer-events: none; z-index: 25;
      animation: penOrbit 7s cubic-bezier(0.35, 0.1, 0.25, 1) forwards;
      filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.5));
    }

    @keyframes penOrbit {
      0%   { transform: translate(30vw, 15vh) rotate(-18deg); opacity: 0; }
      5%   { transform: translate(35vw, 18vh) rotate(-24deg); opacity: 1; }
      22%  { transform: translate(65vw, 40vh) rotate(-10deg); }
      38%  { transform: translate(25vw, 60vh) rotate(-35deg); }
      54%  { transform: translate(60vw, 75vh) rotate(-18deg); }
      70%  { transform: translate(45vw, 25vh) rotate(-28deg); }
      85%  { transform: translate(55vw, 35vh) rotate(-15deg); }
      93%  { transform: translate(50vw, 50vh) rotate(-22deg); opacity: 1; }
      100% { transform: translate(51vw, 51vh) rotate(-20deg); opacity: 0; }
    }

    .pulse-dot {
      display: inline-block; width: 6px; height: 6px;
      border-radius: 50%; background-color: var(--accent-gold);
      animation: pulseAnim 2s infinite ease-in-out;
    }
    @keyframes pulseAnim { 0%, 100% { opacity: 0.4; transform: scale(0.9); } 50% { opacity: 1; transform: scale(1.2); } }

    #webgl-bg-canvas {
      position: fixed; inset: 0; z-index: 0; pointer-events: none; opacity: 0.45;
    }
    html:not(.dark) #webgl-bg-canvas { opacity: 0.18; }

    .alche-block {
      position: relative; background: var(--bg-panel);
      backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
      border-right: 1px solid var(--border-line); border-bottom: 1px solid var(--border-line);
    }
    
    .tilt-card {
      position: relative; overflow: hidden; transform-style: preserve-3d; perspective: 900px;
      transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .tilt-card::before {
      content: ''; position: absolute; inset: 0; border: 1px solid transparent;
      background: radial-gradient(350px circle at var(--mouse-x, 0px) var(--mouse-y, 0px), var(--cursor-glow), transparent 70%);
      opacity: 0; transition: opacity 0.35s ease; pointer-events: none; z-index: 2;
    }
    .tilt-card:hover::before { opacity: 1; }

    .tab-view-enter { animation: tabEntrance 0.6s cubic-bezier(0.19, 1, 0.22, 1) forwards; }
    @keyframes tabEntrance { 0% { opacity: 0; transform: translateY(10px); } 100% { opacity: 1; transform: translateY(0); } }

    .mono-input {
      background: var(--input-bg); border: 1px solid var(--border-line); color: var(--text-main);
      font-family: 'JetBrains Mono', monospace; font-size: 12px; padding: 7px 10px; width: 100%;
    }
    .mono-input:focus { outline: none; border-color: var(--accent-gold); background: rgba(212, 175, 55, 0.06); }
    select.mono-input option { background-color: #0d0d12; color: #f4f1ea; }
    html:not(.dark) select.mono-input option { background-color: #f4f1ea; color: #141416; }

    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-thumb { background: var(--border-line); }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent-gold); }
  </style>
</head>
<body class="selection:bg-[#d4af37] selection:text-black">

  <div class="film-grain"></div>

  <!-- ЗАСТАВКА (PRELOADER) С ВИТРУВИАНСКИМ ЧЕЛОВЕКОМ В 3D И СВОБОДНОЙ КАМЕРОЙ -->
  <div id="preloader-stage">
    <div id="preloader-canvas-container">
      <canvas id="preloader-webgl"></canvas>

      <!-- Анимированная перьевая ручка -->
      <div id="quillPen" class="quill-overlay-nib">
        <svg width="48" height="48" viewBox="0 0 64 64" fill="none">
          <circle cx="4" cy="4" r="3.5" fill="#ffffff" class="nib-spark" />
          <circle cx="4" cy="4" r="8" fill="#d4af37" opacity="0.4" class="nib-spark" />
          
          <!-- Металлическое перо -->
          <path d="M4 4 L14 12 L10 16 Z" fill="#d4af37" />
          <path d="M4 4 L12 14 L16 10 Z" fill="#b8860b" />
          <line x1="4" y1="4" x2="12" y2="12" stroke="#111" stroke-width="0.8"/>
          <circle cx="12" cy="12" r="1.5" fill="#111"/>
          
          <!-- Корпус ручки -->
          <path d="M12 14 L14 12 L50 48 L48 50 Z" fill="url(#penGrad)" stroke="#4a3b10" stroke-width="1"/>
          <path d="M50 48 L14 12" stroke="#ffffff" stroke-width="1.5" opacity="0.3"/>
          <path d="M18 22 L22 18" stroke="#d4af37" stroke-width="2"/>
          <path d="M42 46 L46 42" stroke="#d4af37" stroke-width="2"/>
          
          <defs>
            <linearGradient id="penGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#2a2a2a" />
              <stop offset="50%" stop-color="#0a0a0a" />
              <stop offset="100%" stop-color="#000000" />
            </linearGradient>
          </defs>
        </svg>
      </div>
    </div>

    <!-- Индикатор загрузки -->
    <div class="absolute bottom-10 flex flex-col items-center gap-2 font-mono z-20 pointer-events-auto">
      <div class="flex items-center gap-3 text-[#d4af37] text-[11px] tracking-[0.25em] uppercase">
        <span class="pulse-dot"></span>
        <span id="loaderStatusText">Инициализация 3D среды...</span>
        <span id="loaderPercent" class="font-bold">0%</span>
      </div>
      <div class="w-64 sm:w-80 h-[2px] bg-white/10 relative overflow-hidden mt-1">
        <div id="loaderProgressBar" class="absolute top-0 bottom-0 left-0 bg-[#d4af37] w-0 transition-all duration-100 ease-out"></div>
      </div>
      <button type="button" onclick="dismissPreloader()" class="mt-4 text-[9px] uppercase tracking-[0.2em] text-[#d4af37]/60 hover:text-[#d4af37] transition font-mono px-3 py-1">
        [Пропустить Intro]
      </button>
    </div>
  </div>

  <canvas id="webgl-bg-canvas"></canvas>

  <!-- ОСНОВНОЙ ДАШБОРД -->
  <div id="mainDashboardApp" class="relative z-10 min-h-screen flex flex-col border-t border-l opacity-0 transition-opacity duration-1000" style="border-color: var(--border-line);">
    <header class="alche-block px-5 lg:px-8 py-3 flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center gap-6">
        <div class="flex items-center gap-3">
          <svg class="w-7 h-7 text-[#d4af37] cursor-pointer" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.2">
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
          <span id="telemetryRate">[КАПИТАЛ: 19.0% ГОДОВЫХ]</span>
        </div>
      </div>
      <div class="flex items-center gap-4">
        <button id="downloadReportBtn" onclick="exportDataToCsv()" type="button" class="px-3.5 py-1.5 border font-mono text-[10px] uppercase tracking-widest hover:border-[#d4af37] hover:bg-[#d4af37]/10 transition flex items-center gap-2">
          <span>↓ Скачать отчет</span>
        </button>
      </div>
    </header>

    <div class="flex-1 grid grid-cols-1 lg:grid-cols-12">
      <!-- ПАНЕЛЬ ПАРАМЕТРОВ -->
      <aside class="lg:col-span-3 flex flex-col">
        <div class="alche-block px-5 py-3.5 flex items-center justify-between">
          <span class="font-mono text-[10px] uppercase tracking-[0.2em] text-[#d4af37] font-bold">[00] Параметры Модели</span>
          <button type="button" onclick="runCalculation()" class="font-mono text-[9px] uppercase underline opacity-60 hover:opacity-100 transition">Сброс</button>
        </div>

        <form id="financialInputsForm" class="flex-1 flex flex-col" onsubmit="event.preventDefault();">
          <div class="alche-block p-5 space-y-4">
            <span class="font-serif italic text-base font-semibold">I. Временной горизонт</span>
            <div class="grid grid-cols-2 gap-2.5">
              <div>
                <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Горизонт</label>
                <select id="paramPeriod" class="mono-input" onchange="runCalculation();">
                  <option value="6">6 месяцев</option>
                  <option value="12" selected>12 месяцев</option>
                  <option value="24">24 месяца</option>
                </select>
              </div>
              <div>
                <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Маржа, %</label>
                <input type="number" id="paramMargin" value="20" min="1" max="100" class="mono-input text-center" oninput="runCalculation()">
              </div>
            </div>
            
            <span class="font-serif italic text-base font-semibold block mt-4">II. Капитал и Закупки</span>
            <div>
              <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Стартовая закупка, ₽</label>
              <input type="text" id="paramInitialPurchase" value="25 000 000" class="mono-input font-bold" oninput="formatInput(this); runCalculation();">
            </div>
            <div class="grid grid-cols-2 gap-2.5">
              <div>
                <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Цикл, мес.</label>
                <input type="number" id="paramBatchCycle" value="5" class="mono-input text-center" oninput="runCalculation()">
              </div>
              <div>
                <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">ЦБ РФ, %</label>
                <input type="number" id="paramCbRate" value="17.0" step="0.5" class="mono-input text-center" oninput="runCalculation()">
              </div>
            </div>

            <span class="font-serif italic text-base font-semibold block mt-4">III. Масштабирование</span>
            <div class="grid grid-cols-2 gap-2.5">
              <div>
                <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Средний чек, ₽</label>
                <input type="text" id="paramAov" value="150 000" class="mono-input" oninput="formatInput(this); runCalculation();">
              </div>
              <div>
                <label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Заказов старт.</label>
                <input type="number" id="paramStartOrders" value="40" class="mono-input text-center" oninput="runCalculation()">
              </div>
            </div>
            <div>
              <div class="flex justify-between font-mono text-[10px] mb-1">
                <span class="opacity-70">ПРИРОСТ ЗАКАЗОВ В МЕСЯЦ</span>
                <span id="lblGrowthVal" class="text-[#d4af37] font-bold">+5 шт.</span>
              </div>
              <input type="range" id="paramGrowthSlider" min="0" max="50" step="1" value="5" oninput="runCalculation()">
            </div>
          </div>
        </form>
      </aside>

      <!-- АНАЛИТИКА -->
      <section class="lg:col-span-9 flex flex-col">
        <div class="grid grid-cols-2 sm:grid-cols-4 border-b" style="border-color: var(--border-line);">
          <div class="alche-block tilt-card p-5">
            <div class="font-mono text-[9px] uppercase tracking-widest opacity-60 mb-1">[01] Выручка</div>
            <div id="kpiRev" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#f4f1ea]">0 ₽</div>
          </div>
          <div class="alche-block tilt-card p-5">
            <div class="font-mono text-[9px] uppercase tracking-widest opacity-60 mb-1">[02] Дефицит</div>
            <div id="kpiInjections" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#e63946]">0 ₽</div>
          </div>
          <div class="alche-block tilt-card p-5">
            <div class="font-mono text-[9px] uppercase tracking-widest opacity-60 mb-1">[03] Пиковый долг</div>
            <div id="kpiMaxDebt" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#f4f1ea]">0 ₽</div>
          </div>
          <div class="alche-block tilt-card p-5">
            <div class="font-mono text-[9px] uppercase tracking-widest opacity-60 mb-1">[04] Прибыль</div>
            <div id="kpiProfit" class="font-serif text-2xl xl:text-3xl font-bold tracking-tight text-[#2a9d8f]">0 ₽</div>
          </div>
        </div>

        <div class="flex-1 p-5 lg:p-7 space-y-6">
          <div class="alche-block p-5 border">
            <h3 class="font-serif text-xl font-bold tracking-wide italic mb-4">График обслуживания долга и финансов</h3>
            <div class="h-[400px] relative">
              <canvas id="chartMain"></canvas>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>

  <script>
    // --- PRELOADER THREE.JS LOGIC ---
    let preloaderDismissed = false;
    function dismissPreloader() {
      if (preloaderDismissed) return;
      preloaderDismissed = true;
      document.getElementById('preloader-stage').classList.add('fade-out');
      document.getElementById('mainDashboardApp').classList.remove('opacity-0');
      document.getElementById('mainDashboardApp').classList.add('opacity-100');
      setTimeout(() => document.getElementById('preloader-stage').style.display = 'none', 1100);
    }

    const preCanvas = document.getElementById('preloader-webgl');
    const preContainer = document.getElementById('preloader-canvas-container');
    const preScene = new THREE.Scene();
    const preCamera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
    preCamera.position.z = 25; // Камера свободна и отдалена

    const preRenderer = new THREE.WebGLRenderer({ canvas: preCanvas, alpha: true, antialias: true });
    preRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Свободная камера OrbitControls
    const preControls = new THREE.OrbitControls(preCamera, preRenderer.domElement);
    preControls.enableDamping = true;
    preControls.dampingFactor = 0.05;
    preControls.autoRotate = true;
    preControls.autoRotateSpeed = 1.0;
    preControls.enableZoom = true;
    preControls.maxDistance = 50;
    preControls.minDistance = 10;

    function resizePreloader() {
      preRenderer.setSize(window.innerWidth, window.innerHeight);
      preCamera.aspect = window.innerWidth / window.innerHeight;
      preCamera.updateProjectionMatrix();
    }
    resizePreloader();
    window.addEventListener('resize', resizePreloader);

    const preArmillary = new THREE.Group();
    preScene.add(preArmillary);

    const preGoldMat = new THREE.MeshBasicMaterial({ color: 0xd4af37, wireframe: true, transparent: true, opacity: 0.65 });
    const preRingMatDim = new THREE.MeshBasicMaterial({ color: 0xb8860b, wireframe: true, transparent: true, opacity: 0.3 });

    // ОГРОМНЫЕ СХЕМАТИЧНЫЕ КОЛЕСА АСТРОЛЯБИИ
    // radialSegments = 3 или 4 делает кольца не круглыми "трубами", а плоскими лентами/рамками
    const r1 = new THREE.Mesh(new THREE.TorusGeometry(8.5, 0.2, 4, 120), preGoldMat);
    const r2 = new THREE.Mesh(new THREE.TorusGeometry(9.2, 0.1, 16, 120), preRingMatDim);
    const r3 = new THREE.Mesh(new THREE.TorusGeometry(10.0, 0.15, 3, 150), preGoldMat);
    const r4 = new THREE.Mesh(new THREE.TorusGeometry(10.8, 0.08, 6, 180), preRingMatDim);

    r1.rotation.x = Math.PI / 2;
    r2.rotation.y = Math.PI / 3;
    r3.rotation.z = Math.PI / 4;
    r4.rotation.x = -Math.PI / 6;

    preArmillary.add(r1);
    preArmillary.add(r2);
    preArmillary.add(r3);
    preArmillary.add(r4);

    // Загрузка Витрувианского человека
    const vitruvianImg = new Image();
    vitruvianImg.crossOrigin = "anonymous";
    vitruvianImg.src = "VITRUVIAN_IMAGE_SRC_PLACEHOLDER";

    vitruvianImg.onload = () => {
      const w = vitruvianImg.width;
      const h = vitruvianImg.height;
      const offCanvas = document.createElement('canvas');
      offCanvas.width = w; offCanvas.height = h;
      const oCtx = offCanvas.getContext('2d');
      oCtx.drawImage(vitruvianImg, 0, 0);

      const imgData = oCtx.getImageData(0, 0, w, h);
      const d = imgData.data;

      // Удаление бумаги, инверсия чернил в золото (Zero-CORS issue since local inject)
      for (let i = 0; i < d.length; i += 4) {
        const brightness = (d[i] * 0.299 + d[i+1] * 0.587 + d[i+2] * 0.114);
        const inkStrength = Math.max(0, 215 - brightness);
        const alpha = Math.min(255, inkStrength * 2.8);

        d[i] = 212; d[i+1] = 175; d[i+2] = 55; d[i+3] = alpha;
      }
      oCtx.putImageData(imgData, 0, 0);

      const canvasTexture = new THREE.CanvasTexture(offCanvas);
      const planeMaterial = new THREE.MeshBasicMaterial({
        map: canvasTexture, transparent: true, opacity: 0.95, depthWrite: false, side: THREE.DoubleSide
      });

      let planeH = 14;
      let planeW = planeH * (w / h);
      const vitruvianPlane = new THREE.Mesh(new THREE.PlaneGeometry(planeW, planeH), planeMaterial);
      preScene.add(vitruvianPlane);
    };

    // Таймер прогресса
    const startT = performance.now();
    function animatePreloader(now) {
      if (!preloaderDismissed) {
        requestAnimationFrame(animatePreloader);
        
        preControls.update(); // Вращение камеры мышкой и autoRotate
        
        // Внутреннее вращение колес астролябии
        r1.rotation.x += 0.002; r1.rotation.y -= 0.001;
        r2.rotation.y += 0.003; r2.rotation.z += 0.002;
        r3.rotation.z -= 0.002; r3.rotation.x += 0.003;
        r4.rotation.x += 0.001; r4.rotation.y -= 0.002;
        preArmillary.rotation.y += 0.001;

        preRenderer.render(preScene, preCamera);

        const prog = Math.min((now - startT) / 7000, 1);
        document.getElementById('loaderProgressBar').style.width = `${(prog * 100).toFixed(1)}%`;
        document.getElementById('loaderPercent').textContent = `${Math.floor(prog * 100)}%`;
        if (prog >= 1) dismissPreloader();
      }
    }
    requestAnimationFrame(animatePreloader);


    // --- FINANCIAL DASHBOARD LOGIC ---
    function parseCleanNum(val) { return parseFloat(String(val).replace(/[^\\d.-]/g, '')) || 0; }
    function formatSpaced(num) { return Math.round(num).toLocaleString('ru-RU').replace(/,/g, ' '); }
    function formatInput(input) { input.value = formatSpaced(parseCleanNum(input.value)); }
    
    let chartMainInst = null;
    let latestData = null;

    function runCalculation() {
      const period = parseInt(document.getElementById('paramPeriod').value);
      const marginPct = parseFloat(document.getElementById('paramMargin').value);
      const initialPurchase = parseCleanNum(document.getElementById('paramInitialPurchase').value);
      const batchCycle = parseInt(document.getElementById('paramBatchCycle').value) || 5;
      const aov = parseCleanNum(document.getElementById('paramAov').value);
      const startOrders = parseInt(document.getElementById('paramStartOrders').value) || 40;
      const growthVal = parseFloat(document.getElementById('paramGrowthSlider').value);
      
      document.getElementById('lblGrowthVal').textContent = `+${growthVal} шт.`;

      const xLabels = [], rev = [], debtBalance = [], interestPayments = [];
      let currentDebt = 0, currentOrders = startOrders;

      for (let i = 0; i < period; i++) {
        xLabels.push(`Мес ${i+1}`);
        if(i > 0) currentOrders += growthVal;
        
        const curRev = currentOrders * aov;
        rev.push(curRev);
        
        let costs = curRev * (1 - marginPct/100) + 150000;
        if(i % batchCycle === 0) costs += initialPurchase * 0.2; // условная закупка
        
        const net = curRev - costs;
        if(net < 0) currentDebt += Math.abs(net);
        else currentDebt = Math.max(0, currentDebt - net);
        
        debtBalance.push(currentDebt);
        interestPayments.push(currentDebt * 0.015);
      }

      const sumRev = rev.reduce((a, b) => a + b, 0);
      const maxDebt = Math.max(...debtBalance);
      const netProfit = sumRev * (marginPct/100) - interestPayments.reduce((a,b)=>a+b,0) - (150000*period);

      document.getElementById('kpiRev').textContent = `${formatSpaced(sumRev)} ₽`;
      document.getElementById('kpiInjections').textContent = `${formatSpaced(maxDebt * 0.6)} ₽`;
      document.getElementById('kpiMaxDebt').textContent = `${formatSpaced(maxDebt)} ₽`;
      document.getElementById('kpiProfit').textContent = `${formatSpaced(netProfit)} ₽`;

      if (chartMainInst) chartMainInst.destroy();
      chartMainInst = new Chart(document.getElementById('chartMain').getContext('2d'), {
        type: 'bar',
        data: {
          labels: xLabels,
          datasets: [
            { label: 'Выручка', data: rev, backgroundColor: '#2a9d8f', order: 2 },
            { label: 'Проценты', data: interestPayments, backgroundColor: '#d4af37', order: 3 },
            { label: 'Тело долга', data: debtBalance, type: 'line', borderColor: '#e63946', borderWidth: 2, tension: 0.3, order: 1 }
          ]
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          scales: {
            x: { grid: { display: false }, ticks: { color: '#8e8a80', font: { family: 'JetBrains Mono', size: 10 } } },
            y: { grid: { color: 'rgba(212, 175, 55, 0.1)' }, ticks: { color: '#8e8a80', font: { family: 'JetBrains Mono', size: 10 } } }
          },
          plugins: { legend: { labels: { color: '#8e8a80', font: { family: 'JetBrains Mono', size: 11 } } } }
        }
      });
      latestData = { xLabels, rev, debtBalance, interestPayments };
    }

    function exportDataToCsv() {
      if (!latestData) return;
      let csv = "data:text/csv;charset=utf-8,\uFEFFПериод;Выручка;Проценты;Остаток долга\\n";
      for (let i=0; i<latestData.xLabels.length; i++) {
        csv += `${latestData.xLabels[i]};${Math.round(latestData.rev[i])};${Math.round(latestData.interestPayments[i])};${Math.round(latestData.debtBalance[i])}\\n`;
      }
      const link = document.createElement("a");
      link.setAttribute("href", encodeURI(csv));
      link.setAttribute("download", "Model.csv");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }

    window.onload = runCalculation;
  </script>
</body>
</html>"""

# Прямая интеграция Base64 изображения, чтобы обойти CORS при отрисовке на холсте
html_code = html_code.replace("VITRUVIAN_IMAGE_SRC_PLACEHOLDER", vitruvian_src)

components.html(html_code, height=1350, scrolling=True)
