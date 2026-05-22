# Data Dictionary

Initial normalized deal schema for fixed-rate bullet instruments.

| Field | Type | Required | Description |
|---|---|---:|---|
| `deal_id` | string | yes | Stable unique deal identifier. |
| `product_type` | enum | yes | Product model used for cash-flow generation. |
| `balance_side` | enum | yes | `asset` for bank assets, `liability` for bank liabilities. |
| `currency` | string | yes | ISO-like 3-letter currency code. |
| `principal` | decimal | yes | Outstanding principal amount at deal level. |
| `annual_rate` | decimal | yes | Annual nominal fixed rate as decimal, e.g. `0.12` for 12%. |
| `start_date` | date | yes | Deal start date. |
| `maturity_date` | date | yes | Final contractual maturity date. |
| `payment_frequency` | enum | yes | Interest payment frequency. |

Supported enum values:

| Enum | Values |
|---|---|
| `product_type` | `fixed_rate_loan`, `fixed_rate_deposit` |
| `balance_side` | `asset`, `liability` |
| `payment_frequency` | `at_maturity`, `monthly`, `quarterly` |
