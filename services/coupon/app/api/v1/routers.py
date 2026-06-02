from fastapi import APIRouter
from app.services.CouponService import CouponService

router = APIRouter()
service = CouponService()

class Routes:
    
    @router.get("/coupons/code/{code}")
    async def get_coupon_by_code(code: str):
        try:
            return service.get_coupon_by_code(code)
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/coupons/creation-date/{date}")
    async def get_coupon_by_creation_date(date: str):
        try:
            return service.get_coupon_by_creation_date(date)
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/coupons/expiration-date/{date}")
    async def get_coupon_by_expiration_date(date: str):
        try:
            return service.get_coupon_by_expiration_date(date)
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/coupons/expired")
    async def get_expired_coupons():
        try:
            return service.get_expired_coupons()
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/coupons/valid")
    async def get_valid_coupons():
        try:
            return service.get_valid_coupons()
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/coupons/enabled")
    async def get_enabled_coupons():
        try:
            return service.get_enabled_coupons()
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/coupons/disabled")
    async def get_disabled_coupons():
        try:
            return service.get_disabled_coupons()
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/coupons/search/{text}")
    async def get_coupons_by_text(text: str):
        try:
            return service.get_coupons_by_text(text)
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/coupons/happy-birthday")
    async def get_happy_birthday_coupons():
        try:
            return service.get_happy_birthday_coupons()
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/coupons/referred")
    async def get_referred_coupons():
        try:
            return service.get_referred_coupons()
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/coupons/last/{text}")
    async def get_last_coupon_by_text(text: str):
        try:
            return service.get_last_coupon_by_text(text)
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/coupons")
    async def get_all_coupons():
        try:
            return service.get_all_coupons()
        except ValueError as e:
            return {"error": str(e)}

    @router.post("/coupons/{code}/enable")
    async def enable_coupon(code: str):
        try:
            service.enable_coupon(code)
            return {"status": "enabled"}
        except ValueError as e:
            return {"error": str(e)}

    @router.post("/coupons/{code}/disable")
    async def disable_coupon(code: str):
        try:
            service.disable_coupon(code)
            return {"status": "disabled"}
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/coupons/{code}/is-enabled")
    async def is_enable_coupon(code: str):
        try:
            return {"enabled": service.is_enable_coupon(code)}
        except ValueError as e:
            return {"error": str(e)}

    @router.delete("/coupons/{code}")
    async def delete_coupon(code: str):
        try:
            service.delete_coupon(code)
            return {"status": "deleted"}
        except ValueError as e:
            return {"error": str(e)}

    @router.post("/coupons/unassigned")
    async def create_unassigned_coupon(text: str, discount: float, days: int):
        try:
            service.create_unassigned_coupon(text, discount, days)
            return {"status": "created"}
        except ValueError as e:
            return {"error": str(e)}

    @router.post("/coupons/assigned")
    async def create_assigned_coupon(text: str, discount: float, days: int, user_email: str):
        try:
            service.create_assigned_coupon(text, discount, days, user_email)
            return {"status": "created"}
        except ValueError as e:
            return {"error": str(e)}

    @router.post("/coupons/happy-birthday/{user_email}")
    async def create_happy_birthday_coupon(user_email: str):
        try:
            service.create_happy_birthday_coupon(user_email)
            return {"status": "created"}
        except ValueError as e:
            return {"error": str(e)}

    @router.post("/coupons/referred/{user_email}")
    async def create_referred_coupon(user_email: str):
        try:
            service.create_referred_coupon(user_email)
            return {"status": "created"}
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/users/{email}/coupons")
    async def get_user_coupons(email: str):
        try:
            return service.get_user_coupons(email)
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/users/coupons/all")
    async def get_all_users_coupons():
        try:
            return service.get_all_users_coupons()
        except ValueError as e:
            return {"error": str(e)}

    @router.delete("/users/{email}/coupons/{coupon_code}")
    async def delete_assigned_coupon_from_user(email: str, coupon_code: str):
        try:
            service.delete_asigned_coupon_from_user(email, coupon_code)
            return {"status": "deleted"}
        except ValueError as e:
            return {"error": str(e)}

    @router.post("/users/{email}/coupons/{coupon_code}/apply-assigned")
    async def apply_assigned_coupon(email: str, coupon_code: str, original_price: float):
        try:
            return {"final_price": service.apply_assigned_coupon(email, coupon_code, original_price)}
        except ValueError as e:
            return {"error": str(e)}

    @router.post("/users/{email}/coupons/{coupon_code}/apply-unassigned")
    async def apply_unassigned_coupon(email: str, coupon_code: str, original_price: float):
        try:
            return {"final_price": service.apply_unassigned_coupon(email, coupon_code, original_price)}
        except ValueError as e:
            return {"error": str(e)}

 