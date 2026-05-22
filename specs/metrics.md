# Metrics

Each metric should have:

- purpose;
- formula;
- input fields;
- scenario treatment;
- aggregation;
- validation source;
- acceptance tolerance.

## FTP Income Allocation

Business blocks:

| Code | Name | Role |
|---|---|---|
| `KSB` | Крупный и средний бизнес | Lending and funding block |
| `KRB` | Кредитующий розничный бизнес | Lending-only block |
| `TRB` | Транзакционный розничный бизнес | Funding-only block |
| `UK` | Управление казначейства | Treasury block |
| `UALM` | Управление активами и пассивами | ALM/risk income owner |

ЕТС curve tenors:

| Tenor | Meaning |
|---|---|
| `1D` | 1 day |
| `7D` | 7 days |
| `1M` | 1 month |
| `3M` | 3 months |
| `6M` | 6 months |
| `9M` | 9 months |
| `1Y` | 1 year |
| `2Y` | 2 years |
| `3Y` | 3 years |
| `5Y` | 5 years |
| `7Y` | 7 years |
| `7Y+` | more than 7 years |

Supported ЕТС currencies:

- `KZT`;
- `USD`;
- `EUR`;
- `RUB`;
- `GBP`.

ЕТС is interpolated linearly between curve tenors based on remaining maturity in days.

Initial FTP logic:

| Metric | Owner | Formula |
|---|---|---|
| `ЧПДА` | Lending business block | Customer interest income on assets minus transfer expense |
| `ЧПДП` | Funding business block | Transfer income minus customer interest expense on liabilities |
| `ЧПДР` | `UALM` | Transfer expenses of asset blocks minus transfer income of liability blocks |

Sign convention:

- asset customer interest is positive;
- liability customer interest is negative;
- asset ЕТС interest is positive and treated as transfer expense for the lending block;
- liability ЕТС interest is negative and treated as transfer income for the funding block;
- `UALM.chpdr` is the sum of signed transfer interest across business blocks.

## Capital Adequacy, LCR, NSFR v0

The current implementation is a transparent management prototype. It is not yet the final
NBK regulatory methodology.

Inputs are set at deal level:

| Field | Meaning |
|---|---|
| `risk_weight` | Capital adequacy risk weight |
| `hqla_haircut` | HQLA haircut; `1.00` means not eligible as HQLA |
| `lcr_inflow_rate` | 30-day stressed inflow rate |
| `lcr_outflow_rate` | 30-day stressed outflow rate |
| `nsfr_asf_factor` | Available stable funding factor |
| `nsfr_rsf_factor` | Required stable funding factor |

Formulas:

```text
RWA = sum(asset principal * risk_weight)
Capital adequacy = capital / RWA

HQLA = sum(asset principal * (1 - hqla_haircut))
LCR outflows = sum(liability principal * lcr_outflow_rate)
LCR inflows = sum(asset principal * lcr_inflow_rate)
Capped inflows = min(LCR inflows, 75% * LCR outflows)
Net cash outflows = LCR outflows - capped inflows
LCR = HQLA / Net cash outflows

ASF = capital + sum(liability principal * nsfr_asf_factor)
RSF = sum(asset principal * nsfr_rsf_factor)
NSFR = ASF / RSF
```
