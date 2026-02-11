import time
import asyncio
from fastapi import APIRouter, Response, Request
from ..api import servers_endpoints
from ..api import machine

router = APIRouter()

router.include_router(machine.router, prefix="/machine")
router.include_router(servers_endpoints.router, prefix="/servers")

text_queue = asyncio.Queue()

@router.get("/epoch")
async def get_epoch():
    return Response(
        content=str(int(time.time())),
        media_type="text/plain"
    )

@router.get("/get-text")
async def get_text():
    if text_queue.empty():
        return None
    return Response(
        content=await text_queue.get(),
        media_type="text/plain"
    )

@router.post("/text-dump")
async def post_text(request: Request):
    body = await request.body()          
    text = body.decode("utf-8")           

    await text_queue.put(text)
    return Response(status_code=204)