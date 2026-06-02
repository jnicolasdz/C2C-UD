from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


class FakeSMTP:
    def __init__(self, host: str, port: int, timeout: int | float | None = None) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self.ehlo_calls = 0
        self.started_tls = False
        self.auth_commands: list[tuple[str, str]] = []
        self.sent_messages = []

    def __enter__(self) -> "FakeSMTP":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def ehlo(self) -> None:
        self.ehlo_calls += 1

    def starttls(self, context=None) -> None:
        self.started_tls = True

    def docmd(self, command: str, args: str = "") -> tuple[int, bytes]:
        self.auth_commands.append((command, args))
        if command == "AUTH" and args.startswith("PLAIN "):
            return 235, b"2.7.0 Accepted"
        return 500, b"Unsupported command"

    def send_message(self, message) -> None:
        self.sent_messages.append(message)


def test_news_sends_campaign(monkeypatch) -> None:
    monkeypatch.setenv("SMTP_USERNAME", "test_user")
    monkeypatch.setenv("SMTP_PASSWORD", "test_password")
    monkeypatch.setenv("SMTP_FROM", "no-reply@example.com")
    monkeypatch.setenv("EMAIL_SERVICE_API_KEY", "test-api-key")

    monkeypatch.setattr("app.services.email_service.SMTP", FakeSMTP)

    client = TestClient(app)
    response = client.post(
        "/api/v1/emails/newsletters/news",
        headers={"X-API-Key": "test-api-key"},
        json={
            "recipients": [
                {
                    "codigo_user": 10,
                    "correo_institu": "judlozanol@udistrital.edu.co",
                    "primer_nomb": "Julio",
                },
                {
                    "codigo_user": 11,
                    "correo_institu": "otro@udistrital.edu.co",
                    "primer_nomb": "Ana",
                },
            ],
            "titulo_boletin": "Novedades C2C",
            "contenido_html": "<p>Tenemos noticias interesantes para ti.</p>",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["message"] == "Boletín procesado."
    assert body["correlation_id"] is None
    assert body["data"]["total_recipients"] == 2
    assert body["data"]["sent_successfully"] == 2
    assert body["data"]["failed"] == 0
    assert "timestamp" in body["data"]
