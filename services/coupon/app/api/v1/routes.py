from fastapi import APIRouter

router = APIRouter()

@router.get("/coupon")
async def get_coupon():
    return {"message": "This is the coupon endpoint"}

