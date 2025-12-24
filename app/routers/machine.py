from fastapi import APIRouter
from ..core.linux_services import is_systemctl_available
import psutil

router = APIRouter()

@router.get("/api/system-usage")
def systemUsage():
    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()

    return {
        "cpu":cpu,
        "memory_percent":mem.percent
    }



