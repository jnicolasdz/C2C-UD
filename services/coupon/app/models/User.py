from pydantic import BaseModel
"""
    Module for user data model and operations.
    This module defines the user model using Pydantic for data validation
    and serialization of user information.
    Author: Juan Nicolás Diaz Salamanca <jndiazs@udistrital.edu.co>
"""
class User(BaseModel):

    """
        Represents a user with their coupons and methods for serialization.
        Attributes:
        - user_email: Email address of the user (unique identifier).
        - unassigned_coupons: List of coupon codes that have been generated but not yet assigned to the user.
        - assigned_coupons: List of coupon codes that have been successfully assigned to the user.
        Methods:
        - __str__: Returns a string representation of the user.
        - __to_dict__: Returns a dictionary representation of the user for serialization.
    """
    
    user_email: str
    unassigned_coupons: list[str] = []
    assigned_coupons: list[str] = []

    def __str__(self):
        """
        Returns a string representation of the user.
        The string includes the user's email address.
        """
        return f"User(user_email={self.user_email})"
    
    def __to_dict__(self):
        """
        Returns a dictionary representation of the user for serialization.
        The dictionary includes the user's email, unassigned coupons, and assigned coupons.
        """
        return {
            "user": self.user_email,
            "unassigned_coupons": self.unassigned_coupons,
            "assigned_coupons": self.assigned_coupons
            
        }