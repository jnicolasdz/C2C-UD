import logging
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.email import send_report_confirmation_email
from app.models.report_model import Report
from app.schemas.report_schema import ReportCreate, ReportUpdate
from app.utils.radicado import generate_radicado

logger = logging.getLogger(__name__)


def create_report(db: Session, report_data: ReportCreate) -> Report:
    """Create a report, generate its radicado and send a confirmation email."""
    new_report = Report(
        radicado=generate_radicado(),
        user_name=report_data.user_name,
        user_email=str(report_data.user_email),
        report_type=report_data.report_type,
        subject=report_data.subject,
        description=report_data.description,
        status="RECIBIDO",
    )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    try:
        send_report_confirmation_email(
            to_email=new_report.user_email,
            user_name=new_report.user_name,
            radicado=new_report.radicado,
        )
    except Exception as exc:  # noqa: BLE001 - email failure should not delete a created report.
        logger.exception("Report was created, but confirmation email failed: %s", exc)

    return new_report


def get_reports(db: Session, skip: int = 0, limit: int = 100) -> List[Report]:
    return db.query(Report).order_by(Report.created_at.desc()).offset(skip).limit(limit).all()


def get_report_by_id(db: Session, report_id: int) -> Report:
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reporte no encontrado")
    return report


def get_report_by_radicado(db: Session, radicado: str) -> Report:
    report = db.query(Report).filter(Report.radicado == radicado).first()
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Radicado no encontrado")
    return report


def update_report(db: Session, report_id: int, report_data: ReportUpdate) -> Report:
    report = get_report_by_id(db, report_id)

    update_data = report_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(report, field, value)

    db.commit()
    db.refresh(report)
    return report


def delete_report(db: Session, report_id: int) -> dict:
    report = get_report_by_id(db, report_id)
    db.delete(report)
    db.commit()
    return {"message": "Reporte eliminado correctamente", "deleted_report_id": report_id}
