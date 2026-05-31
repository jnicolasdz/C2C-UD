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

class TestGeolocationService:
    """Pruebas del servicio de geolocalización con repositorio mockeado."""

    @pytest.fixture
    def mock_repo(self):
        return MagicMock()

    @pytest.fixture
    def service(self, mock_repo):
        from app.services.geolocation import GeolocationService
        svc = GeolocationService()
        svc.repository = mock_repo
        return svc

    def _location_mock(self, data=None):
        """Crea un mock de Location que implementa to_dict()."""
        d = data or SAMPLE_LOCATION_DATA
        loc = MagicMock()
        loc.to_dict.return_value = d
        return loc

    # --- get_location_by_id ---

    def test_get_by_id_returns_dict(self, service, mock_repo):
        """get_location_by_id devuelve un diccionario cuando la ubicación existe."""
        mock_repo.get_location_by_id.return_value = self._location_mock()
        result = service.get_location_by_id(1)
        assert result == SAMPLE_LOCATION_DATA

    def test_get_by_id_raises_when_not_found(self, service, mock_repo):
        """get_location_by_id lanza ValueError cuando el ID no existe."""
        mock_repo.get_location_by_id.return_value = None
        with pytest.raises(ValueError, match="does not exist"):
            service.get_location_by_id(9999)

    # --- get_location_by_name ---

    def test_get_by_name_returns_dict(self, service, mock_repo):
        """get_location_by_name devuelve un diccionario cuando el nombre existe."""
        mock_repo.get_location_by_name.return_value = self._location_mock()
        result = service.get_location_by_name("Sede calle 40")
        assert result["name"] == "Sede calle 40"

    def test_get_by_name_raises_when_not_found(self, service, mock_repo):
        """get_location_by_name lanza ValueError cuando el nombre no existe."""
        mock_repo.get_location_by_name.return_value = None
        with pytest.raises(ValueError, match="does not exist"):
            service.get_location_by_name("Desconocida")

    # --- get_location_by_address ---

    def test_get_by_address_returns_dict(self, service, mock_repo):
        """get_location_by_address devuelve un diccionario cuando la dirección existe."""
        mock_repo.get_location_by_address.return_value = self._location_mock()
        result = service.get_location_by_address("Cra 7 #40-62, Bogotá, Colombia")
        assert "address" in result

    def test_get_by_address_raises_when_not_found(self, service, mock_repo):
        """get_location_by_address lanza ValueError cuando la dirección no existe."""
        mock_repo.get_location_by_address.return_value = None
        with pytest.raises(ValueError, match="does not exist"):
            service.get_location_by_address("Calle Falsa 123")

    # --- create_location ---

    def test_create_location_calls_add(self, service, mock_repo):
        """create_location llama a repository.add_location cuando las coordenadas son nuevas."""
        mock_repo.get_location_by_coordinates.return_value = None
        service.create_location(**NEW_LOCATION_DATA)
        mock_repo.add_location.assert_called_once_with(
            name=NEW_LOCATION_DATA["name"],
            description=NEW_LOCATION_DATA["description"],
            address=NEW_LOCATION_DATA["address"],
            latitude=NEW_LOCATION_DATA["latitude"],
            longitude=NEW_LOCATION_DATA["longitude"],
        )

    def test_create_location_raises_on_duplicate_coordinates(self, service, mock_repo):
        """create_location lanza ValueError si ya existe una ubicación con esas coordenadas."""
        mock_repo.get_location_by_coordinates.return_value = self._location_mock()
        with pytest.raises(ValueError, match="coordinates already exists"):
            service.create_location(**NEW_LOCATION_DATA)

    def test_create_location_does_not_add_on_duplicate(self, service, mock_repo):
        """create_location no llama a add_location si las coordenadas ya están registradas."""
        mock_repo.get_location_by_coordinates.return_value = self._location_mock()
        with pytest.raises(ValueError):
            service.create_location(**NEW_LOCATION_DATA)
        mock_repo.add_location.assert_not_called()

    # --- delete_location ---

    def test_delete_location_returns_true(self, service, mock_repo):
        """delete_location devuelve True cuando la ubicación existe y se elimina."""
        mock_repo.delete_location.return_value = True
        assert service.delete_location(1) is True

    def test_delete_location_raises_when_not_found(self, service, mock_repo):
        """delete_location lanza ValueError cuando el ID no existe."""
        mock_repo.delete_location.return_value = False
        with pytest.raises(ValueError, match="does not exist"):
            service.delete_location(9999)