"""
    Module for coupon factory and creation operations.
    This module defines the CouponFactory class using the Singleton pattern
    for creating and managing different types of coupons with predefined rules.
    Author: Juan Nicolás Diaz Salamanca <jndiaz@udistrital.edu.co>
"""
from app.models.Coupon import Coupon
from app.repository.CouponDB import coupon_db
from app.schemas.COUPON_RULES import COUPON_RULES

class CouponFactory :

    """
        Factory class for creating and managing coupons using the Singleton pattern.
        Attributes:
        - _instance: Singleton instance of the CouponFactory.
        - coupon_db: Database connection for coupon operations.
        - happy_birthday: Text identifier for happy birthday coupons.
        - happy_birthday_index: Current index for happy birthday coupon numbering.
        - happy_birthday_discount: Discount percentage for happy birthday coupons.
        - referred: Text identifier for referred coupons.
        - referred_discount: Discount percentage for referred coupons.
        - referred_index: Current index for referred coupon numbering.
        Methods:
        - __new__: Initializes the Singleton instance with coupon rules and database.
        - create_coupon: Creates a generic coupon with specified text, discount, and expiration days.
        - create_happy_birthday_coupon: Creates a happy birthday coupon with predefined rules and expiration date.
        - create_referred_coupon: Creates a referred coupon with predefined rules and expiration date.
    """

    _instance = None
    def __new__(cls, *args, **kwargs):
        """
        Initializes the Singleton instance of the CouponFactory.
        Sets up the coupon database connection and initializes coupon rules for happy birthday and referred coupons.
        Returns:
        - The Singleton instance of the CouponFactory.
        """
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
        """
        Creates a generic coupon with specified text, discount, and expiration days.
        Args:
        - text: The text description of the coupon.
        - discount: The discount percentage as a float (e.g., 0.2 for 20%).
        - days: The number of days until the coupon expires.
        Returns:
        - The created Coupon instance.
        """
        expiration_date = COUPON_RULES.get_expiration_date(days)
        new_coupon = self.coupon_db.create_coupon(text, 0, discount, expiration_date)
        return new_coupon
    
    def create_happy_birthday_coupon(self) -> Coupon:
        """
        Creates a happy birthday coupon with predefined rules and expiration date.
        The coupon text is set to the predefined happy birthday text, and the discount is set to the predefined happy birthday discount.
        The expiration date is determined by the happy birthday expiration rule.
        Returns:
        - The created happy birthday Coupon instance.
        """
        if self.coupon_db.get_last_coupon_by_text(self.happy_birthday) is None:
            self.happy_birthday_index = 1
        else: 
            self.happy_birthday_index = self.coupon_db.get_last_coupon_by_text(self.happy_birthday).id + 1

        new_coupon = self.coupon_db.create_coupon(self.happy_birthday, self.happy_birthday_index, self.happy_birthday_discount,\
                                                COUPON_RULES.get_happy_birthday_expiration_date())                         
        return new_coupon
    
    def create_referred_coupon(self) -> Coupon:
        """
        Creates a referred coupon with predefined rules and expiration date.
        The coupon text is set to the predefined referred text, and the discount is set to the predefined referred discount.
        The expiration date is determined by the referred expiration rule.
        Returns:
        - The created referred Coupon instance.
        """
        if self.coupon_db.get_last_coupon_by_text(self.referred) is None:
            self.referred_index = 1
        else: 
            self.referred_index = self.coupon_db.get_last_coupon_by_text(self.referred).id + 1

        new_coupon = self.coupon_db.create_coupon(self.referred, id, self.referred_discount,\
                                                  COUPON_RULES.get_referred_expiration_date())
        return new_coupon
    
""""
Here we declared the instance in order to use only one instance of the service in the application, 
and to be able to import it directly in the router.
"""
    
coupon_factory = CouponFactory()
    

    

    
    