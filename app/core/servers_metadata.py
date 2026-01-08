from pathlib import Path
import json
from typing import Literal

core_dir = Path(__file__).parent
app_dir = core_dir.parent
data_dir = app_dir / "data"

class ServerMetadata:
    type ValidServerIds = Literal["mc-survival", "mc-redstone", "mc-sweet", "fc-vanilla", "fc-krastorio2"]
    type ValidKeys = Literal["display_name", "service_name", "server_id", "server_type", "folder"]
    @classmethod
    def init_Wserver_id(cls, server_id:ValidServerIds):
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
        return self.data.get[key]

    def __setitem__(self, key:str | ValidKeys, value):
        self.data[key] = value
        
        if self.file_path is None:
            return
        
        self.file_path.write_text(json.dumps(self.data, indent=4))

