from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import mc_survival, mc_redstone, mc_sweet, fc_vanilla, fc_krastorio2, root, servers, machine
from app.lifespan import lifespan


app = FastAPI(lifespan=lifespan)

# Static
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")
app.mount("/files", StaticFiles(directory="files"), name="files")

# Routers
app.include_router(root.router)
app.include_router(machine.router, prefix="/machine")
app.include_router(servers.router, prefix="/servers")
app.include_router(mc_sweet.router, prefix="/servers/mc-sweet")
app.include_router(mc_survival.router, prefix="/servers/mc-survival")
app.include_router(mc_redstone.router, prefix="/servers/mc-redstone")
app.include_router(mc_redstone.router, prefix="/servers/mc-redstone")
app.include_router(fc_vanilla.router, prefix="/servers/fc-vanilla")
app.include_router(fc_krastorio2.router, prefix="/servers/fc-krastorio2")
