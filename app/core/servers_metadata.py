from pathlib import Path
from .servers_core import ServerID, VALID_SERVERS
from .linux_services import ServerService
from enum import Enum
import asyncio
import json

core_dir = Path(__file__).parent
app_dir = core_dir.parent
data_dir = app_dir / "data"


class ValidKeys(Enum):
    DISPLAY_NAME = "display_name"
    SERVICE_NAME = "service_name"
    SERVER_ID = "server_id"
    SERVER_TYPE = "server_type"
    FOLDER = "folder"

    HAS_MODS = "has_mods"
    HAS_RESOURCEPACKS = "has_resourcepacks"
    IS_RUNABLE = "is_runable"
    RUNNING_SERVER_NAME = "running_server_name"


class ServerMetadata:
    @classmethod
    def init_Wserver_id(cls, server_id:ServerID):
        data_file = data_dir / server_id / "metadata.json"
        return cls.init_Wmetadata_file(data_file)

    @classmethod
    def init_Wmetadata_file(cls, file_path:Path, create_file:bool = False):
        if not file_path.exists():
            if not create_file:
                raise FileNotFoundError(f"{str(file_path)} already exists")
            file_path.touch()
            file_path.write_text(json.dumps({}, indent=4))
        
        metadata = cls(json.loads(file_path.read_text()))
        metadata.file_path = file_path
        return metadata

    def __init__(self, data:dict):
        self.data = data
        self.file_path:Path = None

    def __str__(self):
        return json.dumps(self.data, indent=4)
    
    def get(self, key:str | ValidKeys, default = None):
        return self.data.get(key, default)

    def __getitem__(self, key:ValidKeys):
        return self.data[key]

    def __setitem__(self, key:str | ValidKeys, value):
        self.data[key] = value
        
        if self.file_path is None:
            return
        
        self.file_path.write_text(json.dumps(self.data, indent=4))

    async def page_init(self):
        result = {}

        result[ValidKeys.HAS_MODS] = self.get(ValidKeys.HAS_MODS, False)
        result[ValidKeys.HAS_RESOURCEPACKS] = self.get(ValidKeys.HAS_RESOURCEPACKS, False)
        result[ValidKeys.IS_RUNABLE] = self.get(ValidKeys.IS_RUNABLE, False)
        result[ValidKeys.RUNNING_SERVER_NAME] = None

        running_server_name = await is_there_any_running_server(self.get(ValidKeys.SERVER_ID))
        if running_server_name is not None:
            result[ValidKeys.IS_RUNABLE] = False
            result[ValidKeys.RUNNING_SERVER_NAME] = running_server_name
        
        return result

async def is_there_any_running_server(this_server_id:str):
    for server_id in VALID_SERVERS:
        if server_id == this_server_id:
            continue

        server_metadata = ServerMetadata.init_Wserver_id(server_id)
        linux_service = ServerService(server_metadata.get(ValidKeys.SERVICE_NAME))

        print(server_id, linux_service.service_name)

        if await linux_service.is_active():
            return server_metadata.get(ValidKeys.DISPLAY_NAME)
    return None


        