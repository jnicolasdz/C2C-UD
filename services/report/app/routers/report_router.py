from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.report_schema import ReportActionResponse, ReportResponse, ReportCreate, ReportUpdate
from app.services import report_service

router = APIRouter()


@router.post("/", response_model=ReportActionResponse, status_code=201)
def create_report(report_data: ReportCreate, db: Session = Depends(get_db)):
    """
    Crea y persiste el reporte, genera radicado, notifica al usuario y al administrador.
    Retorna success/send_status para que el frontend muestre éxito, error o reintento.
    """
    return report_service.create_report(db, report_data)


@router.get("/", response_model=List[ReportResponse])
def list_reports(
    user_id: Optional[str] = Query(default=None, description="Filtrar por ID del usuario emisor"),
    user_email: Optional[str] = Query(default=None, description="Filtrar por correo del usuario emisor"),
    send_status: Optional[str] = Query(default=None, description="PENDIENTE, ENVIADO o FALLIDO"),
    include_deleted: bool = Query(default=False, description="Incluir reportes eliminados lógicamente"),
    db: Session = Depends(get_db),
):
    return report_service.get_reports(
        db=db,
        user_id=user_id,
        user_email=user_email,
        send_status=send_status,
        include_deleted=include_deleted,
    )


@router.get("/failed", response_model=List[ReportResponse])
def list_failed_reports(
    user_id: Optional[str] = None,
    user_email: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Lista reportes fallidos para mostrar opción de reenvío en el frontend."""
    return report_service.get_failed_reports(db=db, user_id=user_id, user_email=user_email)


@router.get("/pending", response_model=List[ReportResponse])
def list_pending_reports(
    user_id: Optional[str] = None,
    user_email: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return report_service.get_pending_reports(db=db, user_id=user_id, user_email=user_email)


@router.get("/tracking/{radicado}", response_model=ReportResponse)
def track_report(radicado: str, db: Session = Depends(get_db)):
    return report_service.get_report_by_radicado(db, radicado)


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(report_id: int, db: Session = Depends(get_db)):
    return report_service.get_report_by_id(db, report_id)


@router.put("/{report_id}", response_model=ReportActionResponse)
def update_report(report_id: int, report_data: ReportUpdate, db: Session = Depends(get_db)):
    return report_service.update_report(db, report_id, report_data)


@router.post("/{report_id}/retry", response_model=ReportActionResponse)
def retry_report(report_id: int, db: Session = Depends(get_db)):
    """
    Reintenta el envío de un reporte FALLIDO o PENDIENTE conservando el mismo ID y radicado.
    """
    return report_service.retry_report_delivery(db, report_id)


@router.delete("/{report_id}")
def delete_report(report_id: int, db: Session = Depends(get_db)):
    return report_service.delete_report(db, report_id)
