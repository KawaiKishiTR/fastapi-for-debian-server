from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import subprocess
import asyncio

app = FastAPI()

def run_server():
    subprocess.Popen(
        ["sudo", "systemctl", "start", "minecraft"],
    )
def kill_server():
    subprocess.Popen(
        ["sudo", "systemctl", "stop", "minecraft"]
    )
def get_server_status():
    result = subprocess.run(["systemctl", "status", "minecraft"], text=True, capture_output=True, encoding="utf-8")
    if "active (running)" in result.stdout:
        return "running"
    return "stopped"


# HTML dosyanızı burada da dönebilirsiniz
@app.get("/")
async def get():
    with open("index.html") as f:
        return HTMLResponse(f.read())

# Sunucu başlatma endpoint'i
@app.post("/start-server", response_class=HTMLResponse)
def start_server():
    # subprocess ile arka planda başlat
    run_server()
    return {"status":"started"}

# Sunucuyu durdurma endpoint'i
@app.post("/stop-server", response_class=HTMLResponse)
def stop_server():
    # subprocess ile durdur
    kill_server()
    return {"status": "stopped"}

@app.post("/restart-server")
async def restart_server():
    await stop_server()
    await asyncio.sleep(3)
    await start_server()
    return {"status": "restarted"}

# WebSocket ile log gönderimi
clients = []

# Logları göster
@app.get("/logs", response_class=HTMLResponse)
def logs():
    try:
        with open("/home/kawaikishi/minecraft/logs/latest.log", "r") as f:
            log_content = f.read().replace("\n", "<br>")
    except FileNotFoundError:
        log_content = "Log dosyası bulunamadı."
    return f"<h2>Sunucu Logları</h2><pre>{log_content}</pre><a href='/'>Geri Dön</a>"

@app.websocket("/ws/logs")
async def websocket_logs(ws: WebSocket):
    await ws.accept()
    process = await asyncio.create_subprocess_exec(
        "journalctl", "-fu", "minecraft.service",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    try:
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            await ws.send_text(line.decode('utf-8'))
    except Exception as e:
        print("WebSocket disconnected:", e)
    finally:
        process.kill()
        await process.wait()