from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class SMTPSettings(BaseSettings):
	model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

	smtp_username: str = ""
	smtp_password: str = ""
	smtp_from: str | None = None
	email_service_api_key: str = ""
	allowed_institutional_domain: str | None = None
	smtp_host: str = "smtp.gmail.com"
	smtp_port: int = 587
	smtp_use_tls: bool = True
	smtp_use_ssl: bool = False
	smtp_timeout: int = 30

	@property
	def from_address(self) -> str:
		return self.smtp_from or self.smtp_username


def get_smtp_settings() -> SMTPSettings:
	return SMTPSettings()


def build_smtp_config(settings: SMTPSettings | None = None) -> dict[str, object]:
	resolved_settings = settings or get_smtp_settings()

	return {
		"username": resolved_settings.smtp_username,
		"password": resolved_settings.smtp_password,
		"from_address": resolved_settings.from_address,
		"host": resolved_settings.smtp_host,
		"port": resolved_settings.smtp_port,
		"use_tls": resolved_settings.smtp_use_tls,
		"use_ssl": resolved_settings.smtp_use_ssl,
		"timeout": resolved_settings.smtp_timeout,
	}

