from ..core.servers_core import *

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def root_page(request: Request):
    return templates.TemplateResponse(
        "pages/server.html",
        {
            "request": request,
            "server_id":"fc-vanilla",
        }
    )
