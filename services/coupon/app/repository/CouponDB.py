from __future__ import annotations

from datetime import datetime
from app.models.Coupon import Coupon


class CouponDB:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.coupons = []
        return cls._instance

    @staticmethod
    def _parse_date(value) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)
            except ValueError:
                return datetime.strptime(value, "%Y-%m-%d")
        return value

    def get_coupon_object_by_code(self, code: str) -> Coupon | None:
        for coupon in self.coupons:
            if coupon.code == code:
                return coupon
        return None

    def get_coupon_by_code(self, code: str) -> dict | None:
        coupon = self.get_coupon_object_by_code(code)
        return coupon.to_dict() if coupon else None

    def get_coupon_by_creation_date(self, date) -> list[dict]:
        target = self._parse_date(date).date()
        return [coupon.to_dict() for coupon in self.coupons if coupon.creation_date.date() == target]

    def get_coupon_by_expiration_date(self, date) -> list[dict]:
        target = self._parse_date(date).date()
        return [coupon.to_dict() for coupon in self.coupons if coupon.expiration_date.date() == target]

    def get_expired_coupons(self) -> list[dict]:
        now = datetime.now()
        return [coupon.to_dict() for coupon in self.coupons if coupon.expiration_date < now]

    def get_valid_coupons(self) -> list[dict]:
        now = datetime.now()
        return [coupon.to_dict() for coupon in self.coupons if coupon.expiration_date >= now and coupon.enabled]

    def get_coupon_by_enabled(self, enabled: bool) -> list[dict]:
        return [coupon.to_dict() for coupon in self.coupons if coupon.enabled == enabled]

    def get_coupons_by_text(self, text: str) -> list[dict]:
        query = text.lower().strip()
        return [coupon.to_dict() for coupon in self.coupons if query in coupon.text.lower()]

    def get_last_coupon_by_text(self, text: str) -> dict | None:
        query = text.lower().strip()
        coupons = [coupon for coupon in self.coupons if query in coupon.text.lower()]
        if not coupons:
            return None
        return max(coupons, key=lambda c: c.id).to_dict()

    def get_all_coupons(self) -> list[dict]:
        return [coupon.to_dict() for coupon in self.coupons]

    def enable_coupon(self, code: str) -> None:
        coupon = self.get_coupon_object_by_code(code)
        if coupon is None:
            raise ValueError(f"Coupon with code {code} does not exist.")
        coupon.enabled = True

    def disable_coupon(self, code: str) -> None:
        coupon = self.get_coupon_object_by_code(code)
        if coupon is None:
            raise ValueError(f"Coupon with code {code} does not exist.")
        coupon.enabled = False

    def is_enable_coupon(self, code: str) -> bool:
        coupon = self.get_coupon_object_by_code(code)
        if coupon is None:
            raise ValueError(f"Coupon with code {code} does not exist.")
        return bool(coupon.enabled)

    def create_coupon(self, text: str, id: int, discount: float, expiration_date) -> Coupon:
        return Coupon(
            text=text,
            id=id,
            discount=discount,
            creation_date=datetime.now(),
            expiration_date=self._parse_date(expiration_date),
            enabled=True,
        )

    def delete_coupon(self, code: str) -> None:
        coupon = self.get_coupon_object_by_code(code)
        if coupon is None:
            raise ValueError(f"Coupon with code {code} does not exist.")
        self.coupons.remove(coupon)

    def add_coupon(self, new_coupon: Coupon):
        if self.get_coupon_object_by_code(new_coupon.code) is not None:
            raise ValueError(f"Coupon with code {new_coupon.code} already exists.")
        self.coupons.append(new_coupon)


coupon_db = CouponDB()
