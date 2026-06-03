import smtplib
from email.mime.text import MIMEText
from typing import Optional

from app.core.config import settings


class EmailDeliveryError(Exception):
    """Error controlado para reportar fallos de correo al servicio de reportes."""


def _send_email(to_email: str, subject: str, body: str) -> None:
    if not settings.MAIL_ENABLED:
        return

    message = MIMEText(body, "plain", "utf-8")
    message["Subject"] = subject
    message["From"] = settings.SMTP_FROM
    message["To"] = to_email

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
            if settings.MAIL_USE_TLS:
                server.starttls()
            if settings.SMTP_USER and settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_FROM, [to_email], message.as_string())
    except Exception as exc:
        raise EmailDeliveryError(str(exc)) from exc


def send_report_confirmation_email(to_email: str, user_name: str, radicado: str, status: str) -> None:
    subject = "Confirmación de reporte - UD Marketplace"
    body = f"""
Hola {user_name},

Tu reporte fue recibido por el sistema de UD Marketplace.

Radicado asignado: {radicado}
Estado inicial del reporte: {status}

Con este número podrás consultar el seguimiento del reporte.

Atentamente,
Equipo UD Marketplace
""".strip()
    _send_email(to_email=to_email, subject=subject, body=body)


def send_admin_report_email(
    admin_email: str,
    radicado: str,
    user_name: str,
    user_email: str,
    report_type: str,
    subject_value: str,
    description: str,
    user_id: Optional[str] = None,
) -> None:
    subject = f"Nuevo reporte recibido - {radicado}"
    body = f"""
Se registró un nuevo reporte en UD Marketplace.

Radicado: {radicado}
Usuario emisor: {user_name}
ID usuario: {user_id or 'No suministrado'}
Correo usuario: {user_email}
Tipo de reporte: {report_type}
Asunto: {subject_value}

Descripción:
{description}

Este mensaje fue generado automáticamente por el servicio de reportes.
""".strip()
    _send_email(to_email=admin_email, subject=subject, body=body)



def send_report_status_update_email(
    to_email: str,
    user_name: str,
    radicado: str,
    previous_status: str,
    new_status: str,
    delivery_message: Optional[str] = None,
) -> None:
    subject = f"Actualización de estado del reporte {radicado}"
    body = f"""
Hola {user_name},

Tu reporte con radicado {radicado} tuvo una actualización de estado.

Estado anterior: {previous_status}
Nuevo estado: {new_status}

{delivery_message or 'Puedes consultar el seguimiento del reporte con tu radicado.'}

Atentamente,
Equipo UD Marketplace
""".strip()
    _send_email(to_email=to_email, subject=subject, body=body)
