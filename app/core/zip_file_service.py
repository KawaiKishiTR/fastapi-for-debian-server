from ..core.servers_metadata import ServerMetadata
import hashlib
import json
import zipfile
from pathlib import Path
from fastapi import HTTPException
import shutil

BASE_OUT = Path("/srv/website")
data_dir = BASE_OUT / "app" / "data"
files_dir = BASE_OUT / "files"

def compute_files_hash(src_dir:Path) -> str:
    if not src_dir.exists():
        raise HTTPException(404, "mods folder not exists")
    
    h = hashlib.sha256()
    for file in sorted(src_dir.glob("*")):
        if not file.is_file():
            continue
        h.update(file.name.encode())
    return h.hexdigest()

def build_zip(src_dir:Path, zip_path:Path):
    if not src_dir.exists():
        raise HTTPException(404, "mods folder not exists")
    zip_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for file in src_dir.glob("*"):
            if not file.is_file():
                continue

            z.write(file, arcname=file.name)

def create_zip(zip_path:Path, src_path:Path, meta_key:str = "", server_metadata:ServerMetadata = None):
    if server_metadata is None:
        build_zip(src_path, zip_path)
        return
    
    if zip_path.exists():
        hash_key = compute_files_hash(src_path)
        if server_metadata.get(meta_key) == hash_key:
            return
    
    build_zip(src_path, zip_path.with_suffix(".temp"))
    shutil.move(zip_path.with_suffix(".temp"), zip_path)

    server_metadata[meta_key] = hash_key



    





