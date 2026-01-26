import asyncio
from ..core.log_stream import linux_service_log_stream
from ..core.servers_metadata import ServerMetadata, ValidKeys
from ..core.linux_services import ServerService
from ..core import zip_file_service as zipfile
from ..core.minecraft_query import MCQueryWorker
from fastapi.responses import FileResponse, StreamingResponse
from fastapi import APIRouter, Header, HTTPException
from time import strftime
from pathlib import Path

router = APIRouter()

def get_file_time_name():
    return strftime("%Y-%m-%d.%H-%M")

### STATUS BAR
@router.get("/status")
async def get_status(x_server_id: str = Header(...)):
    try:
        meta = ServerMetadata.init_Wserver_id(x_server_id)
        service_name = meta["service_name"]

        active = await ServerService(service_name).is_active()
        if meta.get(ValidKeys.HAS_QUERY):
            worker = MCQueryWorker.workers.get(x_server_id)
            if active and not worker.is_running():
                worker.start()
            elif not active and worker.is_running():
                worker.stop()
            
        return {"active": active}

    except Exception as e:
        print("STATUS ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))

### BUTTONS
@router.post("/start")
async def start_server(x_server_id:str = Header(None)):
    service_name = ServerMetadata.init_Wserver_id(x_server_id)["service_name"]
    await ServerService(service_name).start()

@router.post("/stop")
async def stop_server(x_server_id:str = Header(None)):
    service_name = ServerMetadata.init_Wserver_id(x_server_id)["service_name"]
    await ServerService(service_name).stop()

@router.post("/restart")
async def restart_server(x_server_id:str = Header(None)):
    service_name = ServerMetadata.init_Wserver_id(x_server_id)["service_name"]
    await ServerService(service_name).restart()

### LOG STREAM
@router.get("/log-stream")
async def log_stream(x_server_id:str = Header(None)):
    service_name = ServerMetadata.init_Wserver_id(x_server_id)["service_name"]
    return StreamingResponse(
        linux_service_log_stream(service_name),
        media_type="text/plain"
    )

### DOWNLOADABLE FILE ENDPOINTS
@router.get("/download-mods-zip")
async def download_mods_zip(x_server_id:str):
    server_metadata = ServerMetadata.init_Wserver_id(x_server_id)
    mods_dir = Path(server_metadata["folder"]) / "client_mods"
    zip_path = zipfile.files_dir / x_server_id / "mods.zip"

    zipfile.create_zip(zip_path, mods_dir, "mods_hash_key", server_metadata)

    return FileResponse(
        str(zip_path),
        filename=f"mods-{get_file_time_name()}.zip",
        media_type="application/zip"
    )

@router.get("/download-resourcepacks-zip")
async def download_mods_zip(x_server_id:str):
    server_metadata = ServerMetadata.init_Wserver_id(x_server_id)
    mods_dir = Path(server_metadata["folder"]) / "resourcepacks"
    zip_path = zipfile.files_dir / x_server_id / "resourcepacks.zip"

    zipfile.create_zip(zip_path, mods_dir, "resourcepacks_hash_key", server_metadata)

    return FileResponse(
        str(zip_path),
        filename=f"resourcepacks-{get_file_time_name()}.zip",
        media_type="application/zip"
    )

@router.get("/get-query-data")
async def get_query_data(x_server_id:str):
    worker = MCQueryWorker.workers.get(x_server_id)
    if worker is None:
        raise HTTPException(404, "query worker not found")
    
    return worker.get_cache()
