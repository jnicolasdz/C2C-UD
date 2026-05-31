"""
Module for location data model and operations.

This module defines the Location model using Pydantic for data validation
and serialization of geolocation information.

Author: Juan Nicolás Diaz Salamanca <jndiaz@udistrital.edu.co>
"""

from pydantic import BaseModel
class Location(BaseModel):
    """
    Represents a geographic location with metadata.
        
    This model encapsulates location data including identification,
    descriptive information, and geographic coordinates.
        
    Attributes:
        id (int): Unique identifier for the location.
        name (str): The name of the location.
        description (str): A detailed description of the location.
        address (str): The physical address of the location.
        latitude (float): The latitude coordinate of the location.
        longitude (float): The longitude coordinate of the location.
    """

    id : int 
    name : str
    description : str
    address : str
    latitude : float
    longitude : float

    def __str__(self):
        """
        Return a string representation of the Location object.
            
        Returns:
            str: A formatted string containing all location attributes.
        """
        return f"Location(id={self.id}, name='{self.name}', description='{self.description}', address='{self.address}', latitude={self.latitude}, longitude={self.longitude})"

    def to_dict(self):
        """
        Convert the Location object to a dictionary.
            
        Returns:
            dict: A dictionary containing all location attributes as key-value pairs.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude
        }
    
    

    
