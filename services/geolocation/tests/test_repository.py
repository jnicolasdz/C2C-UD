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
    "latitude": 4.648283,
    "longitude": -74.062759,
}

NEW_LOCATION_DATA = {
    "name": "Sede Nueva",
    "description": "Nueva sede de prueba",
    "address": "Calle 100 #10-20, Bogotá, Colombia",
    "latitude": 4.700000,
    "longitude": -74.050000,
}

class TestRepository:
    """Pruebas del repositorio en memoria."""

    @pytest.fixture
    def repo(self):
        from app.models.repository import Repository
        return Repository()

    # --- Consultas por ID ---

    def test_get_location_by_id_found(self, repo):
        """Recupera una ubicación existente por su ID."""
        loc = repo.get_location_by_id(1)
        assert loc is not None
        assert loc.id == 1

    def test_get_location_by_id_not_found(self, repo):
        """Devuelve None cuando el ID no existe."""
        assert repo.get_location_by_id(9999) is None

    # --- Consultas por nombre ---

    def test_get_location_by_name_found(self, repo):
        """Recupera una ubicación existente por su nombre."""
        loc = repo.get_location_by_name("Sede calle 40")
        assert loc is not None
        assert loc.name == "Sede calle 40"

    def test_get_location_by_name_not_found(self, repo):
        """Devuelve None cuando el nombre no existe."""
        assert repo.get_location_by_name("Sede Inexistente") is None

    # --- Consultas por dirección ---

    def test_get_location_by_address_found(self, repo):
        """Recupera una ubicación existente por su dirección."""
        loc = repo.get_location_by_address("Cra 7 #40-62, Bogotá, Colombia")
        assert loc is not None
        assert loc.address == "Cra 7 #40-62, Bogotá, Colombia"

    def test_get_location_by_address_not_found(self, repo):
        """Devuelve None cuando la dirección no existe."""
        assert repo.get_location_by_address("Calle Falsa 123") is None

    # --- Consultas por coordenadas ---

    def test_get_location_by_coordinates_found(self, repo):
        """Recupera una ubicación existente por sus coordenadas exactas."""
        loc = repo.get_location_by_coordinates(4.648283, -74.062759)
        assert loc is not None

    def test_get_location_by_coordinates_not_found(self, repo):
        """Devuelve None cuando las coordenadas no corresponden a ninguna sede."""
        assert repo.get_location_by_coordinates(0.0, 0.0) is None

    # --- Agregar ubicaciones ---

    def test_add_location_increases_count(self, repo):
        """Agregar una nueva ubicación incrementa el total de sedes almacenadas."""
        initial_ids = [i for i in range(1, 100) if repo.get_location_by_id(i)]
        repo.add_location(**NEW_LOCATION_DATA)
        new_ids = [i for i in range(1, 100) if repo.get_location_by_id(i)]
        assert len(new_ids) == len(initial_ids) + 1

    def test_add_location_assigns_auto_id(self, repo):
        """El ID asignado automáticamente es mayor que cero."""
        repo.add_location(**NEW_LOCATION_DATA)
        loc = repo.get_location_by_name("Sede Nueva")
        assert loc is not None
        assert loc.id > 0

    def test_add_location_is_retrievable(self, repo):
        """Una ubicación recién añadida se puede recuperar por nombre."""
        repo.add_location(**NEW_LOCATION_DATA)
        loc = repo.get_location_by_name("Sede Nueva")
        assert loc.address == NEW_LOCATION_DATA["address"]

    # --- Eliminar ubicaciones ---

    def test_delete_location_returns_true(self, repo):
        """Eliminar una ubicación existente devuelve True."""
        assert repo.delete_location(1) is True

    def test_delete_location_not_found_returns_false(self, repo):
        """Eliminar una ubicación inexistente devuelve False."""
        assert repo.delete_location(9999) is False

    def test_delete_location_actually_removes_it(self, repo):
        """Tras eliminar una ubicación, ya no se puede recuperar por ID."""
        repo.delete_location(1)
        assert repo.get_location_by_id(1) is None