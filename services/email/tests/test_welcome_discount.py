from fastapi.testclient import TestClient

from app.main import app


class FakeSMTP:
    def __init__(self, host=None, port=None, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sent_messages = []
        self.auth_commands = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def ehlo(self):
        return True

    def starttls(self, context=None):
        return True

    def docmd(self, command: str, args: str = ""):
        self.auth_commands.append((command, args))
        if command == "AUTH" and args.startswith("PLAIN "):
            return 235, b"2.7.0 Accepted"
        return 500, b"Unsupported command"

    def send_message(self, message):
        self.sent_messages.append(message)


def test_send_welcome_discount_email_success(monkeypatch):
    monkeypatch.setenv('SMTP_USERNAME', 'test_user')
    monkeypatch.setenv('SMTP_PASSWORD', 'test_password')
    monkeypatch.setenv('SMTP_FROM', 'no-reply@example.com')
    monkeypatch.setenv('EMAIL_SERVICE_API_KEY', 'test-api-key')

    monkeypatch.setattr('app.services.email_service.SMTP', FakeSMTP)

    client = TestClient(app)
    response = client.post(
        '/api/v1/emails/promotions/welcome',
        headers={'X-API-Key': 'test-api-key'},
        json={
            'codigo_user': 101,
            'correo_institu': 'newuser@udistrital.edu.co',
            'primer_nomb': 'María',
            'id_cupon': 5001,
            'fecha_fin_cupon': '2026-07-02',
            'descripcion_prom': 'Bienvenida a C2C - Disfruta de tu descuento especial en tu primera compra.',
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body['success'] is True
    assert body['message'] == 'Cupón de bienvenida enviado.'
    assert body['correlation_id'] is None
    assert body['data']['email_sent_to'] == 'newuser@udistrital.edu.co'
    assert body['data']['id_cupon'] == 5001
    assert 'timestamp' in body['data']
