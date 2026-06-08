from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.schemas.COUPON_RULES import COUPON_RULES
from app.services.CouponService import CouponService


def _service() -> CouponService:
    service = CouponService()
    service.coupon_db = MagicMock()
    service.coupon_factory = MagicMock()
    service.user_db = MagicMock()
    service.coupon_consumption = MagicMock()
    return service


@pytest.mark.parametrize(
    "service_method,db_method,args,db_args,ret",
    [
        ("get_coupon_by_code", "get_coupon_by_code", ("C1",), ("C1",), {"code": "C1"}),
        ("get_coupon_by_creation_date", "get_coupon_by_creation_date", ("2026-01-01",), ("2026-01-01",), [1]),
        ("get_coupon_by_expiration_date", "get_coupon_by_expiration_date", ("2026-12-31",), ("2026-12-31",), [2]),
        ("get_expired_coupons", "get_expired_coupons", (), (), [3]),
        ("get_valid_coupons", "get_valid_coupons", (), (), [4]),
        ("get_enabled_coupons", "get_coupon_by_enabled", (), (True,), [5]),
        ("get_disabled_coupons", "get_coupon_by_enabled", (), (False,), [6]),
        ("get_coupons_by_text", "get_coupons_by_text", ("WELCOME",), ("WELCOME",), [7]),
        ("get_last_coupon_by_text", "get_last_coupon_by_text", ("WELCOME",), ("WELCOME",), {"id": 1}),
        ("get_all_coupons", "get_all_coupons", (), (), [8]),
        ("is_enable_coupon", "is_enable_coupon", ("C1",), ("C1",), True),
    ],
)
def test_service_db_delegation(service_method, db_method, args, db_args, ret) -> None:
    service = _service()
    getattr(service.coupon_db, db_method).return_value = ret

    result = getattr(service, service_method)(*args)

    assert result == ret
    getattr(service.coupon_db, db_method).assert_called_once_with(*db_args)


def test_happy_and_referred_coupon_queries_use_schema_constants() -> None:
    service = _service()
    service.coupon_db.get_coupons_by_text.side_effect = [[{"id": 1}], [{"id": 2}]]

    happy = service.get_happy_birthday_coupons()
    referred = service.get_referred_coupons()

    assert happy == [{"id": 1}]
    assert referred == [{"id": 2}]
    assert service.coupon_db.get_coupons_by_text.call_args_list[0].args[0] == COUPON_RULES.HAPPY_BIRTHDAY_COUPON_TEXT
    assert service.coupon_db.get_coupons_by_text.call_args_list[1].args[0] == COUPON_RULES.REFERRED_COUPON_TEXT


def test_coupon_state_changes_delegate_to_db() -> None:
    service = _service()

    service.enable_coupon("C1")
    service.disable_coupon("C1")
    service.delete_coupon("C1")

    service.coupon_db.enable_coupon.assert_called_once_with("C1")
    service.coupon_db.disable_coupon.assert_called_once_with("C1")
    service.coupon_db.delete_coupon.assert_called_once_with("C1")


def test_create_coupon_flows() -> None:
    service = _service()
    service.coupon_factory.create_coupon.return_value = {"code": "WELCOME-1"}
    service.coupon_factory.create_happy_birthday_coupon.return_value = {"code": "HAPPY-1"}
    service.coupon_factory.create_referred_coupon.return_value = {"code": "REF-1"}

    service.create_unassigned_coupon("WELCOME", 0.2, 10)
    service.create_assigned_coupon("WELCOME", 0.2, 10, "user@example.com")
    service.create_happy_birthday_coupon("user@example.com")
    service.create_referred_coupon("user@example.com")

    assert service.coupon_db.add_coupon.call_count == 4
    service.user_db.add_assigned_coupon_to_user.assert_any_call("user@example.com", "WELCOME-1")
    service.user_db.add_assigned_coupon_to_user.assert_any_call("user@example.com", "HAPPY-1")
    service.user_db.add_assigned_coupon_to_user.assert_any_call("user@example.com", "REF-1")


def test_get_user_coupons_returns_assigned_and_unassigned() -> None:
    service = _service()
    assigned_coupon = SimpleNamespace(to_dict=lambda: {"code": "A1"})
    unassigned_coupon = SimpleNamespace(to_dict=lambda: {"code": "U1"})
    service.user_db.get_user_by_email.return_value = SimpleNamespace(
        assigned_coupons=[assigned_coupon],
        unassigned_coupons=[unassigned_coupon],
    )

    result = service.get_user_coupons("user@example.com")

    assert result == {
        "assigned_coupons": [{"code": "A1"}],
        "unassigned_coupons": [{"code": "U1"}],
    }


def test_get_user_coupons_user_not_found() -> None:
    service = _service()
    service.user_db.get_user_by_email.return_value = None

    with pytest.raises(ValueError, match="does not exist"):
        service.get_user_coupons("missing@example.com")


def test_delete_asigned_coupon_from_user_precondition() -> None:
    service = _service()
    service.user_db.get_user_by_email.return_value = None

    with pytest.raises(ValueError, match="does not exist"):
        service.delete_asigned_coupon_from_user("missing@example.com", "C1")


def test_delete_asigned_coupon_from_user_moves_coupon_to_unassigned() -> None:
    service = _service()
    service.user_db.get_user_by_email.return_value = object()

    service.delete_asigned_coupon_from_user("user@example.com", "C1")

    service.user_db.add_unassigned_coupon_to_user.assert_called_once_with("user@example.com", "C1")


def test_apply_coupon_methods_delegate_to_consumption() -> None:
    service = _service()
    service.coupon_consumption.apply_assigned_coupon.return_value = 55.0
    service.coupon_consumption.apply_unassigned_coupon.return_value = 65.0

    assert service.apply_assigned_coupon("u", "C1", 100.0) == 55.0
    assert service.apply_unassigned_coupon("u", "C2", 100.0) == 65.0

    service.coupon_consumption.apply_assigned_coupon.assert_called_once_with("u", "C1", 100.0)
    service.coupon_consumption.apply_unassigned_coupon.assert_called_once_with("u", "C2", 100.0)
