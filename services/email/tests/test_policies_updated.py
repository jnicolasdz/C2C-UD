from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class FakeSMTP:
    def __init__(self, host: str, port: int, timeout: int | float | None = None) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self.ehlo_calls = 0
        self.started_tls = False
        self.auth_commands: list[tuple[str, str]] = []
        self.sent_messages: list[object] = []

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


def test_policies_updated_sends_email(monkeypatch) -> None:
    monkeypatch.setenv("SMTP_USERNAME", "birdot19@gmail.com")
    monkeypatch.setenv("SMTP_PASSWORD", "app-password")
    monkeypatch.setenv("SMTP_FROM", "birdot19@gmail.com")
    monkeypatch.setenv("EMAIL_SERVICE_API_KEY", "sk_internal_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6")
    monkeypatch.setattr("app.services.email_service.SMTP", FakeSMTP)

    response = client.post(
        "/api/v1/emails/moderation/policies-updated",
        headers={"X-API-Key": "sk_internal_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"},
        json={
            "recipients": [
                {
                    "codigo_user": 24,
                    "correo_institu": "judlozanol@udistrital.edu.co",
                    "primer_nomb": "Julio",
                },
                {
                    "codigo_user": 25,
                    "correo_institu": "testuser@udistrital.edu.co",
                    "primer_nomb": "Ana",
                },
            ],
            "id_doc": 12,
            "tipo_doc": "Reglamento de uso",
            "version_nueva": "2.0",
            "resumen_cambios": "Actualización de plazos, requisitos y sanciones por incumplimiento.",
            "numero_contrato": 4321,
            "enlace_documento": "https://example.com/politicas",
            "fecha_vigencia": "2026-07-01",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["message"] == "Notificación de políticas procesada."
    assert body["correlation_id"] is None
    assert body["data"]["total_recipients"] == 2
    assert body["data"]["sent_successfully"] == 2
    assert body["data"]["failed"] == 0
    assert body["data"]["id_doc"] == 12
    assert body["data"]["version_nueva"] == "2.0"
    assert "timestamp" in body["data"]


def test_policies_updated_rejects_invalid_date(monkeypatch) -> None:
    monkeypatch.setenv("SMTP_USERNAME", "birdot19@gmail.com")
    monkeypatch.setenv("SMTP_PASSWORD", "app-password")
    monkeypatch.setenv("SMTP_FROM", "birdot19@gmail.com")
    monkeypatch.setenv("EMAIL_SERVICE_API_KEY", "sk_internal_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6")

    response = client.post(
        "/api/v1/emails/moderation/policies-updated",
        headers={"X-API-Key": "sk_internal_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"},
        json={
            "recipients": [
                {
                    "codigo_user": 24,
                    "correo_institu": "judlozanol@udistrital.edu.co",
                    "primer_nomb": "Julio",
                }
            ],
            "id_doc": 12,
            "tipo_doc": "Reglamento de uso",
            "version_nueva": "2.0",
            "resumen_cambios": "Actualización de plazos, requisitos y sanciones por incumplimiento.",
            "numero_contrato": 4321,
            "fecha_vigencia": "01-07-2026",
        },
    )

    assert response.status_code == 400
    body = response.json()
    assert body["success"] is False
    assert body["error_code"] == "VAL_003"
