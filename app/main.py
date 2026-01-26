from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import root, servers
from app.api import main as api
from app.lifespan import lifespan
from app.core.minecraft_query import create_workers


app = FastAPI(lifespan=lifespan)
create_workers()

# Static
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")
app.mount("/files", StaticFiles(directory="files"), name="files")

# Routers
app.include_router(root.router)
app.include_router(api.router, prefix="/api/v1")
app.include_router(servers.router, prefix="/servers")
