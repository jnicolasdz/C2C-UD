"""Fábrica de cupones con reglas predefinidas."""

from __future__ import annotations

from app.models.Coupon import Coupon
from app.repository.CouponDB import coupon_db
from app.schemas.COUPON_RULES import COUPON_RULES


class CouponFactory:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.coupon_db = coupon_db
            cls._instance.happy_birthday = COUPON_RULES.HAPPY_BIRTHDAY_COUPON_TEXT
            cls._instance.happy_birthday_discount = COUPON_RULES.HAPPY_BIRTHDAY_DISCOUNT
            cls._instance.happy_birthday_index = 0
            cls._instance.referred = COUPON_RULES.REFERRED_COUPON_TEXT
            cls._instance.referred_discount = COUPON_RULES.REFERRED_DISCOUNT
            cls._instance.referred_index = 0
        return cls._instance

    @staticmethod
    def _last_id(last) -> int | None:
        if last is None:
            return None
        if isinstance(last, dict):
            return last.get("id")
        return getattr(last, "id", None)

    def _next_id_for_text(self, text: str) -> int:
        last = self.coupon_db.get_last_coupon_by_text(text)
        last_id = self._last_id(last)
        return 1 if last_id is None else int(last_id) + 1

    def create_coupon(self, text: str, discount: float, days: int) -> Coupon:
        expiration_date = COUPON_RULES.get_expiration_date(days)
        # El primer genérico conserva el ID 0 del diseño original; los siguientes incrementan
        # para que el frontend pueda crear varios casos de prueba sin chocar códigos.
        last_id = self._last_id(self.coupon_db.get_last_coupon_by_text(text))
        coupon_id = 0 if last_id is None else int(last_id) + 1
        return self.coupon_db.create_coupon(text, coupon_id, discount, expiration_date)

    def create_happy_birthday_coupon(self) -> Coupon:
        self.happy_birthday_index = self._next_id_for_text(self.happy_birthday)
        return self.coupon_db.create_coupon(
            self.happy_birthday,
            self.happy_birthday_index,
            self.happy_birthday_discount,
            COUPON_RULES.get_happy_birthday_expiration_date(),
        )

    def create_referred_coupon(self) -> Coupon:
        self.referred_index = self._next_id_for_text(self.referred)
        return self.coupon_db.create_coupon(
            self.referred,
            self.referred_index,
            self.referred_discount,
            COUPON_RULES.get_referred_expiration_date(),
        )


coupon_factory = CouponFactory()
