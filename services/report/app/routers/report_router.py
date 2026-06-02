from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.report_schema import ReportCreate, ReportResponse, ReportUpdate
from app.services import report_service

router = APIRouter()


@router.post("", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def create_report(report_data: ReportCreate, db: Session = Depends(get_db)):
    return report_service.create_report(db, report_data)


@router.get("", response_model=List[ReportResponse])
def list_reports(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return report_service.get_reports(db, skip=skip, limit=limit)


@router.get("/tracking/{radicado}", response_model=ReportResponse)
def track_report(radicado: str, db: Session = Depends(get_db)):
    return report_service.get_report_by_radicado(db, radicado)


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(report_id: int, db: Session = Depends(get_db)):
    return report_service.get_report_by_id(db, report_id)


@router.put("/{report_id}", response_model=ReportResponse)
def update_report(report_id: int, report_data: ReportUpdate, db: Session = Depends(get_db)):
    return report_service.update_report(db, report_id, report_data)


@router.delete("/{report_id}")
def delete_report(report_id: int, db: Session = Depends(get_db)):
    return report_service.delete_report(db, report_id)
