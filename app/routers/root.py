from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="static")

@router.get("/", response_class=HTMLResponse)
async def root_page(request: Request):
    return RedirectResponse(url="/servers/mc-vanilla")
