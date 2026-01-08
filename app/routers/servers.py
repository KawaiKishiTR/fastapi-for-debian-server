from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def root_page(request: Request):
    return templates.TemplateResponse(
        "pages/servers.html",
        {"request": request}
    )

VALID_SERVERS = {
    "mc-survival",
    "mc-redstone",
    "mc-sweet",
    "fc-vanilla",
    "fc-krastorio2"
}

@router.get("/{server_id}", response_class=HTMLResponse)
async def server_page(request: Request, server_id:str):
    if server_id not in VALID_SERVERS:
        raise HTTPException(404, detail="Server Not Found")
    
    ### TODO: here comes page config calculation

    return templates.TemplateResponse(
        "pages/server.html",
        {
            "request":request,
            "server_id":server_id
            ### TODO:add here page config params
        }
    )

