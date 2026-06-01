from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.database.connection import Base


class Report(Base):
    """Database table for marketplace reports."""

    # Change this name if your database table should have another name.
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    radicado = Column(String(60), unique=True, index=True, nullable=False)

    user_name = Column(String(120), nullable=False)
    user_email = Column(String(180), nullable=False)

    report_type = Column(String(100), nullable=False)
    subject = Column(String(180), nullable=False)
    description = Column(Text, nullable=False)

    status = Column(String(40), nullable=False, default="RECIBIDO")
    response_message = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
