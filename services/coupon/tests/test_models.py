
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.models.Coupon import Coupon
from app.models.User import User


def test_user_to_dict_and_str() -> None:
    user = User(user_email="user@example.com", unassigned_coupons=["U1"], assigned_coupons=["A1"])

    assert str(user) == "User(user_email=user@example.com)"
    assert user.__to_dict__() == {
        "user": "user@example.com",
        "unassigned_coupons": ["U1"],
        "assigned_coupons": ["A1"],
    }


def test_coupon_to_dict_and_str() -> None:
    coupon = Coupon.model_construct(
        code="WELCOME1",
        id=1,
        text="WELCOME",
        discount=0.1,
        creation_date="2026-01-01",
        expiration_date="2026-12-31",
        enabled=True,
    )

    assert str(coupon) == (
        "Coupon(code=WELCOME1, discount=0.1,creation_date=2026-01-01, "
        "expiration_date=2026-12-31, enabled=True)"
    )
    assert coupon.__to_dict__() == {
        "code": "WELCOME1",
        "discount": 0.1,
        "expiration_date": "2026-12-31",
        "enabled": True,
    }
