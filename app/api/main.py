import time
from fastapi import APIRouter, Response
from ..api import servers_endpoints
from ..api import machine

router = APIRouter()

router.include_router(machine.router, prefix="/machine")
router.include_router(servers_endpoints.router, prefix="/servers")



@router.get("/epoch")
def get_epoch():
    return Response(
        content=str(int(time.time())),
        media_type="text/plain"
    )