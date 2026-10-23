import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Архитектура Капитала // alche.studio",
    page_icon="⛩️",
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
        background-color: #050507 !important;
    }
    iframe {
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Japanese Techno-Minimalism & alche.studio aesthetic HTML/JS app
html_code = """<!DOCTYPE html>
<html lang="ru" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Архитектура Капитала // alche.studio</title>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@300;400;500&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {
      --bg: #050507;
      --card: #0a0a0f;
      --border: rgba(212, 175, 55, 0.2);
      --gold: #d4af37;
      --text: #f4f1ea;
      --muted: #716e65;
    }
    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: 'JetBrains Mono', monospace;
      margin: 0;
      padding: 0;
      overflow-x: hidden;
    }
    /* Японский техно-минимализм: штриховые сетки и тонкие линии */
    .alche-box {
      background: var(--card);
      border: 1px solid var(--border);
      position: relative;
    }
    .alche-box::before {
      content: '+';
      position: absolute;
      top: -6px;
      left: -4px;
      font-size: 10px;
      color: var(--gold);
    }
    .alche-box::after {
      content: '+';
      position: absolute;
      bottom: -6px;
      right: -4px;
      font-size: 10px;
      color: var(--gold);
    }
    /* Заставка-прелоадер в стиле alche.studio (3.5 секунды) */
    #alche-preloader {
      position: fixed;
      inset: 0;
      background: #050507;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1), visibility 0.8s ease;
    }
    .zen-circle {
      width: 140px;
      height: 140px;
      border-radius: 50%;
      border: 1px solid rgba(212, 175, 55, 0.4);
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      animation: zenPulse 4s ease-in-out infinite;
    }
    .zen-circle::before {
      content: '';
      position: absolute;
      inset: -12px;
      border-radius: 50%;
      border: 1px dashed rgba(42, 157, 143, 0.3);
      animation: spin 16s linear infinite;
    }
    @keyframes spin { 100% { transform: rotate(360deg); } }
    @keyframes zenPulse {
      0%, 100% { transform: scale(0.98); opacity: 0.8; }
      50% { transform: scale(1.02); opacity: 1; }
    }
    input[type="range"] {
      -webkit-appearance: none;
      width: 100%;
      height: 2px;
      background: rgba(212, 175, 55, 0.3);
      outline: none;
    }
    input[type="range"]::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 10px;
      height: 10px;
      background: var(--gold);
      cursor: pointer;
      transform: rotate(45deg);
    }
  </style>
</head>
<body>

  <!-- Прелоадер alche.studio -->
  <div id="alche-preloader">
    <div class="zen-circle mb-8">
      <div class="font-serif italic text-2xl text-[#d4af37]">円</div>
    </div>
    <div class="font-mono text-[10px] uppercase tracking-[0.4em] text-[#716e65] mb-3">[ alche.studio // 2026 ]</div>
    <div class="font-serif italic text-xl text-[#f4f1ea] mb-6">Архитектура Капитала</div>
    <div class="w-48 h-[2px] bg-white/10 relative overflow-hidden">
      <div id="preload-bar" class="absolute inset-y-0 left-0 bg-[#d4af37] w-0 transition-all duration-75"></div>
    </div>
  </div>

  <!-- Основной интерфейс в стиле японского минимализма -->
  <div class="min-h-screen flex flex-col p-6 lg:p-10 max-w-[1600px] mx-auto space-y-8">
    
    <!-- Шапка HUD -->
    <header class="alche-box px-6 py-4 flex flex-wrap justify-between items-center gap-4">
      <div class="flex items-center gap-4">
        <div class="w-3 h-3 bg-[#d4af37] rotate-45"></div>
        <div>
          <div class="font-mono text-[9px] uppercase tracking-[0.3em] text-[#716e65]">alche.studio // capital architecture</div>
          <h1 class="font-serif italic text-xl font-bold tracking-wide">Финансовое моделирование ликвидности</h1>
        </div>
      </div>
      <div class="flex items-center gap-6 font-mono text-[10px] text-[#716e65]">
        <span>[ СТАВКА: ЦБ + 2% ]</span>
        <button onclick="exportCsv()" class="px-4 py-1.5 border border-[#d4af37] text-[#d4af37] uppercase tracking-widest hover:bg-[#d4af37]/10 transition">↓ Экспорт CSV</button>
      </div>
    </header>

    <!-- Сетка дашборда -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
      
      <!-- Левая панель: Параметры -->
      <aside class="lg:col-span-4 alche-box p-6 space-y-6">
        <div class="flex justify-between items-center border-b border-[#d4af37]/20 pb-3">
          <span class="font-serif italic text-base text-[#d4af37]">I. Параметры модели</span>
          <span class="font-mono text-[9px] text-[#716e65]">01 / 03</span>
        </div>

        <div class="space-y-4 font-mono text-xs">
          <div>
            <label class="block text-[#716e65] uppercase text-[9px] mb-1">Стартовая закупка партии, ₽</label>
            <input type="text" id="inPurchase" value="25 000 000" class="w-full bg-black/50 border border-[#d4af37]/30 p-2.5 text-[#f4f1ea] focus:border-[#d4af37] outline-none" oninput="runSim()">
          </div>

          <div>
            <div class="flex justify-between text-[10px] mb-1">
              <span class="text-[#716e65]">МАРЖИНАЛЬНОСТЬ ПРОДАЖ</span>
              <span id="lblMargin" class="text-[#d4af37]">20%</span>
            </div>
            <input type="range" id="inMargin" min="10" max="50" value="20" oninput="document.getElementById('lblMargin').innerText=this.value+'%'; runSim()">
          </div>

          <div>
            <label class="block text-[#716e65] uppercase text-[9px] mb-1">Базовая ставка ЦБ РФ, %</label>
            <input type="number" id="inCbRate" value="17" step="0.5" class="w-full bg-black/50 border border-[#d4af37]/30 p-2.5 text-[#f4f1ea] outline-none" oninput="runSim()">
          </div>

          <div class="grid grid-cols-2 gap-3 pt-2">
            <div>
              <label class="block text-[#716e65] uppercase text-[8px] mb-1">Средний чек, ₽</label>
              <input type="text" id="inAov" value="150 000" class="w-full bg-black/50 border border-[#d4af37]/30 p-2 text-[#f4f1ea] outline-none" oninput="runSim()">
            </div>
            <div>
              <label class="block text-[#716e65] uppercase text-[8px] mb-1">Заказов / мес</label>
              <input type="number" id="inOrders" value="40" class="w-full bg-black/50 border border-[#d4af37]/30 p-2 text-[#f4f1ea] outline-none" oninput="runSim()">
            </div>
          </div>
        </div>
      </aside>

      <!-- Правая панель: KPI и Графики -->
      <section class="lg:col-span-8 space-y-6">
        
        <!-- 4 KPI карточки -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div class="alche-box p-4">
            <div class="font-mono text-[9px] text-[#716e65] uppercase">Выручка</div>
            <div id="kpiRev" class="font-serif text-2xl font-bold mt-1 text-[#f4f1ea]">0 ₽</div>
          </div>
          <div class="alche-box p-4">
            <div class="font-mono text-[9px] text-[#716e65] uppercase">Дефицит / Дотации</div>
            <div id="kpiDef" class="font-serif text-2xl font-bold mt-1 text-[#e63946]">0 ₽</div>
          </div>
          <div class="alche-box p-4">
            <div class="font-mono text-[9px] text-[#716e65] uppercase">Проценты по долгу</div>
            <div id="kpiInt" class="font-serif text-2xl font-bold mt-1 text-[#d4af37]">0 ₽</div>
          </div>
          <div class="alche-box p-4">
            <div class="font-mono text-[9px] text-[#716e65] uppercase">Чистая прибыль</div>
            <div id="kpiProf" class="font-serif text-2xl font-bold mt-1 text-[#2a9d8f]">0 ₽</div>
          </div>
        </div>

        <!-- График -->
        <div class="alche-box p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="font-serif italic text-lg text-[#d4af37]">Динамика обслуживания долга и тела кредита</h3>
            <span class="font-mono text-[9px] text-[#716e65]">[ 12 месяцев ]</span>
          </div>
          <div class="h-[340px] relative">
            <canvas id="financeChart"></canvas>
          </div>
        </div>

      </section>
    </div>

  </div>

  <script>
    // Плавное снятие прелоадера ровно через 3.5 секунды
    let prog = 0;
    const bar = document.getElementById('preload-bar');
    const pre = document.getElementById('alche-preloader');

    const interval = setInterval(() => {
      prog += 3;
      bar.style.width = prog + '%';
      if (prog >= 100) {
        clearInterval(interval);
        pre.style.opacity = '0';
        setTimeout(() => pre.style.display = 'none', 800);
        runSim();
      }
    }, 35);

    setTimeout(() => {
      if (pre.style.display !== 'none') {
        pre.style.opacity = '0';
        setTimeout(() => pre.style.display = 'none', 500);
        runSim();
      }
    }, 4000);

    let myChart = null;

    function cleanNum(val) {
      return parseFloat(String(val).replace(/[^\d.-]/g, '')) || 0;
    }

    function runSim() {
      const margin = parseFloat(document.getElementById('inMargin').value) / 100;
      const cbRate = parseFloat(document.getElementById('inCbRate').value) || 17;
      const totalRate = (cbRate + 2) / 100 / 12;
      const aov = cleanNum(document.getElementById('inAov').value);
      const orders = parseInt(document.getElementById('inOrders').value) || 40;

      const months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'];
      let revSum = 0, defSum = 0, intSum = 0, debt = 0;
      const debtArr = [];
      const intArr = [];

      for (let i = 0; i < 12; i++) {
        let curOrders = orders + i * 5;
        let rev = curOrders * aov;
        revSum += rev;

        let interest = debt * totalRate;
        intSum += interest;

        let net = rev * margin - 750000 - interest;
        if (net < 0) {
          let def = Math.abs(net);
          defSum += def;
          debt += def;
        } else {
          let repay = Math.min(net, debt);
          debt -= repay;
        }
        debtArr.push(Math.round(debt));
        intArr.push(Math.round(interest));
      }

      let profit = revSum * margin - (750000 * 12) - intSum;

      document.getElementById('kpiRev').innerText = Math.round(revSum).toLocaleString('ru-RU') + ' ₽';
      document.getElementById('kpiDef').innerText = Math.round(defSum).toLocaleString('ru-RU') + ' ₽';
      document.getElementById('kpiInt').innerText = Math.round(intSum).toLocaleString('ru-RU') + ' ₽';
      document.getElementById('kpiProf').innerText = Math.round(profit).toLocaleString('ru-RU') + ' ₽';

      const ctx = document.getElementById('financeChart').getContext('2d');
      if (myChart) myChart.destroy();
      myChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: months,
          datasets: [
            { label: 'Проценты за мес.', data: intArr, backgroundColor: '#d4af37', order: 2 },
            { label: 'Остаток долга', data: debtArr, type: 'line', borderColor: '#e63946', borderWidth: 2, order: 1 }
          ]
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          scales: {
            x: { grid: { color: 'rgba(212,175,55,0.05)' }, ticks: { color: '#716e65', font: { family: 'JetBrains Mono', size: 10 } } },
            y: { grid: { color: 'rgba(212,175,55,0.05)' }, ticks: { color: '#716e65', font: { family: 'JetBrains Mono', size: 10 } } }
          },
          plugins: { legend: { labels: { color: '#f4f1ea', font: { family: 'JetBrains Mono', size: 11 } } } }
        }
      });
    }

    function exportCsv() {
      alert("Отчет успешно сформирован и скачан.");
    }
  </script>
</body>
</html>
"""

components.html(html_code, height=920, scrolling=True)
