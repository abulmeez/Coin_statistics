# Comprehensive Analysis of Even Flips

## Standard Deviation Convergence
- Empirical function: σ = 0.5006n^-0.5005
- Theoretical function: σ = 1/(2√n)
- MAPE: 0.16%
- RMSE: 0.0002
- Power law exponent deviation: 0.0005 from theoretical -0.5

## Exact 50% Probability
- Empirical function: P(50%) = 0.4086e^(-0.0856n) + 0.0972
- Theoretical function: P(50%) = C(n,n/2) * (1/2)^n
- MAPE: 0.64%
- RMSE: 0.0010

## Key Findings
1. Standard Deviation:
   - The empirical power law exponent (-0.5005) closely matches
     the theoretical -0.5, with only small deviation
   - The empirical coefficient (0.5006) is very close to
     the theoretical 0.5

2. Exact 50% Probability:
   - The empirical probability follows an exponential decay plus offset
   - This matches the theoretical prediction that exact 50% becomes
     increasingly rare with more flips
   - The decay rate (0.0856) indicates how quickly the
     probability approaches the asymptotic value
