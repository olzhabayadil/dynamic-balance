from decimal import Decimal

from dbal.data import load_deals_csv
from dbal.metrics import calculate_regulatory_metrics


def test_regulatory_metrics_are_calculated_from_sample_portfolio() -> None:
    deals = load_deals_csv("sample_data/fixed_rate_deals.csv")

    metrics = calculate_regulatory_metrics(deals, capital=Decimal("15000000"))

    assert metrics.rwa > Decimal("0")
    assert metrics.capital_adequacy_ratio > Decimal("0")
    assert metrics.lcr_outflows > Decimal("0")
    assert metrics.net_cash_outflows > Decimal("0")
    assert metrics.available_stable_funding > Decimal("0")
    assert metrics.required_stable_funding > Decimal("0")
    assert metrics.nsfr > Decimal("0")


def test_lcr_inflows_are_capped_at_75_percent_of_outflows() -> None:
    deals = load_deals_csv("sample_data/fixed_rate_deals.csv")

    metrics = calculate_regulatory_metrics(deals, capital=Decimal("15000000"))

    assert metrics.net_cash_outflows >= metrics.lcr_outflows * Decimal("0.25")
