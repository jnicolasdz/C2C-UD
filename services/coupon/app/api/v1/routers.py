"""
Module for coupon API routes and endpoint handlers.

This module defines the API routes for coupon operations using FastAPI,
including endpoints for retrieving, creating, updating, and deleting coupons,
as well as managing user-assigned coupons.

Author: Juan Nicolás Diaz Salamanca <jndiaz@udistrital.edu.co>
"""

from fastapi import APIRouter
from app.services.CouponService import CouponService

router = APIRouter()
service = CouponService()

class Routes:
    """
    Represents API routes for coupon management operations.
    
    Attributes:
    - router: FastAPI APIRouter instance for defining endpoints.
    - service: CouponService instance for handling business logic.
    
    Methods:
    - GET /coupons/code/{code}: Retrieve coupon by code.
    - GET /coupons/creation-date/{date}: Retrieve coupons by creation date.
    - GET /coupons/expiration-date/{date}: Retrieve coupons by expiration date.
    - GET /coupons/expired: Retrieve all expired coupons.
    - GET /coupons/valid: Retrieve all valid coupons.
    - GET /coupons/enabled: Retrieve all enabled coupons.
    - GET /coupons/disabled: Retrieve all disabled coupons.
    - GET /coupons/search/{text}: Search coupons by text.
    - GET /coupons/happy-birthday: Retrieve happy birthday coupons.
    - GET /coupons/referred: Retrieve referred coupons.
    - GET /coupons/last/{text}: Retrieve last coupon by text.
    - GET /coupons: Retrieve all coupons.
    - POST /coupons/{code}/enable: Enable a coupon.
    - POST /coupons/{code}/disable: Disable a coupon.
    - GET /coupons/{code}/is-enabled: Check if coupon is enabled.
    - DELETE /coupons/{code}: Delete a coupon.
    - POST /coupons/unassigned: Create unassigned coupon.
    - POST /coupons/assigned: Create assigned coupon.
    - POST /coupons/happy-birthday/{user_email}: Create happy birthday coupon.
    - POST /coupons/referred/{user_email}: Create referred coupon.
    - GET /users/{email}/coupons: Retrieve user's coupons.
    - GET /users/coupons/all: Retrieve all users' coupons.
    - DELETE /users/{email}/coupons/{coupon_code}: Delete assigned coupon from user.
    - POST /users/{email}/coupons/{coupon_code}/apply-assigned: Apply assigned coupon.
    - POST /users/{email}/coupons/{coupon_code}/apply-unassigned: Apply unassigned coupon.
    """
    
    @router.get("/coupons/code/{code}")
    async def get_coupon_by_code(code: str):
        """
            Retrieves a coupon by its unique code.
            Args:
            - code: The unique code of the coupon to retrieve.
            Returns:
            - The coupon data as a dictionary if found, or an error message if not found or if an exception occurs.
        """
        try:
            return service.get_coupon_by_code(code)
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/coupons/creation-date/{date}")
    async def get_coupon_by_creation_date(date: str):
        """
            Retrieves coupons by their creation date.
            Args:
            - date: The creation date to filter coupons by, in the format "YYYY-MM-DD".
            Returns:
            - A list of coupons created on the specified date, or an error message if an exception occurs.
        """
        try:
            return service.get_coupon_by_creation_date(date)
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/coupons/expiration-date/{date}")
    async def get_coupon_by_expiration_date(date: str):
        """
            Retrieves coupons by their expiration date.
            Args:
            - date: The expiration date to filter coupons by, in the format "YYYY-MM-DD".
            Returns:
            - A list of coupons expiring on the specified date, or an error message if an exception occurs.
        """
        try:
            return service.get_coupon_by_expiration_date(date)
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/coupons/expired")
    async def get_expired_coupons():
        """
            Retrieves all expired coupons.
            Returns:
            - A list of expired coupons, or an error message if an exception occurs."""
        try:
            return service.get_expired_coupons()
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/coupons/valid")
    async def get_valid_coupons():
        """
            Retrieves all valid coupons.
            Returns:
            - A list of valid coupons, or an error message if an exception occurs.
        """
        try:
            return service.get_valid_coupons()
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/coupons/enabled")
    async def get_enabled_coupons():
        """
            Retrieves all enabled coupons.
            Returns:
            - A list of enabled coupons, or an error message if an exception occurs.
        """
        try:
            return service.get_enabled_coupons()
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/coupons/disabled")
    async def get_disabled_coupons():
        """
            Retrieves all disabled coupons.
            Returns:
            - A list of disabled coupons, or an error message if an exception occurs.
        """
        try:
            return service.get_disabled_coupons()
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/coupons/search/{text}")
    async def get_coupons_by_text(text: str):
        """
            Searches for coupons containing specific text.
            Args:
            - text: The text to search for in coupon descriptions.
            Returns:
            - A list of coupons matching the search text, or an error message if an exception occurs"""
        try:
            return service.get_coupons_by_text(text)
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/coupons/happy-birthday")
    async def get_happy_birthday_coupons():
        """
            Retrieves all happy birthday coupons.
            Returns:
            - A list of happy birthday coupons, or an error message if an exception occurs.
        """
        try:
            return service.get_happy_birthday_coupons()
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/coupons/referred")
    async def get_referred_coupons():
        """
            Retrieves all referred coupons.
            Returns:
            - A list of referred coupons, or an error message if an exception occurs.
        """
        try:
            return service.get_referred_coupons()
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/coupons/last/{text}")
    async def get_last_coupon_by_text(text: str):
        """
            Retrieves the last created coupon that contains specific text.
            Args:
            - text: The text to search for in coupon descriptions.
            Returns:
            - The last created coupon matching the search text, or an error message if not found or if an exception occurs.
        """
        try:
            return service.get_last_coupon_by_text(text)
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/coupons")
    async def get_all_coupons():
        """
            Retrieves all coupons.
            Returns:
            - A list of all coupons, or an error message if an exception occurs.
        """
        try:
            return service.get_all_coupons()
        except ValueError as e:
            return {"error": str(e)}

    @router.post("/coupons/{code}/enable")
    async def enable_coupon(code: str):
        """    
        Enables a coupon by its unique code.
        Args:
            - code: The unique code of the coupon to enable.
        Returns:
            - A success message if the coupon is enabled, or an error message if not found or if an exception occurs.
        """
        try:
            service.enable_coupon(code)
            return {"status": "enabled"}
        except ValueError as e:
            return {"error": str(e)}

    @router.post("/coupons/{code}/disable")
    async def disable_coupon(code: str):
        """
            Disables a coupon by its unique code.
            Args:
            - code: The unique code of the coupon to disable.
            Returns:
            - A success message if the coupon is disabled, or an error message if not found or if an exception occurs.
        """
        try:
            service.disable_coupon(code)
            return {"status": "disabled"}
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/coupons/{code}/is-enabled")
    async def is_enable_coupon(code: str):
        """
            Checks if a coupon is enabled by its unique code.
            Args:
            - code: The unique code of the coupon to check.
            Returns:
            - A dictionary indicating whether the coupon is enabled, or an error message if not found or if an exception occurs.
        """
        try:
            return {"enabled": service.is_enable_coupon(code)}
        except ValueError as e:
            return {"error": str(e)}

    @router.delete("/coupons/{code}")
    async def delete_coupon(code: str):
        """
            Deletes a coupon by its unique code.
            Args:
            - code: The unique code of the coupon to delete.
            Returns:
            - A success message if the coupon is deleted, or an error message if not found or if an exception occurs.
        """
        try:
            service.delete_coupon(code)
            return {"status": "deleted"}
        except ValueError as e:
            return {"error": str(e)}

    @router.post("/coupons/unassigned")
    async def create_unassigned_coupon(text: str, discount: float, days: int):
        """
            Creates a new unassigned coupon with the specified text, discount, and expiration days.
            Args:
            - text: The text description of the coupon.
            - discount: The discount percentage as a float (e.g., 0.2 for 20%).
            - days: The number of days until the coupon expires.
            Returns:
            - A success message if the coupon is created, or an error message if an exception occurs"""
        try:
            service.create_unassigned_coupon(text, discount, days)
            return {"status": "created"}
        except ValueError as e:
            return {"error": str(e)}

    @router.post("/coupons/assigned")
    async def create_assigned_coupon(text: str, discount: float, days: int, user_email: str):
        """
            Creates a new assigned coupon with the specified text, discount, expiration days, and assigns it to a user.
            Args:
            - text: The text description of the coupon.
            - discount: The discount percentage as a float (e.g., 0.2 for 20%).
            - days: The number of days until the coupon expires.
            - user_email: The email address of the user to assign the coupon to.
            Returns:
            - A success message if the coupon is created and assigned, or an error message if an exception occurs.
        """
        try:
            service.create_assigned_coupon(text, discount, days, user_email)
            return {"status": "created"}
        except ValueError as e:
            return {"error": str(e)}

    @router.post("/coupons/happy-birthday/{user_email}")
    async def create_happy_birthday_coupon(user_email: str):
        """
            Creates a happy birthday coupon for a user based on predefined rules and assigns it to the user.
            Args:
            - user_email: The email address of the user to assign the happy birthday coupon to.
            Returns:
            - A success message if the coupon is created and assigned, or an error message if an exception occurs.
        """
        try:
            service.create_happy_birthday_coupon(user_email)
            return {"status": "created"}
        except ValueError as e:
            return {"error": str(e)}

    @router.post("/coupons/referred/{user_email}")
    async def create_referred_coupon(user_email: str):
        """
            Creates a referral promotional coupon for a user based on predefined rules and assigns it to the user.
            Args:
            - user_email: The email address of the user to assign the referral coupon to.
            Returns:
            - A success message if the coupon is created and assigned, or an error message if an exception occurs.
        """
        try:
            service.create_referred_coupon(user_email)
            return {"status": "created"}
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/users/{email}/coupons")
    async def get_user_coupons(email: str):
        """
            Retrieves both assigned and unassigned coupons for a specific user.
            Args:
            - email: The email address of the user to retrieve coupons for.
            Returns:
            - A dictionary containing two lists: "assigned_coupons" and "unassigned_coupons", which include the respective coupons for the user. If the user does not exist, an error message is returned.
        """
        try:
            return service.get_user_coupons(email)
        except ValueError as e:
            return {"error": str(e)}

    @router.get("/users/coupons/all")
    async def get_all_users_coupons():
        """
            Retrieves all users with their assigned and unassigned coupons.
            Returns:
            - A dictionary where each key is a user's email and the value is another dictionary containing two lists: "assigned_coupons" and "unassigned_coupons", which include the respective coupons for each user. If an exception occurs, an error message is returned.
        """
        try:
            return service.get_all_users_coupons()
        except ValueError as e:
            return {"error": str(e)}

    @router.delete("/users/{email}/coupons/{coupon_code}")
    async def delete_assigned_coupon_from_user(email: str, coupon_code: str):
        """
            Removes an assigned coupon from a user.
            Args:
            - email: The email address of the user to remove the assigned coupon from.
            - coupon_code: The unique code of the coupon to remove from the user.
            Returns:
            - A success message if the assigned coupon is removed from the user, or an error message if the user does not exist or if an exception occurs.
        """
        try:
            service.delete_asigned_coupon_from_user(email, coupon_code)
            return {"status": "deleted"}
        except ValueError as e:
            return {"error": str(e)}

    @router.post("/users/{email}/coupons/{coupon_code}/apply-assigned")
    async def apply_assigned_coupon(email: str, coupon_code: str, original_price: float):
        """
            Applies a discount using an assigned coupon to a price.
            Args:
            - email: The email address of the user applying the coupon.
            - coupon_code: The unique code of the assigned coupon to apply.
            - original_price: The original price before applying the coupon as a float.
            Returns:
            - The discounted price as a float after applying the coupon, or an error message if the coupon is invalid or if an exception occurs.
        """
        try:
            return {"final_price": service.apply_assigned_coupon(email, coupon_code, original_price)}
        except ValueError as e:
            return {"error": str(e)}

    @router.post("/users/{email}/coupons/{coupon_code}/apply-unassigned")
    async def apply_unassigned_coupon(email: str, coupon_code: str, original_price: float):
        """
            Applies a discount using an unassigned coupon to a price.
            Args:
            - email: The email address of the user applying the coupon.
            - coupon_code: The unique code of the unassigned coupon to apply.
            - original_price: The original price before applying the coupon as a float.
            Returns:
            - The discounted price as a float after applying the coupon, or an error message if the coupon is invalid or if an exception occurs.
        """
        try:
            return {"final_price": service.apply_unassigned_coupon(email, coupon_code, original_price)}
        except ValueError as e:
            return {"error": str(e)}

 