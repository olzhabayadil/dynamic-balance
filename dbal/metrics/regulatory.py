from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from dbal.products.deal import Deal
from dbal.products.enums import BalanceSide


class RegulatoryMetrics(BaseModel):
    model_config = ConfigDict(frozen=True)

    capital: Decimal
    rwa: Decimal
    capital_adequacy_ratio: Decimal
    hqla: Decimal
    lcr_outflows: Decimal
    lcr_inflows: Decimal
    net_cash_outflows: Decimal
    lcr: Decimal
    available_stable_funding: Decimal
    required_stable_funding: Decimal
    nsfr: Decimal


def calculate_regulatory_metrics(
    deals: list[Deal],
    capital: Decimal = Decimal("15000000"),
) -> RegulatoryMetrics:
    rwa = sum(
        (
            deal.principal * deal.risk_weight
            for deal in deals
            if deal.balance_side == BalanceSide.ASSET
        ),
        Decimal("0"),
    )
    hqla = sum(
        (
            deal.principal * (Decimal("1") - deal.hqla_haircut)
            for deal in deals
            if deal.balance_side == BalanceSide.ASSET
        ),
        Decimal("0"),
    )
    lcr_outflows = sum(
        (
            deal.principal * deal.lcr_outflow_rate
            for deal in deals
            if deal.balance_side == BalanceSide.LIABILITY
        ),
        Decimal("0"),
    )
    lcr_inflows = sum(
        (
            deal.principal * deal.lcr_inflow_rate
            for deal in deals
            if deal.balance_side == BalanceSide.ASSET
        ),
        Decimal("0"),
    )
    capped_inflows = min(lcr_inflows, lcr_outflows * Decimal("0.75"))
    net_cash_outflows = max(lcr_outflows - capped_inflows, Decimal("1"))
    available_stable_funding = capital + sum(
        (
            deal.principal * deal.nsfr_asf_factor
            for deal in deals
            if deal.balance_side == BalanceSide.LIABILITY
        ),
        Decimal("0"),
    )
    required_stable_funding = sum(
        (
            deal.principal * deal.nsfr_rsf_factor
            for deal in deals
            if deal.balance_side == BalanceSide.ASSET
        ),
        Decimal("0"),
    )

    return RegulatoryMetrics(
        capital=capital,
        rwa=rwa,
        capital_adequacy_ratio=_ratio(capital, rwa),
        hqla=hqla,
        lcr_outflows=lcr_outflows,
        lcr_inflows=lcr_inflows,
        net_cash_outflows=net_cash_outflows,
        lcr=_ratio(hqla, net_cash_outflows),
        available_stable_funding=available_stable_funding,
        required_stable_funding=required_stable_funding,
        nsfr=_ratio(available_stable_funding, required_stable_funding),
    )


def _ratio(numerator: Decimal, denominator: Decimal) -> Decimal:
    if denominator == 0:
        return Decimal("0")
    return (numerator / denominator).quantize(Decimal("0.0001"))
