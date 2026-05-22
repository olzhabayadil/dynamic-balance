# Acceptance Tests

## Golden Dataset 1: Fixed-Rate Bullet Deals

Source file:

```text
sample_data/fixed_rate_deals.csv
```

Acceptance rules:

- all rows load into normalized `Deal` models;
- fixed-rate loan cash flows are positive;
- fixed-rate deposit cash flows are negative;
- ACT/365 interest is rounded to 2 decimals;
- maturity cash flow includes principal;
- interim monthly and quarterly cash flows include interest only.

Current automated test file:

```text
tests/test_fixed_rate_cashflows.py
```

Portfolio composition:

| Segment | Count | Examples |
|---|---:|---|
| Retail loans | 3 | mortgage-like, car loan, cash loan |
| SME/corporate loans | 3 | working capital, investment, trade finance |
| Retail deposits | 3 | standard retail, VIP term deposit |
| SME/corporate deposits | 3 | KZT/USD/EUR corporate term funding |

Currencies:

- KZT;
- USD;
- EUR.
