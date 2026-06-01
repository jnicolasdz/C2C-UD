from .DescuentoBase import DescuentoBase
from .DescuentoFactory import DescuentoFactory
from .DescuentoPorcentaje import DescuentoPorcentaje
from .DescuentoFijo import DescuentoFijo
from typing import Dict, Any

class FastAPIDescuentoFactory(DescuentoFactory):
    def crear_descuento(self, tipo: str, datos: Dict[str, Any]) -> DescuentoBase:
        if tipo == "porcentaje":
            return DescuentoPorcentaje(**datos)
        elif tipo == "fijo":
            return DescuentoFijo(**datos)
        else:
            raise ValueError(f"Tipo de descuento '{tipo}' no soportado por la fábrica.")
