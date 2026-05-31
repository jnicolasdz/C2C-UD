import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

SAMPLE_LOCATION_DATA = {
    "id": 1,
    "name": "Sede calle 40",
    "description": "Sede de la Universidad Distrital Francisco José de Caldas",
    "address": "Cra 7 #40-62, Bogotá, Colombia",
    "latitude": 4.628101562385973,
    "longitude": -74.06592693333083,
}

NEW_LOCATION_DATA = {
    "name": "Sede Nueva",
    "description": "Nueva sede de prueba",
    "address": "Calle 100 #10-20, Bogotá, Colombia",
    "latitude": 4.700000,
    "longitude": -74.050000,
}


class TestLocationModel:
    """Pruebas del modelo de datos Location."""

    def _make_location(self):
        from app.models.location import Location
        return Location(**SAMPLE_LOCATION_DATA)

    def test_location_creation(self):
        """El modelo se crea correctamente con todos sus campos."""
        loc = self._make_location()
        assert loc.id == 1
        assert loc.name == "Sede calle 40"
        assert loc.latitude == 4.628101562385973
        assert loc.longitude == -74.06592693333083

    def test_to_dict_returns_all_fields(self):
        """to_dict() devuelve un diccionario con las seis claves esperadas."""
        loc = self._make_location()
        d = loc.to_dict()
        assert set(d.keys()) == {"id", "name", "description", "address", "latitude", "longitude"}

    def test_to_dict_values_match(self):
        """Los valores de to_dict() coinciden con los datos originales."""
        loc = self._make_location()
        assert loc.to_dict() == SAMPLE_LOCATION_DATA

    def test_str_representation(self):
        """__str__ incluye el id y el nombre de la sede."""
        loc = self._make_location()
        s = str(loc)
        assert "1" in s
        assert "Sede calle 40" in s