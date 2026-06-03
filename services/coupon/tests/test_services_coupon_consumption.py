from types import SimpleNamespace

import pytest

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import app.services.CouponConsumtion as consumption_module


class StubCouponDB:
    def __init__(self, coupon=None, enabled=False):
        self.coupon = coupon
        self.enabled = enabled

    def get_coupon_by_code(self, coupon_code):
        return self.coupon

    def is_enable_coupon(self, coupon_code):
        return self.enabled


class StubUserDB:
    def __init__(self, consumed_assigned=False, consumed_unassigned=False):
        self.consumed_assigned = consumed_assigned
        self.consumed_unassigned = consumed_unassigned
        self.deleted_assigned = None
        self.added_unassigned = None

    def has_consumed_assigned_coupon(self, email, coupon_code):
        return self.consumed_assigned

    def has_consumed_unassigned_coupon(self, email, coupon_code):
        return self.consumed_unassigned

    def delete_assigned_coupon_from_user(self, email, coupon_code):
        self.deleted_assigned = (email, coupon_code)

    def add_unassigned_coupon_to_user(self, email, coupon_code):
        self.added_unassigned = (email, coupon_code)


def test_calculate_discounted_price() -> None:
    service = consumption_module.CouponConsumption()

    assert service.calculate_discounted_price(100.0, 0.25) == 75.0


def test_apply_assigned_coupon_ok(monkeypatch) -> None:
    coupon = SimpleNamespace(discount=0.2)
    coupon_db = StubCouponDB(coupon=coupon, enabled=False)
    user_db = StubUserDB(consumed_assigned=False)

    monkeypatch.setattr(consumption_module, "user_db", user_db)

    service = consumption_module.CouponConsumption()
    service.coupon_db = coupon_db
    service.user_db = user_db

    final_price = service.apply_assigned_coupon("user@example.com", "C1", 200.0)

    assert final_price == 160.0
    assert user_db.deleted_assigned == ("user@example.com", coupon)


def test_apply_assigned_coupon_precondition_consumed(monkeypatch) -> None:
    user_db = StubUserDB(consumed_assigned=True)
    monkeypatch.setattr(consumption_module, "user_db", user_db)

    service = consumption_module.CouponConsumption()

    with pytest.raises(ValueError, match="already been consumed"):
        service.apply_assigned_coupon("user@example.com", "C1", 100.0)


def test_apply_assigned_coupon_when_coupon_not_found(monkeypatch) -> None:
    user_db = StubUserDB(consumed_assigned=False)
    monkeypatch.setattr(consumption_module, "user_db", user_db)

    service = consumption_module.CouponConsumption()
    service.coupon_db = StubCouponDB(coupon=None, enabled=False)

    with pytest.raises(ValueError, match="does not exist"):
        service.apply_assigned_coupon("user@example.com", "C1", 100.0)


def test_apply_assigned_coupon_when_coupon_is_disabled(monkeypatch) -> None:
    user_db = StubUserDB(consumed_assigned=False)
    monkeypatch.setattr(consumption_module, "user_db", user_db)

    service = consumption_module.CouponConsumption()
    service.coupon_db = StubCouponDB(coupon=SimpleNamespace(discount=0.2), enabled=True)

    with pytest.raises(ValueError, match="Coupon is disable"):
        service.apply_assigned_coupon("user@example.com", "C1", 100.0)


def test_apply_unassigned_coupon_ok(monkeypatch) -> None:
    coupon = SimpleNamespace(discount=0.1)
    coupon_db = StubCouponDB(coupon=coupon, enabled=False)
    user_db = StubUserDB(consumed_unassigned=False)

    monkeypatch.setattr(consumption_module, "user_db", user_db)

    service = consumption_module.CouponConsumption()
    service.coupon_db = coupon_db
    service.user_db = user_db

    final_price = service.apply_unassigned_coupon("user@example.com", "C1", 100.0)

    assert final_price == 90.0
    assert user_db.added_unassigned == ("user@example.com", coupon)


def test_apply_unassigned_coupon_precondition_consumed(monkeypatch) -> None:
    user_db = StubUserDB(consumed_unassigned=True)
    monkeypatch.setattr(consumption_module, "user_db", user_db)

    service = consumption_module.CouponConsumption()

    with pytest.raises(ValueError, match="already been consumed"):
        service.apply_unassigned_coupon("user@example.com", "C1", 100.0)


def test_apply_unassigned_coupon_when_coupon_not_found(monkeypatch) -> None:
    user_db = StubUserDB(consumed_unassigned=False)
    monkeypatch.setattr(consumption_module, "user_db", user_db)

    service = consumption_module.CouponConsumption()
    service.coupon_db = StubCouponDB(coupon=None, enabled=False)

    with pytest.raises(ValueError, match="does not exist"):
        service.apply_unassigned_coupon("user@example.com", "C1", 100.0)


def test_apply_unassigned_coupon_when_coupon_is_disabled(monkeypatch) -> None:
    user_db = StubUserDB(consumed_unassigned=False)
    monkeypatch.setattr(consumption_module, "user_db", user_db)

    service = consumption_module.CouponConsumption()
    service.coupon_db = StubCouponDB(coupon=SimpleNamespace(discount=0.1), enabled=True)

    with pytest.raises(ValueError, match="Coupon is disable"):
        service.apply_unassigned_coupon("user@example.com", "C1", 100.0)
