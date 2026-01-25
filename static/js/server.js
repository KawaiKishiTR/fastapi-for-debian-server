
const input = document.getElementById("cmdInput");

async function server_start() {
    await fetch(`/api/v1/servers/start`, {
        method:"POST",
        headers: {
            'X-Server-Id':`${SERVER_ID}`
        }
    })
    _updateStatus()
}

async function server_stop() {
    await fetch(`/api/v1/servers/stop`, {
        method:"POST",
        headers: {
            'X-Server-Id':`${SERVER_ID}`
        }
    })
    _updateStatus()
}

async function server_restart() {
    await fetch(`/api/v1/servers/restart`, {
        method:"POST",
        headers: {
            'X-Server-Id':`${SERVER_ID}`
        }
    })
    _updateStatus()
}

// Downloadable Files
async function download_mods() {
    await fetch(`/api/v1/servers/download-mods-zip`, {
        headers: {
            'X-Server-Id':`${SERVER_ID}`
        }
    })
}

async function download_resourcepacks() {
    await fetch(`/api/v1/servers/download-resourcepacks-zip`, {
        headers: {
            'X-Server-Id':`${SERVER_ID}`
        }
    })
}


async function _updateStatus() {
    const res = await fetch(`/api/v1/servers/status`, {
        headers: {
            'X-Server-Id': SERVER_ID
        }
    })

    if (!res.ok) {
        const text = await res.text()
        throw new Error(`HTTP ${res.status}: ${text}`)
    }

    const data = await res.json()

    const el = document.getElementById("server-status-title")

    if (data.active) {
        el.innerText = "ÇALIŞIYOR"
        el.className = "status-running"
    } else {
        el.innerText = "DURDURULMUŞ"
        el.className = "status-stopped"
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

    const res = await fetch(`${SERVER_ID}/api/send-rcon-command`, {
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
