from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.connection import Base, engine
from app.models import Report  # noqa: F401 - required so SQLAlchemy registers the table.
from app.routers.report_router import router as report_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # For academic/local development. In production, use Alembic migrations instead.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Microservicio de reportes para UD Marketplace.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(report_router, prefix=f"{settings.API_V1_PREFIX}/reports", tags=["Reports"])


@app.get("/")
def root():
    return {
        "message": "UD Marketplace Reports API is running",
        "docs": "/docs",
        "reports_endpoint": f"{settings.API_V1_PREFIX}/reports",
    }


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "reports-api"}
