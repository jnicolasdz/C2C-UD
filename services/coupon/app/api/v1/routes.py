from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from datetime import datetime
from fastapi_mail import FastMail, MessageSchema, MessageType
from pathlib import Path
import sys

if __package__ is None or __package__ == "":
	sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.models.SolicitudCupon import SolicitudCupon
from app.models.SolicitudNotificacionCupon import SolicitudNotificacionCupon
from app.models.FastAPIDescuentoFactory import FastAPIDescuentoFactory
from app.core.config import conf
from app.core.config import BD_CUPONES

router = APIRouter()

class Routes: 
    @router.get("/descuentos/{codigo}", tags=["Descuentos"])
    async def obtener_info_cupon(codigo: str):
        """Fase 1: Consulta estática de la existencia de un cupón."""
        codigo_upper = codigo.upper()
        if codigo_upper not in BD_CUPONES:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="El cupón ingresado no existe en el sistema."
            )
        return BD_CUPONES[codigo_upper]

    @router.post("/descuentos/aplicar", tags=["Descuentos"])
    async def aplicar_cupon(solicitud: SolicitudCupon):
        """Fase 3: Integración y cálculo polimórfico del descuento."""
        codigo_upper = solicitud.codigo.upper()
        
        if codigo_upper not in BD_CUPONES:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cupón no válido.")
        
        datos_cupon = BD_CUPONES[codigo_upper]
        
        if not datos_cupon["es_activo"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Este cupón está inactivo.")
            
        fecha_exp = datetime.fromisoformat(datos_cupon["fecha_expiracion"])
        if datetime.now() > fecha_exp:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El cupón ya ha expirado.")

        try:
            datos_completos = {**datos_cupon, "codigo": codigo_upper}
            
            fabrica = FastAPIDescuentoFactory()
            descuento_objeto = fabrica.crear_descuento(datos_cupon["tipo"], datos_completos)
            
            monto_a_descontar = descuento_objeto.calcular_descuento(solicitud.total_carrito)
            total_final = max(0.0, solicitud.total_carrito - monto_a_descontar)
            
            return {
                "mensaje": "¡Cupón aplicado con éxito!",
                "codigo": codigo_upper,
                "descuento_aplicado": monto_a_descontar,
                "total_original": solicitud.total_carrito,
                "total_con_descuento": total_final
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error en el motor de descuentos: {str(e)}"
            )

    @router.post("/descuentos/notificar", tags=["Notificaciones (Mail)"])
    async def enviar_correo_descuento(solicitud: SolicitudNotificacionCupon, background_tasks: BackgroundTasks):
        """Puente de integración: Envía cupones asíncronos mediante fastapi-mail."""
        if solicitud.tipo_evento == "bienvenida":
            codigo_cupon = "BIENVENIDA2026"
            asunto = f"¡Bienvenido al Marketplace, {solicitud.nombre_usuario}!"
            cuerpo_html = f"<h3>¡Gracias por registrarte!</h3><p>Usa el código <b>{codigo_cupon}</b> para obtener 15% de descuento.</p>"
        elif solicitud.tipo_evento == "cumpleaños":
            codigo_cupon = "CUMPLE_FELIZ"
            asunto = f"¡Feliz Cumpleaños, {solicitud.nombre_usuario}!"
            cuerpo_html = f"<h3>¡Celébralo con un regalo!</h3><p>Te regalamos $20.000 usando el código: <b>{codigo_cupon}</b></p>"
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Evento de notificación no soportado.")

        mensaje = MessageSchema(
            subject=asunto,
            recipients=[solicitud.email_usuario],
            body=cuerpo_html,
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        background_tasks.add_task(fm.send_message, mensaje)

        return {"status": "success", "mensaje": f"Correo de {solicitud.tipo_evento} programado exitosamente."}
