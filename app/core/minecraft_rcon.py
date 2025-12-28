from mcrcon import MCRcon
from dotenv import load_dotenv
from pathlib import Path

folder = Path(__file__).parent.parent.parent


load_dotenv(folder / ".env")
RCON_HOST="127.0.0.1"

class RconRunner:
    def __init__(self, port, passwd, host=RCON_HOST):
        self.host = host
        self.port = port
        self.passwd = passwd
    
    def run_rcon_command(self, command:str) -> str:
        with MCRcon(host=self.host, password=self.passwd, port=self.port) as mcr:
            response = mcr.command(command)
            return response
        

