from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field

ReportStatus = Literal["RECIBIDO", "EN_REVISION", "EN_PROCESO", "RESUELTO", "RECHAZADO", "CERRADO"]


class ReportBase(BaseModel):
    user_name: str = Field(..., min_length=2, max_length=120, examples=["Sebastián Henriquez"])
    user_email: EmailStr = Field(..., examples=["usuario@correo.com"])
    report_type: str = Field(..., min_length=3, max_length=100, examples=["Problema con publicación"])
    subject: str = Field(..., min_length=3, max_length=180, examples=["No aparece mi producto publicado"])
    description: str = Field(..., min_length=10, examples=["El producto fue creado, pero no aparece en el marketplace."])


class ReportCreate(ReportBase):
    pass


class ReportUpdate(BaseModel):
    user_name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    user_email: Optional[EmailStr] = None
    report_type: Optional[str] = Field(default=None, min_length=3, max_length=100)
    subject: Optional[str] = Field(default=None, min_length=3, max_length=180)
    description: Optional[str] = Field(default=None, min_length=10)
    status: Optional[ReportStatus] = None
    response_message: Optional[str] = None


class ReportResponse(ReportBase):
    id: int
    radicado: str
    status: str
    response_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
