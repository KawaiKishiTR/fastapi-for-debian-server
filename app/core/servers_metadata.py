from pathlib import Path
import json
from typing import TypedDict

core_dir = Path(__file__).parent
app_dir = core_dir.parent
data_dir = app_dir / "data"
server_data_file = data_dir / "server_data.json"

class ServerMetadata(TypedDict):
    display_name:str
    service_name:str
    endpoint:str
    server_type:str
    folder:str
type ServerMetadataDict = dict[str:ServerMetadata]
type ServerMetadataList = list[ServerMetadata]

def load_ServerMetadata_list() -> ServerMetadataList:
    with open(server_data_file, "r", encoding="utf-8") as f:
        return json.load(f)

def load_ServerMetadata_dict() -> ServerMetadataDict:
    data = load_ServerMetadata_list()

    result:ServerMetadataDict = {}
    for metadata in data:
        result[metadata["endpoint"]] = metadata

    return result

def load_ServerMetadata_from_key(key:str, value:str) -> ServerMetadata:
    for metadata in load_ServerMetadata_list():
        if metadata.get(key) == value:
            return metadata

def load_ServerMetadata_from_service_id(service_id:str):
    metadata_f = data_dir / service_id / "metadata.json"
    return json.loads(metadata_f.read_text())


SERVER_METADATA:ServerMetadataDict = load_ServerMetadata_dict()
def reload_server_metadata():
    global SERVER_METADATA
    SERVER_METADATA = load_ServerMetadata_dict()
