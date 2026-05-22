from datetime import date
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class CashFlowType(StrEnum):
    INTEREST = "interest"
    PRINCIPAL = "principal"
    PRINCIPAL_AND_INTEREST = "principal_and_interest"


class CashFlow(BaseModel):
    model_config = ConfigDict(frozen=True)

    deal_id: str
    flow_date: date
    currency: str
    principal: Decimal
    interest: Decimal
    total: Decimal
    flow_type: CashFlowType
