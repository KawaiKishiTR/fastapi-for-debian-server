from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import subprocess

app = FastAPI()

# Basit HTML sayfası
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Minecraft Kontrol Paneli</title>
        </head>
        <body>
            <h1>Minecraft Sunucu Kontrol</h1>
            <form action="/start-server" method="post">
                <button type="submit">Sunucuyu Başlat</button>
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
        ["systemctl", "start", "minecraft"],
    )
    return "<h2>Sunucu başlatıldı!</h2><a href='/'>Geri Dön</a>"

# Logları göster
@app.get("/logs", response_class=HTMLResponse)
def logs():
    try:
        with open("/home/kawaikishi/minecraft/logs/latest.log", "r") as f:
            log_content = f.read().replace("\n", "<br>")
    except FileNotFoundError:
        log_content = "Log dosyası bulunamadı."
    return f"<h2>Sunucu Logları</h2><pre>{log_content}</pre><a href='/'>Geri Dön</a>"
