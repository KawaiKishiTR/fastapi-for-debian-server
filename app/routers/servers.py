from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..core.servers_core import VALID_SERVERS
from ..core.servers_metadata import ServerMetadata
import asyncio

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def root_page(request: Request):
    return templates.TemplateResponse(
        "pages/servers.html",
        {"request": request}
    )



@router.get("/{server_id}", response_class=HTMLResponse)
async def server_page(request: Request, server_id:str):
    if server_id not in VALID_SERVERS:
        raise HTTPException(404, detail="Server Not Found")
    
    return templates.TemplateResponse(
        "pages/server.html",
        {
            "request":request,
            "server_id":server_id,
            "metadata": await ServerMetadata.init_Wserver_id(server_id).page_init()
        }
    )

