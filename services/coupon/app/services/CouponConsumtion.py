"""
    Module for coupon consumption operations and discount calculations.
    This module handles the application and consumption of coupons by users,
    including validation, discount calculation, and tracking of coupon usage.
    Author: Juan Nicolás Diaz Salamanca <jndiaz@udistrital.edu.co>
"""

from app.repository.CouponDB import coupon_db
from app.repository.UserDB import user_db
from app.services.CouponFactory import coupon_factory

class CouponConsumption:
    """
        Handles coupon consumption operations and discount price calculations.
        Attributes:
        - coupon_db: Database connection for coupon operations.
        - user_db: Database connection for user operations.
        - coupon_factory: Factory for creating coupon instances.
        Methods:
        - __init__: Initializes the coupon consumption service with database connections.
        - calculate_discounted_price: Calculates the discounted price based on the original price and discount percentage.
        - apply_assigned_coupon: Applies an assigned coupon to a user's purchase and returns the discounted price.
        - apply_unassigned_coupon: Applies an unassigned coupon to a user's purchase and returns the discounted price.
    """

    def __init__(self):
        """
        Initializes the coupon consumption service.
        Sets up database connections for coupons and users, and initializes the coupon factory.
        """
        self.coupon_db = coupon_db
        self.user_db = user_db
        self.coupon_factory = coupon_factory
    
    def calculate_discounted_price(self, original_price: float, discount: float) -> float:
        """
            Calculates the discounted price based on the original price and discount percentage.
            Args:
            - original_price: The original price before discount as a float.
            - discount: The discount percentage as a float (e.g., 0.2 for 20%).
            Returns:
            - The discounted price as a float.
            For example: calculate_discounted_price(100.0, 0.2) returns 80.0
        """
        return original_price * (1 - discount)
    
    def apply_assigned_coupon(self, email: str, coupon_code: str, original_price: float) -> float:

        """
            Applies an assigned coupon to a user's purchase and returns the discounted price.
            Args:
            - email: The email address of the user.
            - coupon_code: The code of the coupon to apply.
            - original_price: The original price before discount as a float.
            Returns:
            - The discounted price as a float.
            Raises:
            - ValueError: If the coupon has already been consumed by the user, does not exist, or is disabled.
        """

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

        """
            Applies an unassigned coupon to a user's purchase and returns the discounted price.
            Args:
            - email: The email address of the user.
            - coupon_code: The code of the coupon to apply.
            - original_price: The original price before discount as a float.
            Returns:
            - The discounted price as a float.
            Raises:
            - ValueError: If the coupon has already been consumed by the user, does not exist, or is disabled.
        """

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

""""
Here we declared the instance in order to use only one instance of the service in the application, 
and to be able to import it directly in the router.
"""
            
coupon_consumption = CouponConsumption()   

            
