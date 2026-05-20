from fastapi import APIRouter

router = APIRouter()


@router.get("/geolocation")
async def get_geolocation():
    return {"message": "This is the geolocation endpoint"}

