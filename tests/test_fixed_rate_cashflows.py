from datetime import date
from decimal import Decimal

from dbal.cashflows import generate_fixed_rate_bullet_cashflows
from dbal.data import load_deals_csv
from dbal.products import BalanceSide, BusinessBlock, Deal, PaymentFrequency, ProductType


def test_at_maturity_asset_cashflow_is_positive() -> None:
    deal = Deal(
        deal_id="L-001",
        product_type=ProductType.FIXED_RATE_LOAN,
        balance_side=BalanceSide.ASSET,
        currency="KZT",
        principal=Decimal("1000000"),
        annual_rate=Decimal("0.12"),
        ftp_rate=Decimal("0.09"),
        business_block=BusinessBlock.KSB,
        start_date=date(2026, 1, 1),
        maturity_date=date(2027, 1, 1),
        payment_frequency=PaymentFrequency.AT_MATURITY,
    )

    cashflows = generate_fixed_rate_bullet_cashflows(deal, as_of=date(2026, 1, 1))

    assert len(cashflows) == 1
    assert cashflows[0].principal == Decimal("1000000")
    assert cashflows[0].interest == Decimal("120000.00")
    assert cashflows[0].total == Decimal("1120000.00")


def test_at_maturity_liability_cashflow_is_negative() -> None:
    deal = Deal(
        deal_id="D-001",
        product_type=ProductType.FIXED_RATE_DEPOSIT,
        balance_side=BalanceSide.LIABILITY,
        currency="KZT",
        principal=Decimal("500000"),
        annual_rate=Decimal("0.08"),
        ftp_rate=Decimal("0.07"),
        business_block=BusinessBlock.TRB,
        start_date=date(2026, 1, 1),
        maturity_date=date(2026, 7, 1),
        payment_frequency=PaymentFrequency.AT_MATURITY,
    )

    cashflows = generate_fixed_rate_bullet_cashflows(deal, as_of=date(2026, 1, 1))

    assert len(cashflows) == 1
    assert cashflows[0].principal == Decimal("-500000")
    assert cashflows[0].interest == Decimal("-19835.62")
    assert cashflows[0].total == Decimal("-519835.62")


def test_monthly_interest_and_principal_at_maturity() -> None:
    deal = Deal(
        deal_id="L-002",
        product_type=ProductType.FIXED_RATE_LOAN,
        balance_side=BalanceSide.ASSET,
        currency="USD",
        principal=Decimal("250000"),
        annual_rate=Decimal("0.06"),
        ftp_rate=Decimal("0.04"),
        business_block=BusinessBlock.KRB,
        start_date=date(2026, 1, 31),
        maturity_date=date(2026, 7, 31),
        payment_frequency=PaymentFrequency.MONTHLY,
    )

    cashflows = generate_fixed_rate_bullet_cashflows(deal, as_of=date(2026, 1, 31))

    assert [cashflow.flow_date for cashflow in cashflows] == [
        date(2026, 2, 28),
        date(2026, 3, 28),
        date(2026, 4, 28),
        date(2026, 5, 28),
        date(2026, 6, 28),
        date(2026, 7, 28),
        date(2026, 7, 31),
    ]
    assert cashflows[-1].principal == Decimal("250000")
    assert cashflows[-1].interest == Decimal("123.29")


def test_load_sample_deals_csv() -> None:
    deals = load_deals_csv("sample_data/fixed_rate_deals.csv")

    assert len(deals) == 12
    assert deals[0].deal_id == "RL-MTG-001"
    assert deals[0].principal == Decimal("18500000")
    assert deals[0].ftp_rate == Decimal("0.135")
    assert sum(1 for deal in deals if deal.balance_side == BalanceSide.ASSET) == 6
    assert sum(1 for deal in deals if deal.balance_side == BalanceSide.LIABILITY) == 6
