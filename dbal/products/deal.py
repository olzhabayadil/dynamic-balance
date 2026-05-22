from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from dbal.products.enums import BalanceSide, BusinessBlock, PaymentFrequency, ProductType


class Deal(BaseModel):
    model_config = ConfigDict(frozen=True)

    deal_id: str
    product_type: ProductType
    balance_side: BalanceSide
    currency: str = Field(min_length=3, max_length=3)
    principal: Decimal = Field(gt=0)
    annual_rate: Decimal = Field(ge=0)
    business_block: BusinessBlock
    start_date: date
    maturity_date: date
    payment_frequency: PaymentFrequency = PaymentFrequency.AT_MATURITY

    @model_validator(mode="after")
    def validate_dates(self) -> "Deal":
        if self.maturity_date <= self.start_date:
            msg = "maturity_date must be after start_date"
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def validate_block_can_own_product(self) -> "Deal":
        allowed_blocks = {
            ProductType.FIXED_RATE_LOAN: {BusinessBlock.KSB, BusinessBlock.KRB, BusinessBlock.UK},
            ProductType.FIXED_RATE_DEPOSIT: {
                BusinessBlock.KSB,
                BusinessBlock.TRB,
                BusinessBlock.UK,
            },
        }[self.product_type]
        if self.business_block not in allowed_blocks:
            msg = f"{self.business_block} cannot own {self.product_type}"
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def validate_side_matches_product(self) -> "Deal":
        expected_side = {
            ProductType.FIXED_RATE_LOAN: BalanceSide.ASSET,
            ProductType.FIXED_RATE_DEPOSIT: BalanceSide.LIABILITY,
        }[self.product_type]
        if self.balance_side != expected_side:
            msg = f"{self.product_type} must be modeled as {expected_side}"
            raise ValueError(msg)
        return self
