from app.core.config import SMTPSettings, build_smtp_config


def test_build_smtp_config_uses_gmail_defaults(monkeypatch) -> None:
    monkeypatch.setenv("SMTP_USERNAME", "sender@gmail.com")
    monkeypatch.setenv("SMTP_PASSWORD", "app-password")
    monkeypatch.setenv("SMTP_FROM", "sender@gmail.com")
    monkeypatch.setenv("EMAIL_SERVICE_API_KEY", "sk_internal_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6")

    settings = SMTPSettings()
    config = build_smtp_config(settings)

    assert settings.smtp_host == "smtp.gmail.com"
    assert settings.smtp_port == 587
    assert settings.from_address == "sender@gmail.com"
    assert config == {
        "username": "sender@gmail.com",
        "password": "app-password",
        "from_address": "sender@gmail.com",
        "host": "smtp.gmail.com",
        "port": 587,
        "use_tls": True,
        "use_ssl": False,
        "timeout": 30,
    }