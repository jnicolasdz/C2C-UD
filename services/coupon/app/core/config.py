from fastapi_mail import ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="tu_correo_marketplace@gmail.com",
    MAIL_PASSWORD="tu_contraseña_secreta",
    MAIL_FROM="no-reply@marketplace.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

# Base de datos simulada en memoria
BD_CUPONES = {
    "BIENVENIDA2026": {"tipo": "porcentaje", "valor": 15.0, "fecha_expiracion": "2026-12-31T23:59:59", "es_activo": True},
    "CUMPLE_FELIZ": {"tipo": "fijo", "valor": 20000.0, "fecha_expiracion": "2026-12-31T23:59:59", "es_activo": True}
}
