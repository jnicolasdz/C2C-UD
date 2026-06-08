"""Modelo de usuario para el microservicio de cupones."""

from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class User(BaseModel):
    user_email: str
    unassigned_coupons: list[Any] = Field(default_factory=list)
    assigned_coupons: list[Any] = Field(default_factory=list)

    def __init__(self, **data):
        if "email" in data and "user_email" not in data:
            data["user_email"] = data.pop("email")
        super().__init__(**data)

    @property
    def email(self) -> str:
        return self.user_email

    def __str__(self) -> str:
        return f"User(user_email={self.user_email})"

    @staticmethod
    def _serialize_coupon(coupon: Any) -> Any:
        if hasattr(coupon, "to_dict"):
            return coupon.to_dict()
        return coupon

    def to_dict(self) -> dict:
        return {
            "email": self.user_email,
            "user": self.user_email,
            "unassigned_coupons": [self._serialize_coupon(coupon) for coupon in self.unassigned_coupons],
            "assigned_coupons": [self._serialize_coupon(coupon) for coupon in self.assigned_coupons],
        }

    def __to_dict__(self) -> dict:
        return {
            "user": self.user_email,
            "unassigned_coupons": [self._serialize_coupon(coupon) for coupon in self.unassigned_coupons],
            "assigned_coupons": [self._serialize_coupon(coupon) for coupon in self.assigned_coupons],
        }
