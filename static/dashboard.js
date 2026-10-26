/**
 * dashboard.js: Высокопроизводительный фронтенд-контроллер (Three.js + Chart.js)
 */

// 1. Управление аудио (ленивая инициализация + Mute)
let audioCtx = null;
let isAudioMuted = false;

function initAudioContext() {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (audioCtx.state === 'suspended') {
        audioCtx.resume();
    }
}

function playClickSound(freq = 1200, duration = 0.02) {
    if (isAudioMuted) return;
    try {
        initAudioContext();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(320, audioCtx.currentTime + duration);
        gain.gain.setValueAtTime(0.03, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
    } catch (e) {}
}

function toggleMute() {
    isAudioMuted = !isAudioMuted;
    const btn = document.getElementById('muteBtn');
    if (btn) btn.textContent = isAudioMuted ? 'ЗВУК: ВЫКЛ' : 'ЗВУК: ВКЛ';
}

// 2. Адаптивный курсор (отключение на мобильных)
const cursorDot = document.getElementById('custom-cursor');
const cursorFollower = document.getElementById('custom-cursor-follower');
let mouseX = window.innerWidth / 2, mouseY = window.innerHeight / 2;
let followerX = mouseX, followerY = mouseY;

if (window.matchMedia('(pointer: coarse)').matches) {
    if (cursorDot) cursorDot.remove();
    if (cursorFollower) cursorFollower.remove();
} else {
    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX; mouseY = e.clientY;
        if (cursorDot) {
            cursorDot.style.left = `${mouseX}px`;
            cursorDot.style.top = `${mouseY}px`;
        }
    });

    function updateCursor() {
        followerX += (mouseX - followerX) * 0.18;
        followerY += (mouseY - followerY) * 0.18;
        if (cursorFollower) {
            cursorFollower.style.left = `${followerX}px`;
            cursorFollower.style.top = `${followerY}px`;
        }
        requestAnimationFrame(updateCursor);
    }
    requestAnimationFrame(updateCursor);
}

// 3. Быстрый прелоадер (1.8 сек вместо 9 сек + sessionStorage)
const PRELOADER_DURATION = 1800; // Оптимизировано для продуктивности
const hasVisited = sessionStorage.getItem('fin_preloader_seen');

function dismissPreloader() {
    const stage = document.getElementById('preloader-stage');
    const app = document.getElementById('mainDashboardApp');
    sessionStorage.setItem('fin_preloader_seen', 'true');
    if (app) { app.style.opacity = '1'; }
    if (stage) {
        stage.style.transition = 'opacity 0.5s ease';
        stage.style.opacity = '0';
        setTimeout(() => { stage.style.display = 'none'; }, 500);
    }
}

if (hasVisited === 'true') {
    // Мгновенный пропуск, если пользователь уже заходил
    dismissPreloader();
} else {
    const startTime = performance.now();
    function stepLoader(now) {
        const progress = Math.min((now - startTime) / PRELOADER_DURATION, 1.0);
        const bar = document.getElementById('loaderProgressBar');
        const pct = document.getElementById('loaderPercent');
        if (bar) bar.style.width = `${(progress * 100).toFixed(0)}%`;
        if (pct) pct.textContent = `${Math.floor(progress * 100)}%`;

        if (progress >= 0.95) {
            const btnWrap = document.getElementById('exploreBtnWrapper');
            const hud = document.getElementById('preloaderHUD');
            if (hud) hud.style.opacity = '0';
            if (btnWrap) btnWrap.classList.add('active');
        } else {
            requestAnimationFrame(stepLoader);
        }
    }
    requestAnimationFrame(stepLoader);
    setTimeout(() => {
        const title = document.getElementById('preloaderTitle');
        if (title) title.style.opacity = '1';
    }, 400);
}

// 4. Отрисовка графиков по данным, полученным от Python
let chartDebtInstance = null, chartStockInstance = null, chartCFInstance = null;

function renderCharts(data) {
    const isDark = document.documentElement.classList.contains('dark');
    const chartText = isDark ? '#8e8a80' : '#6b665c';
    const chartGrid = isDark ? 'rgba(212, 175, 55, 0.08)' : 'rgba(184, 134, 11, 0.12)';

    // График обслуживания долга
    const ctxDebt = document.getElementById('chartDebt').getContext('2d');
    if (chartDebtInstance) chartDebtInstance.destroy();
    chartDebtInstance = new Chart(ctxDebt, {
        type: 'bar',
        data: {
            labels: data.x_labels,
            datasets: [
                { label: 'Проценты к уплате', data: data.interest_payments, backgroundColor: '#d4af37', order: 2 },
                { label: 'Остаток тела долга', data: data.debt_balance, type: 'line', borderColor: '#e63946', borderWidth: 2.2, yAxisID: 'y1', tension: 0.3, order: 1 }
            ]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            scales: {
                x: { grid: { display: false }, ticks: { color: chartText } },
                y: { grid: { color: chartGrid }, ticks: { color: chartText } },
                y1: { position: 'right', grid: { display: false }, ticks: { color: '#e63946' } }
            }
        }
    });

    // График складского запаса
    const ctxStock = document.getElementById('chartStock').getContext('2d');
    if (chartStockInstance) chartStockInstance.destroy();
    chartStockInstance = new Chart(ctxStock, {
        type: 'bar',
        data: {
            labels: data.x_labels,
            datasets: [
                { label: 'Оплата партии', data: data.cogs_payments, backgroundColor: '#52525b', order: 2 },
                { label: 'Остаток на складе', data: data.inventory_balance, type: 'line', borderColor: '#d4af37', borderWidth: 2.2, yAxisID: 'y1', tension: 0.3, order: 1 }
            ]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            scales: {
                x: { grid: { display: false }, ticks: { color: chartText } },
                y: { grid: { color: chartGrid }, ticks: { color: chartText } },
                y1: { position: 'right', grid: { display: false }, ticks: { color: '#d4af37' } }
            }
        }
    });
}

// Загрузка начальных данных из серверной инъекции
window.addEventListener('DOMContentLoaded', () => {
    if (window.SERVER_FIN_DATA) {
        renderCharts(window.SERVER_FIN_DATA);
    }
});
