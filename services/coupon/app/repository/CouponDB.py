
import datetime

from app.models.Coupon import Coupon

class CouponDB :

    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.coupons = []
        return cls._instance
        
    def get_coupon_by_code(self, code: str) -> Coupon:
        for coupon in self.coupons:
            if coupon.code == code:
                return coupon.to_dict()
        return None
    
    def get_coupon_by_creation_date(self, date: datetime) -> list[Coupon]:
        return [coupon.to_dict() for coupon in self.coupons if coupon.expiration_date == date]
    
    def get_coupon_by_expiration_date(self, date: datetime) -> list[Coupon]:
        return [coupon.to_dict() for coupon in self.coupons if coupon.expiration_date == date]
    
    def get_expired_coupons(self) -> list[Coupon]:
        now = datetime.datetime.now()
        return [coupon.to_dict() for coupon in self.coupons if coupon.expiration_date < now]
    
    def get_valid_coupons(self) -> list[Coupon]:
        now = datetime.datetime.now()
        return [coupon.to_dict() for coupon in self.coupons if coupon.expiration_date >= now and coupon.enabled]
    
    def get_coupon_by_enabled(self, enabled: bool) -> list[Coupon]:
        return [coupon.to_dict() for coupon in self.coupons if coupon.enabled == enabled]
    
    def get_coupons_by_text(self, text: str) -> list[Coupon]:
        return [coupon.to_dict() for coupon in self.coupons if coupon.text == text]
    
    def get_last_coupon_by_text(self, text: str) -> Coupon: 
        coupons = self.get_coupons_by_text(text)
        if not coupons:
            return None
        return max(coupons, key=lambda c: c['id'])
    
    def get_all_coupons(self) -> list[Coupon]:
        return [coupon.to_dict() for coupon in self.coupons]
    
    def enable_coupon(self, code: str) -> None:
        coupon = self.get_coupon_by_code(code)
        if coupon is not None:
            coupon.enabled = True
        else:
            raise ValueError(f"Coupon with code {code} does not exist.")
        
    def disable_coupon(self, code: str) -> None:
        coupon = self.get_coupon_by_code(code)
        if coupon is not None:
            coupon.enabled = False
        else:
            raise ValueError(f"Coupon with code {code} does not exist.")
    
    def is_enable_coupon(self, code: str) -> bool:
        coupon = self.get_coupon_by_code(code)
        if coupon.enable:
            return True
        else: return False

    def create_coupon(self, text: str, id: int, discount: float, expiration_date: datetime) -> Coupon:
        new_coupon = Coupon(text=text, id=id, discount=discount, creation_date=datetime.datetime.now(), expiration_date=expiration_date, enabled=True)
        return new_coupon

    def delete_coupon(self, code: str) -> None:
        coupon = self.get_coupon_by_code(code)
        if coupon is not None:
            self.coupons.remove(coupon)
        else:
            raise ValueError(f"Coupon with code {code} does not exist.")
    
    def add_coupon(self, text: str, id: int, discount: float):
        new_coupon = self.create_coupon(text, id, discount)
        if self.get_coupon_by_code(new_coupon.code) is not None:
            raise ValueError(f"Coupon with code {text+id} already exists.")
        else:
            self.coupons.append(new_coupon)

    def add_coupon(self, new_coupon : Coupon):
        if self.get_coupon_by_code(new_coupon.code) is not None:
            raise ValueError(f"Coupon with code {new_coupon.code} already exists.")
        else:
            self.coupons.append(new_coupon)

coupon_db = CouponDB()