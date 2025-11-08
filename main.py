from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import subprocess

app = FastAPI()

def get_server_status():
    result = subprocess.run(["systemctl", "status", "minecraft"], text=True, capture_output=True, encoding="utf-8")
    if "active (running)" in result.stdout:
        return "running"
    return "stopped"


# Basit HTML sayfası
@app.get("/", response_class=HTMLResponse)
def home():
    server_status = get_server_status()

    return f"""
    <html>
        <head>
            <title>Minecraft Kontrol Paneli</title>
        </head>
        <body>
            <h1>Minecraft Sunucu Kontrol</h1>
            <p>Sunucu Durumu: {server_status}</p>
            <form action="/start-server" method="post">
                <button type="submit">Sunucuyu Başlat</button>
            </form>
            <form action="/stop-server" method="post">
                <button type="submit">Sunucuyu Durdur</button>
            </form>
            <form action="/logs" method="get">
                <button type="submit">Logları Görüntüle</button>
            </form>
        </body>
    </html>
    """

# Sunucu başlatma endpoint'i
@app.post("/start-server", response_class=HTMLResponse)
def start_server():
    # subprocess ile arka planda başlat
    subprocess.Popen(
        ["sudo", "systemctl", "start", "minecraft.service"],
    )
    return "<h2>Sunucu başlatıldı!</h2><a href='/'>Geri Dön</a>"

# Sunucuyu durdurma endpoint'i
@app.post("/stop-server", response_class=HTMLResponse)
def stop_server():
    # subprocess ile durdur
    subprocess.Popen(
        ["sudo", "systemctl", "stop", "minecraft"]
    )
    return "<h2>Sunucu durduruldu!</h2><a href='/'>Geri Dön</a>"

# Logları göster
@app.get("/logs", response_class=HTMLResponse)
def logs():
    try:
        with open("/home/kawaikishi/minecraft/logs/latest.log", "r") as f:
            log_content = f.read().replace("\n", "<br>")
    except FileNotFoundError:
        log_content = "Log dosyası bulunamadı."
    return f"<h2>Sunucu Logları</h2><pre>{log_content}</pre><a href='/'>Geri Dön</a>"
