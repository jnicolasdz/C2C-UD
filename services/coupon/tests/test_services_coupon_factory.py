from types import SimpleNamespace
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import app.services.CouponFactory as factory_module


class StubCouponDB:
    def __init__(self) -> None:
        self.last_by_text = None
        self.created_with = None

    def get_last_coupon_by_text(self, text: str):
        return self.last_by_text

    def create_coupon(self, text, coupon_id, discount, expiration_date):
        self.created_with = (text, coupon_id, discount, expiration_date)
        return {
            "text": text,
            "id": coupon_id,
            "discount": discount,
            "expiration_date": expiration_date,
        }


def test_create_coupon_uses_expiration_rule(monkeypatch) -> None:
    db = StubCouponDB()
    factory = factory_module.CouponFactory()
    factory.coupon_db = db

    monkeypatch.setattr(factory_module.COUPON_RULES, "get_expiration_date", lambda days: f"exp-{days}")

    result = factory.create_coupon("WELCOME", 0.2, 15)

    assert result["text"] == "WELCOME"
    assert db.created_with == ("WELCOME", 0, 0.2, "exp-15")


def test_create_happy_birthday_coupon_first_id(monkeypatch) -> None:
    db = StubCouponDB()
    factory = factory_module.CouponFactory()
    factory.coupon_db = db

    monkeypatch.setattr(factory_module.COUPON_RULES, "get_happy_birthday_expiration_date", lambda: "hb-exp")

    result = factory.create_happy_birthday_coupon()

    assert result["text"] == factory.happy_birthday
    assert db.created_with == (factory.happy_birthday, 1, factory.happy_birthday_discount, "hb-exp")


def test_create_happy_birthday_coupon_increments_from_last(monkeypatch) -> None:
    db = StubCouponDB()
    db.last_by_text = SimpleNamespace(id=7)
    factory = factory_module.CouponFactory()
    factory.coupon_db = db

    monkeypatch.setattr(factory_module.COUPON_RULES, "get_happy_birthday_expiration_date", lambda: "hb-exp")

    factory.create_happy_birthday_coupon()

    assert db.created_with[1] == 8


def test_create_referred_coupon_first_id(monkeypatch) -> None:
    db = StubCouponDB()
    factory = factory_module.CouponFactory()
    factory.coupon_db = db

    monkeypatch.setattr(factory_module.COUPON_RULES, "get_referred_expiration_date", lambda: "ref-exp")

    result = factory.create_referred_coupon()

    assert result["text"] == factory.referred
    assert db.created_with[0] == factory.referred
    assert db.created_with[2] == factory.referred_discount
    assert db.created_with[3] == "ref-exp"


def test_create_referred_coupon_increments_from_last(monkeypatch) -> None:
    db = StubCouponDB()
    db.last_by_text = SimpleNamespace(id=4)
    factory = factory_module.CouponFactory()
    factory.coupon_db = db

    monkeypatch.setattr(factory_module.COUPON_RULES, "get_referred_expiration_date", lambda: "ref-exp")

    factory.create_referred_coupon()

    assert factory.referred_index == 5
