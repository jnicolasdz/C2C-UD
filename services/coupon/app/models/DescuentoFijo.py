from pydantic import Field
from .DescuentoBase import DescuentoBase
class DescuentoFijo(DescuentoBase):
    valor: float = Field(..., gt=0)  # Monto fijo mayor a 0

    def calcular_descuento(self, total_carrito: float) -> float:
        return min(self.valor, total_carrito)  # No puede descontar más del total
