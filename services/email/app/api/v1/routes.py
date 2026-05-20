from fastapi import APIRouter

router = APIRouter()


@router.get("/email")
def health_check() -> dict[str, str]:
    return {"message": "This is the email endpoint"}
