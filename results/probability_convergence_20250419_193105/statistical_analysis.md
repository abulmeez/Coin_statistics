# Statistical Analysis of Convergence

## Standard Deviation Convergence
- MAPE: 0.18%
- RMSE: 0.0002
- Fitted power law: σ = 0.5002 * n^(-0.5002)
- Theoretical model: σ = 1/(2√n)

## Exact 50% Probability
- MAPE: 0.64%
- RMSE: 0.0007
- Theoretical model: P(exactly 50%) = C(n,n/2) * (1/2)^n

## Key Findings
1. Standard Deviation Convergence:
   - The empirical standard deviation follows a power law with exponent -0.5002
   - This is close to the theoretical -0.5 exponent from the 1/2√n relationship

2. Exact 50% Probability:
   - The probability of getting exactly 50% heads decreases with the number of flips
   - This matches the theoretical prediction that it becomes increasingly unlikely
     to get exactly half heads as the number of flips increases
