
from app.models.Coupon import Coupon
from app.repository.CouponDB import coupon_db
from app.schemas.COUPON_RULES import COUPON_RULES

class CouponFactory :

    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.coupon_db = coupon_db
            cls.happy_birthday = COUPON_RULES.HAPPY_BIRTHDAY_COUPON_TEXT
            cls.happy_birthday_index = 0
            cls.happy_birthday_discount = COUPON_RULES.HAPPY_BIRTHDAY_DISCOUNT
            cls.referred = COUPON_RULES.REFERRED_COUPON_TEXT
            cls.referred_discount = COUPON_RULES.REFERRED_DISCOUNT
            cls.referred_index = 0
        return cls._instance
    
    def create_coupon(self, text: str, discount: float, days: int) -> Coupon:
        expiration_date = COUPON_RULES.get_expiration_date(days)
        new_coupon = self.coupon_db.create_coupon(text, 0, discount, expiration_date)
        return new_coupon
    
    def create_happy_birthday_coupon(self) -> Coupon:
        if self.coupon_db.get_last_coupon_by_text(self.happy_birthday) is None:
            self.happy_birthday_index = 1
        else: 
            self.happy_birthday_index = self.coupon_db.get_last_coupon_by_text(self.happy_birthday).id + 1

        new_coupon = self.coupon_db.create_coupon(self.happy_birthday, self.happy_birthday_index, self.happy_birthday_discount,\
                                                COUPON_RULES.get_happy_birthday_expiration_date())                         
        return new_coupon
    
    def create_referred_coupon(self) -> Coupon:
        if self.coupon_db.get_last_coupon_by_text(self.referred) is None:
            self.referred_index = 1
        else: 
            self.referred_index = self.coupon_db.get_last_coupon_by_text(self.referred).id + 1

        new_coupon = self.coupon_db.create_coupon(self.referred, id, self.referred_discount,\
                                                  COUPON_RULES.get_referred_expiration_date())
        return new_coupon
    
coupon_factory = CouponFactory()
    

    

    
    