from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterConfirmationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    codigo_user: int = Field(ge=1)
    correo_institu: Annotated[EmailStr, Field(max_length=150)]
    primer_nomb: Annotated[str, Field(min_length=1, max_length=100)]
    segundo_nom: Annotated[str | None, Field(max_length=100)] = None
    primer_apel: Annotated[str | None, Field(max_length=100)] = None


class EmailVerificationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    codigo_user: int = Field(ge=1)
    correo_institu: Annotated[EmailStr, Field(max_length=150)]
    verification_code: Annotated[str, Field(min_length=6, max_length=8, pattern="^[A-Z0-9]+$")]
    expiration_minutes: int = Field(ge=5, le=60)
    primer_nomb: Annotated[str | None, Field(max_length=100)] = None


class OtpSendRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    codigo_user: int = Field(ge=1)
    correo_institu: Annotated[EmailStr, Field(max_length=150)]
    otp_code: Annotated[str, Field(min_length=6, max_length=6, pattern="^[0-9]{6}$")]
    expiration_minutes: int = Field(ge=1, le=10)
    primer_nomb: Annotated[str | None, Field(max_length=100)] = None
    device_hint: Annotated[str | None, Field(max_length=100)] = None


class PasswordChangedRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    codigo_user: int = Field(ge=1)
    correo_institu: Annotated[EmailStr, Field(max_length=150)]
    fecha_cambio: Annotated[str, Field(pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")]
    primer_nomb: Annotated[str | None, Field(max_length=100)] = None
    ip_origen: Annotated[str | None, Field(max_length=45)] = None


class DiscountAvailableRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    codigo_user: int = Field(ge=1)
    correo_institu: Annotated[EmailStr, Field(max_length=150)]
    id_cupon: int = Field(ge=1)
    id_pub: int = Field(ge=1)
    nombre_pub: Annotated[str, Field(min_length=1, max_length=200)]
    precio_original: float = Field(gt=0)
    descripcion_prom: Annotated[str, Field(min_length=1, max_length=500)]
    fecha_inicio: Annotated[str, Field(pattern=r"^\d{4}-\d{2}-\d{2}$")]
    fecha_fin: Annotated[str, Field(pattern=r"^\d{4}-\d{2}-\d{2}$")]
    primer_nomb: Annotated[str | None, Field(max_length=100)] = None
    precio_con_descuento: Annotated[float | None, Field(gt=0)] = None
    porcentaje_descuento: Annotated[float | None, Field(ge=0, le=100)] = None


class BirthdayDiscountRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    codigo_user: int = Field(ge=1)
    correo_institu: Annotated[EmailStr, Field(max_length=150)]
    primer_nomb: Annotated[str, Field(min_length=1, max_length=100)]
    id_cupon: int = Field(ge=1)
    fecha_fin_cupon: Annotated[str, Field(pattern=r"^\d{4}-\d{2}-\d{2}$")]
    segundo_nom: Annotated[str | None, Field(max_length=100)] = None
    descripcion_prom: Annotated[str | None, Field(max_length=500)] = None


class GeneralPromotionRecipient(BaseModel):
    codigo_user: int = Field(ge=1)
    correo_institu: Annotated[EmailStr, Field(max_length=150)]
    primer_nomb: Annotated[str, Field(min_length=1, max_length=100)]


class GeneralPromotionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    recipients: list[GeneralPromotionRecipient] = Field(min_length=1, max_length=500)
    id_prom: int = Field(ge=1)
    tipo_prom: Annotated[str, Field(min_length=1, max_length=100)]
    descripcion_prom: Annotated[str, Field(min_length=1, max_length=500)]
    fecha_fin_prom: Annotated[str | None, Field(pattern=r"^\d{4}-\d{2}-\d{2}$")] = None


class WelcomeDiscountRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    codigo_user: int = Field(ge=1)
    correo_institu: Annotated[EmailStr, Field(max_length=150)]
    primer_nomb: Annotated[str, Field(min_length=1, max_length=100)]
    id_cupon: int = Field(ge=1)
    fecha_fin_cupon: Annotated[str, Field(pattern=r"^\d{4}-\d{2}-\d{2}$")]
    descripcion_prom: Annotated[str | None, Field(max_length=500)] = None


class ReferralInvitationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    referrer_codigo_user: int = Field(ge=1)
    referrer_nombre: Annotated[str, Field(min_length=1, max_length=100)]
    invitee_correo: Annotated[EmailStr, Field(max_length=150)]
    referral_code: Annotated[str, Field(min_length=1, max_length=50, pattern="^[A-Z0-9_-]+$")]
    referral_link: Annotated[str, Field(min_length=1, max_length=500)]
    mensaje_personalizado: Annotated[str | None, Field(max_length=300)] = None