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

        document.getElementById('cpuUsage').textContent = data.cpu + "%";
        document.getElementById('ramUsage').textContent =
            `${(data.memory_used / (1024**3)).toFixed(2)} GB / ${(data.memory_total / (1024**3)).toFixed(2)} GB (${data.memory_percent}%)`;

    } catch (e) {
        console.error("Metrics fetch failed:", e);
    }
}

// Her 3 saniyede bir güncelle
setInterval(updateMetrics, 3000);
updateMetrics();

// Sunucu durumunu periyodik güncelle
setInterval(updateStatus, 5000);
updateStatus();
