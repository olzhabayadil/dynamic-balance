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

Initial FTP logic:

| Metric | Owner | Formula |
|---|---|---|
| `ЧПДА` | Lending business block | Customer interest income on assets minus transfer expense |
| `ЧПДП` | Funding business block | Transfer income minus customer interest expense on liabilities |
| `ЧПДР` | `UALM` | Transfer expenses of asset blocks minus transfer income of liability blocks |

Sign convention:

- asset customer interest is positive;
- liability customer interest is negative;
- asset FTP interest is positive and treated as transfer expense for the lending block;
- liability FTP interest is negative and treated as transfer income for the funding block;
- `UALM.chpdr` is the sum of signed transfer interest across business blocks.
