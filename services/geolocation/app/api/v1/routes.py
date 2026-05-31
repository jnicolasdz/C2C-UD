from fastapi import APIRouter
from app.services.geolocation import GeolocationService

router = APIRouter()
service = GeolocationService()

@router.get("/geolocation/id/{location_id}")
async def get_location_by_id(location_id: int):
    try:
        return service.get_location_by_id(location_id)
    except ValueError as e:
        return {"error": str(e)}

@router.get("/geolocation/name/{name}")
async def get_location_by_name(name: str):
    try:
        return service.get_location_by_name(name)
    except ValueError as e:
        return {"error": str(e)}

@router.get("/geolocation/address/{address}")
async def get_location_by_address(address: str):
    try:
        return service.get_location_by_address(address)
    except ValueError as e:
        return {"error": str(e)}

@router.get("/geolocation/all_address")
async def get_all_locations():
    try:
        return service.get_all_locations()
    except ValueError as e:
        return {"error": str(e)}

@router.post("/geolocation/add/{name}/{description}/{address}/{latitude}/{longitude}")
async def create_location(name: str, description: str, address: str, latitude: float, longitude: float):
    try:
        service.create_location(name, description, address, latitude, longitude)
        return {"message": "Location created successfully"}
    except ValueError as e:
        return {"error": str(e)}

@router.delete("/geolocation/{location_id}")
async def delete_location(location_id: int):
    try:
        service.delete_location(location_id)
        return {"message": "Location deleted successfully"}
    except ValueError as e:
        return {"error": str(e)}



