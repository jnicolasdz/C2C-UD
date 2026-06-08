import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
import pytest

import app.api.v1.routers as routers_module
from app.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "path,service_method,expected",
    [
        ("/api/v1/coupons/code/C1", "get_coupon_by_code", {"code": "C1"}),
        ("/api/v1/coupons/creation-date/2026-01-01", "get_coupon_by_creation_date", [{"id": 1}]),
        ("/api/v1/coupons/expiration-date/2026-12-31", "get_coupon_by_expiration_date", [{"id": 2}]),
        ("/api/v1/coupons/expired", "get_expired_coupons", [{"id": 3}]),
        ("/api/v1/coupons/valid", "get_valid_coupons", [{"id": 4}]),
        ("/api/v1/coupons/enabled", "get_enabled_coupons", [{"id": 5}]),
        ("/api/v1/coupons/disabled", "get_disabled_coupons", [{"id": 6}]),
        ("/api/v1/coupons/search/WELCOME", "get_coupons_by_text", [{"id": 7}]),
        ("/api/v1/coupons/happy-birthday", "get_happy_birthday_coupons", [{"id": 8}]),
        ("/api/v1/coupons/referred", "get_referred_coupons", [{"id": 9}]),
        ("/api/v1/coupons/last/WELCOME", "get_last_coupon_by_text", {"id": 10}),
        ("/api/v1/coupons", "get_all_coupons", [{"id": 11}]),
        (
            "/api/v1/users/user@example.com/coupons",
            "get_user_coupons",
            {"assigned_coupons": [], "unassigned_coupons": []},
        ),
        ("/api/v1/users/coupons/all", "get_all_users_coupons", {"user@example.com": {}}),
    ],
)
def test_get_endpoints_success(monkeypatch, path: str, service_method: str, expected) -> None:
    monkeypatch.setattr(routers_module.service, service_method, lambda *args, **kwargs: expected)

    response = client.get(path)

    assert response.status_code == 200
    assert response.json() == expected


@pytest.mark.parametrize(
    "path,service_method",
    [
        ("/api/v1/coupons/code/C1", "get_coupon_by_code"),
        ("/api/v1/coupons/creation-date/2026-01-01", "get_coupon_by_creation_date"),
        ("/api/v1/coupons/expiration-date/2026-12-31", "get_coupon_by_expiration_date"),
        ("/api/v1/coupons/expired", "get_expired_coupons"),
        ("/api/v1/coupons/valid", "get_valid_coupons"),
        ("/api/v1/coupons/enabled", "get_enabled_coupons"),
        ("/api/v1/coupons/disabled", "get_disabled_coupons"),
        ("/api/v1/coupons/search/WELCOME", "get_coupons_by_text"),
        ("/api/v1/coupons/happy-birthday", "get_happy_birthday_coupons"),
        ("/api/v1/coupons/referred", "get_referred_coupons"),
        ("/api/v1/coupons/last/WELCOME", "get_last_coupon_by_text"),
        ("/api/v1/coupons", "get_all_coupons"),
        ("/api/v1/users/user@example.com/coupons", "get_user_coupons"),
        ("/api/v1/users/coupons/all", "get_all_users_coupons"),
    ],
)
def test_get_endpoints_error(monkeypatch, path: str, service_method: str) -> None:
    def _raise(*args, **kwargs):
        raise ValueError("boom")

    monkeypatch.setattr(routers_module.service, service_method, _raise)

    response = client.get(path)

    assert response.status_code == 200
    assert response.json() == {"error": "boom"}


def test_is_enabled_endpoint_success(monkeypatch) -> None:
    monkeypatch.setattr(routers_module.service, "is_enable_coupon", lambda *args, **kwargs: True)

    response = client.get("/api/v1/coupons/C1/is-enabled")

    assert response.status_code == 200
    assert response.json() == {"enabled": True}


def test_is_enabled_endpoint_error(monkeypatch) -> None:
    def _raise(*args, **kwargs):
        raise ValueError("boom")

    monkeypatch.setattr(routers_module.service, "is_enable_coupon", _raise)

    response = client.get("/api/v1/coupons/C1/is-enabled")

    assert response.status_code == 200
    assert response.json() == {"error": "boom"}


@pytest.mark.parametrize(
    "method,path,service_method,params,expected",
    [
        ("post", "/api/v1/coupons/C1/enable", "enable_coupon", None, {"status": "enabled"}),
        ("post", "/api/v1/coupons/C1/disable", "disable_coupon", None, {"status": "disabled"}),
        ("delete", "/api/v1/coupons/C1", "delete_coupon", None, {"status": "deleted"}),
        (
            "post",
            "/api/v1/coupons/unassigned",
            "create_unassigned_coupon",
            {"text": "WELCOME", "discount": 0.2, "days": 10},
            {"status": "created"},
        ),
        (
            "post",
            "/api/v1/coupons/assigned",
            "create_assigned_coupon",
            {"text": "WELCOME", "discount": 0.2, "days": 10, "user_email": "user@example.com"},
            {"status": "created"},
        ),
        (
            "post",
            "/api/v1/coupons/happy-birthday/user@example.com",
            "create_happy_birthday_coupon",
            None,
            {"status": "created"},
        ),
        (
            "post",
            "/api/v1/coupons/referred/user@example.com",
            "create_referred_coupon",
            None,
            {"status": "created"},
        ),
        (
            "delete",
            "/api/v1/users/user@example.com/coupons/C1",
            "delete_asigned_coupon_from_user",
            None,
            {"status": "deleted"},
        ),
    ],
)
def test_status_endpoints_success(monkeypatch, method: str, path: str, service_method: str, params, expected) -> None:
    monkeypatch.setattr(routers_module.service, service_method, lambda *args, **kwargs: None)

    response = getattr(client, method)(path, params=params)

    assert response.status_code == 200
    assert response.json() == expected


@pytest.mark.parametrize(
    "method,path,service_method,params",
    [
        ("post", "/api/v1/coupons/C1/enable", "enable_coupon", None),
        ("post", "/api/v1/coupons/C1/disable", "disable_coupon", None),
        ("delete", "/api/v1/coupons/C1", "delete_coupon", None),
        (
            "post",
            "/api/v1/coupons/unassigned",
            "create_unassigned_coupon",
            {"text": "WELCOME", "discount": 0.2, "days": 10},
        ),
        (
            "post",
            "/api/v1/coupons/assigned",
            "create_assigned_coupon",
            {"text": "WELCOME", "discount": 0.2, "days": 10, "user_email": "missing@example.com"},
        ),
        ("post", "/api/v1/coupons/happy-birthday/user@example.com", "create_happy_birthday_coupon", None),
        ("post", "/api/v1/coupons/referred/user@example.com", "create_referred_coupon", None),
        ("delete", "/api/v1/users/user@example.com/coupons/C1", "delete_asigned_coupon_from_user", None),
    ],
)
def test_status_endpoints_error(monkeypatch, method: str, path: str, service_method: str, params) -> None:
    def _raise(*args, **kwargs):
        raise ValueError("precondition failed")

    monkeypatch.setattr(routers_module.service, service_method, _raise)

    response = getattr(client, method)(path, params=params)

    assert response.status_code == 200
    assert response.json() == {"error": "precondition failed"}


@pytest.mark.parametrize(
    "path,service_method,params,expected_price",
    [
        (
            "/api/v1/users/user@example.com/coupons/C1/apply-assigned",
            "apply_assigned_coupon",
            {"original_price": 100.0},
            80.0,
        ),
        (
            "/api/v1/users/user@example.com/coupons/C1/apply-unassigned",
            "apply_unassigned_coupon",
            {"original_price": 100.0},
            70.0,
        ),
    ],
)
def test_apply_coupon_endpoints_success(monkeypatch, path: str, service_method: str, params, expected_price: float) -> None:
    monkeypatch.setattr(routers_module.service, service_method, lambda *args, **kwargs: expected_price)

    response = client.post(path, params=params)

    assert response.status_code == 200
    assert response.json() == {"final_price": expected_price}


@pytest.mark.parametrize(
    "path,service_method,params",
    [
        (
            "/api/v1/users/user@example.com/coupons/C1/apply-assigned",
            "apply_assigned_coupon",
            {"original_price": 100.0},
        ),
        (
            "/api/v1/users/user@example.com/coupons/C1/apply-unassigned",
            "apply_unassigned_coupon",
            {"original_price": 100.0},
        ),
    ],
)
def test_apply_coupon_endpoints_error(monkeypatch, path: str, service_method: str, params) -> None:
    def _raise(*args, **kwargs):
        raise ValueError("coupon invalid")

    monkeypatch.setattr(routers_module.service, service_method, _raise)

    response = client.post(path, params=params)

    assert response.status_code == 200
    assert response.json() == {"error": "coupon invalid"}
