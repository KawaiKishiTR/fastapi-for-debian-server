import asyncio
from mcstatus import JavaServer
from typing import Optional
from ..core.servers_core import VALID_SERVERS
from ..core.servers_metadata import ServerMetadata, ValidKeys

class MCQueryWorker:
    workers:dict[str:"MCQueryWorker"] = {

    }
    def __init__(self, server_id:str, port:int):
        self.server_id = server_id
        self.port = port
        self.task: Optional[asyncio.Task] = None
        self.cache = {
            "online": False,
            "players": 0,
            "max": 0,
            "names": []
        }
        MCQueryWorker.workers[server_id] = self

    async def _run(self, host: str, port: int):
        server = JavaServer(host, port)

        while True:
            try:
                query = await asyncio.to_thread(server.query)

                self.cache["online"] = True
                self.cache["players"] = query.players.online
                self.cache["max"] = query.players.max
                self.cache["names"] = query.players.names or []

            except Exception:
                # server kapalı / query kapalı / timeout
                self.cache["online"] = False
                self.cache["players"] = 0
                self.cache["names"] = []

            await asyncio.sleep(3)

    def start(self):
        if self.task and not self.task.done():
            return

        self.task = asyncio.create_task(self._run("127.0.0.1", self.port))

    def stop(self):
        if self.task:
            self.task.cancel()
            self.task = None

    def get_cache(self):
        return self.cache
    
    def is_running(self):
        return self.task is not None

def create_workers():
    for server_id in VALID_SERVERS:
        metadata = ServerMetadata.init_Wserver_id(server_id)
        if metadata.get(ValidKeys.HAS_QUERY):
            MCQueryWorker(server_id, metadata[ValidKeys.QUERY_PORT])
