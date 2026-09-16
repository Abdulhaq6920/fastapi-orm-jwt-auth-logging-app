from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

SOURCE_FILE = Path("logs/app.log")
OUTPUT_FILE = Path("downloads/app-log-copy.log")
router = APIRouter(prefix="/log_file",tags=["logfiles"])
@router.post("/download_logs")
async def generate_file():

    try:

        with open(SOURCE_FILE,'r') as file:
            data = file.read()


        OUTPUT_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )
        with open(OUTPUT_FILE, "w") as file:
            file.write(data)


        return FileResponse(
            OUTPUT_FILE,
            filename="app-log-copy.log"
        )

    except HTTPException:
        raise