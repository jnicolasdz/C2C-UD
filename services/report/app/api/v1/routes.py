from fastapi import APIRouter

router = APIRouter()


@router.get("/report")
async def get_report():
    return {"message": "This is the report endpoint"}
