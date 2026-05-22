from datetime import date
from decimal import Decimal

from dbal.metrics import ets_rate_for_deal, interpolate_ets_rate
from dbal.org import BusinessBlock
from dbal.products.deal import Deal
from dbal.products.enums import BalanceSide, PaymentFrequency, ProductType


def test_interpolate_ets_rate_between_1y_and_2y() -> None:
    assert interpolate_ets_rate("KZT", 548) == Decimal("0.1465")


def test_ets_rate_uses_deal_remaining_maturity() -> None:
    deal = Deal(
        deal_id="L-ETS-001",
        product_type=ProductType.FIXED_RATE_LOAN,
        balance_side=BalanceSide.ASSET,
        currency="USD",
        principal=Decimal("1000000"),
        annual_rate=Decimal("0.08"),
        business_block=BusinessBlock.KSB,
        start_date=date(2026, 1, 1),
        maturity_date=date(2027, 1, 1),
        payment_frequency=PaymentFrequency.AT_MATURITY,
    )

    assert ets_rate_for_deal(deal, as_of=date(2026, 1, 1)) == Decimal("0.0500")
