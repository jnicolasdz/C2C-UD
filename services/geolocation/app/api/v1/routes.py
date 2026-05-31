"""
Module for geolocation API routes

This module defines the API endpoints for managing location data,
including retrieving, adding, and deleting locations via HTTP requests.

Author: Juan Nicolas Diaz Salamanca <jndiazs@udistrital.edu.co>
"""

from fastapi import APIRouter
from app.services.geolocation import GeolocationService

router = APIRouter()
service = GeolocationService()

class Routes:
    """
    Manage geolocation API endpoints.
    
    Methods:
        get_location_by_id(location_id: int) -> dict:
            Retrieves a Location object by its unique identifier.
        get_location_by_name(name: str) -> dict:
            Retrieves a Location object by its name.
        get_location_by_address(address: str) -> dict:
            Retrieves a Location object by its physical address.
        get_all_locations() -> dict:
            Returns a list of all Location objects.
        create_location(name: str, description: str, address: str, latitude: float, longitude: float) -> dict:
            Creates and adds a new Location object to the repository.
        delete_location(location_id: int) -> dict:
            Deletes a Location object from the repository by its unique identifier.
    """

@router.get("/geolocation/id/{location_id}")
async def get_location_by_id(location_id: int):
    """
    Retrieves a Location object by its unique identifier.
    Args:
        location_id (int): The unique identifier of the location to retrieve.
    
    Returns:
        dict: The Location object with the specified ID, or an error dictionary if not found.
    """
    try:
        return service.get_location_by_id(location_id)
    except ValueError as e:
        return {"error": str(e)}

@router.get("/geolocation/name/{name}")
async def get_location_by_name(name: str):
    """
    Retrieves a Location object by its name.
    Args:
        name (str): The name of the location to retrieve.

    Returns:
        dict: The Location object with the specified name, or an error dictionary if not found.
    """
    try:
        return service.get_location_by_name(name)
    except ValueError as e:
        return {"error": str(e)}

@router.get("/geolocation/address/{address}")
async def get_location_by_address(address: str):
    """
    Retrieves a Location object by its physical address.
    Args:
        address (str): The physical address of the location to retrieve.

    Returns:
        dict: The Location object with the specified address, or an error dictionary if not found.
    """
    try:
        return service.get_location_by_address(address)
    except ValueError as e:
        return {"error": str(e)}

@router.get("/geolocation/all_address")
async def get_all_locations():
    """
    Returns a list of all Location objects in the repository.

    Returns:
        dict: A list containing all Location objects currently stored, or an error dictionary if failed.
    """
    try:
        return service.get_all_locations()
    except ValueError as e:
        return {"error": str(e)}

@router.post("/geolocation/add/{name}/{description}/{address}/{latitude}/{longitude}")
async def create_location(name: str, description: str, address: str, latitude: float, longitude: float):
    """
    Creates and adds a new Location object to the repository.
    Args:
        name (str): The name of the location.
        description (str): A brief description of the location.
        address (str): The physical address of the location.
        latitude (float): The latitude coordinate of the location.
        longitude (float): The longitude coordinate of the location.

    Returns:
        dict: A success message if the location was created, or an error dictionary if it failed.
    """
    try:
        service.create_location(name, description, address, latitude, longitude)
        return {"message": "Location created successfully"}
    except ValueError as e:
        return {"error": str(e)}

@router.delete("/geolocation/{location_id}")
async def delete_location(location_id: int):
    """
    Deletes a Location object from the repository by its unique identifier.
    Args:
        location_id (int): The unique identifier of the location to delete.
        
    Returns:
        dict: A success message if the location was deleted, or an error dictionary if it failed.
    """
    try:
        service.delete_location(location_id)
        return {"message": "Location deleted successfully"}
    except ValueError as e:
        return {"error": str(e)}
