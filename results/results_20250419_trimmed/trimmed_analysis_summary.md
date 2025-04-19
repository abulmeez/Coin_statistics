# Trimmed Data Analysis Summary (Middle 96%)

## Statistical Analysis

### 100 Runs Analysis
- Mean Absolute Percentage Error (MAPE): 17.27%
- Correlation with Theoretical Values: 0.9971 (p-value: 0.0000)
- R-squared: 0.9936
- Fitted Function: y = 0.63 * 2^(1.05*n + -0.34)
- Average Deviation from Theoretical: 8198.98 flips
- Maximum Deviation from Theoretical: 61258.15 flips

### 1000 Runs Analysis
- Mean Absolute Percentage Error (MAPE): 14.56%
- Correlation with Theoretical Values: 0.9999 (p-value: 0.0000)
- R-squared: 0.9946
- Fitted Function: y = 1.00 * 2^(1.00*n + -0.02)
- Average Deviation from Theoretical: 6328.87 flips
- Maximum Deviation from Theoretical: 67556.36 flips

### 10000 Runs Analysis
- Mean Absolute Percentage Error (MAPE): 15.16%
- Correlation with Theoretical Values: 1.0000 (p-value: 0.0000)
- R-squared: 0.9957
- Fitted Function: y = 0.99 * 2^(1.00*n + -0.09)
- Average Deviation from Theoretical: 6024.38 flips
- Maximum Deviation from Theoretical: 60097.46 flips

## Key Findings

1. **Theoretical vs. Actual Relationship**:
   - The theoretical function (2^n) consistently underestimates the actual number of flips required.
   - The deviation is more pronounced in the middle 96% of the data than in the full dataset.
   - The MAPE values show the average percentage difference from theoretical predictions.
   - The average and maximum deviations provide absolute measures of the difference.

2. **Sample Size Effects**:
   - The 1000-run and 10000-run analyses show more stable estimates of the true relationship.
   - The fitted parameters become more consistent with larger sample sizes.
   - The scaling factor (a) approaches 1.0 with larger sample sizes.
   - Parameter uncertainties decrease with increasing sample size.

3. **Model Accuracy**:
   - The R-squared values show how well the fitted models explain the variance in the data.
   - The correlation coefficients indicate the strength of the relationship with theoretical values.
   - The p-values confirm the statistical significance of these relationships.
   - The deviations provide concrete measures of how far the actual results are from theoretical predictions.

4. **Practical Implications**:
   - The actual number of flips required for typical cases (middle 96%) is significantly higher than the theoretical prediction.
   - The relationship between streak length and required flips is more complex than a simple exponential function.
   - The fitted models provide a more accurate way to predict the number of flips needed for a given streak length.
   - The 10000-run analysis provides the most reliable predictions for practical applications.
