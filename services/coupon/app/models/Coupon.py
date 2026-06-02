

from pydantic import BaseModel

class Coupon(BaseModel):

    code: str
    id: int
    text: str
    discount: float
    creation_date: str
    expiration_date: str
    enabled: bool

    def __init__(self):
        self.code = self.text + self.id

    def __str__(self):
        return f"Coupon(code={self.code}, discount={self.discount},creation_date={self.creation_date}, expiration_date={self.expiration_date}, enabled={self.enabled})"
    
    def __to_dict__(self):
        return {
            "code": self.code,
            "discount": self.discount,
            "expiration_date": self.expiration_date,
            "enabled": self.enabled
        }
    
