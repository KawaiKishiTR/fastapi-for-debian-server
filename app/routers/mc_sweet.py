from ..core.servers_core import *
from ..core.minecraft_rcon import send_rcon_command, CommandLine

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def root_page(request: Request):
    return templates.TemplateResponse(
        "pages/server.html",
        {
            "request": request,
            "server_id":"mc-sweet",
        }
    )

# RCON POST ENDPOINT
@router.post("/api/send-rcon-command")
async def send_command(command: CommandLine):
    return send_rcon_command(command, 25577, "gO46Es5SKTkgYkB4FysT")
    