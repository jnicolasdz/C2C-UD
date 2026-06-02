from fastapi import HTTPException

from app.core.email import EmailDeliveryError
from app.models.report_model import Report
from app.schemas.report_schema import ReportCreate, ReportManagementStatus, ReportSendStatus, ReportUpdate
from app.services import report_service


def _report_create(email="usuario@test.com", user_id="u-001"):
    return ReportCreate(
        user_id=user_id,
        user_name="Usuario Prueba",
        user_email=email,
        report_type="Comportamiento inapropiado",
        subject="Publicación sospechosa",
        description="Se reporta una publicación con comportamiento inapropiado dentro del marketplace.",
    )


def _insert_report(db, **overrides):
    data = {
        "radicado": "RPT-TEST-0001",
        "user_id": "u-001",
        "user_name": "Usuario Prueba",
        "user_email": "usuario@test.com",
        "report_type": "Comportamiento inapropiado",
        "subject": "Publicación sospechosa",
        "description": "Descripción suficientemente larga para la prueba.",
        "status": "RECIBIDO",
        "send_status": "FALLIDO",
        "delivery_message": "Error previo",
        "send_attempts": 1,
        "retry_count": 0,
        "is_deleted": False,
    }
    data.update(overrides)
    report = Report(**data)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def test_create_report_success_sets_enviado_and_sends_user_and_admin_email(db_session, monkeypatch):
    sent = {"user": 0, "admin": 0}

    monkeypatch.setattr(report_service, "generate_radicado", lambda: "RPT-TEST-OK")
    monkeypatch.setattr(report_service, "send_report_confirmation_email", lambda **kwargs: sent.__setitem__("user", sent["user"] + 1))
    monkeypatch.setattr(report_service, "send_admin_report_email", lambda **kwargs: sent.__setitem__("admin", sent["admin"] + 1))

    response = report_service.create_report(db_session, _report_create())

    assert response["success"] is True
    assert response["send_status"] == ReportSendStatus.ENVIADO.value
    assert response["retry_available"] is False
    assert response["notification_sent"] is True
    assert response["report"].radicado == "RPT-TEST-OK"
    assert response["report"].user_email == "usuario@test.com"
    assert sent == {"user": 1, "admin": 1}


def test_create_report_email_failure_marks_fallido_and_allows_retry(db_session, monkeypatch):
    monkeypatch.setattr(report_service, "generate_radicado", lambda: "RPT-TEST-FAIL")
    monkeypatch.setattr(
        report_service,
        "send_report_confirmation_email",
        lambda **kwargs: (_ for _ in ()).throw(EmailDeliveryError("SMTP no disponible")),
    )
    monkeypatch.setattr(report_service, "send_admin_report_email", lambda **kwargs: None)

    response = report_service.create_report(db_session, _report_create())

    assert response["success"] is False
    assert response["send_status"] == ReportSendStatus.FALLIDO.value
    assert response["retry_available"] is True
    assert response["notification_sent"] is False
    assert "Error en el envío" in response["message"]
    assert response["report"].send_attempts == 1


def test_retry_failed_report_keeps_original_id_and_radicado(db_session, monkeypatch):
    report = _insert_report(db_session, radicado="RPT-RETRY-001", send_status="FALLIDO")
    original_id = report.id
    original_radicado = report.radicado

    monkeypatch.setattr(report_service, "send_report_confirmation_email", lambda **kwargs: None)
    monkeypatch.setattr(report_service, "send_admin_report_email", lambda **kwargs: None)

    response = report_service.retry_report_delivery(db_session, original_id)

    assert response["success"] is True
    assert response["send_status"] == ReportSendStatus.ENVIADO.value
    assert response["retry_available"] is False
    assert response["notification_sent"] is True
    assert response["report"].id == original_id
    assert response["report"].radicado == original_radicado
    assert response["report"].retry_count == 1
    assert response["report"].send_attempts == 2


def test_retry_report_already_enviado_does_not_send_again(db_session, monkeypatch):
    report = _insert_report(db_session, send_status="ENVIADO", send_attempts=1)

    def fail_if_called(**kwargs):
        raise AssertionError("No se debe reenviar un reporte ya enviado")

    monkeypatch.setattr(report_service, "send_report_confirmation_email", fail_if_called)
    monkeypatch.setattr(report_service, "send_admin_report_email", fail_if_called)

    response = report_service.retry_report_delivery(db_session, report.id)

    assert response["success"] is True
    assert response["send_status"] == ReportSendStatus.ENVIADO.value
    assert response["retry_available"] is False
    assert response["notification_sent"] is None


def test_get_reports_filters_by_user_email_and_excludes_deleted(db_session):
    _insert_report(db_session, radicado="RPT-1", user_email="a@test.com")
    _insert_report(db_session, radicado="RPT-2", user_email="b@test.com")
    _insert_report(db_session, radicado="RPT-3", user_email="a@test.com", is_deleted=True)

    results = report_service.get_reports(db_session, user_email="a@test.com")

    assert len(results) == 1
    assert results[0].radicado == "RPT-1"


def test_get_report_by_radicado_returns_exact_report_and_user_relation(db_session):
    _insert_report(db_session, radicado="RPT-EXACT-001", user_id="u-999", user_email="exact@test.com")

    result = report_service.get_report_by_radicado(db_session, "RPT-EXACT-001")

    assert result.radicado == "RPT-EXACT-001"
    assert result.user_id == "u-999"
    assert result.user_email == "exact@test.com"


def test_update_status_sends_email_to_user(db_session, monkeypatch):
    report = _insert_report(db_session, status="RECIBIDO", send_status="ENVIADO")
    sent = {"status": 0}

    monkeypatch.setattr(report_service, "send_report_status_update_email", lambda **kwargs: sent.__setitem__("status", sent["status"] + 1))

    response = report_service.update_report(
        db_session,
        report.id,
        ReportUpdate(status=ReportManagementStatus.RESUELTO),
    )

    assert response["success"] is True
    assert response["notification_sent"] is True
    assert response["report"].status == ReportManagementStatus.RESUELTO.value
    assert sent["status"] == 1


def test_update_without_status_change_does_not_send_status_email(db_session, monkeypatch):
    report = _insert_report(db_session, status="RECIBIDO")

    def fail_if_called(**kwargs):
        raise AssertionError("No se debe enviar correo si no cambia el estado")

    monkeypatch.setattr(report_service, "send_report_status_update_email", fail_if_called)

    response = report_service.update_report(db_session, report.id, ReportUpdate(subject="Nuevo asunto válido"))

    assert response["success"] is True
    assert response["notification_sent"] is None
    assert response["report"].subject == "Nuevo asunto válido"


def test_delete_report_is_logical_for_audit(db_session):
    report = _insert_report(db_session)

    response = report_service.delete_report(db_session, report.id)

    assert response["success"] is True
    deleted = report_service.get_report_by_id(db_session, report.id, include_deleted=True)
    assert deleted.is_deleted is True
    assert deleted.deleted_at is not None
    assert deleted.status == "CERRADO"


def test_get_report_by_id_raises_404_when_not_found(db_session):
    try:
        report_service.get_report_by_id(db_session, 999)
        assert False, "Debe lanzar HTTPException"
    except HTTPException as exc:
        assert exc.status_code == 404
