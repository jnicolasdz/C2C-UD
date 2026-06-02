from __future__ import annotations

import base64
from datetime import datetime, timezone
from email.mime.text import MIMEText
import ssl
from pathlib import Path
from smtplib import SMTP, SMTPAuthenticationError, SMTPException, SMTPRecipientsRefused

from jinja2 import Environment, FileSystemLoader, TemplateNotFound, select_autoescape

from app.core.config import SMTPSettings, build_smtp_config
from app.schemas.email_schema import RegisterConfirmationRequest

TEMPLATE_NAME = "auth/register_confirmation.html"
TEMPLATE_ROOT = Path(__file__).resolve().parents[1] / "templates"
template_environment = Environment(
    loader=FileSystemLoader(str(TEMPLATE_ROOT)),
    autoescape=select_autoescape(("html", "xml")),
)


class EmailServiceError(Exception):
    pass


class TemplateMissingError(EmailServiceError):
    pass


class InstitutionalDomainError(EmailServiceError):
    pass


class SMTPDeliveryError(EmailServiceError):
    pass


class SMTPAuthError(EmailServiceError):
    pass


def _build_display_name(payload: RegisterConfirmationRequest) -> str:
    name_parts = [payload.primer_nomb]
    if payload.segundo_nom:
        name_parts.append(payload.segundo_nom)
    if payload.primer_apel:
        name_parts.append(payload.primer_apel)
    return " ".join(name_parts)


def _validate_institutional_domain(payload: RegisterConfirmationRequest, settings: SMTPSettings) -> None:
    if not settings.allowed_institutional_domain:
        return

    email = payload.correo_institu.lower()
    allowed_domain = settings.allowed_institutional_domain.lower()
    if not allowed_domain.startswith("@"):
        allowed_domain = f"@{allowed_domain}"

    if not email.endswith(allowed_domain):
        raise InstitutionalDomainError(
            "El correo no pertenece al dominio institucional permitido."
        )


def _render_register_confirmation_html(payload: RegisterConfirmationRequest) -> str:
    try:
        template = template_environment.get_template(TEMPLATE_NAME)
    except TemplateNotFound as exc:
        raise TemplateMissingError("No se encontró el template de registro.") from exc

    return template.render(
        codigo_user=payload.codigo_user,
        correo_institu=payload.correo_institu,
        primer_nomb=payload.primer_nomb,
        segundo_nom=payload.segundo_nom,
        primer_apel=payload.primer_apel,
        display_name=_build_display_name(payload),
    )


def _authenticate_with_plain(smtp_client: SMTP, username: str, password: str) -> None:
    normalized_password = "".join(password.split())
    auth_payload = base64.b64encode(f"\0{username}\0{normalized_password}".encode("utf-8")).decode("ascii")
    code, _ = smtp_client.docmd("AUTH", f"PLAIN {auth_payload}")
    if code != 235:
        raise SMTPAuthenticationError(code, b"SMTP AUTH PLAIN failed")


def send_register_confirmation_email(
    payload: RegisterConfirmationRequest,
    settings: SMTPSettings | None = None,
) -> dict[str, str]:
    resolved_settings = settings or SMTPSettings()
    _validate_institutional_domain(payload, resolved_settings)

    html_body = _render_register_confirmation_html(payload)
    message = MIMEText(html_body, "html", "utf-8")
    message["Subject"] = "Confirmación de registro"
    message["From"] = resolved_settings.from_address
    message["To"] = str(payload.correo_institu)

    smtp_config = build_smtp_config(resolved_settings)

    try:
        if smtp_config["use_ssl"]:
            with SMTP(smtp_config["host"], smtp_config["port"], timeout=smtp_config["timeout"]) as smtp_client:
                smtp_client.ehlo()
                _authenticate_with_plain(
                    smtp_client,
                    smtp_config["username"],
                    smtp_config["password"],
                )
                smtp_client.send_message(message)
        else:
            with SMTP(smtp_config["host"], smtp_config["port"], timeout=smtp_config["timeout"]) as smtp_client:
                smtp_client.ehlo()
                if smtp_config["use_tls"]:
                    smtp_client.starttls(context=ssl.create_default_context())
                    smtp_client.ehlo()
                _authenticate_with_plain(
                    smtp_client,
                    smtp_config["username"],
                    smtp_config["password"],
                )
                smtp_client.send_message(message)
    except SMTPAuthenticationError as exc:
        raise SMTPAuthError("Error de autenticación SMTP.") from exc
    except (SMTPRecipientsRefused, SMTPException, OSError) as exc:
        raise SMTPDeliveryError("No fue posible entregar el correo.") from exc

    return {
        "email_sent_to": str(payload.correo_institu),
        "template_used": TEMPLATE_NAME,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }