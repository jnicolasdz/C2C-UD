from functools import lru_cache
import json
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "UD Marketplace Reports API"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@report_db:5432/marketplace_reports"

    SMTP_HOST: str = "mailpit"
    SMTP_PORT: int = 1025
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "reportes@udmarketplace.local"
    MAIL_ENABLED: bool = True
    MAIL_USE_TLS: bool = False
    ADMIN_REPORT_EMAIL: str = "admin@udmarketplace.local"
    NOTIFY_USER_ON_STATUS_UPDATE: bool = True

    # Se deja como string para aceptar el formato antiguo del proyecto:
    # CORS_ORIGINS=http://localhost:4200,http://localhost:5173
    # También acepta formato JSON:
    # CORS_ORIGINS=["http://localhost:4200","http://localhost:5173"]
    CORS_ORIGINS: str = (
        "http://localhost:3000,http://localhost:4200,http://localhost:5173,"
        "http://localhost:5500,http://127.0.0.1:5500"
    )

    @property
    def cors_origins(self) -> List[str]:
        value = (self.CORS_ORIGINS or "").strip()

        if not value:
            return []

        if value.startswith("["):
            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    return [str(origin).strip() for origin in parsed if str(origin).strip()]
            except json.JSONDecodeError:
                pass

        return [origin.strip() for origin in value.split(",") if origin.strip()]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
