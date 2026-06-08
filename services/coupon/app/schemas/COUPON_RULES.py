from datetime import datetime, timedelta


HAPPY_BIRTHDAY_COUPON_TEXT = "HAPPYBIRTHDAY"
HAPPY_BIRTHDAY_DISCOUNT = 0.25
_HAPPY_BIRTHDAY_LIFESPAN = 30

REFERRED_COUPON_TEXT = "REFERRED"
REFERRED_DISCOUNT = 0.15
_REFERRED_LIFESPAN = 5

_HB_TEXT = HAPPY_BIRTHDAY_COUPON_TEXT
_HB_DISCOUNT = HAPPY_BIRTHDAY_DISCOUNT
_REF_TEXT = REFERRED_COUPON_TEXT
_REF_DISCOUNT = REFERRED_DISCOUNT


def get_happy_birthday_expiration_date() -> datetime:
    now = datetime.now()
    return datetime(year=now.year, month=now.month, day=now.day) + timedelta(days=_HAPPY_BIRTHDAY_LIFESPAN)


def get_referred_expiration_date() -> datetime:
    return datetime.now() + timedelta(days=_REFERRED_LIFESPAN)


def get_expiration_date(lifespan: int) -> datetime:
    return datetime.now() + timedelta(days=lifespan)


class COUPON_RULES:
    HAPPY_BIRTHDAY_COUPON_TEXT = _HB_TEXT
    HAPPY_BIRTHDAY_DISCOUNT = _HB_DISCOUNT
    REFERRED_COUPON_TEXT = _REF_TEXT
    REFERRED_DISCOUNT = _REF_DISCOUNT

    @staticmethod
    def get_happy_birthday_expiration_date() -> datetime:
        return get_happy_birthday_expiration_date()

    @staticmethod
    def get_referred_expiration_date() -> datetime:
        return get_referred_expiration_date()

    @staticmethod
    def get_expiration_date(lifespan: int) -> datetime:
        return get_expiration_date(lifespan)