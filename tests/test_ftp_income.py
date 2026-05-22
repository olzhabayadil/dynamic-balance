from datetime import date
from decimal import Decimal

from dbal.data import load_deals_csv
from dbal.metrics import calculate_ftp_income
from dbal.products.enums import BusinessBlock


def test_ftp_income_is_split_between_business_blocks_and_ualm() -> None:
    deals = load_deals_csv("sample_data/fixed_rate_deals.csv")

    results = {}
    for result in calculate_ftp_income(deals, as_of=date(2026, 1, 1)):
        results[result.business_block] = result

    assert BusinessBlock.KRB in results
    assert BusinessBlock.KSB in results
    assert BusinessBlock.TRB in results
    assert BusinessBlock.UALM in results

    assert results[BusinessBlock.KRB].chpda > Decimal("0")
    assert results[BusinessBlock.TRB].chpdp != Decimal("0")
    assert results[BusinessBlock.UALM].chpdr != Decimal("0")


def test_ftp_risk_income_equals_transfer_expenses_less_transfer_income() -> None:
    deals = load_deals_csv("sample_data/fixed_rate_deals.csv")
    results = calculate_ftp_income(deals, as_of=date(2026, 1, 1))
    block_rows = [result for result in results if result.business_block != BusinessBlock.UALM]
    ualm = next(result for result in results if result.business_block == BusinessBlock.UALM)

    expected_chpdr = sum((result.transfer_interest for result in block_rows), Decimal("0"))

    assert ualm.chpdr == expected_chpdr
