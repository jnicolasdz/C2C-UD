from fastapi import APIRouter

router = APIRouter()


@router.get("/email")
def get_email() -> dict[str, str]:
    return {"message": "This is the email endpoint"}
