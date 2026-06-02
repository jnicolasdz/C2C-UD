from app.repository.CouponDB import coupon_db
from app.repository.UserDB import user_db
from app.services.CouponFactory import coupon_factory
class CouponConsumption :

    def __init__(self):
        self.coupon_db = coupon_db
        self.user_db = user_db
        self.coupon_factory = coupon_factory
    
    def calculate_discounted_price(self, original_price: float, discount: float) -> float:
        return original_price * (1 - discount)
    
    def apply_assigned_coupon(self, email: str, coupon_code: str, original_price: float) -> float:

        if user_db.has_consumed_assigned_coupon(email, coupon_code):
            raise ValueError(f"Coupon with code {coupon_code} has already been consumed by user {email}.")
        else: 
            coupon = self.coupon_db.get_coupon_by_code(coupon_code)
            if coupon is None:
                raise ValueError(f"Coupon with code {coupon_code} does not exist.")
            elif self.coupon_db.is_enable_coupon(coupon_code):
                raise ValueError(f"Coupon is disable")
            else:
                discounted_price = self.calculate_discounted_price(original_price, coupon.discount)
                self.user_db.delete_assigned_coupon_from_user(email, coupon)
                return discounted_price

    def apply_unassigned_coupon(self, email: str, coupon_code: str, original_price: float) -> float:

        if user_db.has_consumed_unassigned_coupon(email, coupon_code):
            raise ValueError(f"Coupon with code {coupon_code} has already been consumed by user {email}.")
        else: 
            coupon = self.coupon_db.get_coupon_by_code(coupon_code)
            if coupon is None:
                raise ValueError(f"Coupon with code {coupon_code} does not exist.")
            elif self.coupon_db.is_enable_coupon(coupon_code):
                raise ValueError(f"Coupon is disable")
            else:
                discounted_price = self.calculate_discounted_price(original_price, coupon.discount)
                self.user_db.add_unassigned_coupon_to_user(email, coupon)
                return discounted_price
            
coupon_consumption = CouponConsumption()   

            
