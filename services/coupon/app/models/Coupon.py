"""
Modelo de cupón para el microservicio de cupones.

Se ajustó para que pueda ser usado desde formularios reales del frontend:
- genera código automáticamente cuando no se envía,
- serializa fechas de forma segura,
- mantiene compatibilidad con los endpoints existentes.
"""

from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel


class Coupon(BaseModel):
    code: str = ""
    id: int
    text: str
    discount: float
    creation_date: datetime
    expiration_date: datetime
    enabled: bool = True

    def __init__(self, **data):
        super().__init__(**data)
        if not self.code:
            object.__setattr__(self, "code", f"{self.text}{self.id}")

    def __str__(self) -> str:
        return (
            f"Coupon(code={self.code}, discount={self.discount},"
            f"creation_date={self.creation_date}, expiration_date={self.expiration_date}, enabled={self.enabled})"
        )

    @staticmethod
    def _date_value(value):
        return value.isoformat() if hasattr(value, "isoformat") else value

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "id": self.id,
            "text": self.text,
            "discount": self.discount,
            "creation_date": self._date_value(self.creation_date),
            "expiration_date": self._date_value(self.expiration_date),
            "enabled": self.enabled,
        }

    def __to_dict__(self) -> dict:
        return {
            "code": self.code,
            "discount": self.discount,
            "expiration_date": self._date_value(self.expiration_date),
            "enabled": self.enabled,
        }
