from pydantic import Field
from .DescuentoBase import DescuentoBase
class DescuentoPorcentaje(DescuentoBase):
    valor: float = Field(..., gt=0, le=100)  # Debe estar entre 0% y 100%

    def calcular_descuento(self, total_carrito: float) -> float:
        return total_carrito * (self.valor / 100.0)