from fastapi import FastAPI, WebSocket, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from mcrcon import MCRcon
import subprocess
import asyncio
import psutil
import os

from dotenv import load_dotenv
load_dotenv()

class Command(BaseModel):
    command: str


app = FastAPI()

# Statik dosyalar
app.mount("/static", StaticFiles(directory="static"), name="static")
# Jinja2 şablon sistemi
templates = Jinja2Templates(directory="templates")



def start_server_():
    subprocess.Popen(
        ["sudo", "systemctl", "start", "minecraft@survival"],
    )
def stop_server_():
    subprocess.Popen(
        ["sudo", "systemctl", "stop", "minecraft@survival"]
    )
def restart_server_():
    subprocess.Popen(
        ["sudo", "systemctl", "restart", "minecraft@survival"]
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


@app.get("/metrics")
async def metrics():
    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()

    return {
        "cpu":cpu,
        "memory_used":mem.used,
        "memory_total":mem.total,
        "memory_percent":mem.percent
    }

@app.post("/start-server")
def start_server():
    # subprocess ile arka planda başlat
    start_server_()
    return {"status":"started"}
@app.post("/stop-server")
def stop_server():
    # subprocess ile durdur
    stop_server_()
    return {"status": "stopped"}
@app.post("/restart-server")
def restart_server():
    restart_server_()
    return {"status": "restarted"}


@app.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    await websocket.accept()
    process = await asyncio.create_subprocess_exec(
        "journalctl", "-u", "minecraft@survival.service", "-f", "-n", "20",
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
        "systemctl", "is-active", "minecraft@survival.service",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, _ = await proc.communicate()
    return stdout.decode().strip() == "active"

@app.post("/send-command")
async def send_command(cmd: Command):
    try:
        with MCRcon("127.0.0.1", os.getenv("RCON_PASSWORD"), port=25575) as mcr:
            response = mcr.command(cmd.command)

        return {"status": "ok", "response": response}

    except Exception as e:
        return {"status": "error", "error": str(e)}
