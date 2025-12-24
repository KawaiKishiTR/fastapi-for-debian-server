from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import mc_survival, root, servers, machine

app = FastAPI()

# Static
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")

# Routers
app.include_router(root.router)
app.include_router(machine.router, prefix="/machine")
app.include_router(servers.router, prefix="/servers")
app.include_router(mc_survival.router, prefix="/servers/mc-survival")