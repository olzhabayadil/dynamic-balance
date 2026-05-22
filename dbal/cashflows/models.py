from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict


class CashFlowType(str, Enum):
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
