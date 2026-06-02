"""
Module for location repository operations

This module defines the Repository class for managing location data,
including adding, retrieving, and deleting locations.

Author: Juan Nicolás Diaz Salamanca <jndiaz@udistrital.edu.co>
"""

import app.models.location as location

class Repository:

    """
    Manage a collection of Location objects.
    Attributes:
        __locations (list): A private list to store Location objects.
        __index (int): A private index to assign unique IDs to locations.
    Methods:
        __init__(): Initializes the Repository with predefined locations.
        create_location(name: str, description: str, address: str, latitude: float, longitude: float) -> location.Location:
            Creates a new Location object with the provided attributes.
        add_location(name: str, description: str, address: str, latitude: float, longitude: float) -> None:
            Adds a new Location object to the repository.
        get_location_by_id(location_id: int) -> location.Location:
            Retrieves a Location object by its unique identifier.
        get_location_by_name(name: str) -> location.Location:
            Retrieves a Location object by its name.
        get_location_by_address(address: str) -> location.Location:
            Retrieves a Location object by its physical address.
        get_location_by_coordinates(latitude: float, longitude: float) -> location.Location:
            Retrieves a Location object by its geographic coordinates.
        get_all_locations() -> list:
            Returns a list of all Location objects in the repository.
        delete_location(location_id: int) -> bool:
            Deletes a Location object from the repository by its unique identifier.
    """

    def __init__(self):
        """
        Initializes the Repository with a predefined set of locations.

        Each location is created with a unique ID and stored in the __locations list.
        """
        self.__locations = []
        self.__index = 0

        self.add_location(name="Sede calle 40", \
                                     description="Sede de la Universidad Distrital Francisco José de Caldas", \
                                     address="Cra 7 #40-62, Bogotá, Colombia", \
                                        latitude=4.628101562385973, longitude=-74.06592693333083)
        self.add_location(name="Sede macarena A",
                                     description="Sede de la Universidad Distrital Francisco José de Caldas", \
                                     address="Cra 3 #N26A-40, Bogotá, Colombia", \
                                     latitude=4.613573017288183, longitude=-74.06404637326503)
        self.add_location(name="Sede macarena B",
                                     description="Sede de la Universidad Distrital Francisco José de Caldas", \
                                     address="Cra 3A #26B-1, Bogotá, Colombia", \
                                     latitude=4.6135794463079245,longitude=-74.06526948179399)
        self.add_location(name="Sede calle 34",
                                     description="Sede de la Universidad Distrital Francisco José de Caldas", \
                                     address="Cl 34 #13-15, Bogotá, Colombia", \
                                     latitude=4.621984336272019, longitude=-74.06837850449529)
        self.add_location(name="Sede Tecnologica",
                                     description="Sede de la Universidad Distrital Francisco José de Caldas", \
                                     address="Cl 68d Bis A Sur #49F - 70 Bloque 6, piso 1, Tecnológica, Bogotá", \
                                     latitude=4.579922365316238, longitude=-74.15757937482532)
        self.add_location(name="Sede Bosa",
                                     description="Sede de la Universidad Distrital Francisco José de Caldas", \
                                     address="Cl 52 Sur #93d-39, Bogotá, Colombia", \
                                     latitude=4.6384071630332, longitude=-74.1862601018121)
        self.add_location(name="Sede Vivero",
                                     description="Sede de la Universidad Distrital Francisco José de Caldas", \
                                     address="Cra 5 #15-82, Bogotá", \
                                     latitude=4.597362864708261, longitude=-74.06460621077917)
        self.add_location(name="Sede ASAB",
                                     description="Sede de la Universidad Distrital Francisco José de Caldas",
                                     address="Cra 15 #15-2, Bogotá, Colombia", \
                                     latitude=4.6048557389443046, longitude=-74.07873154783844)
        self.add_location(name="Sede Paiba",
                                     description="Sede de la Universidad Distrital Francisco José de Caldas",
                                     address="Cl 13 #31-75, Bogotá, Colombia", \
                                     latitude=4.615281339898904, longitude=-74.09331682907303)

    def create_location(self, name: str, description: str, address: str, \
                        latitude: float, longitude: float) -> location.Location:
        """
        Creates a new Location object with the provided attributes.
        Args:
            name (str): The name of the location.
            description (str): A brief description of the location.
            address (str): The physical address of the location.
            latitude (float): The latitude coordinate of the location.
            longitude (float): The longitude coordinate of the location.

        Returns:
            location.Location: A new Location object with a unique ID and the provided attributes.
        """
        self.__index +=1
        return location.Location(id=self.__index, name=name, description=description, \
                                 address=address, latitude=latitude, longitude=longitude)
    
    def add_location(self, name: str, description: str, address: str, \
                     latitude: float, longitude: float) -> None:
        """
        Adds a new Location object to the repository.
        Args:
            name (str): The name of the location.
            description (str): A brief description of the location.
            address (str): The physical address of the location.
            latitude (float): The latitude coordinate of the location.
            longitude (float): The longitude coordinate of the location.

        Returns:
            None
        """
        
        self.__locations.append(self.create_location(name=name, description=description, address=address, \
                                                  latitude=latitude, longitude=longitude))
    
    def get_location_by_id(self, location_id: int) -> location.Location:
        """
        Retrieves a Location object by its unique identifier.
        Args:
            location_id (int): The unique identifier of the location to retrieve.
        
        Returns:
            location.Location: The Location object with the specified ID, or None if not found.
        """
        for loc in self.__locations:
            if loc.id == location_id:
                return loc
        return None
    
    def get_location_by_name(self, name: str) -> location.Location:
        """
        Retrieves a Location object by its name.
        Args:
            name (str): The name of the location to retrieve.

        Returns:
            location.Location: The Location object with the specified name, or None if not found.
        """
        for loc in self.__locations:
            if loc.name == name:
                return loc
        return None
    
    def get_location_by_address(self, address: str) -> location.Location:
        """
        Retrieves a Location object by its physical address.
        Args:
            address (str): The physical address of the location to retrieve.

        Returns:
            location.Location: The Location object with the specified address, or None if not found.
        """
        for loc in self.__locations:
            if loc.address == address:
                return loc
        return None
    
    def get_location_by_coordinates(self, latitude: float, longitude: float) -> location.Location:
        """
        Retrieves a Location object by its geographic coordinates.
        Args:
            latitude (float): The latitude coordinate of the location to retrieve.
            longitude (float): The longitude coordinate of the location to retrieve.
        
        Returns:
            location.Location: The Location object with the specified coordinates, or None if not found.
        """
        for loc in self.__locations:
            if loc.latitude == latitude and loc.longitude == longitude:
                return loc
        return None
    
    def get_all_locations(self) -> list:
        """
        Returns a list of all Location objects in the repository.

        Returns:
            list: A list containing all Location objects currently stored in the repository.
        """
        return self.__locations
    
    def delete_location(self, location_id: int) -> bool:
        """Deletes a Location object from the repository by its unique identifier.
        Args:            
            location_id (int): The unique identifier of the location to delete.
            
        Returns:
            bool: True if the location was successfully deleted, False if the location was not found.
        """
        for i, loc in enumerate(self.__locations):
            if loc.id == location_id:
                del self.__locations[i]
                return True
        return False