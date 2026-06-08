from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class ReportManagementStatus(str, Enum):
    RECIBIDO = "RECIBIDO"
    EN_REVISION = "EN_REVISION"
    EN_PROCESO = "EN_PROCESO"
    RESUELTO = "RESUELTO"
    RECHAZADO = "RECHAZADO"
    CERRADO = "CERRADO"


class ReportSendStatus(str, Enum):
    PENDIENTE = "PENDIENTE"
    ENVIADO = "ENVIADO"
    FALLIDO = "FALLIDO"


class ReportBase(BaseModel):
    user_id: Optional[str] = Field(default=None, description="Identificador del usuario emisor si existe en el marketplace")
    user_name: str = Field(..., min_length=2, max_length=120)
    user_email: EmailStr
    report_type: str = Field(..., min_length=2, max_length=80)
    subject: str = Field(..., min_length=3, max_length=150)
    description: str = Field(..., min_length=5)


class ReportCreate(ReportBase):
    pass


class ReportUpdate(BaseModel):
    user_id: Optional[str] = None
    user_name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    user_email: Optional[EmailStr] = None
    report_type: Optional[str] = Field(default=None, min_length=2, max_length=80)
    subject: Optional[str] = Field(default=None, min_length=3, max_length=150)
    description: Optional[str] = Field(default=None, min_length=5)
    status: Optional[ReportManagementStatus] = None
    send_status: Optional[ReportSendStatus] = None
    delivery_message: Optional[str] = None


class ReportResponse(ReportBase):
    id: int
    radicado: str
    status: str
    send_status: str
    delivery_message: Optional[str] = None
    send_attempts: int
    retry_count: int
    last_send_attempt_at: Optional[datetime] = None
    is_deleted: bool
    deleted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ReportActionResponse(BaseModel):
    success: bool
    message: str
    send_status: str
    retry_available: bool = False
    notification_sent: Optional[bool] = None
    report: ReportResponse
