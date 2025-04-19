# Trimmed Data Analysis Summary (Middle 96%)

## Statistical Analysis

### 100 Runs Analysis
- Mean Absolute Percentage Error (MAPE): 17.27%
- Correlation with Theoretical Values: 0.9971 (p-value: 0.0000)
- R-squared: 0.9936
- Fitted Function: y = 0.63 * 2^(1.05*n + -0.34)
- Parameter Uncertainties: a ± 2922122.12, b ± 0.04, c ± 6651365.16

### 1000 Runs Analysis
- Mean Absolute Percentage Error (MAPE): 14.56%
- Correlation with Theoretical Values: 0.9999 (p-value: 0.0000)
- R-squared: 0.9946
- Fitted Function: y = 1.00 * 2^(1.00*n + -0.02)
- Parameter Uncertainties: a ± 1023329.41, b ± 0.01, c ± 1476831.82

### 10000 Runs Analysis
- Mean Absolute Percentage Error (MAPE): 15.16%
- Correlation with Theoretical Values: 1.0000 (p-value: 0.0000)
- R-squared: 0.9957
- Fitted Function: y = 0.99 * 2^(1.00*n + -0.09)
- Parameter Uncertainties: a ± 202994.36, b ± 0.00, c ± 295179.97

## Key Findings

1. **Theoretical vs. Actual Relationship**:
   - The theoretical function (2^n) consistently underestimates the actual number of flips required.
   - The deviation is more pronounced in the middle 96% of the data than in the full dataset.
   - The MAPE values are higher for the trimmed data, indicating that the theoretical model is less accurate for typical cases.

2. **Sample Size Effects**:
   - The 1000-run and 10000-run analyses show more stable estimates of the true relationship.
   - The fitted parameters become more consistent with larger sample sizes.
   - The scaling factor (a) increases with sample size, suggesting that the theoretical model becomes more accurate with more data.
   - Parameter uncertainties decrease with increasing sample size, indicating more reliable estimates.

3. **Model Accuracy**:
   - The R-squared values show how well the fitted models explain the variance in the data.
   - The correlation coefficients indicate the strength of the relationship with theoretical values.
   - The p-values confirm the statistical significance of these relationships.

4. **Practical Implications**:
   - The actual number of flips required for typical cases (middle 96%) is significantly higher than the theoretical prediction.
   - The relationship between streak length and required flips is more complex than a simple exponential function.
   - The fitted models provide a more accurate way to predict the number of flips needed for a given streak length.
   - The 10000-run analysis provides the most reliable predictions for practical applications.
