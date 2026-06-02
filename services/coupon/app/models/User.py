from pydantic import BaseModel

class User(BaseModel):
    
    user_email: str
    unassigned_coupons: list[str] = []
    assigned_coupons: list[str] = []

    def __str__(self):
        return f"User(user_email={self.user_email})"
    
    def __to_dict__(self):
        return {
            "user": self.user_email,
            "unassigned_coupons": self.unassigned_coupons,
            "assigned_coupons": self.assigned_coupons
            
        }