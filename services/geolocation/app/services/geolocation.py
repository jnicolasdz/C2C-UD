"""
Module for geolocation service operations

This module defines the GeolocationService class for managing location data operations,
including retrieving, creating, and deleting locations with validation.

Author: Juan Nicolás Diaz Salamanca <jndiazs@udistrital.edu.co>
"""

import app.models.repository as repository_module

class GeolocationService:
    """
    Provide geolocation service operations with validation.
    
    Attributes:
        repository (repository_module.Repository): A Repository instance for managing location data.
    
    Methods:
        __init__(): Initializes the GeolocationService with a Repository instance.
        get_location_by_id(location_id: int) -> dict:
            Retrieves a location by its unique identifier.
        get_location_by_name(name: str) -> dict:
            Retrieves a location by its name.
        get_location_by_address(address: str) -> dict:
            Retrieves a location by its physical address.
        get_all_locations() -> list:
            Returns a list of all available locations.
        create_location(name: str, description: str, address: str, latitude: float, longitude: float) -> None:
            Creates and adds a new location to the repository.
        delete_location(location_id: int) -> bool:
            Deletes a location by its unique identifier.
    """

    def __init__(self):
        """
        Initializes the GeolocationService with a Repository instance.
        """
        self.repository = repository_module.Repository()

    def get_location_by_id(self, location_id: int) -> dict:
        """
        Retrieves a location by its unique identifier.
        
        Args:
            location_id (int): The unique identifier of the location to retrieve.
        
        Returns:
            dict: A dictionary representation of the Location object.
        
        Raises:
            ValueError: If no location with the given ID exists.
        """
        if self.repository.get_location_by_id(location_id=location_id) is None:
            raise ValueError("Location with the given ID does not exist.")
        return self.repository.get_location_by_id(location_id=location_id).to_dict()
    
    def get_location_by_name(self, name: str) -> dict:
        """
        Retrieves a location by its name.
        
        Args:
            name (str): The name of the location to retrieve.
        
        Returns:
            dict: A dictionary representation of the Location object.
        
        Raises:
            ValueError: If no location with the given name exists.
        """
        if self.repository.get_location_by_name(name=name) is None:
            raise ValueError("Location with the given name does not exist.")
        return self.repository.get_location_by_name(name=name).to_dict()
    
    def get_location_by_address(self, address: str) -> dict:
        """
        Retrieves a location by its physical address.
        
        Args:
            address (str): The physical address of the location to retrieve.
        
        Returns:
            dict: A dictionary representation of the Location object.
        
        Raises:
            ValueError: If no location with the given address exists.
        """
        if self.repository.get_location_by_address(address=address) is None:
            raise ValueError("Location with the given address does not exist.")
        return self.repository.get_location_by_address(address=address).to_dict()

    def get_all_locations(self) -> list:
        """
        Returns a list of all available locations.
        
        Returns:
            list: A list of dictionaries, each representing a Location object.
        
        Raises:
            ValueError: If no locations are available in the repository.
        """
        if self.repository.get_all_locations() is None or len(self.repository.get_all_locations()) == 0:
            raise ValueError("No locations available.")
        return [loc.to_dict() for loc in self.repository.get_all_locations()]
    
    def create_location(self, name: str, description: str, address: str, latitude: float, longitude: float) -> None:
        """
        Creates and adds a new location to the repository.
        
        Args:
            name (str): The name of the location.
            description (str): A brief description of the location.
            address (str): The physical address of the location.
            latitude (float): The latitude coordinate of the location.
            longitude (float): The longitude coordinate of the location.
        
        Returns:
            None
        
        Raises:
            ValueError: If a location with the same coordinates already exists.
        """
        if self.repository.get_location_by_coordinates(latitude=latitude, longitude=longitude) is not None:
            raise ValueError("A location with the same coordinates already exists.")
        else:
            self.repository.add_location(name=name, description=description, address=address, latitude=latitude, longitude=longitude)

    def delete_location(self, location_id: int) -> bool:
        """
        Deletes a location by its unique identifier.
        
        Args:
            location_id (int): The unique identifier of the location to delete.
        
        Returns:
            bool: True if the location was successfully deleted.
        
        Raises:
            ValueError: If no location with the given ID exists.
        """
        if self.repository.delete_location(location_id=location_id):
            return True
        else:
            raise ValueError("Location with the given ID does not exist.")
