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