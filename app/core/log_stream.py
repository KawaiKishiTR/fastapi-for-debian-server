import re
import asyncio
from fastapi.responses import StreamingResponse

MAX_LINE_LENGHT = 200
SYSTEMD_PREFIX = re.compile(
    r"^\w{3}\s+\d+\s[\d:]+\s[\w\-]+\s[\w\-]+\[\d+\]:\s*"
)

def clean_log_line(line:str) -> str:
    return SYSTEMD_PREFIX.sub("", line)

def split_long_line(line:str, max_len:int):
    return [
        line[i:i + max_len]
        for i in range(0, len(line), max_len)
    ]

async def linux_service_log_stream(service_name):
    process = await asyncio.create_subprocess_exec(
        "journalctl", "-u", service_name,
        "-f", "-n", "20",
        "-o", "cat",
        "--no-hostname",
        "--no-pager",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    try:
        while True:
            line = await process.stdout.readline()
            if not line:
                await asyncio.sleep(0.1)
                continue

            decoded = line.decode("utf-8", errors="ignore").rstrip()
            cleaned = clean_log_line(decoded)

            for part in split_long_line(cleaned, MAX_LINE_LENGHT):
                yield part + "\n"
    
    except asyncio.CancelledError:
        process.terminate()
        raise

