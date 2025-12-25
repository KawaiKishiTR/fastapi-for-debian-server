from fastapi import APIRouter
from collections import deque
import psutil, asyncio

router = APIRouter()

HISTORY_LENGHT = 100
cpu_history = deque(maxlen=HISTORY_LENGHT)
ram_history = deque(maxlen=HISTORY_LENGHT)

@router.get("/api/system-usage")
def systemUsage():
    return {
        "cpu":cpu_history[-1],
        "ram":ram_history[-1]
    }

@router.get("/api/system-history")
def system_history():
    return {
        "cpu":list(cpu_history),
        "ram":list(ram_history)
    }



def _collect_system_usage():
    cpu = psutil.cpu_percent(interval=None)
    mem = psutil.virtual_memory()

    cpu_history.append(cpu)
    ram_history.append(mem.percent)

async def stats_loop(stop_event: asyncio.Event):
    while not stop_event.is_set():
        _collect_system_usage()
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=3)
        except asyncio.TimeoutError:
            pass


