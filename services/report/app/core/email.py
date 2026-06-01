import logging
import smtplib
from email.mime.text import MIMEText

from app.core.config import settings

logger = logging.getLogger(__name__)


def send_report_confirmation_email(to_email: str, user_name: str, radicado: str) -> bool:
    """
    Send a confirmation email after a report is created.

    In development, docker-compose includes Mailpit. You can check sent emails at:
    http://localhost:8025
    """
    if not settings.MAIL_ENABLED:
        logger.info("Mail disabled. Confirmation for %s would be sent to %s", radicado, to_email)
        return False

    subject = "Confirmación de reporte - UD Marketplace"
    body = f"""
Hola {user_name},

Tu reporte fue recibido exitosamente en el sistema de UD Marketplace.

Radicado asignado: {radicado}
Estado inicial: RECIBIDO

Con este número podrás hacer seguimiento al estado de tu reporte.

Gracias por ayudarnos a mejorar la plataforma.

Atentamente,
Equipo UD Marketplace
""".strip()

    message = MIMEText(body, "plain", "utf-8")
    message["Subject"] = subject
    message["From"] = settings.SMTP_FROM
    message["To"] = to_email

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
        if settings.MAIL_USE_TLS:
            server.starttls()
        if settings.SMTP_USER and settings.SMTP_PASSWORD:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_FROM, [to_email], message.as_string())

    logger.info("Confirmation email sent for report %s to %s", radicado, to_email)
    return True
