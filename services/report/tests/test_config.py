from app.core.config import Settings


def test_cors_origins_accepts_comma_separated_format():
    settings = Settings(CORS_ORIGINS="http://localhost:4200,http://localhost:5173")

    assert settings.cors_origins == ["http://localhost:4200", "http://localhost:5173"]


def test_cors_origins_accepts_json_array_format():
    settings = Settings(CORS_ORIGINS='["http://localhost:4200","http://localhost:5173"]')

    assert settings.cors_origins == ["http://localhost:4200", "http://localhost:5173"]
