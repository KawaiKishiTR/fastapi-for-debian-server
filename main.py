from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import subprocess
import asyncio

app = FastAPI()

# Statik dosyalar
app.mount("/static", StaticFiles(directory="static"), name="static")
# Jinja2 şablon sistemi
templates = Jinja2Templates(directory="templates")



def run_server():
    subprocess.Popen(
        ["sudo", "systemctl", "start", "minecraft"],
    )
def kill_server():
    subprocess.Popen(
        ["sudo", "systemctl", "stop", "minecraft"]
    )
def restart_server_():
    subprocess.Popen(
        ["sudo", "systemctl", "restart", "minecraft"]
    )



# HTML dosyanızı burada da dönebilirsiniz
# === HTML SAYFASI ===
@app.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    # Burada template'e dinamik veri geçebilirsin (örnek: sunucu durumu)
    server_running = await check_server_status()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "server_running": server_running}
    )


@app.post("/start-server")
def start_server():
    # subprocess ile arka planda başlat
    run_server()
    return {"status":"started"}
@app.post("/stop-server")
def stop_server():
    # subprocess ile durdur
    kill_server()
    return {"status": "stopped"}
@app.post("/restart-server")
def restart_server():
    restart_server_()
    return {"status": "restarted"}


@app.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    await websocket.accept()
    process = await asyncio.create_subprocess_exec(
        "journalctl", "-u", "minecraft.service", "-f", "-n", "20",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            line = line.decode("utf-8").split(":", 3)[-1][1:]
            await websocket.send_text(line)
    except Exception as e:
        await websocket.send_text(f"[ERROR] {e}")
    finally:
        process.terminate()
        await process.wait()

# === SUNUCU DURUMU SORGULAMA ===
@app.get("/status")
async def status():
    running = await check_server_status()
    return {"running": running}


# === HELPER: systemctl status kontrolü ===
async def check_server_status():
    proc = await asyncio.create_subprocess_exec(
        "systemctl", "is-active", "minecraft.service",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, _ = await proc.communicate()
    return stdout.decode().strip() == "active"
