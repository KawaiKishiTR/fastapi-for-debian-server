from ..core.servers_core import *
from ..core.minecraft_rcon import send_rcon_command, CommandLine
from fastapi.responses import RedirectResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")


service_name = "minecraft@sweet"
server_service = ServerService(service_name)
server_metadata = load_ServerMetadata_from_service_name(service_name)


@router.get("/", response_class=HTMLResponse)
async def root_page(request: Request):
    return templates.TemplateResponse(
        "pages/server.html",
        {
            "request": request,
            "api_base":"/servers/mc-sweet",
            **server_metadata
        }
    )

#SERVER CONTROL BUTTONS
@router.post("/api/server-start")
async def start_server():
    await server_service.start()

@router.post("/api/server-stop")
async def stop_server():
    await server_service.stop()

@router.post("/api/server-restart")
async def restart_server():
    await server_service.restart()

#BACKEND STATUS ENDPOINT
@router.get("/api/server-status")
async def server_status():
    active = await server_service.is_active()
    return {"active": active}

#SERVICE LOG STREAM
@router.get("/api/service-logs")
async def service_logs():
    return StreamingResponse(
        linux_service_log_stream(server_metadata["service_name"]),
        media_type="text/plain"
    )

# FILE Download
@router.get("/api/download-mods-zip")
def download_mods_zip():
    return RedirectResponse("/files/mods.zip") 

@router.get("/api/download-resourcepacks-zip")
def download_resourcepacks_zip():
    return RedirectResponse("/files/resourcepacks.zip")

# RCON POST ENDPOINT
@router.post("/api/send-rcon-command")
async def send_command(command: CommandLine):
    send_rcon_command(command, 25577, "gO46Es5SKTkgYkB4FysT")
    