from abc import ABC, abstractmethod
from typing import Dict, Any
from .DescuentoBase import DescuentoBase

class DescuentoFactory(ABC):
    @abstractmethod
    def crear_descuento(self, tipo: str, datos: Dict[str, Any]) -> DescuentoBase:
        pass