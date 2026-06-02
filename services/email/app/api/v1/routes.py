from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException, status

from app.core.config import SMTPSettings, get_smtp_settings
from app.schemas.email_schema import (
    BirthdayDiscountRequest,
    DiscountAvailableRequest,
    EmailVerificationRequest,
    GeneralPromotionRequest,
    OtpSendRequest,
    PasswordChangedRequest,
    RegisterConfirmationRequest,
)
from app.services.email_service import (
    InstitutionalDomainError,
    SMTPAuthError,
    SMTPDeliveryError,
    TemplateMissingError,
    send_birthday_discount_email,
    send_discount_available_email,
    send_email_verification_email,
    send_general_promotion_email,
    send_otp_email,
    send_password_changed_email,
    send_register_confirmation_email,
)

router = APIRouter()


def _error_response(
    error_code: str,
    message: str,
    correlation_id: str | None = None,
    details: list[dict[str, object]] | None = None,
) -> dict[str, object | None]:
    return {
        "success": False,
        "error_code": error_code,
        "message": message,
        "details": details,
        "correlation_id": correlation_id,
    }


def _verify_api_key(
    x_api_key: str = Header(..., alias="X-API-Key"),
    settings: SMTPSettings = Depends(get_smtp_settings),
) -> SMTPSettings:
    if not settings.email_service_api_key or x_api_key != settings.email_service_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=_error_response("AUTH_001", "API Key ausente o inválida."),
        )

    return settings


@router.get("/health")
def health() -> dict[str, object]:
    settings = SMTPSettings()
    return {
        "success": True,
        "message": "Email service is running",
        "correlation_id": None,
        "data": {
            "service": "C2C-UD Email Microservice",
            "smtp_host": settings.smtp_host,
            "smtp_port": settings.smtp_port,
            "smtp_configured": bool(settings.smtp_username and settings.smtp_password),
        },
    }


@router.get("/emails/health")
def service_health() -> dict[str, object]:
    return health()


@router.get("/email")
def legacy_health() -> dict[str, object]:
    return health()


@router.post("/emails/auth/register-confirmation", status_code=status.HTTP_200_OK)
def register_confirmation(
    payload: RegisterConfirmationRequest,
    settings: SMTPSettings = Depends(_verify_api_key),
    x_correlation_id: str | None = Header(default=None, alias="X-Correlation-ID"),
) -> dict[str, object | None]:
    try:
        data = send_register_confirmation_email(payload, settings=settings)
    except InstitutionalDomainError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_error_response("VAL_003", str(exc), correlation_id=x_correlation_id),
        ) from exc
    except TemplateMissingError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=_error_response("TPL_001", str(exc), correlation_id=x_correlation_id),
        ) from exc
    except SMTPAuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=_error_response("SMTP_002", str(exc), correlation_id=x_correlation_id),
        ) from exc
    except SMTPDeliveryError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=_error_response("SMTP_001", str(exc), correlation_id=x_correlation_id),
        ) from exc

    return {
        "success": True,
        "message": "Correo de confirmación enviado exitosamente.",
        "correlation_id": x_correlation_id,
        "data": data,
    }


@router.post("/emails/auth/email-verification", status_code=status.HTTP_200_OK)
def email_verification(
    payload: EmailVerificationRequest,
    settings: SMTPSettings = Depends(_verify_api_key),
    x_correlation_id: str | None = Header(default=None, alias="X-Correlation-ID"),
) -> dict[str, object | None]:
    try:
        data = send_email_verification_email(payload, settings=settings)
    except InstitutionalDomainError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_error_response("VAL_003", str(exc), correlation_id=x_correlation_id),
        ) from exc
    except TemplateMissingError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=_error_response("TPL_001", str(exc), correlation_id=x_correlation_id),
        ) from exc
    except SMTPAuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=_error_response("SMTP_002", str(exc), correlation_id=x_correlation_id),
        ) from exc
    except SMTPDeliveryError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=_error_response("SMTP_001", str(exc), correlation_id=x_correlation_id),
        ) from exc

    return {
        "success": True,
        "message": "Correo de verificación enviado exitosamente.",
        "correlation_id": x_correlation_id,
        "data": data,
    }


@router.post("/emails/auth/send-otp", status_code=status.HTTP_200_OK)
def send_otp(
    payload: OtpSendRequest,
    settings: SMTPSettings = Depends(_verify_api_key),
    x_correlation_id: str | None = Header(default=None, alias="X-Correlation-ID"),
) -> dict[str, object | None]:
    try:
        data = send_otp_email(payload, settings=settings)
    except InstitutionalDomainError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_error_response("VAL_003", str(exc), correlation_id=x_correlation_id),
        ) from exc
    except TemplateMissingError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=_error_response("TPL_001", str(exc), correlation_id=x_correlation_id),
        ) from exc
    except SMTPAuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=_error_response("SMTP_002", str(exc), correlation_id=x_correlation_id),
        ) from exc
    except SMTPDeliveryError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=_error_response("SMTP_001", str(exc), correlation_id=x_correlation_id),
        ) from exc

    return {
        "success": True,
        "message": "OTP enviado exitosamente.",
        "correlation_id": x_correlation_id,
        "data": data,
    }


@router.post("/emails/auth/password-changed", status_code=status.HTTP_200_OK)
def password_changed(
    payload: PasswordChangedRequest,
    settings: SMTPSettings = Depends(_verify_api_key),
    x_correlation_id: str | None = Header(default=None, alias="X-Correlation-ID"),
) -> dict[str, object | None]:
    try:
        data = send_password_changed_email(payload, settings=settings)
    except InstitutionalDomainError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_error_response("VAL_003", str(exc), correlation_id=x_correlation_id),
        ) from exc
    except TemplateMissingError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=_error_response("TPL_001", str(exc), correlation_id=x_correlation_id),
        ) from exc
    except SMTPAuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=_error_response("SMTP_002", str(exc), correlation_id=x_correlation_id),
        ) from exc
    except SMTPDeliveryError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=_error_response("SMTP_001", str(exc), correlation_id=x_correlation_id),
        ) from exc

    return {
        "success": True,
        "message": "Correo de alerta enviado exitosamente.",
        "correlation_id": x_correlation_id,
        "data": data,
    }


@router.post("/emails/promotions/discount-available", status_code=status.HTTP_200_OK)
def discount_available(
    payload: DiscountAvailableRequest,
    settings: SMTPSettings = Depends(_verify_api_key),
    x_correlation_id: str | None = Header(default=None, alias="X-Correlation-ID"),
) -> dict[str, object | None]:
    try:
        data = send_discount_available_email(payload, settings=settings)
    except InstitutionalDomainError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_error_response("VAL_003", str(exc), correlation_id=x_correlation_id),
        ) from exc
    except TemplateMissingError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=_error_response("TPL_001", str(exc), correlation_id=x_correlation_id),
        ) from exc
    except SMTPAuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=_error_response("SMTP_002", str(exc), correlation_id=x_correlation_id),
        ) from exc
    except SMTPDeliveryError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=_error_response("SMTP_001", str(exc), correlation_id=x_correlation_id),
        ) from exc

    return {
        "success": True,
        "message": "Correo de descuento enviado.",
        "correlation_id": x_correlation_id,
        "data": data,
    }


@router.post("/emails/promotions/birthday", status_code=status.HTTP_200_OK)
def birthday_discount(
    payload: BirthdayDiscountRequest,
    settings: SMTPSettings = Depends(_verify_api_key),
    x_correlation_id: str | None = Header(default=None, alias="X-Correlation-ID"),
) -> dict[str, object | None]:
    try:
        data = send_birthday_discount_email(payload, settings=settings)
    except InstitutionalDomainError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_error_response("VAL_003", str(exc), correlation_id=x_correlation_id),
        ) from exc
    except TemplateMissingError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=_error_response("TPL_001", str(exc), correlation_id=x_correlation_id),
        ) from exc
    except SMTPAuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=_error_response("SMTP_002", str(exc), correlation_id=x_correlation_id),
        ) from exc
    except SMTPDeliveryError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=_error_response("SMTP_001", str(exc), correlation_id=x_correlation_id),
        ) from exc

    return {
        "success": True,
        "message": "Correo de cumpleaños enviado.",
        "correlation_id": x_correlation_id,
        "data": data,
    }


@router.post("/emails/promotions/general", status_code=status.HTTP_200_OK)
def general_promotion(
    payload: GeneralPromotionRequest,
    settings: SMTPSettings = Depends(_verify_api_key),
    x_correlation_id: str | None = Header(default=None, alias="X-Correlation-ID"),
) -> dict[str, object | None]:
    try:
        data = send_general_promotion_email(payload, settings=settings)
    except TemplateMissingError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=_error_response("TPL_001", str(exc), correlation_id=x_correlation_id),
        ) from exc
    except SMTPAuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=_error_response("SMTP_002", str(exc), correlation_id=x_correlation_id),
        ) from exc
    except SMTPDeliveryError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=_error_response("SMTP_001", str(exc), correlation_id=x_correlation_id),
        ) from exc

    return {
        "success": True,
        "message": "Campaña procesada.",
        "correlation_id": x_correlation_id,
        "data": data,
    }
