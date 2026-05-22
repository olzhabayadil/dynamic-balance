from datetime import date
from decimal import Decimal

import pandas as pd
import streamlit as st

from dbal.cashflows import CashFlow, generate_fixed_rate_bullet_cashflows
from dbal.data import load_deals_csv
from dbal.products import Deal


def _deals_frame(deals: list[Deal]) -> pd.DataFrame:
    rows = [deal.model_dump(mode="json") for deal in deals]
    return pd.DataFrame(rows)


def _cashflows_frame(cashflows: list[CashFlow]) -> pd.DataFrame:
    rows = [cashflow.model_dump(mode="json") for cashflow in cashflows]
    frame = pd.DataFrame(rows)
    if frame.empty:
        return frame

    for column in ["principal", "interest", "total"]:
        frame[column] = frame[column].map(_format_decimal)
    return frame


def _format_decimal(value: object) -> str:
    if isinstance(value, Decimal):
        return f"{value:,.2f}"
    return str(value)


st.set_page_config(page_title="Dynamic Balance", layout="wide")

st.title("Dynamic Balance")
st.caption("ALM modeling workspace")

as_of = st.date_input("As of date", value=date(2026, 1, 1))
deals = load_deals_csv("sample_data/fixed_rate_deals.csv")
cashflows = [
    cashflow
    for deal in deals
    for cashflow in generate_fixed_rate_bullet_cashflows(deal, as_of=as_of)
]

assets = sum((deal.principal for deal in deals if deal.balance_side == "asset"), Decimal("0"))
liabilities = sum(
    (deal.principal for deal in deals if deal.balance_side == "liability"),
    Decimal("0"),
)

metric_left, metric_middle, metric_right = st.columns(3)
metric_left.metric("Deals", len(deals))
metric_middle.metric("Loan principal", _format_decimal(assets))
metric_right.metric("Deposit principal", _format_decimal(liabilities))

left, right = st.columns(2)

with left:
    st.subheader("Sample portfolio")
    st.dataframe(_deals_frame(deals), use_container_width=True, hide_index=True)

with right:
    st.subheader("Generated cash flows")
    st.dataframe(_cashflows_frame(cashflows), use_container_width=True, hide_index=True)
