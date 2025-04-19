# Statistical Analysis Summary

## 100 Runs Analysis
- Mean Absolute Percentage Error (MAPE): 35.48%
- Fitted Function: y = 0.98 * 2^(0.95*n + 0.46)

## 1000 Runs Analysis
- Mean Absolute Percentage Error (MAPE): 34.80%
- Fitted Function: y = 0.65 * 2^(0.98*n + 0.42)

## 10000 Runs Analysis
- Mean Absolute Percentage Error (MAPE): 35.62%
- Fitted Function: y = 0.67 * 2^(0.99*n + 0.18)

## Key Findings
1. The theoretical function (2^n) tends to underestimate the actual number of flips required.
2. The fitted functions show that the actual relationship is more complex than the simple theoretical model.
3. The relationship between streak length and required flips is better modeled by a function of the form a * 2^(b*n + c).
4. The 10000-run analysis provides the most reliable predictions for practical applications.
