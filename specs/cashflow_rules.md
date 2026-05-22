# Cash-Flow Rules

## Sign Convention

Cash flows are signed from the bank liquidity perspective:

- asset inflows are positive;
- liability outflows are negative.

## Fixed-Rate Bullet Instruments

Interest amount:

```text
interest = principal * annual_rate * days / 365
```

Where:

- `days` is calculated on ACT/365;
- cash-flow amounts are rounded to 2 decimal places;
- principal is paid only on `maturity_date`;
- interest dates depend on `payment_frequency`.

## Payment Dates

| Frequency | Rule |
|---|---|
| `at_maturity` | one payment on maturity date |
| `monthly` | monthly anniversaries from start date, plus maturity date |
| `quarterly` | quarterly anniversaries from start date, plus maturity date |

If an anniversary day does not exist in a month, the payment date uses the last day of that month.
