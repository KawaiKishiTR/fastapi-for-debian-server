from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..core.linux_services import ServerService
from ..core.servers_metadata import load_ServerMetadata_from_service_name
