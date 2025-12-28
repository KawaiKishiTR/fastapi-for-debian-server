from mcrcon import MCRcon
from pathlib import Path
from pydantic import BaseModel
from fastapi import HTTPException


folder = Path(__file__).parent.parent.parent

class CommandLine(BaseModel):
    command:str

RCON_HOST="127.0.0.1"

def run_rcon_command(command:str, port:int, passwd:str, host=RCON_HOST) -> str:
    with MCRcon(host=host, password=passwd, port=port) as mcr:
        response = mcr.command(command)
        return response

def send_rcon_command(command: CommandLine, port:int, passwd:str, host=RCON_HOST):
    cmd = command.command.strip()

    if not cmd:
        raise HTTPException(status_code=400, detail="Boş Komut")
    
    try:
        output = run_rcon_command(cmd, port, passwd, host)
        return {"output":output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))