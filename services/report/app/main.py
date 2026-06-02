from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.connection import Base, engine
from app.routers.report_router import router as report_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.1.0",
    description="Microservicio de reportes para UD Marketplace con persistencia, filtros, estados de envío y reintentos.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(report_router, prefix=f"{settings.API_V1_PREFIX}/reports", tags=["Reports"])


@app.get("/")
def root():
    return {
        "service": "reports",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "reports",
    }
