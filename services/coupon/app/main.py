from fastapi import FastAPI
from pathlib import Path
import sys


# Allow running this file directly: python ./app/main.py
if __package__ is None or __package__ == "":
	sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.api.v1.routes import router


app = FastAPI(
    title="Marketplace - Módulo de Descuentos, Cupones y Notificaciones",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")



