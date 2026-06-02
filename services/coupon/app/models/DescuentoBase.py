from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from datetime import datetime
class DescuentoBase(BaseModel, ABC):
    codigo: str = Field(..., min_length=5, max_length=20)
    fecha_expiracion: datetime
    es_activo: bool = True

    @abstractmethod
    def calcular_descuento(self, total_carrito: float) -> float:
        pass