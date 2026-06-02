import sys
from pathlib import Path
from fastapi import FastAPI
import uvicorn

# Allow running this file directly: python ./app/main.py
if __package__ is None or __package__ == "":
	sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.api.v1.routers import router

app = FastAPI(title="Cuopon Service")
app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
	uvicorn.run(app, host="127.0.0.1", port=8000)


