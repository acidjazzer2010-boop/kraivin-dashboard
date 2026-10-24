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
          },
          colors: {
            obsidian: '#070709',
            obsidianCard: '#0d0d12',
            alabaster: '#f4f1ea',
            alabasterCard: '#ffffff',
            gold: '#00d4ff', /* Обновлено на неоново-голубой для совместимости с Tailwind */
            vermilion: '#e63946',
            jade: '#2a9d8f',
          }
        }
      }
    }
  </script>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <style>
    :root {
      --bg-space: #070709;
      --bg-panel: rgba(13, 13, 18, 0.85);
      --bg-cell-hover: rgba(24, 24, 34, 0.95);
      --text-main: #f4f1ea;
      --border-line: rgba(0, 212, 255, 0.16);
      --accent-gold: #00d4ff;
      --input-bg: rgba(255, 255, 255, 0.025);
      --cursor-glow: rgba(0, 212, 255, 0.18);
      --table-header-bg: rgba(13, 13, 18, 0.98);
      --grain-opacity: 0.035;
    }

    html:not(.dark) {
      --bg-space: #f4f1ea;
      --bg-panel: rgba(255, 255, 255, 0.92);
      --bg-cell-hover: rgba(246, 243, 235, 0.98);
      --text-main: #141416;
      --border-line: rgba(0, 85, 170, 0.22);
      --accent-gold: #0055aa;
      --input-bg: rgba(0, 0, 0, 0.03);
      --cursor-glow: rgba(0, 85, 170, 0.15);
      --table-header-bg: rgba(244, 241, 234, 0.98);
      --grain-opacity: 0.02;
    }

    * { box-sizing: border-box; border-color: var(--border-line); }
    body { background-color: var(--bg-space); color: var(--text-main); font-family: 'JetBrains Mono', monospace; overflow-x: hidden; margin: 0; padding: 0; transition: background-color 0.5s ease, color 0.5s ease; }
    .film-grain { position: fixed; inset: 0; pointer-events: none; z-index: 999; opacity: var(--grain-opacity); background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E"); }

    #preloader-stage { position: fixed; inset: 0; background: #060608; z-index: 900; display: flex; flex-direction: column; align-items: center; justify-content: center; transition: opacity 1.1s cubic-bezier(0.19, 1, 0.22, 1), transform 1.1s cubic-bezier(0.19, 1, 0.22, 1); }
    #preloader-stage.fade-out { opacity: 0; transform: scale(1.05); pointer-events: none; }
    #preloader-canvas-container { position: absolute; inset: 0; width: 100vw; height: 100vh; display: flex; align-items: center; justify-content: center; cursor: grab; z-index: 10; }
    #preloader-canvas-container:active { cursor: grabbing; }
    #preloader-webgl { width: 100% !important; height: 100% !important; outline: none; }

    .quill-overlay-nib { position: absolute; top: 0; left: 0; pointer-events: none; z-index: 25; animation: penOrbit 7s cubic-bezier(0.35, 0.1, 0.25, 1) forwards; filter: drop-shadow(0 0 10px rgba(0, 212, 255, 0.5)); }
    @keyframes penOrbit { 0% { transform: translate(30vw, 15vh) rotate(-18deg); opacity: 0; } 5% { transform: translate(35vw, 18vh) rotate(-24deg); opacity: 1; } 22% { transform: translate(65vw, 40vh) rotate(-10deg); } 38% { transform: translate(25vw, 60vh) rotate(-35deg); } 54% { transform: translate(60vw, 75vh) rotate(-18deg); } 70% { transform: translate(45vw, 25vh) rotate(-28deg); } 85% { transform: translate(55vw, 35vh) rotate(-15deg); } 93% { transform: translate(50vw, 50vh) rotate(-22deg); opacity: 1; } 100% { transform: translate(51vw, 51vh) rotate(-20deg); opacity: 0; } }
    .pulse-dot { display: inline-block; width: 6px; height: 6px; border-radius: 50%; background-color: var(--accent-gold); animation: pulseAnim 2s infinite ease-in-out; }
    @keyframes pulseAnim { 0%, 100% { opacity: 0.4; transform: scale(0.9); } 50% { opacity: 1; transform: scale(1.2); } }

    #webgl-bg-canvas { position: fixed; inset: 0; z-index: 0; pointer-events: none; opacity: 0.45; }
    html:not(.dark) #webgl-bg-canvas { opacity: 0.18; }
    .alche-block { position: relative; background: var(--bg-panel); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border-right: 1px solid var(--border-line); border-bottom: 1px solid var(--border-line); }
    .tilt-card { position: relative; overflow: hidden; transform-style: preserve-3d; perspective: 900px; transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1); }
    .tilt-card::before { content: ''; position: absolute; inset: 0; border: 1px solid transparent; background: radial-gradient(350px circle at var(--mouse-x, 0px) var(--mouse-y, 0px), var(--cursor-glow), transparent 70%); opacity: 0; transition: opacity 0.35s ease; pointer-events: none; z-index: 2; }
    .tilt-card:hover::before { opacity: 1; }
    .tab-view-enter { animation: tabEntrance 0.6s cubic-bezier(0.19, 1, 0.22, 1) forwards; }
    @keyframes tabEntrance { 0% { opacity: 0; transform: translateY(10px); } 100% { opacity: 1; transform: translateY(0); } }

    .mono-input { background: var(--input-bg); border: 1px solid var(--border-line); color: var(--text-main); font-family: 'JetBrains Mono', monospace; font-size: 12px; padding: 7px 10px; width: 100%; }
    .mono-input:focus { outline: none; border-color: var(--accent-gold); background: rgba(0, 212, 255, 0.06); }
    select.mono-input option { background-color: #0d0d12; color: #f4f1ea; }
    html:not(.dark) select.mono-input option { background-color: #f4f1ea; color: #141416; }
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-thumb { background: var(--border-line); }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent-gold); }
  </style>
</head>
<body class="selection:bg-[#00d4ff] selection:text-black">

  <div class="film-grain"></div>

  <!-- PRELOADER -->
  <div id="preloader-stage">
    <div id="preloader-canvas-container">
      <canvas id="preloader-webgl"></canvas>
      <div id="quillPen" class="quill-overlay-nib">
        <svg width="48" height="48" viewBox="0 0 64 64" fill="none">
          <circle cx="4" cy="4" r="3.5" fill="#ffffff" class="nib-spark" />
          <circle cx="4" cy="4" r="8" fill="#00d4ff" opacity="0.4" class="nib-spark" />
          <path d="M4 4 L14 12 L10 16 Z" fill="#00d4ff" />
          <path d="M4 4 L12 14 L16 10 Z" fill="#0088cc" />
          <line x1="4" y1="4" x2="12" y2="12" stroke="#111" stroke-width="0.8"/>
          <circle cx="12" cy="12" r="1.5" fill="#111"/>
          <path d="M12 14 L14 12 L50 48 L48 50 Z" fill="url(#penGrad)" stroke="#00d4ff" stroke-width="1"/>
          <path d="M50 48 L14 12" stroke="#ffffff" stroke-width="1.5" opacity="0.3"/>
          <path d="M18 22 L22 18" stroke="#00d4ff" stroke-width="2"/>
          <path d="M42 46 L46 42" stroke="#00d4ff" stroke-width="2"/>
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
    <div class="absolute bottom-10 flex flex-col items-center gap-2 font-mono z-20 pointer-events-auto">
      <div class="flex items-center gap-3 text-[#00d4ff] text-[11px] tracking-[0.25em] uppercase">
        <span class="pulse-dot"></span><span id="loaderStatusText">Инициализация 3D среды...</span><span id="loaderPercent" class="font-bold">0%</span>
      </div>
      <div class="w-64 sm:w-80 h-[2px] bg-white/10 relative overflow-hidden mt-1">
        <div id="loaderProgressBar" class="absolute top-0 bottom-0 left-0 bg-[#00d4ff] w-0 transition-all duration-100 ease-out"></div>
      </div>
      <button type="button" onclick="dismissPreloader()" class="mt-4 text-[9px] uppercase tracking-[0.2em] text-[#00d4ff]/60 hover:text-[#00d4ff] transition font-mono px-3 py-1">
        [Пропустить Intro]
      </button>
    </div>
  </div>

  <canvas id="webgl-bg-canvas"></canvas>

  <!-- MAIN APP -->
  <div id="mainDashboardApp" class="relative z-10 min-h-screen flex flex-col border-t border-l opacity-0 transition-opacity duration-1000" style="border-color: var(--border-line);">
    <header class="alche-block px-5 lg:px-8 py-3 flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center gap-6">
        <div class="flex items-center gap-3">
          <svg class="w-7 h-7 text-[#00d4ff] cursor-pointer" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.2">
            <circle cx="16" cy="16" r="14" /><rect x="6" y="6" width="20" height="20" />
            <polygon points="16,2 30,26 2,26" stroke-width="0.8" stroke-dasharray="1 1"/>
          </svg>
          <div>
            <div class="font-mono text-[9px] uppercase tracking-[0.25em] text-[#00d4ff] opacity-80">AUREA PROPORTIO // 1 : 1.618</div>
            <div class="font-serif italic text-lg lg:text-xl font-bold tracking-wide leading-none">Архитектура Капитала</div>
          </div>
        </div>
      </div>
      <div class="flex items-center gap-4">
        <button onclick="exportDataToCsv()" class="px-3.5 py-1.5 border font-mono text-[10px] uppercase hover:bg-[#00d4ff]/10 flex items-center gap-2">↓ Скачать</button>
        <button onclick="toggleTheme()" class="px-3.5 py-1.5 border font-mono text-[10px] uppercase hover:bg-[#00d4ff]/10 flex items-center gap-2">Тема</button>
      </div>
    </header>

    <div class="flex-1 grid grid-cols-1 lg:grid-cols-12">
      <aside class="lg:col-span-3 flex flex-col">
        <div class="alche-block px-5 py-3.5 flex items-center justify-between">
          <span class="font-mono text-[10px] uppercase text-[#00d4ff] font-bold">[00] Параметры</span>
          <button onclick="runCalculation()" class="font-mono text-[9px] uppercase underline opacity-60 hover:opacity-100">Сброс</button>
        </div>
        <form id="financialInputsForm" class="flex-1 flex flex-col" onsubmit="event.preventDefault();">
          <div class="alche-block p-5 space-y-4">
            <div class="grid grid-cols-2 gap-2.5">
              <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Горизонт</label><select id="paramPeriod" class="mono-input" onchange="runCalculation();"><option value="6">6 мес</option><option value="12" selected>12 мес</option></select></div>
              <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Маржа, %</label><input type="number" id="paramMargin" value="20" class="mono-input text-center" oninput="runCalculation()"></div>
            </div>
            <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Закупка, ₽</label><input type="text" id="paramInitialPurchase" value="25 000 000" class="mono-input font-bold" oninput="formatInput(this); runCalculation();"></div>
            <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Средний чек, ₽</label><input type="text" id="paramAov" value="150 000" class="mono-input font-bold" oninput="formatInput(this); runCalculation();"></div>
            <div class="grid grid-cols-2 gap-2.5">
              <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Заказов старт</label><input type="number" id="paramStartOrders" value="40" class="mono-input text-center" oninput="runCalculation()"></div>
              <div><label class="block font-mono text-[9px] uppercase opacity-70 mb-1">Прирост</label><input type="number" id="paramGrowthSlider" value="5" class="mono-input text-center" oninput="runCalculation()"></div>
            </div>
          </div>
        </form>
      </aside>
      <section class="lg:col-span-9 flex flex-col">
        <div class="grid grid-cols-2 sm:grid-cols-4 border-b" style="border-color: var(--border-line);">
          <div class="alche-block tilt-card p-5"><div class="font-mono text-[9px] uppercase opacity-60 mb-1">Выручка</div><div id="kpiRev" class="font-serif text-2xl font-bold text-[#f4f1ea]">0 ₽</div></div>
          <div class="alche-block tilt-card p-5"><div class="font-mono text-[9px] uppercase opacity-60 mb-1">Дефицит</div><div id="kpiInjections" class="font-serif text-2xl font-bold text-[#e63946]">0 ₽</div></div>
          <div class="alche-block tilt-card p-5"><div class="font-mono text-[9px] uppercase opacity-60 mb-1">Пиковый долг</div><div id="kpiMaxDebt" class="font-serif text-2xl font-bold text-[#f4f1ea]">0 ₽</div></div>
          <div class="alche-block tilt-card p-5"><div class="font-mono text-[9px] uppercase opacity-60 mb-1">Прибыль</div><div id="kpiProfit" class="font-serif text-2xl font-bold text-[#2a9d8f]">0 ₽</div></div>
        </div>
        <div class="flex-1 p-5 space-y-6">
          <div class="alche-block p-5 border h-[400px] relative"><canvas id="chartMain"></canvas></div>
        </div>
      </section>
    </div>
  </div>

  <script>
    let preloaderDismissed = false;
    function dismissPreloader() {
      if (preloaderDismissed) return;
      preloaderDismissed = true;
      document.getElementById('preloader-stage').classList.add('fade-out');
      document.getElementById('mainDashboardApp').classList.remove('opacity-0');
      document.getElementById('mainDashboardApp').classList.add('opacity-100');
      setTimeout(() => document.getElementById('preloader-stage').style.display = 'none', 1100);
    }
    const startT = performance.now();
    function updatePreloaderProgress(now) {
      if (preloaderDismissed) return;
      const prog = Math.min((now - startT) / 4000, 1);
      document.getElementById('loaderProgressBar').style.width = `${(prog * 100).toFixed(1)}%`;
      document.getElementById('loaderPercent').textContent = `${Math.floor(prog * 100)}%`;
      if (prog >= 1) dismissPreloader();
      else requestAnimationFrame(updatePreloaderProgress);
    }
    requestAnimationFrame(updatePreloaderProgress);

    // 3D PRELOADER - ГИГАНТСКИЙ МАСШТАБ И ТОНКИЕ ЛИНИИ
    const preCanvas = document.getElementById('preloader-webgl');
    const preScene = new THREE.Scene();
    const preCamera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
    preCamera.position.z = 80; // Отдаленная стартовая камера

    const preRenderer = new THREE.WebGLRenderer({ canvas: preCanvas, alpha: true, antialias: true });
    preRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    const preControls = new THREE.OrbitControls(preCamera, preRenderer.domElement);
    preControls.enableDamping = true; preControls.dampingFactor = 0.05;
    preControls.autoRotate = true; preControls.autoRotateSpeed = 0.5;
    preControls.maxDistance = 150; preControls.minDistance = 5;

    function resizePreloader() {
      preRenderer.setSize(window.innerWidth, window.innerHeight);
      preCamera.aspect = window.innerWidth / window.innerHeight;
      preCamera.updateProjectionMatrix();
    }
    resizePreloader(); window.addEventListener('resize', resizePreloader);

    const preArmillary = new THREE.Group(); preScene.add(preArmillary);

    // Неоново-голубой цвет для чертежных линий
    let tintColor = 0x00d4ff; 
    let dimColor = 0x0088cc;
    
    const preGoldMat = new THREE.MeshBasicMaterial({ color: tintColor, wireframe: true, transparent: true, opacity: 0.6 });
    const preRingMatDim = new THREE.MeshBasicMaterial({ color: dimColor, wireframe: true, transparent: true, opacity: 0.3 });

    // ОГРОМНЫЕ ТОНКИЕ КОЛЬЦА (радиус 30-55, толщина 0.1)
    const r1 = new THREE.Mesh(new THREE.TorusGeometry(30, 0.1, 4, 150), preGoldMat);
    const r2 = new THREE.Mesh(new THREE.TorusGeometry(38, 0.1, 8, 150), preRingMatDim);
    const r3 = new THREE.Mesh(new THREE.TorusGeometry(46, 0.1, 3, 200), preGoldMat);
    const r4 = new THREE.Mesh(new THREE.TorusGeometry(55, 0.1, 6, 200), preRingMatDim);
    r1.rotation.x = Math.PI / 2; r2.rotation.y = Math.PI / 3; r3.rotation.z = Math.PI / 4; r4.rotation.x = -Math.PI / 6;
    preArmillary.add(r1); preArmillary.add(r2); preArmillary.add(r3); preArmillary.add(r4);

    // ВИТРУВИАНСКИЙ ЧЕЛОВЕК - ИНЪЕКЦИЯ BASE64
    const vitruvianImg = new Image();
    vitruvianImg.src = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZAAAAERCAYAAABVU/GxAAAgAElEQVR42u19DYhNafz/9y41G2WjbJSNslE2W7bRbzSKRo1GjUYRRRRRRBFFtmwUUUQRRRRRRBFFFFFE0ard/yrbKlpFq2gVraL7n89vPs/vPPPMOeeel+ece869z6dOd+a+nJfn5fv+Uvl/F/9HSojW3uNR79Hee9wThzio8rXihsLBIt72HsPdumoufFWy++2KwDxaM7hmozCOKje42+QOtjGC6wpr7K4bDusCs2MgFgj5CDIPCdE8Rvce13uP5dp787mwu2Nec23v0cajrLjNZ5/V5Iyj3dGhXFAhA8GaO1nA+5tP2tBdkvFc2ntMdwwkPa71HmcifO9K7zGm99itvTeFr6NiXnN87zGs9/hcYq1jBjf1rSYmap3aGnDIHlu45lq4BovEvD+RDkwoyVh+5D0XU1ooqQ8kCnp6j0spzzGDzOhMyZ7d+Tn6o4Mb8YEbityxsPc4W8D12NHkQlUpNJCVvcd27f/FxucwS22UbGx8lyyc407JmMdiMo9Fjnn0w62CMg+YUVaTmBURafclNI9zXIuLNMGmKGvCISUGZ2w2ONh7PKb0914GmoKGUj175KbCaR1NiCuU0McXlKBNIo1Iynx1P+U5HhdpHXDr1DGQQCkYts/JfH3Xezz02SCQvkb2HofcNFhhHmk2pFPn6wcQ1aIGaWD/jrWsvc2jZoI1u6v3eNV7rOs9fus9Frjl4BgITD7LxXP+vAohTkfcFKQCNLpBKZiHYuKDqA1ecUNaFxTVN/OCDMQ27okX8qszK4eSIY4PBOFkm/laCye4KX4OYRJZEivYldc28Lx1cvMdTal5XOFcPZO+aDMHBx03eo/fMzw/1u4d/j22Sce4rcz3GkUDgSMNttBxlHihVXTxt2FMAAtiX50eFBL16AZdcIhoWSj2bMitlP7eOnrpUAftaCaFPfhLj/ceK5pwfItqQu40aCpofr8E7qgaCJgGnOGwWcJme60G8wCneh/zZpH8t83Sg8Ov8rQBF1vVMvMQah6Yz3eOVjrUCYe4pt9IsSK18sKXgt4XzNujSCPAPIbz/f/L6/HLA+kkw7hjMISsJZG4UUTdlJwvNMECg9nwJJn23ALcj6tB5pAVsK8v9x7TpHnydoqogcwQzzf6STwfVT/FQakkI/glmDFgpvqQsxoLrIopBY8hd/xACbpRcV76yi8UKewRi6mL8xW2NroafG6aGaomnW1cEc/BDv9cM5i0Phbwnu5oCgV4wg2/L4GBTCQRfqtxmXrkZRyL+f0jlFYa2flb1NyO0RKtvMJgcWhUZB01VSFdWi6NnzNSZE3rRq0NfqLEA9/IYadVSgEzC3hvz8Rz/gWZs3okfQ0fl59STLTnJLgNpQaeNs/JISN85YagcNjIDbOmoMxDl5huSbAvxIb2MdQth0ICc/4mp2shuXCeeAEkDo6BOARgZ++xt/eYLS7JUqHTDUEhkaeZ+xI1EISw73ZDXxw4G3Vx8I/0hc01iqpuIzrurdNCHDQo53pbgbVzx0AcHPMoCFyocHQg7PJOEzGRD064qD+cCav+qDrm4ZAScGo3U8Ms7JWL0pxJh04DcejHPD46ScohJRDt9qTJnnlJ7/FSXISWYyCOeTg4pEKz9tPZQhrmmEid4ExY9WMeWxzzcHBIjU0ysDS8Q0EYCBK5uvk37KytbsisMI8dvcceNxQODtbgmEgdUMuEhTInqMDYwuOVG7LEQOjhfemrPPqLGw4Hh8yYiDNn5TXgPtV4wwjgAzdkqTSPolTTdXBo9L3mmEgOiOMDyZp5dDT4gj7hmIeDQ66aiEOBGEjWmNV7LG5Q5oFaPivccnNwcEzEMZBscFf64rpnNBjzQJ+TS26pOTg4JtJoKFIeSKM1HsLCXSR9LYAdHBzqy0ScT6TBGUijMY+Z0hy1iRwcHBNpUrhEQvvYyYXabMwDfdu7LZ4POUfz3XJysIRp0rjmrDangRQfUXpAn5Y+H87PGd4HEjrRD/5czHtHHk9QdVuz899yfh8VT9H3HLWWPvN1GF/fS1/gw9re43fp63/+p/T1qR/Bz1VPE3xnNN8DUKb9GK8zXvo6HOqdMXs4hq1kxCf4W5WP9EW8/CTghfTlKBWlei/maFzvccZ4H71NbsQkDBM45h85Vg+lz6fWwzF9Jf19bAv5/pOAa0UJx1drHc8xlfN9JOQcMzgfl3zWlUiyrpI9fOYbFubjpnYvUdpEL+YYbEhxTeyHaznRpfFSpxSLOHkgzQwsupckWO+4aUdwMy+Tvu5so2Ke8yUnfQwJ7ysS4vkkGihzMoTEYzA38RDjHLiXQXwdqX3+kcRfNKL7ieccxPc/8Xufte+p/8dYGrcHHKcJPp+947VGWrrWF47hYL6+5usY3oNqwYo+JVt97uUpxyQsiOMOzzM04JlOkHgrAvKA96XmYBDvbzhfP/CaauyHaXMuBtN8p70/yOfaH3mu4dp46N97z2sOMT77xP8/8HWY9llLgffkNc7VbxEk8FsSnCbwiAJMjzbGQ7T1Oy0BQV9Oxjs1p7FIw6gdA8mJgVQifOcUGYqScvD/WOnzh2ymBDqLm3VIBEmo6IC0O52EBgw0LM8F5q0rdbi/cwFzpVAruXMltSUFsw9FByVcoQY0vQDzElfTaQRcJgN8TMHhhTEG+h6OooUc7j0mSbLGVRfJkFYZaydLjXe02GniFgvOB2KPwYgmTWNhIgJrKaUkfL6HzAMta69KXzlq9dvLJX1uEOd13Ci1kiSv1On+TOlQzdUCztNcwxQDH9Z58fpvfzTOMdRHuq1QcGg3Pjtap3lpNuZxnQIK8q12kGirMdjG1zW9x2rO/wIfQUJ85jmpBnaHFoaXOT3/PWqSzoRVQg3ElGz8JFpzoYKZbNHeP0eG45A9kz9CQhJF8/uPc7PMeL+LjOWseCYrv7nGNeD/OeSG3wrW9x4HtP9hdpxA4vl1yO+2krnoJqV/pc9cFbQOjktfLcCkGmXeWmC71MEH6DQQu4xFSbQgMG3G+wu0/zdrzKZCadclPGXPPOZSEo2a2HkvgAjATzWKzGMn53uzNtfvte865pGeaZylVrifmkaVh/JDfV1j7h/LQH/EN9IXqHEx4HfQPtL4AvPWAusSQOIYSHKcNAiFDjj4HmjqMxb/BR9pZ65GdHRCt80Nr3XmAY2hh3/7Oe47yAzM9874mEtWUDOpkgiZ5flBnNZRynVIhwPUzhdwLpS5dwf3TUWCneiYn03cq37YRQay0OezL27oa8OZsJJpGkoF/ibkN3/0Hj9In78DEirssqsMolYJIXgLpA5OsRICfo0RIRKfrtnNFC8/ZzUZyQ6f7+lQUVLPSMhGUkDoJjEDA0HE10vtHhAGejpkjh3iAb6p2wnG02/fHpaBJkwzMALYSu3nWzf8wXB5IPYYiokf+KrCKsE89orXQe1mEFPn+c8b7zn4YyKJuwnUVtPt1zukf3LnSxKTkdQW4o4xzI+PKMWagKSMAIpONz1WcMcS81DvmcEVQ32+/94Ne204E1Y2zEPHNEOdVpgV8ptV2oapUPr6p0nHG+aJnSTICutpdoDjEKGWMDUt1z5/TuahaxXbjHOqqLC1KbWfIMzW/j4tnt1+p9tCifbcrBqfq2OjwWzU+wu1/++ECG66gOHgGIhVHJToWea/Sf+wUbV4j0f4rRk7DtPLliYdc5iKxhrvwS7+iVrGM272p9oYj9XGfY2P9PrAmJekbQRwzi7D1GIKGsgj+VF7v8Vto1j4m69RkuSwN/f1HtspVFQ1Iews5z2sQi/8WCr0Gtqj84P4o13tGecDiad1oATHiAiM4yoJxfoaxCcMv0pfOYolbvgTzZXyQ+Dvi2Q0mJN1/M4vJDRxTSNB2qgZYtpOBqcEgPEUHoqSbFhkwEdxOMZeAdFHSC5MxI84ztBI4bOaSoFCRUHW8l1+poaqfj/CTccAIBgFEWqHnAYSj1iELabNmoQJbQF1dPR8kHU+5wuTfH+SgcUEwZhOuqmoOQet4jmxQQyQA7BJmwMQpAnGXCTVQBT2G5/d0z5v1TRPxzw8Cf+s9v958cxNYB6nNO1BYbvPefZTaOsWr1bdCm2sN5F5XOW5v6lxX/ALqxJFn9w0+QJh8PARdTkNJL6k6YcuEqkz5MynZWA597/FP678joSXS/iLv3tJ9fxIE417KwnAMGoQqDm2I+J8hUmvtT5PgueUdLdI/5BeVXhQNRc75rZTP+gRa8J9dClkfBGODaf3UjKZoP2pNMLrZFZLZGBIdhDgFztIC8APbopCJCjHQGpiPqWjuITmMheg7rvo4OKfksB8slTTPpohKgtmjHbxTHjbyUijtAZWDALhtaM1AlMN0SBsCBl+58X6uZAR0yozVL0ooZCwL8b46uMYZJL6Tzx/UyXhfL6PoLE4BuIQaeEm3fTLqZJ/zUUNCetaSoKifovzzHFT5Ds2m8ist6fZHyHEK+w7FR9NaoZ2X3elf2WCZsFOamMbOR6oQj0xAYOutW9sMGulhThmHwLnAwnHHxEko1o4QeZRpUSkegScMxZ8j8ZwFNq5iOeLF56oNkWFzKNKdR124Fficg92cWz2pmQeSbUPkYEl4R9xHeH9UQ3IPNTzqjXcKV54NMJnt1J42kom8oRzNDHGNXRCPieAsCPi7S2FtEpK4v8xgvDgGEgTPGNSgnqYi2iTLW1P+iJCqpRIVTl32GXfUKUHwdPDfOGIPSteg6eg84IoTebrdW7WZgRMfD/HmI+KQTCmG4y/lhTrtzbALO74EDbMLSKxrjTguN8h87jI9X2dgg+SZWFChDN6FccRIc1rUuyhXyS4UROisRDocsnCM2F/wvT4TtLlCjkGUmJsJ/FN0vJxtdhvCPNI20Sq/SuksG+1zWESq23ULHaFnHeLRhAr/O5+CW4JC8fl0gaba8yX3kDpmHhx/2HS7O/8fyiFDTWGUyIQMz/t1C+58BjnGUmPL/je/pKPdw+f4R8yjYtkJLr0j+S/AxynU5au60fM94r9nudYD4PJkA46VhGwCRrcBwKzDxyvcVtTmhEzthenn+kj6PxQyV+SONqKCJlB5opX5WguO8yxjOK3qHUuv1IYyA04F3JtoUY50jgHovC+43ch2Y7j98rgwzKbgeVd66tK7RAaOfI01pPZ475QafenDK65nlr9Cj7vZumfEOogjV8LK4n/YqUmNWbOwCm5wfQU1D0vi0QmPXS4mxLWQil34biKZUZfCVhP63zm6Y7093t8azAWdV+rIzC3ojGOFkr9w/iMK3NkHPpczNfGcQaFqrkZX1eZv89I/1BjhyZhIElwNOfNMY+vCPFFVdCbOWwMHVd4KPv1l5KtCyR9tUr/aCgQl98pQQZJtFG0EPM7Qf6we2TI8MEs9WEQyi9zxGB2Ra+2fEXTqG7zb5QUmVUn7VLNB5jZJWrne6R/3o0twAfyIkMBpSHgorD6A86/U3W6NjbmUDKPk1ys23O+PjbHDfEygsvgPNzss6lhthxUY7NXQzSBHeJvvuoI+L5iEEsDtBjdf6VH2RU5GmsnD+UUnyqeXyMPXDXmqOLD2EZkxDyEmtdb4z0EA+x1ZNIxkDCVdVkB7mMZN8w28S/AuDXDa6sQyQoleeUgnVEnbRCAea0r4Dt62W29LfCkGNItjj/4/2Jt3FcbROxmDGaE8Wv3+c5xH4JYNPRwjW3lfSIM/VGO2obqIogkUvgg9oXMf1xAW40SVKP6wOjAOGx0ZNKDM2F5+KdgEuF2EnOELN4Xfydx1kTokngd3+6LvwM5K3RwA/fUuObDCKaPIPiNo27rPizBPSV0DSgId7XvVrjGRhbUFLKRTHd5HRjcco2xQmj5jn/D3wLz2SsJDt2NyzygtXyO8N0v4l+Nd444U5a3gVwm+v/hcwhDLcKCQWmUcTLQrv+zhIf42pYO49QUygPwG62TaGXyozCQJPPux6hQu2u8DzHGOoN5bWqOUn2c+c2beehjp8rUnNAYOEKx05iVF5Nx3KJAMiiiEAQBDv7JHwPuGVrRJmk+QJgcq8bQaSDegih6dvDcgPuGnRpRQPfyEDh4TTgxsyjq2M5NPonSX5RrDNWITlDNq6BnEUq4JrNopVR8SDvXO4kXEfe9D4HU/55SMAaSN/NQiYfPtLEyscbCdYZwLjF38Gk8jvi7oRKcvDuP996MDGSKaM22HAPx7KFl7D+uRx7tkuhZ2DaYCMbNtr8ITLCDhNuGRBuG59ToEHK72kfrUMRdlYA/HaCR/B1xvBb4zFse2C19ju8nlL6R0Aj7vsq6B1EdnvN9VY2xyRIIx0ee00bx+sFEAYSkCQGfXdLWRLP168EauuIYiIf7Uv7aRNiIKPveKfaz5/0A4gP7PqKOZop/i9AkgM0bDmxk1p9JOA5RCZLe5fCwQdjMc5wgoVgSg1mZzOZ8zkR6KaVFEM3xMjBDvhpAFLO+J7OidB7jcZNj8Emi53d9irjWys5AOsQLi46CZ/o/zR6FBensRUm1Dx0HKbWr6KHNGV0HoZWfxWuWBGYFs9N1SuKQZj/wHuCziRvyiM39nST3sXTF3NB7xd+hWjEOs4T8HxLNQZ8VYP6ZEUIQqtQ01lG7UhrGVJ9nU8e8jNfoczIPzA9MPwspvJ3N+LpdJJA3Yl5rWMTv/ZrTHm/N6LxYJ0NjfL9fMEOzO9HjOEmjfE81DyrCc2VBxNq54E7EkPzg9N9BJrdO0pmnojxzGi0uaoJhXG1ItdiF1mMr4GGb+DfXwhzt1BhMvYM/FmqEu0yRSyoptGKJNiRFp3ghxTcyOD+0/ndJhehm1kC6LWse+6U4BQr1Uu/QCNZbOu+nGMwDgO39WzINVbBQz7mw/cxpiFRVI8A2mJTpPD8tdqPltvO8W43r3CWhSVvO3BZTP6vdC8YAyam3NU21qPgk0VrafsxQi5pBTehORsxDyDxakv64mRkIJAxbvg9Il/ALwM46vyDPd028vhhgbq8snDNt1NAe3tMPJB5Pfb6ThgkvSsB0TCJ7V7xkNvNIgqkJtK7j4pnJ/I7t2r3v1N4/Jl415noyDXWo6tPQPh+KVwARlQKGiD3fWRYAUX0d4XtDqWVlAYzP84yfE1GIbx0DiYf1Ej0aIwpGkhi+l+L5U1SJ+CPc1PelGE2nKhwv3BN8UYiS+SxeGRd1YHH/ZbzXHXDOcwm1kEpEaVM0oqjuvxYeUuoOuqc249nu8/0fxN9XAQ1Q+bpuGoxwVR3mcb7BdGfzXtaIF9Bxl39/S6Ko1uSDgtOJDxG/d0rCE1rrKbRFYVKJkzSb1QcS1Ec5TKoKI0prqW4ikuFMCZ6/k5IrGB/s8kmTEfeSwKeVeOO0IIVT9GqN76uM71owcxDi5I9E+c0izYQT9uyHEgg09Uj60wHb+dEY86agtJFTBd8j0AKRjzTNEo1oSDSjBgLCaTvpDgTg95IwD0TptFMiHCd9vhLdDNIT41yb+Nu0PhYlQe+I8N1rhkTeTe0P9/4bv1OrLL3SVMb73Ici5DMDNIBaDEVHFOYhCZnHsRwJlh4B1M7rK+bxc8z7WFcC5gHAfBUnOukSNS3HQBocWyWbipo7In5vRp2f/xZNCDpBnq0RT1XWfZv2neU1iD9MTzZ8LLiv3TF/g6SmieJ1eozipF8UokEc1FT7OFrAKu3vlwHM5SB/g5Dn5zThRG0odTPgelnhP02oeKj9fZcCGJ4RjdqQa3KyAenE05jfnyfhARiOgTQIVpGIJoGycyLPAo7pXxMwo54CMBETY0kcZpA4odzDdulfQVb9vTtAA7PV1XCLBW3mhxqfR52nqNqAaBoBGCmcxKrMuKroC4bRRZPId9T+pkk0+zM0q8kWNI6VNT5fy3uFRvlG0zI38F6VFjadz4B2tQhEWVaSvY9nUwmd22p896VEK7qoAz6xxc1ETOudid5BwpOX6QfO2O9T/B5mn4WUNP6kBGna2rv5nl8F0S4uzKJFnxwTr8UqmEVYi9A/yEDviVcOww8XJfvktDD4leOuBGgd5ndUCXudYMPXMyKEMKnvjtaEDRt+ipOSvpXqSs5FkLajt6h9QcZwgPOsd/UEMzwi5YLKzerW5uEptdYoDCEOvuGcn7F47z1cxyOpbZ8r0uDWWwOZSGktr4X02MJ5MIFzObGrNSllJzf7ZX52jZtyuWEu2lfATQazxDMSjRUS3DhJxIsOml5DK5nH9/F5nqHNM2ju+Vp7755BxE/5MAxTSzUx3Oc9EKZfApjSVAubHSVW0oQ1q7k5FsA8MM+3qU2r8RnH104fM06rFBdt4plfzag2VRlBvTdBBka9mbglWtHAmFht+bmgES7KkVZGV/frHIW1nov0Wg7XCpMgo2xEU4o8TubgJ13uNkwx/5LQ3NUk/bhayElKROsyGp/VJFi4zx0JxkfXZvwIcKdGiNMSVr1/hFAbhMS/hCaKBcZ9VQLm0SzqVwmY8/1cq5UI6yJs/ahS7sI1oGuvKHYYpQlWrYi5/yixViLO1xtKzENJMHdozGUM78t2KCnm74RFGqLqfvmt3SjXqlKzmiGe+bOd/8eNMMQ6vy72Ahzm89nU3BcK9dZAEGf9JadrvbF8vlNcJL9SugGRec4FtNlHtT3AjXiQUt9/ESW6m9wgJzJkHqKZJrZLfDvuGzINSPrjxT/5Dpm0Q0gkT9bYMGeNc6zkmKn/O6R/ZNRE8WpgmVVvo5itrpPxXQ0hUvsCzF1+5iCshb+M91W/GXVP3xrPAML1kXNc0Z7HjALbRUn7Vz7TbeP5BocQGn1OdnCsVnBdrtKI70JK4Iv4nl83wLCumHqezt8J9+L5kHnDftumMfcp4h/Fd5JCUQfXkJ47ozQ8NcZrOMe/0YJwVOJFYenr3CYucD4LxzzUYqsnjkk+SW37xa5zq1NbKI/FK7b3jGaraWQmq320q25NottIyXmZBIc2zpJ4eRIKcIhGzYDeSJPTI0qdQTbcxQGffavNp2gS3DLe+xWa/S5J/6qfunRY1RjZIgoXZzjW0Bxnxpyjv31U/gvaddR9nCEDmkXtoKox6qoxRhsN81WbZiJrD7lW1DnTCdb4kO/NC2AKyo/xJUC71LWc+dI/Gk+H0hDDIsT0xEsIOCqvaB4J/BZe65n4t/utpRmZ/ystbjf3UDeFnTCNeZl4Dv5bZApXjfOu5vr8SMa5j/Ov7j0Jdkl6f2spUG8TlopGytqpnDbJR19wiA8fJV5nvpvi+QzCGEGt8x/gQt7Mjb5B2/i65HZD+lecjVNiY4H0z5Tv5BwsJdFRJc7f87s3jI3WRg1KN2m0kfAG5dZ0cPPiPvfIwCirICKr7u2qJM/biTvvarwrMYheGLaSSX6RaE7bKOMiPlL2MuM3WzjW3STmOtFv0RinWlNT+f0rIQJDrXX2UuLb6DeQKX/kmms1hMsnFP6CAIf/uATjeoVr+1CIwLme35ldJ5rjGEgE294QyT6paDkJfpps6TyyfvdqEu6zGhKovmkfc5NH8SucJ2EeRqJ+hYxLx0NjI4PofE2TwSjemzLndHEef+RvXnJTg6G847UGBdzLCfF8SPNlYAmYbjKfDTmvyw+aJtCZwiyxmAxkFRlT3L4R/3KeKgnWqdTQHFrEP0oNBBtRZMMp2c+QgQEVNvaA331eoulIrQuF36V/FNpt/j9cwrsZ1iLkl8W/y6fCX9Qyk/b7eEWt7JA0JmDheNcMpUxsSAJRGMh98coe/Cf+FS7jOFy3kumtpDS2nCaCUTkTVf3Zt3PzgrlN1swdUYoYbiST1AlXxWCgjzWJt0fSNzlS2k/eWG8w5iRl/lUZ9ChrxjTXzU7I9M7KwMKAp6R4eR7HNSZTK1jgGPfMpIhCmY4rNZhMs2ohSrh70QiJhHkl7mygRHFZ+juBz3OhnODmqxrMw4zsqZWcpGLPd2mqvJBg76mDRK6eYTG1kB4+gyrRHrUC7j5+/2u+vhYvvBLYROaxUZNI00In4nCUX0x4nqPiFXSMgsna3xclWbXWkRJug1cFFascK93RntSRu0gGlmwpYpLg8oha10eu27nUVCoRDtHW9Sdx8AMYMUyfB8rOQNYam9VEj0UJYDu1gsGGtLdAIzJna6jrFR+TkYlhIQysHlCmJRD3R3xeJBqmjQgbzfHA5tZLlyOiZj8ZS1fKa0w2pPI4kXhgOJt5T6s0AhRVQoP5C/6xdmok3THvfXCAxFzlvY3ViF4W0XlFlZz9xvGp+Je936kx0/01zgst8bZ4PrpPZEBpMFf6h5s3Cg4oAbfMPdHXcpK31CB+tp5xmIVNtZoS9gUpfilrBTiA33IzZtVv/YcAQtmdcsxXGCahOPWjZvMe1iS4ropK0zWBf3j9qJrVFI1grhfPF5EnYY+TDwRGeZca9AnLAs9iamQHxL93xYQA5lc1xrMawixhKp6pvYfIv+cp7/sKBaEVBbPYwPf8QiyEHH8ltevjJEXWvY5HauadTvFCKhWw4QZZlsjgGPubTOAtJdTnNX6jb3hVqO9+yGK+YGhQypG7t04LbhE30z5qYXkVzpujEaakAsaJlOtR9VGxgW8lnlnurUYc68E8wLii5kFUNQHrG0vM4zgFrtXUfpXmHhaR99pnjFS5nRkyMMpMv3+zYOgzSZYHUnR0ciw7bJzsK8vqb5d4pb3D7Iet3OAbfaQY02y0PeD3LVxc22lSmqJ9vpXmgweWGeRomnB+5LUHiRf6ek88O786egxGMlgG+kQUI7kq/ctB76S0cJ3/byzA4kNkzjLpn4yVFWBu2kTGuS3mbxFJdqgkJhmFbT5rTQkOe+pw/8NDCK4fo7VdTWIFmbfOwM9L/yKXpu/Hr6DnPe0e50q478PP6pAW0yS7ZlNJcIRCoJXqAoO5OG0VvvtRG/Swbl7LDdPAbjKEl9qEgwlMDCBWj7QB8GNYyhH9kpIs/rdVhOwBDxD+xzU29kWJ3kNijqF2q8zTzQUkdiq5UYX4ZoFHJAjTyFjjmFOOlkwqPCsDg6prYjsAACAASURBVBGU4x3S4pY63FMWJUzSAsKb7suYV0MrqmiCqa65zKeANiHk98No6rFBL4pUQ+yBhOdtxdZAXmpEPS32kPDNIHEJKgRn1qZ5zO/r5SI+0Tx0rMY1D/B8+jmVOesUF1kWFSznimdX1Y8/xCub8Kd4PRS2Se0oIL9M3N3a86B8xf2CLEQVUaWXfYcWddDiNa5oZog4CZPHpDxo92Ee+rMmNQdtJGM6aqzPzwFavYn5BR2vMT4a/HaDGVeNzy9QEIOwCdPYW5qodoRoIUMa1IQlYrGhXpZ5IK00d0QxkYHhdBmSVmsKCShN4cRa0kyac/gRSN38dke8Am5htYaucbzyMmsElTCJgpt8vjtk5gclutm0i8+6lL+DVDi1gJJxUui5Q8pctZHjc1CStxq2ATCePHqs746oZf9JAfVEyH6yuR+Wk4nOsXS+D43IkLIM4w0yP/kBxKXFx4SRFMMLONZ+dldoMar3BkIGZ/J91SZU/X+Ar4+oMarw1lfcSIczVJNx/tOGFPuXprG28XNoXggw+M2QYi+QmStzQ4t2jlqYommSsInDJ/JQI76bS77/dK0Z9v21ZCjKfxOFeTz0mS+zkKUqGdQj/sEYq8XrlqgXsMzK7/aPdh3M4RLOL+jAJZqq5tByoBfMPFFjP9mEStq1hSHSgLDBQIKc1JPEizrBd/ZLfo7gdwl/11OneagESCd3uMmGahLqUPH8ASqXYrX0bzt6OMa1YXa6LAMDGG5rREh34mJTPxavS+F9/o9Q3O/IMHA/16m5HDaI2SqeC3kVHT4ERVXE7ZT+SWzIiYCJ83dqZzvE6/pXVhzTiD7GECbBCT7S9U0ZaCp9SuZtVmld5cNMMJcXOV4bfc51mMzrAefmgrbebOQx7Dau98wg/GfIHGbyHi9Q81xUx7mBn2CwOGRqwlKx9bNCzA/CxTmS0vOxEOJtI/sYmyFJ7H4rJX1szCOGBlTvkgSqFMYHSjIVw9RwkWO9koz7Bc0+4yVZJAl+P9byM9/WJGHVC8M00eDzydQ8dJ/cHm7mTVwnFw2CmYfP4zavb9N8ZpbIUSXfq9S6lA8R61L5Qu5KcGgzcnY+UduLEuN/nlpi1N4hYXhfY60tovDRKZ55Fs/4hGvb7KFTb2BsusVekMhSruPR0kBIw0BmUP38IP17MChs1iTEdhKzUzk8Uxpiv5yL+5gh3Raxpo15TztJmMdKf8frH+KfqNcmnkO+okmcqoTGDsv3u5Ta0xHNbLLbh+ioplkvqIHp9ZnmaEJJkhL3SXGa930vp7Wqnk0vJNgecP2gc8zg+HVwrnfJwOrOJyRakttCjv2ykOdQ9bfABNdL/zDqrXwOxSxuhAibRcFlMruvC0KbGo6BdFCqOCMDy7GrXr6vpXbpjiIxkKCFXJSJr/L+7iQ035wnI/9dk25f0vRUD4DpPQ/RIGbQDLYqQGI3pWMwvV8yutdtlplqUIHOuJWfze+D8MFfcFLTCiAQwMd2xZLmv5vn3qXdwzvSgufimVm3kml958OQhmnzrvwymwpEG6FxjpD0/ejLxkDa4whKWVfjjXUzliboo/T3J+wl0TwiyVP3izLxSc1zfoS7R7zmQkWue7RWvJ4MK0kcN4WYV7J6FmVeyoqBXKT2h9d9OZloBnMNxO1VMkO8TohKi+nkud6SOWAPwi93S8qJ25yPHyye8zcKfmcK/NyxBIpGK+fuR+i3k6nssXxeh2LMd5YMRDXbWiF2TWZ+58qj50zeQODMaGq5ECanUPt9xfdg0jpEbWkhtRqUfEGEXpImXDZxnwzEdlfBIncqbCfzj2xO/KoJiMwvUv5onbJjrQQnlWbBVKqWznWHBM8k7Co8PUnGu1kMUA9FftRg875BPJ+IYhit4lUrPkhCDZM3wrufkZlYKfRnAVmUcx9f4Pm6R+YROSWgaBqI3iM7CZ5mJLU4DSQ5OrlpEGxxyuJ8INTTL1t6qni5EfM0dTxJYqo579UazGZmDU0C93s+bD82wXoICwZYJvkE2kQBTIk9GcxJQ9GSomkgaZJt4LA7ErJoi4AuaT7coGnihcVzViS41MZDgwgojUTlyWzXhJUP4t9HwtRi9krtMjQzjN9UxSsjcl57Bc41ydxf5DNjzA9T87gXMqenCnTvnzM6L/wfOxtlguuhgSCR6Y3PYumgGps0nO957zHO5/02qtDYzEkdejakho2Uxmc7pcSaJFcLWGewqauWr0FlULA+zIZDcGQHRQX9RSYQVm5mBbXpbRrTQnjyoYDnqFDAQNSPM7nWHycppGRRfiSIVjkNJAJgC31mqPXAF0kXCz424P0HlITAPOCoeyq1u5NlAUjgH5tUC4H/Y6UM7NmSBlFKjY/kNW+IVwpGfDQUrIcN0r/D36gQJgUnaK1WyscNjafiwzwUVHjwtQIxj/3SvzJAs+GTZNfSdmyjDNJXGRKMoIYl78l9lSPtDV9bLBMYHcpkoGzxz+ow1rDZz5PiJUxlDZh2RpB5jrFsCvCb57nGe3DSLicx/IfaiDJR9WhMQ89XAqFfwvfh5P7N51rjtN/+LtF6bQdhWwHnTUnInU3KQFDKJKuaem8aZZCyYCCQNGeJZy5qMxbhG42zKy6v7ORpJux1hI2IxKefQiRBB/tA6OYQEvwLFs87RiPMikgjsXVYCBH/VmMMUQvwIWmuVrRV2mQzU6hYW4B5e8LXZ026bhWN6sjg3EcaZZCyYCB/UpvYTfW9i5sd0t5CmhV09VD1Bh/CjRRXC2mjZLlOBlb0jQrcm19BQQc7G/FFBufdF0Mz0XEn5trKg4jqgs9qXm9+nRmJqgg9sQHW4Foe3TF+o9pBZJEIidSCmwUYl04eiSt5Z8FAsEEfkpiPpkQI09FgCbcp3tIYShyu/4BMSS36JJhHSfmeONjGY8k28/ZBxucGEZ2e0fnVOp9lSKfXqK05TdkOhpIWxREwWyRbU1NHncaiS7yq4y0U7hPnptQrD6RTmyAbBAD27JkxpUsdrWRwD0LO7/JAki/YLP0+WcwNpH+E7o7LeGyUk346Jd4rbrlkiji5QBcpVI4r0bqNurYV7R1OBoIAppeSwMRcrzyQG3yIYZLeca5KhH9IcY5HGUuyzYw4zAOhk3B4P40hoc3U1oAtjJX8ImUuUPN1zCN7xEkk/SDJTeJFFubgKvgkXsveT2QeL5Pso3pnotsotgiiszRjbu40kPyBeUXZD5gnz4QwImizKLf+bQb3cF28AJBKDusKob8r3NQXAmdJn7KqVA0z/9Q6Pdt8sRTQ0ggdt8Y46a0hsSyGNptVvP5sEvn3GZz7rqZBK9NrPaJzYA9/J8nNv40KhPH+nuH5t1HwWVKHZ7MWDdkI1XifSz62aqeBNPcayGJNAch2n0gCPohmBUi+53IQjGDS+MLrfnRMpB9uUjidmPEaKDVdKYIGAvNTmho4Y91ab3ogWzptIc56AEmPcOyuMt7PSxO55qMFOfRB+WgdSqCBIPkQUQFJeqLnwcWdBuIB9lP4JorWKKhMc4Q2w5NoSkA7aNXz3qF4c+R8qwXXQAC0tlxNbeQlOf9HEqpHbi0XCojeUBUD6s1ELlNS/KVkYwizyGyOI9b8J8dACqmBONRAkcq5HyHTuEVtBPbHcVI7O9xtvHyhGgOByc+o87284L2UbQ08ISN+T+YBYrXXLa1C4UtO62BbmQepaP1AVHQAQnthz0brS2RJBlWwRamU391azxW3OD8wN9bbbr6ODE0xk5UlGcPJ0peodpXPgFDlZ25pFQqqH8juDK8B2rXcMZDscI+S7siAz6dL+RynDnahamKBmR0t0X2rEinT+Qym4xyJlPfd9NYNo/kK03pPRtdArkmpg4CKzkCQxPUuRDrDJmsmE9YMt6//V+WvcvO90sblQwmfZaSmSS831v10SRZU4mBnn6nuqBBQYVrPotVE6ee36ImEN9xa7ocx0rwROyhv8oYbG+Gveo7EHR4wZ6GF6oKCPwsy61eKZ34bRil3gvQVVpzKtT+/AefRWhZ0hsBagn8CtbCuJaBDndyrbxtdCBgsDmUCHK7Dm/TZEbmE0iIXNebRyc3dReayS6K1uq0n9NBNPM96atinfAjrhQaaP8zVpBJpiq8TCrHdFARgOfnS6JvyK3EoEy5I83U01IHQ132GhrqcG1XPGF5b0Ps/zFe9nPZg8Zpt4VnONujcQctC/adjJdJ4gbi9MuDTQE+kE2SWmGu0P17YiJNa9lImeSXiuETC4mMpibHqvV4p6HrdQ40jKiG9SWJ0xk1xrtgofaHVMyVetGG39Devwk97q1FpS5k1EOdQdtAxlJt1tLYxw7DXslSIa/8rtcMyYRt/EuF8Ksz3mWMedcEXarhxQ9XN+mW1km3flXmQysxAlGq5v/c46NZ70wMmB1Q2HRdBooM9HkUMz1m69l5qCui+eDzgO/v5inu8R41JYTeZhf4eumTOkYF1shzygWq2lDWeS/26EzY1A1ElvM9IMfoLO+QDEP+7MjDB61ZEswByK6I6cqMKJhu1NRnU42GDdm+IzlEFRFWS7BxJV1TUwS5gDp2Uw3UQibe+URiI7nwsegih6heBWlkuXt4OVNmY7oLe31lK8mcMQr2Sx02pbboCIUcuyfYIG/eNeDknYVDMqk1q124DkxkhXm9qVFrYIs4kWzQMokaZBwMZU9ZB0p3oYB6Ie0Z9ntHi9Vi4WlDJ6C9uPudEtwdlFlR9kmHPhZ8Adtqi5eSoEuQQdJBQeI/3epbvz6zx+7/5nJWIc1/LGRp1HSmGg/12iP9vo1a0z9HtwmA/Banvc7jWWwoVpWYgwg3YRgbymQ+Fh1tSwHv/g8xummMg1pnICM7/JEpIZdLwMFfTJVqr5LznFddDVjPqX42Svkx01ENy5XiKyUDmST6NykpLX8xEwikkHiAaw/l6scD3fsytc+vQTTC3Cn6vu0mQ7xr3ei/i72dF+A6c8za70r1xDKMUQFTfIDcM8RgIQgaRgXmgBPc+QbyKmQ4eYFuHyamRy52gaCJCYbcY71+NeZ5aDLKd66zHkhZWkeJnyjv0AYmPX9wwxGMgZZPo37gp7Af4BcZL4zfhUqGtehvbLo152sJdvl60bGIAo4OfZo9bsoUFhNMhbhjCUfZSJtfcFA7AM2meYovQQjr59zi+2nJGQlO4QMaBENvVls5bIaPzYx5giL+6JVwIDBXXEz22BuJQbtxpsueFzw6RVIgQQz+NwxbPXclIUAnLfoc2haiy02SIR6lRIphhgVveuQLBQ+/dMDgG4tCYWK4xjK0ZXme1DGz2lAYwM+pmNrO8+Q7pC2Bx2nV98VJKXmYkD5TZhOUcXI2JKqX0tfz7ee9xUrzMc5RAh2+ig1qCOk5ldC+Hxa7jGwwJJkaEyyPPYKT0TyJ84JhHYYTrlhLdb10Sv8vMQJx62ZhAfapZFBAQJQWHM6oOqIgrlHRHnscSjakgEe+zRvRtw3aM/gkyCiRqwlF7x017IWEjjDevCgMw5S6uB5ctK4a79d2QOEEtA0S7lukITKWLBFjfqAi/vWfhXlTYrZ41nhRITEPpFITJK5MVamghj2Vz7zFZ+pIKFTMZRgLmtJH6YIgl+tgiXtWELPFW6hA15nwgDkVBldrHCRJSENwNNX6DyreIOkPEzATtfZi4ZnLTomLBDynv7VPC3yF/5Gcequ4WMtCXUwBSpUtg1kIggCumWBzYiub7nGL9xEFd1o5jIA5FAaR9lDOHb+BH8br2hWG09O+/8U688junqdan7aUBJpY0P+qSeAmIFY1RmpnoR9z0F1IDsYFbDb1pS9yREBsRdbAe5HQt15GwGFBZ4e1kENBadkpfJFalJOvWvM9tZHpvxF6PEod0QGVntKf9vk5rohTI0omODd4hXolwEzaiBlrcOm8qqDLzqLiL7HA42xdLtmG8WREMaFqH+UwI3UV5+pduigsDmJ7Gu2EIR1YmLDCH5xLsyGyltIXXNGU3nCO9ebCaxBYZ3IuMz2CuKpsZ6IGhPYNgRa0i7JA9QJ8+uWGoDwN5HoExQHtIE5kA2+JoN4VNgyMBTEJpuGtK9jzQPk5pTGRFyHcRxYMgAVd9Ol84C0cNZGXCqsU8Blvg7rB/d7opbHpML6FkC3v3MInmv0M0Gkx0k9xUNyTzWF3mQapXFNYDC8QfDMglEzYnQFDhQ0D4LsyYZXI8qwrS8N2oRm3KlOuXv7LBTXfdkIcJq0VKXFW8nmG8aVukXslJKlvo9lHhsEv7e1vJNFG1ZlWSIl5Hknk4k2xzMQ8A5skXZR2kMpcy+TmnSXZhlcUGckfKZMZ67fPeMGoeKkMdSYcb3dTWFagQ8HtOAsVBp4HUB2ULs0NY8y23N1MD5h/kTYwp4Rowu2i2GkLKbkqleLaXToCpG36T/tUNssIwKbF/q+wMpLWEanEPpZsbbo8mxhnDBFAmjDG0W9y/HnSC2lfjKP065lE/wDcxNIfroLRNaRvAlTkTHcgrg9PGdUAohlDieCaN33bWNlD36nHv8ad4RQY/5LTJs1xL6v8ucYUTi4TL0teJcnDO66FU+Mqtk8y1nFYShxZqIC8c80gE5El8IQMGoV0s5e9ZrdbWasc8Cgcwjs9uGGoPkkMw2iyplx9J7D5L8/QrzwIqkRDl1RshL6LFeC6H4uCluNIyTgNJAURGTLZwHmgbH8hEXBdFO0BvDlUX62mJn0PP+YBv7F/pKwPUxf8Xu6l2cAykfIC/AqYSm/HZLWQkDnagnNETU5wDRRlhg94cMDfbtb+rPI5n8Cwoa4IKw99IX3LsO/5/xk1zXdfXUDcMxWAgXRmd901GUhpqdKGNqq1IqUckDM73kRyQzJeTqD+0dE7VshRr6AD/biejgLlxm8Y84OicJ17NKp3hJE02Ve139XWGv52Zs/74LI3tA9lrCEh1ZSCqEZC+oRZSkm+T7OrKoKPbZClHKKcjCumAvA9Er6HsOZzPc/l+miz0BdKXl4M1pErC3yOzQKUDlFm/qn1fNYdaTulUaSVHe49/Elx/pnHeIGzmdQ6S2bkkw+zxZw7XQPBEvbpQtnHvpAoSsuFER3LcR6p8qtkPsm2HaFLepYwGAaW9EW63xa33hsctTUN4SwIPdKfUFMEgZvkwq+HUOKo+vzmhaSV4PUIin0TTVZrIMx6P+d5Hal3ozghn7iK+d8UthVyQR5WL1VK/YoovKTilsooMtrix9Th2vUx7e8YD0e3WelMAkvdp/l3RXkF816U4r19BTtUPG8IJTFam32MGr/1fzHu4LwP9ahWNgczWNPgfeQBnKC1eN57fITu0SPYVeSdL/fq/YE2ljmS06QO5VkdO7tD4OJMR8YT56XDAZzCTvQnRHFo0DeVQRLPB2IDP3hga0c/aZ/DFrNc0EweHtIAmu6dIDCQII6W/f8TBIQlAqLPyI63m+RGV9VfvcV76WuYKpTQwrYc+96MQ1Y79IECgqlDD2k5NXv8O/ItPeB/w/7jIoPzg8kBqII9EQpdh65AGkLxVUbtpAd8Bkf1CIgviC3/cbxReQASOhWgfOlQ0lSrQ+A81HzCLF+LvDxFeKwhweG8iQwoTpB5R08D9DvJhThfcUsgVg8TlbRVCA8lDFdvuprJhcYAaQpjpqo0b/qb0RU6BMXwkUX4X8rtVPK95LOHrt9LX0Al/j9M+F+P7+0Kugc/Q5wMtd2dRm/DDVE1LySroZLW45MQ4yNIHYhbRLCXKXkwRaCcTGZGx+cQ5LusDhNfuDBn/LOZGj7Cq5LiWlKYzTuyV0VFAuCYc/WedVSAS9pPI/5TR+Z9yPkpdlfsrw1SwtITPgCiG4W69NwSgSSIcVk883Vkn5h0UH/+bDDR9WRPopM/JDiI/StMagPMpzovxRGXZZY55REZbxkLpBGmAlg66D2QYDweHvAFJ7w4lshGGRD4z53v5S7snE//RrPFjivOfqPE5NBD4YpD3AXOTKrS4QLze6XExnoxJ/R5ZyBfFCyFVDPuNuGoJCqp6tkMEDWS+lK8xj0PjYCM1j1U+n93J+V7gO9Gd7isNopIWaBTVEfL5OOlzpFdJ9KvSP+O9ndaCs8bvbvLwwyc+1ypqdBPE84XAcQ8n/w4eB91y/D9m6hBRA7lAlfn3kj4HNgdKfB9yU1pK7PNhFNU6SMOmfwKSuu70hhlIlTZJ2p4Y4cC1fHbf8V52SZ8D/ikJGrSTBxT2Bhm/6ZDgpDTFEHs0BqW+O5yM8TMZyyu3HP8XWUdgvW6EQWoEJ7qQeRyU7GzlzoluHyCCI0n4HvHvUSTSLZS+a415KwlyxdIci/h3C/RbCzNSaEdR11OVhOYC1/g0MhA/5gWn74aE99NBgnnHLct+wgNMez9kcO4/qPWV3h/VKA2lDjnVu3RQxAqlRHRnIojgSYkW0LHN8j2ZIb8zfb6jMuLh1P424XV+jvFdMFWYplDAcSE1BfyPmlk/GeOWFLfcchyA9xmee5I0SDCD6wfiUA8g2kpVrwXzaNfeP03mEaW21BjLGuZbHyan11pDSLHyHaQpKbIzqoWAr8gLGUomAW0NJin0QelxSykztIgrG9N0DMSVTCkHYKaCyeoiJetuah3wC1zRtMo8NGg9XHeV9M82x9+Xtf+niJcfMi7h9ZRT/mKM3+w3/sd9wqEO89Zut5wygYvAsrgBkzoM8wRKPtwX56soA6b6EEiYZO5SI3mZ4ybXfSi3NMZhaigS8FkcQINR0T0Ime+U2rkAyF6/Kf1NVKvJgB+I6zOTFeCDG5/BeS+Kf7RhQ2sgUyRl45EcsMyt+dICxBElS2CeGSRed8BagBT+LsV1Ed1k5mWYZU3O8PUaTRpzqR09j3mtHjLOJxpjiJJIdstHE0FuyBK3bDIFTIZDMjgv1sGxZmMgItlmZTo0H44aGq6uVeyLeA5oKmmqECBsdUXI5zA3qc50c0hUYGJbJ8Fl2YNwSfon7yVBkszlhW6pJYIKb3awwED2SXnS7re5aS0FYHqBCQcOdITEwjmNPuMjY2qdSVuCViNordsSaBphSHqvYDpbxYvcieLrQ3LmXrHQtrRJ8UVcNV6rGkgZgBak6920FhabKdUjCukEhRIQx1+kz1QEk0EcH9ZCSdazoRqRoF+Q8N7YO3MatwvateD/mBLhN084nvitK0+STAMZZPmc6Cg52zGQ4uKSuMKKRYbqzdHJ/9EJsCPne1BhuFEYFcKEw0xVW3O656d87aH20RnhN9BW1ogrnpgUnyS49H5SRAmacAzEwSEAKglPRWHBn3CLmkk1gTaRpG/G6RhaDmrEnQv4rKJpBFlDMQG0IEX01mS3lDIHEgkHu2FoPgbyOEfJ0MEeYQS+i/l7mCzj1G7Cd9dZvP+fJbifehaYQOaxxS2dXBjIZ4vnW9lo2sf/SlENUgvLhO3aVa4WVjbooRaB8X3We3yf4BzIaP824hzOi6m1RJn3JGsjyW+Qpb/NrUMrWBiiWSocl77gju8dDWkuDcShPLgkXjmOpBt1ZMTNe0GyaRVrZq/XQhu15Lj4ha9X3bJJDZgBa0WmIefHhfE2KQN5LK5PepmYSBqEhVrOJ3FHouKCjO7/mKYhRAGk2ikJrwUJtsstmVRA0AYc5LUi0z6LvTBe+PjeNeJg+jmJyh4pAAnvJxKOX9x+KRQ2UmNA35m33MijU54zqJwJnOWIuFoUwVzhh79imBxm9h63I663QbynNEA58FN89gNuWcXCLQtrKy52S4OaHnUfSDdVtkF8PVXyZ7Npc6y3/RILEG1U59Th2p1cE1mEg8IWjbIcqEc12/LcvNKYU5JWsHHnvEriNKvG9+B0nyTJW/Vuo7ZTMSTcPY43WMVJCqMTG4B+ZIavNKn9Azku1LaXDfBsKFq3v0HmCSYP9IVYWodrj5R42eFxAM1Ar8Bri9nfNzSbPBLpKjSPnKzxvWEpta4dfO2hYNHtmEcmGGNJA4EZtWELXioGggccyr8vSGM0mEFkTiNkpS8lA/lCYpF34p0SKmwSeCTG3SWhx/9JWxGf9dmsyHCflvIeLyf83ZwITB73F6f52fyA9yHkwdc3XhyygK0Q3vMW1mNhoftArrg1U0hAQn+vaQFjcr4+BApbtZTgA1lDovdc+np8JyXWyiywkH9D43xmabN2J/zdNR5hJguUZp8X45wrOQcmHokrUZIlIDQNcsMQnYE0IiDZXpX6+A5sAU5SmBeRvY3aRq/rcA82CBWih/ZpxP8FCX5c7CZTrfis5SJIenP4fG/Fv4I1xiBO5NlsjSGpvBlYCC6SEaEYJZpy/S7OoW4T8AMPTXkO+LvuNfIgNWoioZ+kWu9zNBM6SMxgrnnCzXjFwtiqCrqnjPfE4vzAvDbBwjlxX34RYEkK6l3WtKKKps1NpIbi1qZ9YJ6mp2QiDU83ip4HstKt41ICEjKixuD430vmcZFET/ktfpX4/pyK+EcH2myuNMGWcCYDfTRAZ4JzzTX+h6P+ATXSc265ZQKYRF1b2xoosgkLEsAUmgHSRJlMcxpEXQDTCswqz0g0YUpUSXcIRT0k6fMh9GudsXAe5eu5I30JfzaYCNYezI82zIBgxCjdMpKaGMwjCEQ4zb+PuGVnDQhSeJtS+2j4LqlpTVjdlDJBGBAtcsHivT3khobNd17Kc6VlII4BxUeU9WDD/GTThFX1YQBi6byzqJmlXUtHqZk/JiNBSDBMhavckrOKo9SQv3c0w64GguxexLIjzE05p5EYNZFq3x1L93aBzOmihXOdoNrv+qbnh6jChA3mYRu2I3CgQd+0dK5VZCCotnCXknI338M+RHCCc6anR5p+6GlbF5cGSXwgY7lglYo/jMzjqkXmoTYdynvbyIhH3+ulbk/UHXv5+pt4kVhFgWJGqJllO6R9i3gFFG0mlSG8exqZ9XRJ3yPewcMwSZ7/1MP5aHgk0UB2Gf+vpSbyZ8Gf9ZLbE3VDOyWyTdLn21INkcalOOd/fH1N/1b9lgAAHehJREFUTdUWuijB91geA9TJQjRVm4Vz4ZnR80a1uV3nlph1jEiohW5spkGyEYV1iJpH0Usfz8vQ5GEDMxp4nU3ixoKzFw71Y5I+n6WFDMl2GQ9oq1lk+w8L+WxzzHNdJfNoCjNJnfA+hZY9txkZSHeK8+yRcmSyvy7ofUEq/VzytbRW+xsO9IdkFq0knoiog/8Mmeiw46epBwXt43dqMEpwOWjpOaAhqYip3RbH54P2tynIxLW3r/B5b6ExBw7pgOjBuBYaFcXXNFU9FAOBxDWyTvewPMdrgWj9UdC5+FKidQNTDPwY6NqGbNttZBaKgF2gUIG2AEjEeknmAdgINW3heWC6gXP6owXiqcxAKsnvYw3N4HbM81+U/m0SdOaUVJM4r0m9yDlpCrt7gbUQCE0bmmmAVBjvQqlPCffV0ufcRnjjzzldM68WpA4e7lPL0scQJq19CecPjuhp4pVpX0sNJO0cdZJojKEWtTDgnN0JpEzc92NqTiqgQ517PY9xKdYlGPQnsRtK38w4SK15uqMTtTWQcxaYB6TQ9hjfh7MSjso3JASdOT0zJIRf3f7IFYp5tKaQ7oC7PI9iPMrUdMjCPSofzQMS4Tc1vpsECL31q54Lp/3YJAKgeOawM2Rsq91yswKYXeM40avNyLxtZqJDapsaQx2/xs30jK95dUHEZt3v9kcmmE8ihjlVfSueap8rgg8z4g8JpG3Vp+aCpgm8EjsBHPCPjdS0iyCB5lcygjg4rP2tJNrjhsS6S/onHEbFGvGSNl2ekz0gsm9EzN8saLZBslULq43cOm4C0yEykkM5P/cCmlUc7AJE7CKJ8FMSxAk+av2kBMwD5/jOeP8KmdI97XtJccbQjIKkybjMaj+1AnMM4AiHyUn5AH/mPcRNOIQvCL6Qk2Rup90ytALM8+cY6/NQMw6SLQbyQOzUIsqT0E1xeyQTXKIm6tcK9HiC89ViCpC+EQL9xqLpQmckJuJqTmFO1ZnGmCyhBoJ6V8+N79YyTbXUYHwO8fBF4hVTbMpcHJvVeMvWxRDJj1fdPskEG8Vr8qQk778kmeNZJNwxCYKJPKQtlhmIX6+SxQnP+SlE8PLbR9DKTZ9ImMDzjPf9TlzCrC3E0T72NesgfdXECwQbtcPtk0ygSpZ8q703XiNucSJVdkX4DoIxTvDvtP6tM4ZE7yflx2WCx2p8x1yHpi8Dz3SyBhMFA7nplp41xMkD2eQYSHMCWojzhdhFVwIm4QfleIZPpVZLXcWY4GRfb+EZUInVL68kqdkTmkZQTsm5AMKvOhF28ZnCglNw7vaIzNYhGqLkZWF+TjXzIDU7A4EW0ub2ihXAF4FktqsBzCNOhArMBzd4nji9NO5pTCcpIO0P4rr4vYamEIXAKK0mqOSKKkBqhsCr548S3q7GGwme58lwt7klmQrQNsMKU7YGaIuOgTQZsPn+ccOQCrtJuBaGaB5Rnbv/UiK/RC0EvgCYqKL4H0D44bSelOJZ3oTcc5ISFbWaZiGKCiHEdwM+38Ax/TvkHIqxdZNRg/jtcMsyFQbV0EKQdf5Lsw+SYyD9JVeHeNgufVnVmw1JOA7+MJgHiDTMN6pYIJzj4yRalB+0oAMhxDgMShNVDmnxIcJbJL6P5QUZYVg7gdERNKfvNK2mKv2j00a79WwdYB6PAz47H7A+mk/6TtmRUEFVkkW0yYOSjgWihL4PMUW4Uib9sZoEu0NT5aPYg0Go0fwI1ZFhqvrWZ4zhhI/rmNzI3yWdp+fUBu6SAAfNeZy1UCVDBIGfGvAdaFfIBRnKscQ9rAn47lJjjPV7aaVU7NapHcAPhmTCuY4eZK+BqDBFP+bRmsF9d2Rw3hMSv6x2MwOEbpYmiUV1JmKNIIluBJnHP9qGBEM6LsmiWtKGUsJUtkeT3j+GfPdDhPMp3wXMSk9CvjeC13yiMeYgfAwgZsAj4/928aLhHJLRNL+K0f+5obGvgYShldKVrW6FkGBRNsVm+9xakoWTOIJVeZT/mJnw9ysp6VV4rgUZzV+S3wad618S61kRzgmG2EJi1ELGc8lnf2AMkfsBkyCc39NCNPmwZ1TMYwP3xxm3RBMDggySYac7WhCMwTldZ7xFYp+liayS0HzSLFhNiRpzuZaMPM1mAvNQCXtFqiOkQpHvk5jrGBaRebRqTDEsgECPMPuFUu99Eq57AWsU0W6fuX8XGZ9VqUkPcwwkFaDtTfFhHi5UWgNMWIspCWaFRxKvJEC9Md4tC1+gxtJhbqqtFpgHNiNMX98bEjtMPwfJrMJCUU2n9PqETKjL5z34JBAZ5VfbLWoVYdS2WifRos/WGlqZ1GBSYBooewKz61ufz1WL36du2abCM0N4UvPqoCSW/3fxf9ZTtT7mhiO2OcONT33OAb+JaoD2mgLK2ITn8yuXclq8sOG0TBL5HLNrfA8aA6LO4Fe6KsG5NHGf6R21FQQ4zJDo+TQOfebE6RojdzQgQAN57pjHAMwR1x7UDwe5kdJ2Xatqkn6SAovfcjPjgMlnXIp7QXtds0UspPvfLYzXHWpUtVrj7iGhgsZyzRijJFABDYgAQ6Y7St4/FFepNw508z5MrS/dkPhrIG4UakvIcaQPqLpIQmqU8s7Ie0DGPsqy77UglUMSvp2BNJdUQrzIQxFdPONnSZfbonCd6wAO9DhVcrGGDqe8NpjGKOM9MH5kV//itnckYWmCeCVlnPYRoIE4BDDXlFJgI6CVRAeS7BMLBFXE6yU+w+J9Lk7x2x7pH4L8jFrAO0nXY3w+X7uphcTpYmijb7wegqrmbpIky6ZvRkAInOiYR3Q1zWEg4Kx8G/M3cRrRFB26zRx2eZt1f0BgbUTmQVPoSvjbf33eG0NCC0k9TUb32RT7a0ZKrcoUgibxWVa5LR0ZyEQfK+nNtU4DaWKck/CCan5A/P3rBnl++IG2aUz0FCXqNOcD4Fi21YBnD+cpLlBCBaGuL/j/URLbrWKnRa7eTztucUcwVluh5IoBjeLz/cZnPei2d6T5O+CGwjGQNIgb9/25gZ4d9vsOMlFFiNKYQA7yPOcy2OxBhe96At5HZ8HfKWVCG4KTFM50mK/ep7wf+I30zPhnMX+PopTKLHfS0hiNJzG8yOcbRi0JvhbnXB8I+KFcHo1jIKmh4r6XR/z+UJpBlpf4mXWfwky+Vim5ptU+9lLKt4HlZBDY7EHdJcPyKSaTocHBjZwU5FU8IZOMazq6rv29nhqEKq3+JIHm+xP/XmpRC0FyHBzor6gFwkSLultL3Dbvh82apuwQtrBcFFYkInXc2IhhkuM46avi2SLldljupZS6ks8Be/6cFOe7TeleZVB/FjutQP+W2kmNfr6EsHa5lyM+L7QD5RfaqD2P3gcE5qi4YfJt1BSwjrrEnhNXjcNVnveEDAxhdugbpyfUUh2cBpIKJzRCUysqa7wmuZQ92gUEUTldUZF0bMrzwTHcQaa0h8TWRtOjLdqmV8c/ZFjqb/U5CP5DbR7nBZyz25A+VY93SO4HSYAfUjvA+8859//y/2tcLwh/fiHxCn8q8xV8FqpT4XZLc3qB9zeWmpljHsFMdqQbCqeB2F5UW0koVtSQHsta0h73Drs4KhNMMkwgIIKPLIxhlvMT9Tth2kcPpf8o9wqz1WvpH532H7UXaK5/WlgL1Yjab5KxgqkG/qNdFua3Ufa56oB5nZrjBXFwGoglYKP9KOF26Qclfr4HZB6IJFunEa69KYkLfBSXMrjfVknXvtbEYYkXHTZbBuagtJAwp2Uef5CZ28YjEsq11ESeUMNqduZxUBsfYKikizh0DMTBF1PFXmRMUQACr/pXwO4LR6ueSZ+2GOZhEqpOy/f9iBLinxG+uyjCd+BQjtv3XH8mFSiwT2MecQuVtlLTxXjNF/uFSFVjK2hJL6hpmr4oCEg7m2xfrzW0PFVfzSEELpEwGSrSOBmq+0nsYPOHCQu+CjPsNE0FUkWQP0s2US2nJbiDn45zPnOoY6FGXF/EuP4t7W+EyZ4hw4RpC36SEQmY4kGe5yXnAxWQeyxqcSc47y8NLelX6cvAn9Vk+9lvL2O9PnekrgYhbDIfCFTSK5YWmDQAE1moEVZIYHModW2hZL3O0uZUhHZWTps/zW/SNqW6xnFEyLOtzG/4VVosrzXc6ylqG2Bae3mNU9JcCJrvy2Smy8QhEM1kwoIk/MbyOe9Jtr1UsoZeYfQQCd8PZLI2qhH/p0nmtpkHzDxnCzimGMOdFpnHQcnGP3GLzANreBAFiWZjHohy2xPw2WCxU5HAaSANAhD6pGXrw6RSqLqLxX52dV54ToYBIvIjmconEpc0Ei/MYeish1wGmGAQMmvbkZ40QiloPp9L8r4i5nk3hxCnvDStqOOn9gVCh+c2ET04GjKmCNUeIsnbNTsNJCU6C/Sc0D6yqk81uKCScC2m8ZkaguqdDT/CdDKT3yxc4z5f92TAPMDcjmc0LmmB7PP5lpiHcmQ/NAi+beB+LzYR85AazEMoRA1zLKJ+DAQSWHtG545bCnyEZJvYN13KVfp9HBnf19LnOH6gMVowFtjD01TK/ZuazCpqZjaZx1rpn+W/KME5VnG+jkt/Ux2iub6kvL93lFx1STcusG9+pRaHVxSzVFFxby2O5SpN2MN9728SuhdVm/siDnVjIAhHHJ3RuYdJvOzetxmPI+zIy6T8/UNgF1cJhElVd5TIQGmR7ySbTpeHuK6m8P8kpkN1Xys0wryNxH5vinsDUxtFAQcBCk8p6a7l68MY6+knng/M/QnXPOprobDlXUtjqcYBOQ+oC9YMpcvjmAI/N+Dz2+zDk1kYL0wM7zMm3HEci7dymBg4IGdJOSOz7lPaAsFLUwTyLAnntIzvd4d4DZtsnhMlQ7akOAfm/w01PGzUiSnv6YDPnkIy61bLz35WmqNXSFWil2fHWE9osOdvpaAwiuv0k6TreZMZA0Ec/S8ZEu6iSgbLOEnwLXxd0HtsIzEaQekWGwUd8Fo07eMXzZRyL8bm1Ild1hn5aX1sYPJJw7qDgIAB1FC6SU3hJ4vnhhaCMjrPE0jStZjUeml8e/8HCp0bSk5j0gBrE75ga+VZyhqF1ZGTViEJN+srTtK6go5fK6XlyWQkc3yeNe4YKwYCCfnnjO9/t9jpWW7Oa1qivE28wocvyEhsFCxEqRH4Z5Cb8Ixry8bz688NX9LLtBJpQXGVa/27GL+ByRHRlUPFIXcNJGsUMT5bScTIth7NTYnQ2DUFvNdH4pkAe8RLevtP+05c5vGJUvLdnO4fRNSmGcuGxKnMYCDCMN+esHRv+zRm8VRjHjY1kbNk/jN4gDYgB+WSlBuqdH0lwXoY4lhEOMqaSPipgPcEe2m7YSJBjamlBbi329JX8uM+pWS9SNwl8ezfSbKd1fN9TaJ+LQUD3hjwWZfxekHsOAN1Av+bxfFGVN7EjKT5iZwjdSi/W1WSRz2qOVfMYzbPqzOP5VxHZcJRSd5PZbD0T7R1aCAGcquA9wSm9t5nY54sABOZKX1O8nvUElpIEGzk6qjCkv+kJOqwUQfVjRpJzUb5mNR7L1Le+wrJJtR8Ocf4L8muout6jrlejTgtw7pJ5iHUck6SsV6nNo35bSsJjcD9r0ypnb1zLKIxGUgRgZDIOwHS3Umpf4vbE+JFlrSQAI+SeOHQQdqH2mxHUpzrXojEd4pSPez0qs6UkKilQZt4JrdHlsd6XO/xvWSXfwTn9x4SfBsmrCfUTqHJqJ4wyzjWf3J+cZ0ytCsAc92dclxcEmFENc3BHh6FmAiq3JT1KnlyR4KTA3WndFzt4wkZx2CJZi/fzPvwI0RRzEg7+DrJgvbwwNCAyoZ9hgCQpnzKD1yjy6gJqvyYQyUbE5iN91tgqi1STFO500AaFDAHdYV8XhEvTyJvKGfzYhnYAAlIkvtwWdMOhkr0+PoxIdJdmAkGzAL5D0jKOy/2TE/qmmVNokOZmB5NEKiFWomSKllRx/GSjAXWx2FLGtlnacxQXqeBFBSQiJ+SWF+ooYmAgB7L6b4QSfOckuoZXr81gGDG2XjdCTfqmYRmkHs8wIDfS7Qe9VHQrpk9yoTNXG8ImYYpDmazKGbSySGfveTnP5IZIdkMpW4WlWQ8dlpgHu3iEBmuJ3o01AqVBDGdIAM7u4WdT/WNyHpTbRbPOX2SxAb3+pGMBQQdETcdMTYf7h/hyjuo5j8q6LxEwb+9xzfa+TbE0Kayuqc019YFAf3ZdMApPjvkHCuodUwn04ZZ6EiB9yeY/37L4469gsrMMx35C4YzYdkBEgfjFB/EQoe562bG97VH+kc2wb49kRIlzE6we+8Sr1dHFBOIIlKzSVwgrW6U/Fqgnta0Kht4Lf3NimkLCr4hk74u+ffUNpsfgXn85/O9Wg7iDxQQlHnviMZ4kFexvUB773wGzEOo5b53pM0xkDzwKIEUrrK9syrACGZwV9vserhnkCO/VsvZLu3ecb6VNJ3sk+yzzxWWSF+G/zgSuDTEDGM/UhsPG0QIjFnVFpuf8zo8JZ6ZUuFrMl0d92oQTmitMDMuN7TZ2XwfY3ZWwn1+eQBhzPMy0viGiIvEcgyk4KgYUr1NgIAhGxq+GThOR3HT79Qktz94qAisWvk1kD4PUcJGeOqxnMdrKYnGQk3D2pbynGCEiwO0rCRQkTtt1Ajy7li5hK+/Ge/pFQI2SXDUHcyqU6iltvN7VQokCJyA2RLVFeAvgRm2tU57p0rtOis/7lBxPuLaBMz5QCIv1izt2qdJxOplOwdhPlnj+g/Fc76/JHOqR0JnB4nzMElfDyqs1/0cSZZV/x+l+G+197aJF36c55o9JP3rse2MqCkqBrqGWgbG4UjB9iM0/qkZXuMiha5p4uA0kIIDEuIFboz5dbj+HKnt0G8lsT3Ae61XNQAwDhQU3ML7WULJOG6J8yDNYC21iKsJ708lacKx+xcZbT2k9Aqf5ZX23s8x1qOQacwtIPM4kTHzAIaIayjlGEiJsICb/rz075JnA4spBW8lYfubGxGEFyashTWk7YPa5n0u6ZoupQWSFXUfDmz+cFbHLcsS5CCdr0ntaUrQwLE7ngwE97e7DmNVoRQdNzT1DF9/LaAlAD6PFTlcC5n3g8QhFM7GVzxUNE1kpqVznjH+PxBgspAQqVw39cQhrMrRmsQchPDRySTEr/kcIMQ7yEj04otx63CBCcEn1EYi28ZrwPat+qLArPcjCXAcUwbuDz1Vlou9irxJoBj/XWpt38fUik8XZE+oSgl5mnghKI1x5KgGsXI+kMiST97+ic+UgOJeF6aZWs5tSOs3tGerlZNSJUFMascHod9XsDlqF8+xDJ8OzHL3yDyeUBM0GXuS+9hMLeRYndbubs73FD7ndzHHFIzzAQWayeI1Gyv6PkiLvRRKpoqD00BKOjfbEhBGqN6LKXHCFu9XzO8GiboyRYUxj4ua1pGUgbzOeKx6EvxGhbLCL7ArgkYYl2E+IWPeU+d1tEW8UjXVmOupon0fxHR4HQS3j1Kfpk6f6/C8pYPzgRQbO0jcq+Jfw8oPkKRVuZCwSrBPIkjWPRpxBmNKEvcPM86rjMdJFXFcm+B3OwPu+YGmpcWtqLtPkvdFyQKoqIvw58caYY5speD34RdaktP9LuY1F0j9OgJCgHNOdMdASo9r3MSnY2z8bVLbqRwlykjvhzA1BVH8mMM4vU+gIb0JeP8EmYcaw7InlKFhGMKKfxLPH9bB1yiFEnUtrOpzrDa+32F896n2915+PygK7g+u9YpY7N2dEM6J7hhIw0BPOgwrew5n8Aeq4Iiy0iNplnKDVn0YhB/upLxn+Bneit0eEqYmpsJ35yUwOayK+L1GKuu9hJL9TUN7i4KqNm5675a1GtMQnlsXdiZofyMKEGHBCORAEMNJ4/yTpH75UCbzcCZ+ywyk1Q1Z3ZkIMoThzPzL5/OFlJZfUmN4TKlTAaUuxmnnGhFDC0qCe2K3p3Ynn6+NzwoGqfwXNvNSusiQGhUXNIJ9RYLLlqvINhRlnKW9D5OYHqE0STx/HY5n2hqrGAxhEL8zhHO4lAKPMllVCjJGWGctjuTYZSBD3ZDVHee4ycZrGxaEVNUtukHJaY+xqU+TUAyJsUlVlNLBgjz7DUqvDzgOcwM0sLSYI/39HjcacB1VNC1xUIgGirXzDZl3JeTYpP2NcOE1PppL0LpTa/JCgcbHaR8ZMJAyNFjZ3CRzV9FMMEhUG6sRz08+m/YKN0XcUNc0GkieAIH7U+LlLvQEaNnthrb9RMrTCzzuGrob8JlKfFRJe7WajqliospXd9gQeuCf8ktAvVIgrcNkah/EwSoDKXpUQk+TqZ3HtM0HbUM1RTprfG8LN3GcMilV7RplALSEidTMosLPvDZa+sx+er7DNRKUOGOHtQi/wNoCjpXJZJ+FaB9xEyH98iZucn1uNK5VCdAii4CPTguxz0CKTpwRifO2CecRG/GIRrwGadLdc/FyEc7HPO8Lie5orjd2S/9IoaTAmMEu30VNTmkpU2KcA3MBP9Qtaof7CzZWcKTD5LmYjGK8DCx3klTrnCgD/R5H+bqO15pdUK1DxydxPhDrDORDCSb9dZPO5RqfTalMW4qo6p9HySspk+0fTk8ECbyxcK7x1EQghapEyjiZ9NBslEnnnMTPI8lLW4fzeyb/9/Nv2tAOFDMHQ93LNViGddUijRV9VwgGUnSVDlE/F5p8TisB0h3e+40bGsUU9fpYQfZ9aB+dJXnuNSTUyHdAH467MX6718d8AUZ0MuG9gECqPiUnpH6Vi/3QSu0DGsbP4vk6EChx2EcbS8o0qoYmiBIqX5doH01wGoh9BuJQLkbypyEF/sj3vzM2931K2m3G77PUQnosngu5ILfFs7PjueNUoDW/C5MffB4bUhBQOI0XFmQtIGnvOIWBwWRqr3h/WzSCucaCtlH10cYqJdw/ECJcImEtIpNjMUVIOOtKOk7Vkm4C04wgxnOo58IrnJ8PabbI2uQC5/IwsZsjknTekJHfFfK9uM2l8H3k6pwr0PyDWR+gMAAz9GgSR4w//IZoCzzFwhqv+ggxZcVpzvsIcai7BrKfavNGN+R100ZmGlLiX5r0ic9hs5+uMQ/MGZzuqBWFOkrXxV5E0Y8ZMI8u8Te31eqZXquR1heJ31zqTMHmH2M9TvpMkhvI4KCFfOJ8/xSTsFYDDn29VUq+ZzDvnx3pKAYDwSJFdNQsN+R1wx1ualUvCo5is8nRPe1vhAQjMxh2coS0InLmkKV7eZbB810jQYQZDuHK8IHAlBW1Z3pQbaa4eUUXSmL6uCYD/YWXa/wGZXH04ItTxuf7GoBxKDgHehTJ1PUDsWYKKRueixehVTGeU09C7JHsTU1ZAM5ilCPZajxjkPZyNeA76jMw0Bsx1ssL8crGlAFgHt01xqnqI6UPkvjNqsqA4xyPbx35q78GUhSC4uBhnME49ByKG9pnbVKcznRiaEjHqUWt9vn8EbWnKIz/mvbspkNdSdzXG3w91IoU05mH0kQfiFe6pNHw0WkhtREWljuDEuop4707JX3W8eLF5jtoWijn9bb2HnwUSP4aSQ2kiJqIassL0yhKjahESlWNYAbfHxdRi1Sa1z3j/SWUtJfGHNNqydbBATJlc5yUBiac/ykc30qD74sh4vqBJGYgC7lIzD4OZQ5rGx3xe2U12aTBHUMbQY/wlZokJgUeEzNKRt2nHgUVNXijEsBokFcyRuKbMo9z/EB0Ee00p+DrAMy2I4T5tcXYR2UHntM50WvAz4TVxc0HzeODD8Mpa1E5ML/WiJuo2TWSOYYkVm2i50ftLz9ncpwAEDDfG+LlEuwxxnS/RGvklBdU2fbn4gVZ/MK18IVaWaWJmIeCM2El0ECuBfwt1ErKqoVAAoxiwnIVOL0uiADyd9byiBuF1UPJ/VAdn2VpzO+vMhhmp8RPpjwaos2gCsB3BdRA4eeCORC5QAjnfkpmUo/qE52kMy111HzBPFz7igQaSBig0g1r8DF5Isl6fzcq1pEIPhP/TONam/CLJuHWA8qHF7VGlmnugjkXYcFxMtuXaNqcnidxW/oaYJ0s4Dzjnh+Il0szsY73coPzVe/SSS4TPYEGUksyxWbqIGEok0M9al/ue25Z1NRKqtp7c2r8JksgRwNF+hDsMYXCDTTNA1zbLRpBjNovHXWx9IKcKzRNTGlVtaRiPZFQd6jj/oaTOP7D8xSh2jHKmqAh1JoCrbdHUt+gl7dcSw4h+P9m4sLD9QaLPAAAAABJRU5ErkJggg==";

    let vitruvianPlane = null;
    vitruvianImg.onload = () => {
      const w = vitruvianImg.width; const h = vitruvianImg.height;
      const offCanvas = document.createElement('canvas');
      offCanvas.width = w; offCanvas.height = h;
      const oCtx = offCanvas.getContext('2d');
      oCtx.drawImage(vitruvianImg, 0, 0);

      const imgData = oCtx.getImageData(0, 0, w, h); const d = imgData.data;
      // Делаем пиксели белыми, чтобы окрасить их через материал
      for (let i = 0; i < d.length; i += 4) {
        if(d[i+3] > 0) { d[i] = 255; d[i+1] = 255; d[i+2] = 255; }
      }
      oCtx.putImageData(imgData, 0, 0);

      const canvasTexture = new THREE.CanvasTexture(offCanvas);
      const planeMaterial = new THREE.MeshBasicMaterial({ map: canvasTexture, color: tintColor, transparent: true, opacity: 0.95, side: THREE.DoubleSide, depthWrite: false });
      
      let planeH = 45; let planeW = planeH * (w / h); // Масштабируем фигуру
      vitruvianPlane = new THREE.Mesh(new THREE.PlaneGeometry(planeW, planeH), planeMaterial);
      preScene.add(vitruvianPlane);
    };

    function animatePreloader3D() {
      if (!preloaderDismissed) requestAnimationFrame(animatePreloader3D);
      preControls.update();
      r1.rotation.x += 0.002; r1.rotation.y -= 0.001;
      r2.rotation.y += 0.003; r2.rotation.z += 0.002;
      r3.rotation.z -= 0.002; r3.rotation.x += 0.003;
      r4.rotation.x += 0.001; r4.rotation.y -= 0.002;
      preArmillary.rotation.y += 0.001;
      preRenderer.render(preScene, preCamera);
    }
    animatePreloader3D();

    // BACKGROUND ASTROLABE
    const bgCanvas = document.getElementById('webgl-bg-canvas');
    const bgScene = new THREE.Scene();
    const bgCamera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 1000);
    bgCamera.position.z = 24;
    const bgRenderer = new THREE.WebGLRenderer({ canvas: bgCanvas, alpha: true, antialias: true });
    bgRenderer.setSize(window.innerWidth, window.innerHeight);

    const bgArmillaryGroup = new THREE.Group(); bgScene.add(bgArmillaryGroup);
    const bgRingMat = new THREE.MeshBasicMaterial({ color: tintColor, wireframe: true, transparent: true, opacity: 0.32 });
    [8.5, 10.5, 12.5].forEach(r => bgArmillaryGroup.add(new THREE.Mesh(new THREE.TorusGeometry(r, 0.04, 16, 120), bgRingMat)));

    function animateBg() {
      requestAnimationFrame(animateBg);
      bgArmillaryGroup.rotation.x += 0.002; bgArmillaryGroup.rotation.y += 0.003;
      bgRenderer.render(bgScene, bgCamera);
    }
    animateBg();

    let isDark = true;
    function toggleTheme() {
      isDark = !isDark;
      document.documentElement.classList.toggle('dark', isDark);
      tintColor = isDark ? 0x00d4ff : 0x0055aa;
      dimColor = isDark ? 0x0088cc : 0x003388;
      
      bgRingMat.color.setHex(tintColor);
      preGoldMat.color.setHex(tintColor);
      preRingMatDim.color.setHex(dimColor);
      if(vitruvianPlane) vitruvianPlane.material.color.setHex(tintColor);
      
      runCalculation();
    }

    function parseCleanNum(val) { return parseFloat(String(val).replace(/[^0-9.-]/g, '')) || 0; }
    function formatSpaced(num) { return Math.round(num).toLocaleString('ru-RU').replace(/,/g, ' '); }
    function formatInput(input) { input.value = formatSpaced(parseCleanNum(input.value)); }
    
    let chartMainInst = null;
    let latestData = null;

    function runCalculation() {
      const period = parseInt(document.getElementById('paramPeriod').value);
      const marginPct = parseFloat(document.getElementById('paramMargin').value);
      const initialPurchase = parseCleanNum(document.getElementById('paramInitialPurchase').value);
      const aov = parseCleanNum(document.getElementById('paramAov').value);
      const startOrders = parseInt(document.getElementById('paramStartOrders').value) || 40;
      const growthVal = parseFloat(document.getElementById('paramGrowthSlider').value);

      const xLabels = [], rev = [], debtBalance = [], interestPayments = [];
      let currentDebt = 0, currentOrders = startOrders;

      for (let i = 0; i < period; i++) {
        xLabels.push(`Мес ${i+1}`);
        if(i > 0) currentOrders += growthVal;
        const curRev = currentOrders * aov;
        rev.push(curRev);
        let costs = curRev * (1 - marginPct/100) + 150000;
        if(i % 5 === 0) costs += initialPurchase * 0.2; 
        
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

      const chartColor = isDark ? '#00d4ff' : '#0055aa';
      
      if (chartMainInst) chartMainInst.destroy();
      chartMainInst = new Chart(document.getElementById('chartMain').getContext('2d'), {
        type: 'bar',
        data: {
          labels: xLabels,
          datasets: [
            { label: 'Выручка', data: rev, backgroundColor: chartColor, order: 2 },
            { label: 'Тело долга', data: debtBalance, type: 'line', borderColor: '#e63946', borderWidth: 2, tension: 0.3, order: 1 }
          ]
        },
        options: { responsive: true, maintainAspectRatio: false }
      });
      latestData = { xLabels, rev, debtBalance, interestPayments };
    }

    function exportDataToCsv() {
      if (!latestData) return;
      let csv = "data:text/csv;charset=utf-8,﻿Период;Выручка;Проценты;Остаток долга\n";
      for (let i=0; i<latestData.xLabels.length; i++) {
        csv += `${latestData.xLabels[i]};${Math.round(latestData.rev[i])};${Math.round(latestData.interestPayments[i])};${Math.round(latestData.debtBalance[i])}\n`;
      }
      const link = document.createElement("a");
      link.setAttribute("href", encodeURI(csv)); link.setAttribute("download", "Model.csv");
      document.body.appendChild(link); link.click(); document.body.removeChild(link);
    }

    window.onload = runCalculation;
  </script>
</body>
</html>"""

components.html(html_code, height=1350, scrolling=True)
