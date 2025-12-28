from pathlib import Path
from dataclasses import dataclass
import json

core_f = Path(__file__).parent
app_f = core_f.parent
data_f = app_f / "data"
server_data_file = data_f / "server_data.json"

type ServerMetadata = dict[str:str]

def load_ServerMetadata_list() -> list["ServerMetadata"]:
    with open(server_data_file, "r", encoding="utf-8") as f:
        return json.load(f)
    
def load_ServerMetadata_from_service_name(service_name:str) -> "ServerMetadata":
    for metadata in load_ServerMetadata_list():
        if metadata.get("service_name") == service_name:
            return metadata
