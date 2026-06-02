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
        self.sent_message = None

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
        self.sent_message = message


def test_send_otp_sends_email(monkeypatch) -> None:
    monkeypatch.setenv("SMTP_USERNAME", "birdot19@gmail.com")
    monkeypatch.setenv("SMTP_PASSWORD", "app-password")
    monkeypatch.setenv("SMTP_FROM", "birdot19@gmail.com")
    monkeypatch.setenv("EMAIL_SERVICE_API_KEY", "sk_internal_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6")
    monkeypatch.setattr("app.services.email_service.SMTP", FakeSMTP)

    response = client.post(
        "/api/v1/emails/auth/send-otp",
        headers={"X-API-Key": "sk_internal_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"},
        json={
            "codigo_user": 10,
            "correo_institu": "judlozanol@udistrital.edu.co",
            "otp_code": "482910",
            "expiration_minutes": 5,
            "primer_nomb": "Birdot",
            "device_hint": "Chrome en Windows",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["message"] == "OTP enviado exitosamente."
    assert body["correlation_id"] is None
    assert body["data"]["email_sent_to"] == "judlozanol@udistrital.edu.co"
    assert body["data"]["otp_expires_in_minutes"] == 5
    assert body["data"]["template_used"] == "auth/otp_code.html"


def test_send_otp_rejects_invalid_otp_code(monkeypatch) -> None:
    monkeypatch.setenv("SMTP_USERNAME", "birdot19@gmail.com")
    monkeypatch.setenv("SMTP_PASSWORD", "app-password")
    monkeypatch.setenv("SMTP_FROM", "birdot19@gmail.com")
    monkeypatch.setenv("EMAIL_SERVICE_API_KEY", "sk_internal_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6")

    response = client.post(
        "/api/v1/emails/auth/send-otp",
        headers={"X-API-Key": "sk_internal_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"},
        json={
            "codigo_user": 10,
            "correo_institu": "judlozanol@udistrital.edu.co",
            "otp_code": "48291A",
            "expiration_minutes": 5,
        },
    )

    assert response.status_code == 400
    body = response.json()
    assert body["success"] is False
    assert body["error_code"] == "VAL_003"