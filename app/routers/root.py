from ..core.servers_core import *
from fastapi.responses import RedirectResponse


router = APIRouter()
templates = Jinja2Templates(directory="static")

@router.get("/", response_class=HTMLResponse)
async def root_page(request: Request):
    return RedirectResponse(url="/servers/mc-survival")
