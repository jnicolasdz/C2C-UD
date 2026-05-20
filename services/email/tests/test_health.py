from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/v1/email")
    assert response.status_code == 200
    assert response.json() == {"message": "This is the email endpoint"}
