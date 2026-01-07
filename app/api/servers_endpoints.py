import asyncio
from ..core.log_stream import linux_service_log_stream
from ..core.servers_metadata import SERVER_METADATA, reload_server_metadata
from ..core.linux_services import ServerService
from ..core import zip_file_service as zipfile
from fastapi import APIRouter, Header, HTTPException
from pathlib import Path
from fastapi.responses import FileResponse, StreamingResponse

router = APIRouter()

def _get_service_name_from_id(id:str):
    metadata = SERVER_METADATA.get(id)
    if not metadata:
        raise HTTPException(400, "Invalid server id")
    
    return metadata["service_name"]

def _get_folder_from_id(id):
    metadata = SERVER_METADATA.get(id)
    if not metadata:
        raise HTTPException(400, "Invalid server id")
    
    return metadata["folder"]

### STATUS BAR
@router.get("/status")
async def get_status(x_server_id:str = Header(None)):
    service_name = _get_service_name_from_id(x_server_id)
    return await ServerService(service_name).is_active()

### BUTTONS
@router.post("/start")
async def start_server(x_server_id:str = Header(None)):
    service_name = _get_service_name_from_id(x_server_id)
    await ServerService(service_name).start()

@router.post("/stop")
async def stop_server(x_server_id:str = Header(None)):
    service_name = _get_service_name_from_id(x_server_id)
    await ServerService(service_name).stop()

@router.post("/restart")
async def restart_server(x_server_id:str = Header(None)):
    service_name = _get_service_name_from_id(x_server_id)
    await ServerService(service_name).restart()

### LOG STREAM
@router.get("/log_stream")
async def log_stream(x_server_id:str = Header(None)):
    service_name = _get_service_name_from_id(x_server_id)
    return StreamingResponse(
        linux_service_log_stream(service_name),
        media_type="text/plain"
    )

### DOWNLOADABLE FILE ENDPOINTS
@router.get("/download-mods-zip")
async def download_mods_zip(x_server_id:str = Header(None)):
    mods_dir = Path(_get_folder_from_id(x_server_id)) / "mods" #TODO: data yapısı değişince değişicek
    zip_path = zipfile.files_dir / x_server_id / "mods.zip"
    data_dir = zipfile.data_dir / x_server_id
    data_dir.mkdir(parents=True, exist_ok=True)
    data_file = data_dir / "metadata.json"

    zipfile.create_zip(zip_path, mods_dir, "mods_hash_key", data_file)

    return FileResponse(str(zip_path))

@router.get("/download-resourcepacks-zip")
async def download_mods_zip(x_server_id:str = Header(None)):
    mods_dir = Path(_get_folder_from_id(x_server_id)) / "resourcepacks" #TODO: data yapısı değişince değişicek
    zip_path = zipfile.files_dir / x_server_id / "resourcepacks.zip"
    data_dir = zipfile.data_dir / x_server_id
    data_dir.mkdir(parents=True, exist_ok=True)
    data_file = data_dir / "metadata.json"

    zipfile.create_zip(zip_path, mods_dir, "resourcepacks_hash_key", data_file)

    return FileResponse(str(zip_path))

### RELOAD ALL METADATA
@router.get("/reload-metadata")
async def reload_metadata():
    reload_server_metadata()
    return SERVER_METADATA
