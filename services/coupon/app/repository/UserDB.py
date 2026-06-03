from __future__ import annotations

from app.models.User import User
from app.repository.CouponDB import coupon_db


class UserDB:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.users = []
            cls._instance.coupon_db = coupon_db
        return cls._instance

    @staticmethod
    def _coupon_code(coupon_or_code) -> str:
        return getattr(coupon_or_code, "code", coupon_or_code)

    def _resolve_coupon(self, coupon_or_code):
        if hasattr(coupon_or_code, "code"):
            return coupon_or_code
        coupon = self.coupon_db.get_coupon_object_by_code(coupon_or_code)
        if coupon is None:
            raise ValueError(f"Coupon with code {coupon_or_code} does not exist.")
        return coupon

    def get_user_by_email(self, email: str) -> User | None:
        for user in self.users:
            if user.email == email:
                return user
        return None

    def get_user(self, email: str) -> dict | None:
        user = self.get_user_by_email(email)
        return user.to_dict() if user else None

    def get_all_users(self) -> list[dict]:
        return [user.to_dict() for user in self.users]

    def create_user(self, email: str) -> User:
        return User(email=email)

    def add_user(self, email: str) -> User:
        user = self.get_user_by_email(email)
        if user is not None:
            return user
        user = self.create_user(email)
        self.users.append(user)
        return user

    def delete_user(self, email: str) -> None:
        user = self.get_user_by_email(email)
        if user is None:
            raise ValueError(f"User with email {email} does not exist.")
        self.users.remove(user)

    def add_assigned_coupon_to_user(self, email: str, coupon_code: str) -> None:
        user = self.add_user(email)
        coupon = self._resolve_coupon(coupon_code)
        if coupon not in user.assigned_coupons:
            user.assigned_coupons.append(coupon)

    def add_unassigned_coupon_to_user(self, email: str, coupon_code: str) -> None:
        user = self.add_user(email)
        coupon = self._resolve_coupon(coupon_code)
        if coupon not in user.unassigned_coupons:
            user.unassigned_coupons.append(coupon)

    def has_consumed_assigned_coupon(self, email: str, assigned_coupon_code: str) -> bool:
        user = self.get_user_by_email(email)
        if user is None:
            return True
        return not any(coupon.code == assigned_coupon_code for coupon in user.assigned_coupons)

    def has_consumed_unassigned_coupon(self, email: str, unassigned_coupon_code: str) -> bool:
        user = self.get_user_by_email(email)
        if user is None:
            return False
        return any(coupon.code == unassigned_coupon_code for coupon in user.unassigned_coupons)

    def delete_assigned_coupon_from_user(self, email: str, coupon_code: str) -> None:
        user = self.get_user_by_email(email)
        code = self._coupon_code(coupon_code)
        coupon = self._resolve_coupon(coupon_code)
        if user is None:
            raise ValueError(f"User with email {email} does not exist.")
        current = next((c for c in user.assigned_coupons if c.code == code), None)
        if current is None:
            raise ValueError(f"Coupon with code {code} is not in user's assigned coupons.")
        user.assigned_coupons.remove(current)

    def delete_unassigned_coupon_from_user(self, email: str, coupon_code: str) -> None:
        user = self.get_user_by_email(email)
        code = self._coupon_code(coupon_code)
        coupon = self._resolve_coupon(coupon_code)
        if user is None:
            raise ValueError(f"User with email {email} does not exist.")
        current = next((c for c in user.unassigned_coupons if c.code == code), None)
        if current is None:
            raise ValueError(f"Coupon with code {code} is not in user's unassigned coupons.")
        user.unassigned_coupons.remove(current)


user_db = UserDB()
