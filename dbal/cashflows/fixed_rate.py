from calendar import monthrange
from datetime import date
from decimal import Decimal

from dbal.cashflows.models import CashFlow, CashFlowType
from dbal.products import BalanceSide, Deal, PaymentFrequency

DAYS_IN_YEAR = Decimal("365")


def generate_fixed_rate_bullet_cashflows(deal: Deal, as_of: date) -> list[CashFlow]:
    if as_of >= deal.maturity_date:
        return []

    payment_dates = _payment_dates(deal.start_date, deal.maturity_date, deal.payment_frequency)
    future_dates = [payment_date for payment_date in payment_dates if payment_date > as_of]

    cashflows: list[CashFlow] = []
    period_start = deal.start_date
    for payment_date in payment_dates:
        interest_start = max(period_start, as_of)
        interest = Decimal("0")
        if payment_date > as_of and payment_date > interest_start:
            interest = _signed_amount(
                _interest_amount(deal.principal, deal.annual_rate, interest_start, payment_date),
                deal.balance_side,
            )

        principal = Decimal("0")
        if payment_date == deal.maturity_date and payment_date in future_dates:
            principal = _signed_amount(deal.principal, deal.balance_side)

        if payment_date in future_dates and (interest != 0 or principal != 0):
            cashflows.append(
                CashFlow(
                    deal_id=deal.deal_id,
                    flow_date=payment_date,
                    currency=deal.currency,
                    principal=principal,
                    interest=interest,
                    total=principal + interest,
                    flow_type=_flow_type(principal, interest),
                )
            )

        period_start = payment_date

    return cashflows


def _payment_dates(
    start_date: date,
    maturity_date: date,
    frequency: PaymentFrequency,
) -> list[date]:
    if frequency == PaymentFrequency.AT_MATURITY:
        return [maturity_date]

    months = {
        PaymentFrequency.MONTHLY: 1,
        PaymentFrequency.QUARTERLY: 3,
    }[frequency]

    dates: list[date] = []
    next_date = _add_months(start_date, months)
    while next_date < maturity_date:
        dates.append(next_date)
        next_date = _add_months(next_date, months)
    dates.append(maturity_date)
    return dates


def _add_months(input_date: date, months: int) -> date:
    month_index = input_date.month - 1 + months
    year = input_date.year + month_index // 12
    month = month_index % 12 + 1
    day = min(input_date.day, monthrange(year, month)[1])
    return date(year, month, day)


def _interest_amount(
    principal: Decimal,
    annual_rate: Decimal,
    start_date: date,
    end_date: date,
) -> Decimal:
    days = Decimal((end_date - start_date).days)
    return (principal * annual_rate * days / DAYS_IN_YEAR).quantize(Decimal("0.01"))


def _signed_amount(amount: Decimal, side: BalanceSide) -> Decimal:
    if side == BalanceSide.ASSET:
        return amount
    return -amount


def _flow_type(principal: Decimal, interest: Decimal) -> CashFlowType:
    if principal != 0 and interest != 0:
        return CashFlowType.PRINCIPAL_AND_INTEREST
    if principal != 0:
        return CashFlowType.PRINCIPAL
    return CashFlowType.INTEREST
