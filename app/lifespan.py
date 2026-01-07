import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.machine import stats_loop

@asynccontextmanager
async def lifespan(app: FastAPI):
    stop_event = asyncio.Event()
    task = asyncio.create_task(stats_loop(stop_event))

    yield

    stop_event.set()
    await task








