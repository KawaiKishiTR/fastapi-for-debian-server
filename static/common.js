// === Grafikler için veri bufferları ===
let cpuHistory = [];
let ramHistory = [];

// === Grafik setup ===
const systemCtx = document.getElementById('systemChart').getContext('2d');

const systemChart = new Chart(systemCtx, {
    type: 'line', // ana tip
    data: {
        labels: Array(100).fill(""),
        datasets: [
            {
                label: 'CPU (%)',
                data: cpuHistory,
                borderWidth: 2,
                tension: 0.2,
                pointRadius: 0,
                pointHoverRadius: 0,
                fill: false,
                borderColor: '#3498db', // 🔵 CPU çizgisi rengi
                backgroundColor: '#3498db',
                order:1
            },
            {
                label: 'RAM (%)',
                type: 'bar',          // 🔴 kritik satır
                data: ramHistory,
                borderWidth: 0,
                barThickness: 4,
                backgroundColor: 'rgba(243, 156, 18, 0.35)', // yarı saydam
                order: 0
            }
        ]
    },
    options: {
        plugins: {
            title: {
                display: true,
                text: "CPU / RAM Kullanımı",
                color: "#f39c12",
                font: { size: 16 }
            }
        },
        animation: false,
        scales: {
            x: {
                ticks: { display: false },
                grid: { display: false }
            },
            y: {
                beginAtZero: true,
                max: 100
            }
        }
    }
});

async function updateMetrics() {
    try {
        const res = await fetch('/machine/api/system-usage');
        const data = await res.json();

    cpuHistory.push(data.cpu);
    if (cpuHistory.length > 100) cpuHistory.shift();

    ramHistory.push(data.ram);
    if (ramHistory.length > 100) ramHistory.shift();

    // === Grafik veri güncelleme ===
    systemChart.data.datasets[0].data = cpuHistory;
    systemChart.data.datasets[1].data = ramHistory;
    systemChart.update();

    } catch (e) {
        console.error("Metrics fetch failed:", e);
    }
}

async function setSystemMetricsHistory() {
    const historyRes = await fetch(`/machine/api/system-history`);
    const history = await historyRes.json();
    cpuHistory.splice(0, 100, ...history.cpu);
    ramHistory.splice(0, 100, ...history.ram);
    systemChart.data.datasets[0].data = cpuHistory;
    systemChart.data.datasets[1].data = ramHistory;
    systemChart.update();
}

async function init() {
    await setSystemMetricsHistory();
    setInterval(updateMetrics, 3000);
}


document.addEventListener("DOMContentLoaded", () => {
    init();
});