import platform
import shutil
import asyncio


def is_systemctl_available() -> bool:
    return (
        platform.system() == "Linux"
        and shutil.which("systemctl") is not None
    )

class ServerService:
    #============================
    #===== INSTANCE METHODS =====
    #============================
    def __init__(self, service_name:str):
        self.service_name = service_name
    
    async def start(self):
        await self._run_systemctl("start", self.service_name)
    async def stop(self):
        await self._run_systemctl("stop", self.service_name)
    async def restart(self):
        await self._run_systemctl("restart", self.service_name)

    async def is_active(self):
        return await self._is_active(self.service_name)


    #==========================
    #===== STATIC METHODS =====
    #==========================
    @staticmethod
    async def _run_systemctl(action: str, service_name: str) -> bool:
        if not is_systemctl_available():
            raise RuntimeError("systemctl bu ortamda kullanılamaz")

        proc = await asyncio.create_subprocess_exec(
            "sudo", "systemctl", action, service_name,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        await proc.communicate()
        return proc.returncode == 0
    
    @staticmethod
    async def _is_active(service_name:str) -> bool:
        if not is_systemctl_available():
            return False
        
        proc = await asyncio.create_subprocess_exec(
            "systemctl", "is-active", service_name,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, _ = await proc.communicate()
        return stdout.decode().strip() == "active"
    

