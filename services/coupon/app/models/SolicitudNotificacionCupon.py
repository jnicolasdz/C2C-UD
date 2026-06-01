from pydantic import BaseModel, EmailStr
class SolicitudNotificacionCupon(BaseModel):
    email_usuario: EmailStr
    nombre_usuario: str
    tipo_evento: str  # "bienvenida" o "cumpleaños"
