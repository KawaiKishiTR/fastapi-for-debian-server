
const input = document.getElementById("cmdInput");

async function server_start() {
    await fetch(`${API_BASE}/api/server-start`, {method:"POST"})
    console.log(`POST Atıldı: ${API_BASE}/api/server-start`)
    _updateStatus()
}

async function server_stop() {
    await fetch(`${API_BASE}/api/server-stop`, {method:"POST"})
    console.log(`POST Atıldı: ${API_BASE}/api/server-stop`)
    _updateStatus()
}

async function server_restart() {
    await fetch(`${API_BASE}/api/server-restart`, {method:"POST"})
    console.log(`POST Atıldı: ${API_BASE}/api/server-restart`)
    _updateStatus()
}



async function _updateStatus() {
        const res = await fetch(`${API_BASE}/api/server-status`)
        const data = await res.json()        
        if (data.active) {
            document.getElementById("server-status-title").innerText = "ÇALIŞIYOR"
            document.getElementById("server-status-title").className = "status-running"
        } else {
            document.getElementById("server-status-title").innerText = "DURDURULMUŞ"
            document.getElementById("server-status-title").className = "status-stopped"
        }
}

async function updateStatus() {
    try {
        await _updateStatus()
    } catch (err) {
        console.error("Status Alınamadı:", err)
    } finally {
        setTimeout(updateStatus, 3000)
    }

}

async function sendCommand() {
    const command = input.value.trim();
    if (!command) return;

    const res = await fetch(`${API_BASE}/api/send-rcon-command`, {
        method:"POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({command})
    });

    const data = await res.json();

    if (!res.ok) {
        appendLog(`[HATA] ${data.detail}\n`);
        return;
    }

    appendLog(`[RCON] ${data.output}\n`);
    input.value = "";
}

updateStatus()
