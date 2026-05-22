from enum import StrEnum


class BalanceSide(StrEnum):
    ASSET = "asset"
    LIABILITY = "liability"


class BusinessBlock(StrEnum):
    KSB = "KSB"
    KRB = "KRB"
    TRB = "TRB"
    UK = "UK"
    UALM = "UALM"


class ProductType(StrEnum):
    FIXED_RATE_LOAN = "fixed_rate_loan"
    FIXED_RATE_DEPOSIT = "fixed_rate_deposit"


class PaymentFrequency(StrEnum):
    AT_MATURITY = "at_maturity"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
