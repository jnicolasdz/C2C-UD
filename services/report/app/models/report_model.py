from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.database.connection import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    radicado = Column(String(50), unique=True, index=True, nullable=False)

    # Datos del usuario emisor del reporte.
    user_id = Column(String(80), nullable=True, index=True)
    user_name = Column(String(120), nullable=False)
    user_email = Column(String(150), nullable=False, index=True)

    report_type = Column(String(80), nullable=False)
    subject = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)

    # Estado funcional del reporte dentro de la gestión.
    status = Column(String(50), default="RECIBIDO", nullable=False, index=True)

    # Estado técnico del envío/notificación del reporte.
    # Valores esperados: PENDIENTE, ENVIADO, FALLIDO.
    send_status = Column(String(50), default="PENDIENTE", nullable=False, index=True)
    delivery_message = Column(Text, nullable=True)
    send_attempts = Column(Integer, default=0, nullable=False)
    retry_count = Column(Integer, default=0, nullable=False)
    last_send_attempt_at = Column(DateTime(timezone=True), nullable=True)

    # Auditoría básica. DELETE se maneja como eliminación lógica para no perder trazabilidad.
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
