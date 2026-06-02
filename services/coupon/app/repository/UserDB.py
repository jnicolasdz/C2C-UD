
from app.models.Coupon import Coupon
from app.models.User import User
from app.repository.CouponDB import coupon_db

class UserDB :
    
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.users = []
            cls._instance.coupon_db = coupon_db
        return cls._instance
    
    def get_user(self, email: str) -> User:
        for user in self.users:
            if user.email == email:
                return user.to_dict()
        return None
    
    def get_all_users(self) -> list[User]:
        return [user.to_dict() for user in self.users]
    
    def create_user(self, email: str) -> User:
        new_user = User(email=email)
        return new_user

    def delete_user(self, email: str) -> None:
        user = self.get_user_by_email(email)
        if user is not None:
            self.users.remove(user)
        else:
            raise ValueError(f"User with email {email} does not exist.")
    
    def add_user(self, email: str):
        new_user = self.create_user(email)
        if self.get_user_by_email(email) is not None:
            raise ValueError(f"User with email {email} already exists.")
        else:
            self.users.append(new_user)
    
    def add_assigned_coupon_to_user(self, email: str, coupon_code: str) -> None:
        user = self.get_user_by_email(email)
        coupon = self.coupon_db.get_coupon_by_code(coupon_code)
        if coupon is None:
            raise ValueError(f"Coupon with code {coupon_code} does not exist.")
        if user is not None:
            user.assigned_coupons.append(coupon)
        else:
            raise ValueError(f"User with email {email} does not exist.")
        
    def add_unassigned_coupon_to_user(self, email: str, coupon_code : str) -> None:
        user = self.get_user_by_email(email)
        coupon = self.coupon_db.get_coupon_by_code(coupon_code)
        if coupon is None:
            raise ValueError(f"Coupon with code {coupon_code} does not exist.")
        if user is not None:
            user.unassigned_coupons.append(coupon)
        else:
            raise ValueError(f"User with email {email} does not exist.")
    
    def has_consumed_assigned_coupon(self, email: str, assigned_coupon_code: str) -> bool:
        user = self.get_user_by_email(email)
        coupon = self.coupon_db.get_coupon_by_code(assigned_coupon_code)
        if coupon is None:
            raise ValueError(f"Coupon with code {assigned_coupon_code} does not exist.")
        for coupon in user.assigned_coupons:
            if coupon.code == assigned_coupon_code:
                return False
        return True
    
    def has_consumed_unassigned_coupon(self, email: str, unassigned_coupon_code : str) -> bool:
        user = self.get_user_by_email(email)
        coupon = self.coupon_db.get_coupon_by_code(unassigned_coupon_code)
        if coupon is None:
            raise ValueError(f"Coupon with code {unassigned_coupon_code} does not exist.")
        for coupon in user.unassigned_coupons:
            if coupon.code == unassigned_coupon_code:
                return True
        return False
    
    def delete_assigned_coupon_from_user(self, email: str, coupon_code: str) -> None:
        user = self.get_user_by_email(email)
        coupon = self.coupon_db.get_coupon_by_code(coupon_code)
        if coupon is None:
            raise ValueError(f"Coupon with code {coupon_code} does not exist.")
        if user is not None:
            if coupon in user.assigned_coupons:
                user.assigned_coupons.remove(coupon)
            else:
                raise ValueError(f"Coupon with code {coupon.code} is not in user's assigned coupons.")
        else:
            raise ValueError(f"User with email {email} does not exist.")
    
    def delete_unassigned_coupon_from_user(self, email: str, coupon_code : str) -> None:
        user = self.get_user_by_email(email)
        coupon = self.coupon_db.get_coupon_by_code(coupon_code)
        if coupon is None:
            raise ValueError(f"Coupon with code {coupon_code} does not exist.")
        if user is not None:
            if coupon in user.unassigned_coupons:
                user.unassigned_coupons.remove(coupon)
            else:
                raise ValueError(f"Coupon with code {coupon.code} is not in user's unassigned coupons.")
        else:
            raise ValueError(f"User with email {email} does not exist.")
        
user_db = UserDB()