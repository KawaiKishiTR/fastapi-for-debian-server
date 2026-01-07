from fastapi import APIRouter
from ..api import servers_endpoints
from ..api import machine

router = APIRouter()

router.include_router(machine.router, prefix="/machine")
router.include_router(servers_endpoints.router, prefix="/servers")
