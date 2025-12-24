from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..core.linux_services import ServerService


router = APIRouter()
server_service = ServerService("minecraft@survival")
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def root_page(request: Request):
    return templates.TemplateResponse(
        "pages/mc-survival.html",
        {
            "request": request,
            "api_base":"/servers/mc-survival"
        }
    )

@router.post("/api/server-start")
async def start_server():
    server_service.start()

@router.post("/api/server-stop")
async def stop_server():
    server_service.stop()

@router.post("/api/server-restart")
async def restart_server():
    server_service.restart()

@router.get("/api/server-status")
async def server_status():
    active = await server_service.is_active()
    return {"active": active}