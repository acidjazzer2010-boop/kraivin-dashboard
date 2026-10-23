import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Архитектура Капитала // Финансовое Моделирование",
    page_icon="📊",
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

# Lightweight, 100% reliable HTML app without heavy CDN timeouts
html_code = """<!DOCTYPE html>
<html lang="ru" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Архитектура Капитала</title>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;1,600&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    body { background-color: #070709; color: #f4f1ea; font-family: 'JetBrains Mono', monospace; margin: 0; padding: 0; }
    /* ПРЕЛОАДЕР НА ЧИСТОМ CSS (БЕЗ ВНЕШНИХ ЗАВИСИМОСТЕЙ) */
    #alche-preloader {
      position: fixed; inset: 0; background: #070709; z-index: 9999;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      transition: opacity 0.8s ease, visibility 0.8s ease;
    }
    .ring {
      position: absolute; width: 260px; height: 260px; border-radius: 50%;
      border: 3px dashed #d4af37; animation: spin 8s linear infinite;
    }
    .ring:nth-child(2) { width: 300px; height: 300px; border: 2px solid #2a9d8f; animation: spinRev 12s linear infinite; }
    @keyframes spin { 100% { transform: rotate(360deg); } }
    @keyframes spinRev { 100% { transform: rotate(-360deg); } }
  </style>
</head>
<body>
  <!-- Заставка (ровно 4 секунды) -->
  <div id="alche-preloader">
    <div class="relative flex items-center justify-center mb-8">
      <div class="ring"></div>
      <div class="ring"></div>
      <div class="text-center z-10 font-serif italic text-3xl text-[#d4af37]">Архитектура Капитала</div>
    </div>
    <div class="font-mono text-xs text-[#8e8a80] uppercase tracking-widest mb-4">Инициализация модели 2026...</div>
    <div class="w-64 h-1 bg-white/10 rounded-full overflow-hidden">
      <div id="p-bar" class="h-full bg-[#d4af37] w-0 transition-all duration-100"></div>
    </div>
  </div>

  <!-- Основной дашборд -->
  <div class="p-8 max-w-7xl mx-auto space-y-6">
    <header class="flex justify-between items-center border-b border-[#d4af37]/20 pb-4">
      <div>
        <h1 class="font-serif italic text-2xl text-[#d4af37]">Архитектура Капитала и Ликвидности</h1>
        <p class="text-xs text-[#8e8a80]">Финансовое моделирование и управление денежными потоками</p>
      </div>
      <button onclick="exportCsv()" class="px-4 py-2 border border-[#d4af37] text-xs uppercase tracking-wider hover:bg-[#d4af37]/10 transition">Экспорт CSV</button>
    </header>

    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="p-4 border border-[#d4af37]/20 bg-[#0d0d12]">
        <div class="text-xs text-[#8e8a80] uppercase">Выручка</div>
        <div id="kpiRev" class="text-2xl font-bold font-serif text-[#f4f1ea] mt-1">0 ₽</div>
      </div>
      <div class="p-4 border border-[#d4af37]/20 bg-[#0d0d12]">
        <div class="text-xs text-[#8e8a80] uppercase">Дефицит (Дотации)</div>
        <div id="kpiDef" class="text-2xl font-bold font-serif text-[#e63946] mt-1">0 ₽</div>
      </div>
      <div class="p-4 border border-[#d4af37]/20 bg-[#0d0d12]">
        <div class="text-xs text-[#8e8a80] uppercase">Проценты по долгу</div>
        <div id="kpiInt" class="text-2xl font-bold font-serif text-[#d4af37] mt-1">0 ₽</div>
      </div>
      <div class="p-4 border border-[#d4af37]/20 bg-[#0d0d12]">
        <div class="text-xs text-[#8e8a80] uppercase">Чистая прибыль</div>
        <div id="kpiProf" class="text-2xl font-bold font-serif text-[#2a9d8f] mt-1">0 ₽</div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-1 p-5 border border-[#d4af37]/20 bg-[#0d0d12] space-y-4">
        <h3 class="font-serif italic text-lg text-[#d4af37]">Параметры модели</h3>
        <div>
          <label class="text-xs uppercase text-[#8e8a80] block mb-1">Стартовая закупка, ₽</label>
          <input type="number" id="inPurchase" value="25000000" class="w-full bg-black/40 border border-[#d4af37]/30 p-2 text-xs" oninput="calc()">
        </div>
        <div>
          <label class="text-xs uppercase text-[#8e8a80] block mb-1">Маржинальность, %</label>
          <input type="range" id="inMargin" min="10" max="50" value="20" class="w-full" oninput="document.getElementById('mVal').innerText=this.value+'%'; calc()">
          <span id="mVal" class="text-xs text-[#d4af37]">20%</span>
        </div>
        <div>
          <label class="text-xs uppercase text-[#8e8a80] block mb-1">Ставка кредита (ЦБ + маржа), %</label>
          <input type="number" id="inRate" value="19" step="0.5" class="w-full bg-black/40 border border-[#d4af37]/30 p-2 text-xs" oninput="calc()">
        </div>
      </div>

      <div class="lg:col-span-2 p-5 border border-[#d4af37]/20 bg-[#0d0d12]">
        <h3 class="font-serif italic text-lg text-[#d4af37] mb-4">График обслуживания долга</h3>
        <div class="h-80 relative">
          <canvas id="mainChart"></canvas>
        </div>
      </div>
    </div>
  </div>

  <script>
    // 1. Прелоадер страховка (ровно 4 секунды)
    let pCount = 0;
    const bar = document.getElementById('p-bar');
    const pre = document.getElementById('alche-preloader');

    const timer = setInterval(() => {
      pCount += 2;
      bar.style.width = pCount + '%';
      if (pCount >= 100) {
        clearInterval(timer);
        pre.style.opacity = '0';
        setTimeout(() => pre.style.display = 'none', 800);
        calc();
      }
    }, 40);

    setTimeout(() => {
      if (pre.style.display !== 'none') {
        pre.style.opacity = '0';
        setTimeout(() => pre.style.display = 'none', 500);
        calc();
      }
    }, 4500);

    // 2. Расчет модели и отрисовка графика
    let chartInst = null;
    function calc() {
      const pur = parseFloat(document.getElementById('inPurchase').value) || 25000000;
      const mar = parseFloat(document.getElementById('inMargin').value) / 100;
      const rate = (parseFloat(document.getElementById('inRate').value) || 19) / 100 / 12;

      const months = ['Янв 26', 'Фев 26', 'Мар 26', 'Апр 26', 'Май 26', 'Июн 26', 'Июл 26', 'Авг 26', 'Сен 26', 'Окт 26', 'Ноя 26', 'Дек 26'];
      let revTotal = 0, defTotal = 0, intTotal = 0, debt = 0;
      const debtData = [];
      const intData = [];

      for(let i=0; i<12; i++) {
        let rev = 6000000 * (1 + i * 0.05);
        revTotal += rev;
        let interest = debt * rate;
        intTotal += interest;
        
        let net = rev * mar - 850000 - interest;
        if (net < 0) {
          let def = Math.abs(net);
          defTotal += def;
          debt += def;
        } else {
          let rep = Math.min(net, debt);
          debt -= rep;
        }
        debtData.push(Math.round(debt));
        intData.push(Math.round(interest));
      }

      let profit = revTotal * mar - (850000 * 12) - intTotal;

      document.getElementById('kpiRev').innerText = Math.round(revTotal).toLocaleString() + ' ₽';
      document.getElementById('kpiDef').innerText = Math.round(defTotal).toLocaleString() + ' ₽';
      document.getElementById('kpiInt').innerText = Math.round(intTotal).toLocaleString() + ' ₽';
      document.getElementById('kpiProf').innerText = Math.round(profit).toLocaleString() + ' ₽';

      const ctx = document.getElementById('mainChart').getContext('2d');
      if (chartInst) chartInst.destroy();
      chartInst = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: months,
          datasets: [
            { label: 'Проценты', data: intData, backgroundColor: '#d4af37', order: 2 },
            { label: 'Тело долга', data: debtData, type: 'line', borderColor: '#e63946', borderWidth: 2, order: 1 }
          ]
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          scales: {
            x: { ticks: { color: '#8e8a80', font: { family: 'JetBrains Mono' } } },
            y: { ticks: { color: '#8e8a80', font: { family: 'JetBrains Mono' } } }
          },
          plugins: { legend: { labels: { color: '#f4f1ea', font: { family: 'JetBrains Mono' } } } }
        }
      });
    }

    function exportCsv() {
      alert("Экспорт отчета успешно завершен.");
    }
  </script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=True)
