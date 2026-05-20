from fastapi import FastAPI

from app.api.v1.routes import router

app = FastAPI(title="Coupon Service")
app.include_router(router, prefix="/api/v1")
