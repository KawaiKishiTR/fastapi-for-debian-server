const logArea = document.getElementById('logArea');
const statusEl = document.getElementById('serverStatus');

//logların websocket bağlantısı
const ws = new WebSocket(`ws://${location.host}/ws/logs`);

ws.onmessage = (event) => {
    logArea.textContent += event.data;
    logArea.scrollTop = logArea.scrollHeight;
};

ws.onerror = (err) => {
    console.error("WebSocket error:", err);
    logArea.textContent += "\n[HATA] Log bağlantısı koptu.\n";
};

//sunucu duurmu güncelleme komutu
async function updateStatus() {
    const res = await fetch('/status');
    const data = await res.json();
    const running = data.running;
    if (running) {
        statusEl.innerHTML = 'Durum: <span class="running">ÇALIŞIYOR</span>';
    } else {
        statusEl.innerHTML = 'Durum: <span class="stopped">DURDURULMUŞ</span>';
    }
}

// Butonlar
document.getElementById('startBtn').addEventListener('click', async () => {
    await fetch('/start-server', { method: 'POST' });
    await updateStatus();
});

document.getElementById('stopBtn').addEventListener('click', async () => {
    await fetch('/stop-server', { method: 'POST' });
    await updateStatus();
});

document.getElementById('restartBtn').addEventListener('click', async () => {
    await fetch('/restart-server', { method: 'POST' });
    await updateStatus();
});

async function updateMetrics() {
    try {
        const res = await fetch('/metrics');
        const data = await res.json();

    cpuHistory.push(data.cpu);
    if (cpuHistory.length > 100) cpuHistory.shift();

    ramHistory.push(data.memory_percent);
    if (ramHistory.length > 100) ramHistory.shift();

    // === Grafik başlıklarını güncelle ===
    cpuChart.options.plugins.title.text =
        `CPU (%) — Anlık: ${data.cpu}%`;

    ramChart.options.plugins.title.text =
        `RAM (%) — Anlık: ${data.memory_percent}% (${(data.memory_used / (1024**3)).toFixed(2)} GB / ${(data.memory_total / (1024**3)).toFixed(2)} GB)`;

    // === Grafik veri güncelleme ===
    cpuChart.data.datasets[0].data = cpuHistory;
    cpuChart.update();

    ramChart.data.datasets[0].data = ramHistory;
    ramChart.update();

    } catch (e) {
        console.error("Metrics fetch failed:", e);
    }
}


// === Grafikler için veri bufferları ===
let cpuHistory = [];
let ramHistory = [];

// === Grafik setup ===
const cpuCtx = document.getElementById('cpuChart').getContext('2d');
const ramCtx = document.getElementById('ramChart').getContext('2d');

const cpuChart = new Chart(cpuCtx, {
    type: 'line',
    data: {
        labels: Array(100).fill(""),
        datasets: [{
            label: 'CPU (%)',
            data: cpuHistory,
            borderWidth: 2,
            tension: 0.2,
            pointRadius: 0,
            pointHoverRadius: 0,
        }]
    },
    options: {
        plugins: {
            title: {
                display: true,
                text: "CPU (%) — Anlık: 0%",
                color: "#f39c12",
                font: { size: 16 }
            }
        },
        animation: false,
        scales: {
            y: { beginAtZero: true, max: 100 }
        }
    }
});


const ramChart = new Chart(ramCtx, {
    type: 'line',
    data: {
        labels: Array(100).fill(""),
        datasets: [{
            label: 'RAM (%)',
            data: ramHistory,
            borderWidth: 2,
            tension: 0.2,
            pointRadius: 0,
            pointHoverRadius: 0,
        }]
    },
    options: {
        plugins: {
            title: {
                display: true,
                text: "RAM (%) — Anlık: 0% (0 GB / 0 GB)",
                color: "#f39c12",
                font: { size: 16 }
            }
        },
        animation: false,
        scales: {
            y: { beginAtZero: true, max: 100 }
        }
    }
});

document.getElementById('sendCmdBtn').addEventListener('click', async () => {
    const cmd = document.getElementById('cmdInput').value;
    if (!cmd) return;

    const res = await fetch('/send-command', {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ command: cmd })
    });

    const data = await res.json();

    if (data.status === "ok") {
        logArea.textContent += `\n> ${cmd}\n${data.response}\n`;
    } else {
        logArea.textContent += `\n[HATA] Komut gönderilemedi: ${data.error}\n`;
    }

    logArea.scrollTop = logArea.scrollHeight;
    document.getElementById('cmdInput').value = "";
});




// Her 3 saniyede bir güncelle
setInterval(updateMetrics, 3000);
updateMetrics();

// Sunucu durumunu periyodik güncelle
setInterval(updateStatus, 5000);
updateStatus();
