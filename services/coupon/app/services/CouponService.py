from app.services.CouponFactory import coupon_factory
from app.services.CouponConsumtion import coupon_consumption
from app.repository.CouponDB import coupon_db
from app.repository.UserDB import user_db
from app.schemas.COUPON_RULES import COUPON_RULES

import datetime

class CouponService :

    def __init__(self):
        self.coupon_factory = coupon_factory
        self.coupon_consumption = coupon_consumption
        self.coupon_db = coupon_db
        self.user_db = user_db
    
    def get_coupon_by_code(self, code: str):
        return self.coupon_db.get_coupon_by_code(code)
    
    def get_coupon_by_creation_date(self, date: datetime):
        return self.coupon_db.get_coupon_by_creation_date(date)
    
    def get_coupon_by_expiration_date(self, date: datetime):
        return self.coupon_db.get_coupon_by_expiration_date(date)
    
    def get_expired_coupons(self):
        return self.coupon_db.get_expired_coupons()
    
    def get_valid_coupons(self):
        return self.coupon_db.get_valid_coupons()

    def get_enabled_coupons(self):
        return self.coupon_db.get_coupon_by_enabled(True)
    
    def get_disabled_coupons(self):
        return self.coupon_db.get_coupon_by_enabled(False)
    
    def get_coupons_by_text(self, text: str):
        return self.coupon_db.get_coupons_by_text(text)
    
    def get_happy_birthday_coupons(self):
        return self.coupon_db.get_coupons_by_text(COUPON_RULES.HAPPY_BIRTHDAY_COUPON_TEXT)
    
    def get_referred_coupons(self):
        return self.coupon_db.get_coupons_by_text(COUPON_RULES.REFERRED_COUPON_TEXT)

    def get_last_coupon_by_text(self, text: str):
        return self.coupon_db.get_last_coupon_by_text(text)
    
    def get_all_coupons(self):
        return self.coupon_db.get_all_coupons()
    
    def enable_coupon(self, code: str):
        self.coupon_db.enable_coupon(code)
    
    def disable_coupon(self, code: str):
        self.coupon_db.disable_coupon(code)
    
    def is_enable_coupon(self, code: str) -> bool:
        return self.coupon_db.is_enable_coupon(code)
    
    def delete_coupon(self, code: str):
        self.coupon_db.delete_coupon(code)

    def create_unassigned_coupon(self, text: str, discount: float, days: int):
        self.coupon_db.add_coupon(self.coupon_factory.create_coupon(text, discount, days))
        
    def create_assigned_coupon(self, text: str, discount: float, days: int, user_email: str):
        new_coupon = self.coupon_factory.create_coupon(text, discount, days)
        self.coupon_db.add_coupon(new_coupon)
        self.user_db.add_assigned_coupon_to_user(user_email, new_coupon["code"])

    def create_happy_birthday_coupon(self, user_email: str):
        new_coupon = self.coupon_factory.create_happy_birthday_coupon()
        self.coupon_db.add_coupon(new_coupon)
        self.user_db.add_assigned_coupon_to_user(user_email, new_coupon["code"])
    
    def create_referred_coupon(self, user_email: str):
        new_coupon = self.coupon_factory.create_referred_coupon()
        self.coupon_db.add_coupon(new_coupon)
        self.user_db.add_assigned_coupon_to_user(user_email, new_coupon["code"])

    def get_user_coupons(self, email: str):
        user = self.user_db.get_user_by_email(email)
        if user is not None:
            return {
                "assigned_coupons": [coupon.to_dict() for coupon in user.assigned_coupons],
                "unassigned_coupons": [coupon.to_dict() for coupon in user.unassigned_coupons]
            }
        else:
            raise ValueError(f"User with email {email} does not exist.")
        
    def get_all_users_coupons(self):
        users = self.user_db.get_all_users()
        return {user['email']: {
                "assigned_coupons": [coupon.to_dict() for coupon in user['assigned_coupons']],
                "unassigned_coupons": [coupon.to_dict() for coupon in user['unassigned_coupons']]
            } for user in users}
    
    def delete_asigned_coupon_from_user(self, email: str, coupon_code: str):
        user = self.user_db.get_user_by_email(email)
        if user is not None:
            self.user_db.add_unassigned_coupon_to_user(email, coupon_code)
        else:
            raise ValueError(f"User with email {email} does not exist.")
    
    def apply_assigned_coupon(self, email: str, coupon_code: str, original_price: float) -> float:
        return self.coupon_consumption.apply_assigned_coupon(email, coupon_code, original_price)

    def apply_unassigned_coupon(self, email: str, coupon_code: str, original_price: float) -> float:
        return self.coupon_consumption.apply_unassigned_coupon(email, coupon_code, original_price)

    



    