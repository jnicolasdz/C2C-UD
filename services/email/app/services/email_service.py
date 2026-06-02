from __future__ import annotations

import base64
from datetime import datetime, timezone
from email.mime.text import MIMEText
import ssl
from pathlib import Path
from smtplib import SMTP, SMTPAuthenticationError, SMTPException, SMTPRecipientsRefused

from jinja2 import Environment, FileSystemLoader, TemplateNotFound, select_autoescape
from pydantic import BaseModel

from app.core.config import SMTPSettings, build_smtp_config
from app.schemas.email_schema import (
    BirthdayDiscountRequest,
    DiscountAvailableRequest,
    EmailVerificationRequest,
    GeneralPromotionRequest,
    OtpSendRequest,
    PasswordChangedRequest,
    RegisterConfirmationRequest,
    ReferralInvitationRequest,
    ReferralRewardRequest,
    WelcomeDiscountRequest,
)

TEMPLATE_NAME = "auth/register_confirmation.html"
EMAIL_VERIFICATION_TEMPLATE_NAME = "auth/email_verification.html"
OTP_TEMPLATE_NAME = "auth/otp_code.html"
PASSWORD_CHANGED_TEMPLATE_NAME = "auth/password_changed.html"
DISCOUNT_AVAILABLE_TEMPLATE_NAME = "promotions/discount_available.html"
BIRTHDAY_DISCOUNT_TEMPLATE_NAME = "promotions/birthday_discount.html"
GENERAL_PROMOTION_TEMPLATE_NAME = "promotions/general_promotion.html"
WELCOME_DISCOUNT_TEMPLATE_NAME = "promotions/welcome_discount.html"
REFERRAL_INVITATION_TEMPLATE_NAME = "referrals/referral_invitation.html"
REFERRAL_REWARD_TEMPLATE_NAME = "referrals/referral_reward.html"
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


def _build_verification_display_name(payload: EmailVerificationRequest) -> str:
    return payload.primer_nomb or "Usuario"


def _build_otp_display_name(payload: OtpSendRequest) -> str:
    return payload.primer_nomb or "Usuario"


def _build_password_changed_display_name(payload: PasswordChangedRequest) -> str:
    return payload.primer_nomb or "Usuario"


def _validate_institutional_domain(payload: BaseModel, settings: SMTPSettings) -> None:
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


def _render_email_verification_html(payload: EmailVerificationRequest) -> str:
    try:
        template = template_environment.get_template(EMAIL_VERIFICATION_TEMPLATE_NAME)
    except TemplateNotFound as exc:
        raise TemplateMissingError("No se encontró el template de verificación de correo.") from exc

    return template.render(
        codigo_user=payload.codigo_user,
        correo_institu=payload.correo_institu,
        verification_code=payload.verification_code,
        expiration_minutes=payload.expiration_minutes,
        display_name=_build_verification_display_name(payload),
    )


def _render_otp_html(payload: OtpSendRequest) -> str:
    try:
        template = template_environment.get_template(OTP_TEMPLATE_NAME)
    except TemplateNotFound as exc:
        raise TemplateMissingError("No se encontró el template de OTP.") from exc

    return template.render(
        codigo_user=payload.codigo_user,
        correo_institu=payload.correo_institu,
        otp_code=payload.otp_code,
        expiration_minutes=payload.expiration_minutes,
        display_name=_build_otp_display_name(payload),
        device_hint=payload.device_hint,
    )


def _render_password_changed_html(payload: PasswordChangedRequest) -> str:
    try:
        template = template_environment.get_template(PASSWORD_CHANGED_TEMPLATE_NAME)
    except TemplateNotFound as exc:
        raise TemplateMissingError("No se encontró el template de cambio de contraseña.") from exc

    return template.render(
        codigo_user=payload.codigo_user,
        correo_institu=payload.correo_institu,
        fecha_cambio=payload.fecha_cambio,
        display_name=_build_password_changed_display_name(payload),
        ip_origen=payload.ip_origen,
    )


def _render_discount_available_html(payload: DiscountAvailableRequest) -> str:
    try:
        template = template_environment.get_template(DISCOUNT_AVAILABLE_TEMPLATE_NAME)
    except TemplateNotFound as exc:
        raise TemplateMissingError("No se encontró el template de descuento disponible.") from exc

    return template.render(
        codigo_user=payload.codigo_user,
        correo_institu=payload.correo_institu,
        id_cupon=payload.id_cupon,
        id_pub=payload.id_pub,
        nombre_pub=payload.nombre_pub,
        precio_original=payload.precio_original,
        descripcion_prom=payload.descripcion_prom,
        fecha_inicio=payload.fecha_inicio,
        fecha_fin=payload.fecha_fin,
        precio_con_descuento=payload.precio_con_descuento,
        porcentaje_descuento=payload.porcentaje_descuento,
        primer_nomb=payload.primer_nomb,
    )


def _render_birthday_discount_html(payload: BirthdayDiscountRequest) -> str:
    try:
        template = template_environment.get_template(BIRTHDAY_DISCOUNT_TEMPLATE_NAME)
    except TemplateNotFound as exc:
        raise TemplateMissingError("No se encontró el template de descuento de cumpleaños.") from exc

    return template.render(
        codigo_user=payload.codigo_user,
        correo_institu=payload.correo_institu,
        primer_nomb=payload.primer_nomb,
        segundo_nom=payload.segundo_nom,
        id_cupon=payload.id_cupon,
        fecha_fin_cupon=payload.fecha_fin_cupon,
        descripcion_prom=payload.descripcion_prom,
    )


def _render_welcome_discount_html(payload: WelcomeDiscountRequest) -> str:
    try:
        template = template_environment.get_template(WELCOME_DISCOUNT_TEMPLATE_NAME)
    except TemplateNotFound as exc:
        raise TemplateMissingError("No se encontró el template de cupón de bienvenida.") from exc

    return template.render(
        codigo_user=payload.codigo_user,
        correo_institu=payload.correo_institu,
        primer_nomb=payload.primer_nomb,
        id_cupon=payload.id_cupon,
        fecha_fin_cupon=payload.fecha_fin_cupon,
        descripcion_prom=payload.descripcion_prom,
    )


def _render_referral_invitation_html(payload: ReferralInvitationRequest) -> str:
    try:
        template = template_environment.get_template(REFERRAL_INVITATION_TEMPLATE_NAME)
    except TemplateNotFound as exc:
        raise TemplateMissingError("No se encontró el template de invitación de referido.") from exc

    return template.render(
        referrer_codigo_user=payload.referrer_codigo_user,
        referrer_nombre=payload.referrer_nombre,
        invitee_correo=payload.invitee_correo,
        referral_code=payload.referral_code,
        referral_link=payload.referral_link,
        mensaje_personalizado=payload.mensaje_personalizado,
    )


def _render_referral_reward_html(payload: ReferralRewardRequest) -> str:
    try:
        template = template_environment.get_template(REFERRAL_REWARD_TEMPLATE_NAME)
    except TemplateNotFound as exc:
        raise TemplateMissingError("No se encontró el template de recompensa por referido.") from exc

    return template.render(
        codigo_user=payload.codigo_user,
        correo_institu=payload.correo_institu,
        primer_nomb=payload.primer_nomb,
        referred_user_nombre=payload.referred_user_nombre,
        recompensa_descripcion=payload.recompensa_descripcion,
        id_cupon_recompensa=payload.id_cupon_recompensa,
    )


def _render_general_promotion_html(payload: GeneralPromotionRequest, recipient: object) -> str:
    try:
        template = template_environment.get_template(GENERAL_PROMOTION_TEMPLATE_NAME)
    except TemplateNotFound as exc:
        raise TemplateMissingError("No se encontró el template de promoción general.") from exc

    return template.render(
        codigo_user=recipient.codigo_user,
        correo_institu=recipient.correo_institu,
        primer_nomb=recipient.primer_nomb,
        id_prom=payload.id_prom,
        tipo_prom=payload.tipo_prom,
        descripcion_prom=payload.descripcion_prom,
        fecha_fin_prom=payload.fecha_fin_prom,
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


def send_email_verification_email(
    payload: EmailVerificationRequest,
    settings: SMTPSettings | None = None,
) -> dict[str, str | int]:
    resolved_settings = settings or SMTPSettings()
    _validate_institutional_domain(payload, resolved_settings)

    html_body = _render_email_verification_html(payload)
    message = MIMEText(html_body, "html", "utf-8")
    message["Subject"] = "Código de verificación"
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
        "code_expires_in_minutes": payload.expiration_minutes,
        "template_used": EMAIL_VERIFICATION_TEMPLATE_NAME,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def send_otp_email(
    payload: OtpSendRequest,
    settings: SMTPSettings | None = None,
) -> dict[str, str | int]:
    resolved_settings = settings or SMTPSettings()
    _validate_institutional_domain(payload, resolved_settings)

    html_body = _render_otp_html(payload)
    message = MIMEText(html_body, "html", "utf-8")
    message["Subject"] = "Código OTP de verificación"
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
        "otp_expires_in_minutes": payload.expiration_minutes,
        "template_used": OTP_TEMPLATE_NAME,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def send_password_changed_email(
    payload: PasswordChangedRequest,
    settings: SMTPSettings | None = None,
) -> dict[str, str]:
    resolved_settings = settings or SMTPSettings()
    _validate_institutional_domain(payload, resolved_settings)

    html_body = _render_password_changed_html(payload)
    message = MIMEText(html_body, "html", "utf-8")
    message["Subject"] = "Alerta de cambio de contraseña"
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
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

def send_discount_available_email(
    payload: DiscountAvailableRequest,
    settings: SMTPSettings | None = None,
) -> dict[str, str | int]:
    resolved_settings = settings or SMTPSettings()
    _validate_institutional_domain(payload, resolved_settings)

    html_body = _render_discount_available_html(payload)
    message = MIMEText(html_body, 'html', 'utf-8')
    message['Subject'] = 'Descuento disponible para ti'
    message['From'] = resolved_settings.from_address
    message['To'] = str(payload.correo_institu)

    smtp_config = build_smtp_config(resolved_settings)

    try:
        if smtp_config['use_ssl']:
            with SMTP(smtp_config['host'], smtp_config['port'], timeout=smtp_config['timeout']) as smtp_client:
                smtp_client.ehlo()
                _authenticate_with_plain(
                    smtp_client,
                    smtp_config['username'],
                    smtp_config['password'],
                )
                smtp_client.send_message(message)
        else:
            with SMTP(smtp_config['host'], smtp_config['port'], timeout=smtp_config['timeout']) as smtp_client:
                smtp_client.ehlo()
                if smtp_config['use_tls']:
                    smtp_client.starttls(context=ssl.create_default_context())
                    smtp_client.ehlo()
                _authenticate_with_plain(
                    smtp_client,
                    smtp_config['username'],
                    smtp_config['password'],
                )
                smtp_client.send_message(message)
    except SMTPAuthenticationError as exc:
        raise SMTPAuthError('Error de autenticación SMTP.') from exc
    except (SMTPRecipientsRefused, SMTPException, OSError) as exc:
        raise SMTPDeliveryError('No fue posible entregar el correo.') from exc

    return {
        'email_sent_to': str(payload.correo_institu),
        'id_cupon': payload.id_cupon,
        'timestamp': datetime.now(timezone.utc).isoformat(),
    }


def send_birthday_discount_email(
    payload: BirthdayDiscountRequest,
    settings: SMTPSettings | None = None,
) -> dict[str, str | int]:
    resolved_settings = settings or SMTPSettings()
    _validate_institutional_domain(payload, resolved_settings)

    html_body = _render_birthday_discount_html(payload)
    message = MIMEText(html_body, 'html', 'utf-8')
    message['Subject'] = 'Descuento de cumpleaños'
    message['From'] = resolved_settings.from_address
    message['To'] = str(payload.correo_institu)

    smtp_config = build_smtp_config(resolved_settings)

    try:
        if smtp_config['use_ssl']:
            with SMTP(smtp_config['host'], smtp_config['port'], timeout=smtp_config['timeout']) as smtp_client:
                smtp_client.ehlo()
                _authenticate_with_plain(
                    smtp_client,
                    smtp_config['username'],
                    smtp_config['password'],
                )
                smtp_client.send_message(message)
        else:
            with SMTP(smtp_config['host'], smtp_config['port'], timeout=smtp_config['timeout']) as smtp_client:
                smtp_client.ehlo()
                if smtp_config['use_tls']:
                    smtp_client.starttls(context=ssl.create_default_context())
                    smtp_client.ehlo()
                _authenticate_with_plain(
                    smtp_client,
                    smtp_config['username'],
                    smtp_config['password'],
                )
                smtp_client.send_message(message)
    except SMTPAuthenticationError as exc:
        raise SMTPAuthError('Error de autenticación SMTP.') from exc
    except (SMTPRecipientsRefused, SMTPException, OSError) as exc:
        raise SMTPDeliveryError('No fue posible entregar el correo.') from exc

    return {
        'email_sent_to': str(payload.correo_institu),
        'id_cupon': payload.id_cupon,
        'timestamp': datetime.now(timezone.utc).isoformat(),
    }


def send_welcome_discount_email(
    payload: WelcomeDiscountRequest,
    settings: SMTPSettings | None = None,
) -> dict[str, str | int]:
    resolved_settings = settings or SMTPSettings()
    _validate_institutional_domain(payload, resolved_settings)

    html_body = _render_welcome_discount_html(payload)
    message = MIMEText(html_body, 'html', 'utf-8')
    message['Subject'] = 'Bienvenida a C2C - Cupón especial'
    message['From'] = resolved_settings.from_address
    message['To'] = str(payload.correo_institu)

    smtp_config = build_smtp_config(resolved_settings)

    try:
        if smtp_config['use_ssl']:
            with SMTP(smtp_config['host'], smtp_config['port'], timeout=smtp_config['timeout']) as smtp_client:
                smtp_client.ehlo()
                _authenticate_with_plain(
                    smtp_client,
                    smtp_config['username'],
                    smtp_config['password'],
                )
                smtp_client.send_message(message)
        else:
            with SMTP(smtp_config['host'], smtp_config['port'], timeout=smtp_config['timeout']) as smtp_client:
                smtp_client.ehlo()
                if smtp_config['use_tls']:
                    smtp_client.starttls(context=ssl.create_default_context())
                    smtp_client.ehlo()
                _authenticate_with_plain(
                    smtp_client,
                    smtp_config['username'],
                    smtp_config['password'],
                )
                smtp_client.send_message(message)
    except SMTPAuthenticationError as exc:
        raise SMTPAuthError('Error de autenticación SMTP.') from exc
    except (SMTPRecipientsRefused, SMTPException, OSError) as exc:
        raise SMTPDeliveryError('No fue posible entregar el correo.') from exc

    return {
        'email_sent_to': str(payload.correo_institu),
        'id_cupon': payload.id_cupon,
        'timestamp': datetime.now(timezone.utc).isoformat(),
    }


def send_referral_invitation_email(
    payload: ReferralInvitationRequest,
    settings: SMTPSettings | None = None,
) -> dict[str, str]:
    resolved_settings = settings or SMTPSettings()
    
    # Validate institutional domain for invitee
    class InviteePayload:
        def __init__(self, correo_institu):
            self.correo_institu = correo_institu
    
    _validate_institutional_domain(InviteePayload(payload.invitee_correo), resolved_settings)

    html_body = _render_referral_invitation_html(payload)
    message = MIMEText(html_body, 'html', 'utf-8')
    message['Subject'] = f'{payload.referrer_nombre} te invita a unirte a C2C'
    message['From'] = resolved_settings.from_address
    message['To'] = str(payload.invitee_correo)

    smtp_config = build_smtp_config(resolved_settings)

    try:
        if smtp_config['use_ssl']:
            with SMTP(smtp_config['host'], smtp_config['port'], timeout=smtp_config['timeout']) as smtp_client:
                smtp_client.ehlo()
                _authenticate_with_plain(
                    smtp_client,
                    smtp_config['username'],
                    smtp_config['password'],
                )
                smtp_client.send_message(message)
        else:
            with SMTP(smtp_config['host'], smtp_config['port'], timeout=smtp_config['timeout']) as smtp_client:
                smtp_client.ehlo()
                if smtp_config['use_tls']:
                    smtp_client.starttls(context=ssl.create_default_context())
                    smtp_client.ehlo()
                _authenticate_with_plain(
                    smtp_client,
                    smtp_config['username'],
                    smtp_config['password'],
                )
                smtp_client.send_message(message)
    except SMTPAuthenticationError as exc:
        raise SMTPAuthError('Error de autenticación SMTP.') from exc
    except (SMTPRecipientsRefused, SMTPException, OSError) as exc:
        raise SMTPDeliveryError('No fue posible entregar el correo.') from exc

    return {
        'email_sent_to': str(payload.invitee_correo),
        'referral_code': payload.referral_code,
        'timestamp': datetime.now(timezone.utc).isoformat(),
    }


def send_referral_reward_email(
    payload: 'ReferralRewardRequest',
    settings: SMTPSettings | None = None,
) -> dict[str, str | int]:
    resolved_settings = settings or SMTPSettings()
    _validate_institutional_domain(payload, resolved_settings)

    html_body = _render_referral_reward_html(payload)
    message = MIMEText(html_body, 'html', 'utf-8')
    message['Subject'] = 'Has recibido tu recompensa por referido'
    message['From'] = resolved_settings.from_address
    message['To'] = str(payload.correo_institu)

    smtp_config = build_smtp_config(resolved_settings)

    try:
        if smtp_config['use_ssl']:
            with SMTP(smtp_config['host'], smtp_config['port'], timeout=smtp_config['timeout']) as smtp_client:
                smtp_client.ehlo()
                _authenticate_with_plain(
                    smtp_client,
                    smtp_config['username'],
                    smtp_config['password'],
                )
                smtp_client.send_message(message)
        else:
            with SMTP(smtp_config['host'], smtp_config['port'], timeout=smtp_config['timeout']) as smtp_client:
                smtp_client.ehlo()
                if smtp_config['use_tls']:
                    smtp_client.starttls(context=ssl.create_default_context())
                    smtp_client.ehlo()
                _authenticate_with_plain(
                    smtp_client,
                    smtp_config['username'],
                    smtp_config['password'],
                )
                smtp_client.send_message(message)
    except SMTPAuthenticationError as exc:
        raise SMTPAuthError('Error de autenticación SMTP.') from exc
    except (SMTPRecipientsRefused, SMTPException, OSError) as exc:
        raise SMTPDeliveryError('No fue posible entregar el correo.') from exc

    result = {
        'email_sent_to': str(payload.correo_institu),
        'timestamp': datetime.now(timezone.utc).isoformat(),
    }
    if payload.id_cupon_recompensa is not None:
        result['id_cupon_recompensa'] = payload.id_cupon_recompensa
    return result


def send_general_promotion_email(
    payload: GeneralPromotionRequest,
    settings: SMTPSettings | None = None,
) -> dict[str, int | str]:
    resolved_settings = settings or SMTPSettings()
    smtp_config = build_smtp_config(resolved_settings)
    total_recipients = len(payload.recipients)
    sent_successfully = 0
    failed = 0

    try:
        if smtp_config['use_ssl']:
            smtp_client_context = SMTP(smtp_config['host'], smtp_config['port'], timeout=smtp_config['timeout'])
        else:
            smtp_client_context = SMTP(smtp_config['host'], smtp_config['port'], timeout=smtp_config['timeout'])

        with smtp_client_context as smtp_client:
            smtp_client.ehlo()
            if not smtp_config['use_ssl'] and smtp_config['use_tls']:
                smtp_client.starttls(context=ssl.create_default_context())
                smtp_client.ehlo()

            _authenticate_with_plain(
                smtp_client,
                smtp_config['username'],
                smtp_config['password'],
            )

            for recipient in payload.recipients:
                try:
                    _validate_institutional_domain(recipient, resolved_settings)
                    html_body = _render_general_promotion_html(payload, recipient)
                    message = MIMEText(html_body, 'html', 'utf-8')
                    message['Subject'] = f"Promoción especial: {payload.tipo_prom}"
                    message['From'] = resolved_settings.from_address
                    message['To'] = str(recipient.correo_institu)
                    smtp_client.send_message(message)
                    sent_successfully += 1
                except InstitutionalDomainError:
                    failed += 1
                except SMTPRecipientsRefused:
                    failed += 1

    except SMTPAuthenticationError as exc:
        raise SMTPAuthError('Error de autenticación SMTP.') from exc
    except (SMTPException, OSError) as exc:
        raise SMTPDeliveryError('No fue posible entregar el correo.') from exc

    return {
        'total_recipients': total_recipients,
        'sent_successfully': sent_successfully,
        'failed': failed,
        'timestamp': datetime.now(timezone.utc).isoformat(),
    }
