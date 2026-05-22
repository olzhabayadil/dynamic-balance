from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from dbal.cashflows import generate_fixed_rate_bullet_cashflows
from dbal.products import BalanceSide, BusinessBlock, Deal


class FtpIncomeResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    business_block: BusinessBlock
    customer_interest: Decimal
    transfer_interest: Decimal
    chpda: Decimal
    chpdp: Decimal
    chpdr: Decimal


def calculate_ftp_income(deals: list[Deal], as_of: date) -> list[FtpIncomeResult]:
    rows: dict[BusinessBlock, FtpIncomeResult] = {}

    for deal in deals:
        customer_interest = _sum_interest(deal, as_of, deal.annual_rate)
        transfer_interest = _sum_interest(deal, as_of, deal.ftp_rate)

        if deal.balance_side == BalanceSide.ASSET:
            chpda = customer_interest - transfer_interest
            chpdp = Decimal("0")
            chpdr = transfer_interest
        else:
            chpda = Decimal("0")
            chpdp = abs(transfer_interest) - abs(customer_interest)
            chpdr = transfer_interest

        _add_to_block(
            rows,
            deal.business_block,
            customer_interest,
            transfer_interest,
            chpda,
            chpdp,
            Decimal("0"),
        )
        _add_to_block(
            rows,
            BusinessBlock.UALM,
            Decimal("0"),
            Decimal("0"),
            Decimal("0"),
            Decimal("0"),
            chpdr,
        )

    return list(rows.values())


def _sum_interest(deal: Deal, as_of: date, rate: Decimal) -> Decimal:
    rate_deal = deal.model_copy(update={"annual_rate": rate})
    return sum(
        (cashflow.interest for cashflow in generate_fixed_rate_bullet_cashflows(rate_deal, as_of)),
        Decimal("0"),
    )


def _add_to_block(
    rows: dict[BusinessBlock, FtpIncomeResult],
    block: BusinessBlock,
    customer_interest: Decimal,
    transfer_interest: Decimal,
    chpda: Decimal,
    chpdp: Decimal,
    chpdr: Decimal,
) -> None:
    previous = rows.get(
        block,
        FtpIncomeResult(
            business_block=block,
            customer_interest=Decimal("0"),
            transfer_interest=Decimal("0"),
            chpda=Decimal("0"),
            chpdp=Decimal("0"),
            chpdr=Decimal("0"),
        ),
    )
    rows[block] = FtpIncomeResult(
        business_block=block,
        customer_interest=previous.customer_interest + customer_interest,
        transfer_interest=previous.transfer_interest + transfer_interest,
        chpda=previous.chpda + chpda,
        chpdp=previous.chpdp + chpdp,
        chpdr=previous.chpdr + chpdr,
    )
