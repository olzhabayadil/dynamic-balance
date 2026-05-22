from enum import Enum


class BalanceSide(str, Enum):
    ASSET = "asset"
    LIABILITY = "liability"


class BusinessBlock(str, Enum):
    KSB = "KSB"
    KRB = "KRB"
    TRB = "TRB"
    UK = "UK"
    UALM = "UALM"


class ProductType(str, Enum):
    FIXED_RATE_LOAN = "fixed_rate_loan"
    FIXED_RATE_DEPOSIT = "fixed_rate_deposit"


class PaymentFrequency(str, Enum):
    AT_MATURITY = "at_maturity"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
