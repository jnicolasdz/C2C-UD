from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.email import (
    EmailDeliveryError,
    send_admin_report_email,
    send_report_confirmation_email,
    send_report_status_update_email,
)
from app.models.report_model import Report
from app.schemas.report_schema import ReportCreate, ReportSendStatus, ReportUpdate
from app.utils.radicado import generate_radicado


def _retry_available(report: Report) -> bool:
    return report.send_status in {ReportSendStatus.FALLIDO.value, ReportSendStatus.PENDIENTE.value}


def _attempt_delivery(report: Report) -> tuple[bool, str]:
    """
    Intenta notificar al usuario y al administrador.
    Retorna (success, message) para que el frontend pueda reaccionar.
    """
    report.send_attempts = (report.send_attempts or 0) + 1
    report.last_send_attempt_at = datetime.now(timezone.utc)

    try:
        send_report_confirmation_email(
            to_email=report.user_email,
            user_name=report.user_name,
            radicado=report.radicado,
            status=report.status,
        )

        send_admin_report_email(
            admin_email=settings.ADMIN_REPORT_EMAIL,
            radicado=report.radicado,
            user_id=report.user_id,
            user_name=report.user_name,
            user_email=report.user_email,
            report_type=report.report_type,
            subject_value=report.subject,
            description=report.description,
        )
    except EmailDeliveryError as exc:
        report.send_status = ReportSendStatus.FALLIDO.value
        report.delivery_message = f"Error en el envío: {exc}"
        return False, report.delivery_message

    report.send_status = ReportSendStatus.ENVIADO.value
    report.delivery_message = "Envío exitoso. El reporte fue guardado y notificado correctamente."
    return True, report.delivery_message


def create_report(db: Session, report_data: ReportCreate):
    new_report = Report(
        radicado=generate_radicado(),
        user_id=report_data.user_id,
        user_name=report_data.user_name,
        user_email=report_data.user_email,
        report_type=report_data.report_type,
        subject=report_data.subject,
        description=report_data.description,
        status="RECIBIDO",
        send_status=ReportSendStatus.PENDIENTE.value,
        delivery_message="Reporte recibido. Envío pendiente de confirmación.",
    )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    success, message = _attempt_delivery(new_report)
    db.commit()
    db.refresh(new_report)

    return {
        "success": success,
        "message": message,
        "send_status": new_report.send_status,
        "retry_available": _retry_available(new_report),
        "notification_sent": success,
        "report": new_report,
    }


def get_reports(
    db: Session,
    user_id: Optional[str] = None,
    user_email: Optional[str] = None,
    send_status: Optional[str] = None,
    include_deleted: bool = False,
):
    query = db.query(Report)

    if not include_deleted:
        query = query.filter(Report.is_deleted.is_(False))

    if user_id:
        query = query.filter(Report.user_id == user_id)

    if user_email:
        query = query.filter(Report.user_email == user_email)

    if send_status:
        query = query.filter(Report.send_status == send_status.upper())

    return query.order_by(Report.created_at.desc()).all()


def get_failed_reports(db: Session, user_id: Optional[str] = None, user_email: Optional[str] = None):
    return get_reports(
        db=db,
        user_id=user_id,
        user_email=user_email,
        send_status=ReportSendStatus.FALLIDO.value,
    )


def get_pending_reports(db: Session, user_id: Optional[str] = None, user_email: Optional[str] = None):
    return get_reports(
        db=db,
        user_id=user_id,
        user_email=user_email,
        send_status=ReportSendStatus.PENDIENTE.value,
    )


def get_report_by_id(db: Session, report_id: int, include_deleted: bool = False):
    query = db.query(Report).filter(Report.id == report_id)

    if not include_deleted:
        query = query.filter(Report.is_deleted.is_(False))

    report = query.first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reporte no encontrado",
        )

    return report


def get_report_by_radicado(db: Session, radicado: str):
    report = (
        db.query(Report)
        .filter(Report.radicado == radicado)
        .filter(Report.is_deleted.is_(False))
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reporte no encontrado para el radicado indicado",
        )

    return report


def update_report(db: Session, report_id: int, report_data: ReportUpdate):
    report = get_report_by_id(db, report_id)
    previous_status = report.status
    update_data = report_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(report, field, value.value if hasattr(value, "value") else value)

    status_changed = "status" in update_data and report.status != previous_status
    notification_sent = None
    message = "Reporte actualizado correctamente."

    if status_changed and settings.NOTIFY_USER_ON_STATUS_UPDATE:
        try:
            send_report_status_update_email(
                to_email=report.user_email,
                user_name=report.user_name,
                radicado=report.radicado,
                previous_status=previous_status,
                new_status=report.status,
                delivery_message=report.delivery_message,
            )
            notification_sent = True
            message = "Reporte actualizado correctamente. Se notificó al usuario sobre el cambio de estado."
        except EmailDeliveryError as exc:
            notification_sent = False
            message = f"Reporte actualizado correctamente, pero no se pudo notificar al usuario: {exc}"

    db.commit()
    db.refresh(report)

    return {
        "success": True,
        "message": message,
        "send_status": report.send_status,
        "retry_available": _retry_available(report),
        "notification_sent": notification_sent,
        "report": report,
    }


def retry_report_delivery(db: Session, report_id: int):
    report = get_report_by_id(db, report_id)

    if report.send_status == ReportSendStatus.ENVIADO.value:
        return {
            "success": True,
            "message": "El reporte ya se encuentra en estado ENVIADO. No requiere reintento.",
            "send_status": report.send_status,
            "retry_available": False,
            "notification_sent": None,
            "report": report,
        }

    report.retry_count = (report.retry_count or 0) + 1
    report.send_status = ReportSendStatus.PENDIENTE.value
    report.delivery_message = "Reintento de envío en proceso."
    db.commit()
    db.refresh(report)

    success, message = _attempt_delivery(report)
    db.commit()
    db.refresh(report)

    return {
        "success": success,
        "message": message,
        "send_status": report.send_status,
        "retry_available": _retry_available(report),
        "notification_sent": success,
        "report": report,
    }


def delete_report(db: Session, report_id: int):
    """
    Eliminación lógica para conservar integridad, seguimiento y auditoría.
    """
    report = get_report_by_id(db, report_id)
    report.is_deleted = True
    report.deleted_at = datetime.now(timezone.utc)
    report.status = "CERRADO"
    db.commit()

    return {
        "success": True,
        "message": "Reporte eliminado lógicamente. Se conserva para auditoría.",
        "report_id": report_id,
        "radicado": report.radicado,
    }
