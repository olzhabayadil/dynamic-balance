from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from dbal.products.deal import Deal

DAYS_IN_YEAR = Decimal("365")


class EtsPoint(BaseModel):
    model_config = ConfigDict(frozen=True)

    tenor: str
    days: int
    rate: Decimal


class EtsCurve(BaseModel):
    model_config = ConfigDict(frozen=True)

    currency: str
    points: tuple[EtsPoint, ...]


TENOR_DAYS = {
    "1D": 1,
    "7D": 7,
    "1M": 30,
    "3M": 91,
    "6M": 182,
    "9M": 273,
    "1Y": 365,
    "2Y": 730,
    "3Y": 1095,
    "5Y": 1825,
    "7Y": 2555,
    "7Y+": 3650,
}

DEFAULT_ETS_CURVES = {
    "KZT": {
        "1D": "0.1250",
        "7D": "0.1275",
        "1M": "0.1300",
        "3M": "0.1350",
        "6M": "0.1400",
        "9M": "0.1425",
        "1Y": "0.1450",
        "2Y": "0.1480",
        "3Y": "0.1500",
        "5Y": "0.1530",
        "7Y": "0.1550",
        "7Y+": "0.1575",
    },
    "USD": {
        "1D": "0.0420",
        "7D": "0.0430",
        "1M": "0.0440",
        "3M": "0.0460",
        "6M": "0.0480",
        "9M": "0.0490",
        "1Y": "0.0500",
        "2Y": "0.0520",
        "3Y": "0.0530",
        "5Y": "0.0540",
        "7Y": "0.0550",
        "7Y+": "0.0560",
    },
    "EUR": {
        "1D": "0.0280",
        "7D": "0.0290",
        "1M": "0.0300",
        "3M": "0.0320",
        "6M": "0.0340",
        "9M": "0.0350",
        "1Y": "0.0360",
        "2Y": "0.0370",
        "3Y": "0.0380",
        "5Y": "0.0390",
        "7Y": "0.0400",
        "7Y+": "0.0410",
    },
    "RUB": {
        "1D": "0.1100",
        "7D": "0.1120",
        "1M": "0.1150",
        "3M": "0.1200",
        "6M": "0.1240",
        "9M": "0.1270",
        "1Y": "0.1300",
        "2Y": "0.1320",
        "3Y": "0.1340",
        "5Y": "0.1360",
        "7Y": "0.1380",
        "7Y+": "0.1400",
    },
    "GBP": {
        "1D": "0.0440",
        "7D": "0.0450",
        "1M": "0.0460",
        "3M": "0.0480",
        "6M": "0.0500",
        "9M": "0.0510",
        "1Y": "0.0520",
        "2Y": "0.0530",
        "3Y": "0.0540",
        "5Y": "0.0550",
        "7Y": "0.0560",
        "7Y+": "0.0570",
    },
}


def default_ets_curve(currency: str) -> EtsCurve:
    curve = DEFAULT_ETS_CURVES[currency]
    points = tuple(
        EtsPoint(tenor=tenor, days=TENOR_DAYS[tenor], rate=Decimal(rate))
        for tenor, rate in curve.items()
    )
    return EtsCurve(currency=currency, points=points)


def ets_rate_for_deal(deal: Deal, as_of: date) -> Decimal:
    remaining_days = max((deal.maturity_date - as_of).days, 1)
    return interpolate_ets_rate(deal.currency, remaining_days)


def interpolate_ets_rate(currency: str, days: int) -> Decimal:
    points = sorted(default_ets_curve(currency).points, key=lambda point: point.days)
    if days <= points[0].days:
        return points[0].rate
    if days >= points[-1].days:
        return points[-1].rate

    lower = points[0]
    upper = points[-1]
    for index, point in enumerate(points[:-1]):
        next_point = points[index + 1]
        if point.days <= days <= next_point.days:
            lower = point
            upper = next_point
            break

    if lower.days == upper.days:
        return lower.rate

    ratio = Decimal(days - lower.days) / Decimal(upper.days - lower.days)
    return (lower.rate + (upper.rate - lower.rate) * ratio).quantize(Decimal("0.0001"))
