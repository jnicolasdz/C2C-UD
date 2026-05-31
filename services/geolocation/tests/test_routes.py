import pytest
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

class TestRoutes:
    """Pruebas de integración de los endpoints usando TestClient de FastAPI."""

    @pytest.fixture
    def client(self):
        from app.main import app
        return TestClient(app)

    # --- GET /geolocation/id/{location_id} ---

    def test_get_by_id_ok(self, client):
        """Endpoint GET por ID devuelve 200 y los datos de la ubicación."""
        response = client.get("/api/v1/geolocation/id/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert "name" in data

    def test_get_by_id_not_found(self, client):
        """Endpoint GET por ID devuelve un error cuando el ID no existe."""
        response = client.get("/api/v1/geolocation/id/9999")
        assert response.status_code == 200   # FastAPI devuelve 200 con cuerpo de error
        assert "error" in response.json()

    # --- GET /geolocation/name/{name} ---

    def test_get_by_name_ok(self, client):
        """Endpoint GET por nombre devuelve los datos correctos."""
        response = client.get("/api/v1/geolocation/name/Sede calle 40")
        assert response.status_code == 200
        assert response.json()["name"] == "Sede calle 40"

    def test_get_by_name_not_found(self, client):
        """Endpoint GET por nombre devuelve error cuando el nombre no existe."""
        response = client.get("/api/v1/geolocation/name/Sede Inexistente")
        assert "error" in response.json()

    # --- GET /geolocation/address/{address} ---

    def test_get_by_address_ok(self, client):
        """Endpoint GET por dirección devuelve los datos correctos."""
        response = client.get("/api/v1/geolocation/address/Cra 7 %2340-62%2C Bogotá%2C Colombia")
        assert response.status_code == 200
        assert "address" in response.json()

    def test_get_by_address_not_found(self, client):
        """Endpoint GET por dirección devuelve error cuando la dirección no existe."""
        response = client.get("/api/v1/geolocation/address/Calle%20falsa%20123")
        assert "error" in response.json()

    # --- POST /geolocation/add/... ---

    def test_create_location_ok(self, client):
        """Endpoint POST crea una nueva ubicación con coordenadas únicas."""
        response = client.post("/api/v1/geolocation/add/Sede%20Nueva/Nueva%20sede%20de%20prueba"
        "/Calle%20100%20%2310-20%2C%20Bogot%C3%A1%2C%20Colombia/4.700000/-74.050000"
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Location created successfully"

    def test_create_location_duplicate_coordinates(self, client):
        """Endpoint POST rechaza una ubicación con coordenadas ya registradas."""
        # Primero se crea
        response = client.post("/api/v1/geolocation/add/Sede%20Nueva/Nueva%20sede%20de%20prueba"
        "/Calle%20100%20%2310-20%2C%20Bogot%C3%A1%2C%20Colombia/4.700000/-74.050000"
        )
        # Segundo intento con las mismas coordenadas
        response = client.post("/api/v1/geolocation/add/Sede%20Nueva/Nueva%20sede%20de%20prueba"
        "/Calle%20100%20%2310-20%2C%20Bogot%C3%A1%2C%20Colombia/4.700000/-74.050000"
        )
        assert "error" in response.json()

    # --- DELETE /geolocation/{location_id} ---

    def test_delete_location_ok(self, client):
        """Endpoint DELETE elimina una ubicación existente correctamente."""
        response = client.delete("/api/v1/geolocation/1")
        assert response.status_code == 200
        assert response.json()["message"] == "Location deleted successfully"

    def test_delete_location_not_found(self, client):
        """Endpoint DELETE devuelve error cuando el ID no existe."""
        response = client.delete("/api/v1/geolocation/9999")
        assert "error" in response.json()

    def test_delete_location_is_actually_gone(self, client):
        """Tras eliminar una sede, consultarla por ID devuelve error."""
        client.delete("/api/v1/geolocation/2")
        response = client.get("/api/v1/geolocation/id/2")
        assert "error" in response.json()