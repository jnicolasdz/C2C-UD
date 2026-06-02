from pydantic import BaseModel, Field

class SolicitudCupon(BaseModel):
    codigo: str
    total_carrito: float = Field(..., gt=0)

