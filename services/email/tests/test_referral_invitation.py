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


def test_send_referral_invitation_email_success(monkeypatch):
    monkeypatch.setenv('SMTP_USERNAME', 'test_user')
    monkeypatch.setenv('SMTP_PASSWORD', 'test_password')
    monkeypatch.setenv('SMTP_FROM', 'no-reply@example.com')
    monkeypatch.setenv('EMAIL_SERVICE_API_KEY', 'test-api-key')

    monkeypatch.setattr('app.services.email_service.SMTP', FakeSMTP)

    client = TestClient(app)
    response = client.post(
        '/api/v1/emails/referrals/invitation',
        headers={'X-API-Key': 'test-api-key'},
        json={
            'referrer_codigo_user': 50,
            'referrer_nombre': 'Carlos',
            'invitee_correo': 'newuser@udistrital.edu.co',
            'referral_code': 'REF_C2C_ABC123_XYZ',
            'referral_link': 'https://c2c.udistrital.edu.co/register?ref=REF_C2C_ABC123_XYZ',
            'mensaje_personalizado': 'Te va a encantar esta plataforma, es muy práctica.',
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body['success'] is True
    assert body['message'] == 'Invitación de referido enviada.'
    assert body['correlation_id'] is None
    assert body['data']['email_sent_to'] == 'newuser@udistrital.edu.co'
    assert body['data']['referral_code'] == 'REF_C2C_ABC123_XYZ'
    assert 'timestamp' in body['data']
