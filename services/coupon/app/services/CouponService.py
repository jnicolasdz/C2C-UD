"""
    Module for coupon service operations and business logic.
    This module defines the CouponService class that handles all coupon-related
    operations including retrieval, creation, management, and consumption of coupons.
    It acts as an intermediary between the data access layer and the application logic.
    Author: Juan Nicolás Diaz Salamanca <jndiaz@udistrital.edu.co>
"""

from app.services.CouponFactory import coupon_factory
from app.services.CouponConsumtion import coupon_consumption
from app.repository.CouponDB import coupon_db
from app.repository.UserDB import user_db
from app.schemas.COUPON_RULES import COUPON_RULES

import datetime

class CouponService :

    """
        Service class for managing coupon operations and business logic.
        Attributes:
        - coupon_factory: Factory for creating new coupon instances.
        - coupon_consumption: Handler for coupon consumption and discount application.
        - coupon_db: Database access object for coupon operations.
        - user_db: Database access object for user operations.
        Methods:
        - get_coupon_by_code: Retrieves a coupon by its unique code.
        - get_coupon_by_creation_date: Retrieves coupons by creation date.
        - get_coupon_by_expiration_date: Retrieves coupons by expiration date.
        - get_expired_coupons: Retrieves all expired coupons.
        - get_valid_coupons: Retrieves all valid (non-expired) coupons.
        - get_enabled_coupons: Retrieves all enabled coupons.
        - get_disabled_coupons: Retrieves all disabled coupons.
        - get_coupons_by_text: Retrieves coupons by text description.
        - get_happy_birthday_coupons: Retrieves all happy birthday promotional coupons.
        - get_referred_coupons: Retrieves all referral promotional coupons.
        - get_last_coupon_by_text: Retrieves the most recent coupon by text description.
        - get_all_coupons: Retrieves all coupons from the database.
        - enable_coupon: Enables a coupon by its code.
        - disable_coupon: Disables a coupon by its code.
        - is_enable_coupon: Checks if a coupon is enabled.
        - delete_coupon: Deletes a coupon by its code.
        - create_unassigned_coupon: Creates a new unassigned coupon.
        - create_assigned_coupon: Creates a new coupon and assigns it to a user.
        - create_happy_birthday_coupon: Creates a birthday promotional coupon for a user.
        - create_referred_coupon: Creates a referral promotional coupon for a user.
        - get_user_coupons: Retrieves both assigned and unassigned coupons for a specific user.
        - get_all_users_coupons: Retrieves all users with their assigned and unassigned coupons.
        - delete_asigned_coupon_from_user: Removes an assigned coupon from a user.
        - apply_assigned_coupon: Applies a discount using an assigned coupon to a price.
        - apply_unassigned_coupon: Applies a discount using an unassigned coupon to a price.
    """

    def __init__(self):
        """
        Initializes the CouponService with required dependencies.
        Sets up references to the coupon factory, consumption handler, and database access objects.
        """
        self.coupon_factory = coupon_factory
        self.coupon_consumption = coupon_consumption
        self.coupon_db = coupon_db
        self.user_db = user_db
    
    def get_coupon_by_code(self, code: str):
        """
            Retrieves a coupon by its unique code.
            Args:
            - code: The unique code of the coupon to retrieve.
            Returns:
            - The coupon data as a dictionary if found, or None if not found.
        """
        return self.coupon_db.get_coupon_by_code(code)
    
    def get_coupon_by_creation_date(self, date: datetime):
        """
            Retrieves coupons by their creation date.
            Args:
            - date: The creation date to filter coupons by.
            Returns:
            - A list of coupons created on the specified date.
        """
        return self.coupon_db.get_coupon_by_creation_date(date)
    
    def get_coupon_by_expiration_date(self, date: datetime):
        """
            Retrieves coupons by their expiration date.
            Args:
            - date: The expiration date to filter coupons by.
            Returns:
            - A list of coupons that expire on the specified date.
        """
        return self.coupon_db.get_coupon_by_expiration_date(date)
    
    def get_expired_coupons(self):
        """
            Retrieves all expired coupons.
            Returns:
            - A list of all coupons that have expired.
        """
        return self.coupon_db.get_expired_coupons()
    
    def get_valid_coupons(self):
        """
            Retrieves all valid (non-expired) coupons.
            Returns:
            - A list of all coupons that are currently valid and not expired.
        """
        return self.coupon_db.get_valid_coupons()

    def get_enabled_coupons(self):
        """
            Retrieves all enabled coupons.
            Returns:
            - A list of all coupons that are currently enabled.
        """
        return self.coupon_db.get_coupon_by_enabled(True)
    
    def get_disabled_coupons(self):
        """
            Retrieves all disabled coupons.
            Returns:
            - A list of all coupons that are currently disabled.
        """
        return self.coupon_db.get_coupon_by_enabled(False)
    
    def get_coupons_by_text(self, text: str):
        """
            Retrieves coupons by their text description.
            Args:
            - text: The text description to filter coupons by.
            Returns:
            - A list of coupons that match the specified text description.
        """
        return self.coupon_db.get_coupons_by_text(text)
    
    def get_happy_birthday_coupons(self):
        """
            Retrieves all happy birthday promotional coupons.
            Returns:
            - A list of all coupons that are categorized as happy birthday promotions.
        """
        return self.coupon_db.get_coupons_by_text(COUPON_RULES.HAPPY_BIRTHDAY_COUPON_TEXT)
    
    def get_referred_coupons(self):
        """
            Retrieves all referral promotional coupons.
            Returns:
            - A list of all coupons that are categorized as referral promotions.
        """
        return self.coupon_db.get_coupons_by_text(COUPON_RULES.REFERRED_COUPON_TEXT)

    def get_last_coupon_by_text(self, text: str):
        """
            Retrieves the most recent coupon by its text description.
            Args:
            - text: The text description to filter coupons by.
            Returns:
            - The most recently created coupon that matches the specified text description, or None if no such coupon exists.
        """
        return self.coupon_db.get_last_coupon_by_text(text)
    
    def get_all_coupons(self):
        """
            Retrieves all coupons from the database.
            Returns:
            - A list of all coupons currently stored in the database.
        """
        return self.coupon_db.get_all_coupons()
    
    def enable_coupon(self, code: str):
        """
            Enables a coupon by its unique code.
            Args:
            - code: The unique code of the coupon to enable.
            Returns:
            - None. The method performs the action of enabling the coupon in the database."""
        self.coupon_db.enable_coupon(code)
    
    def disable_coupon(self, code: str):
        """
            Disables a coupon by its unique code.
            Args:
            - code: The unique code of the coupon to disable.
            Returns:
            - None. The method performs the action of disabling the coupon in the database.
        """
        self.coupon_db.disable_coupon(code)
    
    def is_enable_coupon(self, code: str) -> bool:
        """
            Checks if a coupon is enabled by its unique code.
            Args:            
            - code: The unique code of the coupon to check.
            Returns:
            - A boolean value indicating whether the coupon is enabled (True) or not (False).
        """
        return self.coupon_db.is_enable_coupon(code)
    
    def delete_coupon(self, code: str):
        """
            Deletes a coupon by its unique code.
            Args:
            - code: The unique code of the coupon to delete.
            Returns:
            - None. The method performs the action of deleting the coupon from the database.
        """
        self.coupon_db.delete_coupon(code)

    def create_unassigned_coupon(self, text: str, discount: float, days: int):
        """
            Creates a new unassigned coupon with the specified text, discount, and expiration days.
            Args:
            - text: The text description of the coupon.
            - discount: The discount percentage as a float (e.g., 0.2 for 20%).
            - days: The number of days until the coupon expires.
            Returns:
            - None. The method creates a new coupon and adds it to the database without assigning it to any user.
        """
        self.coupon_db.add_coupon(self.coupon_factory.create_coupon(text, discount, days))
        
    def create_assigned_coupon(self, text: str, discount: float, days: int, user_email: str):
        """
            Creates a new coupon with the specified text, discount, and expiration days, and assigns it to a user.
            Args:
            - text: The text description of the coupon.
            - discount: The discount percentage as a float (e.g., 0.2 for 20%).
            - days: The number of days until the coupon expires.
            - user_email: The email address of the user to assign the coupon to.
            Returns:
            - None. The method creates a new coupon, adds it to the database, and assigns it to the specified user.
        """
        new_coupon = self.coupon_factory.create_coupon(text, discount, days)
        self.coupon_db.add_coupon(new_coupon)
        self.user_db.add_assigned_coupon_to_user(user_email, new_coupon["code"])

    def create_happy_birthday_coupon(self, user_email: str):
        """
            Creates a birthday promotional coupon for a user based on predefined rules.
            The coupon is created with the predefined happy birthday text and discount, and the expiration date is determined by the happy birthday expiration rule.
            Args:
            - user_email: The email address of the user to assign the happy birthday coupon to.
            Returns:
            - None. The method creates a new happy birthday coupon, adds it to the database, and assigns it to the specified user.
        """
        new_coupon = self.coupon_factory.create_happy_birthday_coupon()
        self.coupon_db.add_coupon(new_coupon)
        self.user_db.add_assigned_coupon_to_user(user_email, new_coupon["code"])
    
    def create_referred_coupon(self, user_email: str):
        """
            Creates a referral promotional coupon for a user based on predefined rules.
            The coupon is created with the predefined referred text and discount, and the expiration date is determined by the referred expiration rule.
            Args:
            - user_email: The email address of the user to assign the referral coupon to.
            Returns:
            - None. The method creates a new referral coupon, adds it to the database, and assigns it to the specified user.
        """
        new_coupon = self.coupon_factory.create_referred_coupon()
        self.coupon_db.add_coupon(new_coupon)
        self.user_db.add_assigned_coupon_to_user(user_email, new_coupon["code"])

    def get_user_coupons(self, email: str):
        """
            Retrieves both assigned and unassigned coupons for a specific user.
            Args:
            - email: The email address of the user to retrieve coupons for.
            Returns:
            - A dictionary containing two lists: "assigned_coupons" and "unassigned_coupons", which include the respective coupons for the user. If the user does not exist, a ValueError is raised.
        """
        user = self.user_db.get_user_by_email(email)
        if user is not None:
            return {
                "assigned_coupons": [coupon.to_dict() for coupon in user.assigned_coupons],
                "unassigned_coupons": [coupon.to_dict() for coupon in user.unassigned_coupons]
            }
        else:
            raise ValueError(f"User with email {email} does not exist.")
        
    def get_all_users_coupons(self):
        """
            Retrieves all users with their assigned and unassigned coupons.
            Returns:
            - A dictionary where each key is a user's email and the value is another dictionary containing two lists: "assigned_coupons" and "unassigned_coupons", which include the respective coupons for each user.
        """
        users = self.user_db.get_all_users()
        return {user['email']: {
                "assigned_coupons": [coupon.to_dict() for coupon in user['assigned_coupons']],
                "unassigned_coupons": [coupon.to_dict() for coupon in user['unassigned_coupons']]
            } for user in users}
    
    def delete_asigned_coupon_from_user(self, email: str, coupon_code: str):
        """
            Removes an assigned coupon from a user.
            Args:
            - email: The email address of the user to remove the assigned coupon from.
            - coupon_code: The unique code of the coupon to remove from the user.
            Returns:
            - None. The method performs the action of removing the specified assigned coupon from the user in the database. 
            Exceptions:
            - If the user does not exist, a ValueError is raised.
        """
        user = self.user_db.get_user_by_email(email)
        if user is not None:
            self.user_db.add_unassigned_coupon_to_user(email, coupon_code)
        else:
            raise ValueError(f"User with email {email} does not exist.")
    
    def apply_assigned_coupon(self, email: str, coupon_code: str, original_price: float) -> float:
        """
            Applies a discount using an assigned coupon to a price.
            Args:
            - email: The email address of the user applying the coupon.
            - coupon_code: The unique code of the assigned coupon to apply.
            - original_price: The original price before applying the coupon as a float.
            Returns:
            - The discounted price as a float after applying the coupon.
        """
        return self.coupon_consumption.apply_assigned_coupon(email, coupon_code, original_price)

    def apply_unassigned_coupon(self, email: str, coupon_code: str, original_price: float) -> float:
        """
            Applies a discount using an unassigned coupon to a price.
            Args:
            - email: The email address of the user applying the coupon.
            - coupon_code: The unique code of the unassigned coupon to apply.
            - original_price: The original price before applying the coupon as a float.
            Returns:
            - The discounted price as a float after applying the coupon.
        """
        return self.coupon_consumption.apply_unassigned_coupon(email, coupon_code, original_price)

    



    