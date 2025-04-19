# Coin Flip Streak Analysis

This project analyzes the number of coin flips required to achieve streaks of heads of various lengths. It includes both theoretical analysis and Monte Carlo simulations to understand the relationship between streak length and required flips.

## Project Structure

The project is organized into date-based directories for each set of simulations:

```
Coin_statistics/
├── longest_streak_finder.py    # Main simulation script
├── analyze_streak_results.py   # Analysis and visualization script
├── results_YYYYMMDD_100/      # Results directory for 100 runs
│   ├── streak_simulation_results_YYYYMMDD_HHMMSS.csv
│   ├── individual_runs.png
│   ├── median_plot.png
│   ├── combined_plot.png
│   ├── trimmed_plot.png
│   ├── individual_runs_n10.png
│   ├── median_plot_n10.png
│   ├── combined_plot_n10.png
│   └── trimmed_plot_n10.png
└── results_YYYYMMDD_1000/     # Results directory for 1000 runs
    ├── streak_simulation_results_YYYYMMDD_HHMMSS.csv
    ├── individual_runs.png
    ├── median_plot.png
    ├── combined_plot.png
    ├── trimmed_plot.png
    ├── individual_runs_n10.png
    ├── median_plot_n10.png
    ├── combined_plot_n10.png
    └── trimmed_plot_n10.png
```

## How to Use

1. Run the simulation script to generate new results:
   ```bash
   python longest_streak_finder.py
   ```
   This will create two new directories:
   - `results_YYYYMMDD_100/` for 100 simulation runs
   - `results_YYYYMMDD_1000/` for 1000 simulation runs

2. Analyze the results and generate visualizations:
   ```bash
   python analyze_streak_results.py
   ```
   This will create various plots in each results directory and generate a statistical summary.

## Analysis Details

The analysis includes:

1. **Individual Runs Plot**: Shows the number of flips required for each streak length across all simulation runs.
2. **Median Plot**: Compares the median number of flips required with the theoretical function (2^n).
3. **Combined Plot**: Shows individual runs, median values, and theoretical function together.
4. **Trimmed Plot**: Shows theoretical, median, and trimmed mean values (excluding extreme values).

Each plot is generated for two ranges:
- n=1 to 20 (full range)
- n=1 to 10 (zoomed in view)

## Statistical Analysis

The analysis includes several statistical measures:

1. **Mean Absolute Percentage Error (MAPE)**: Measures the average percentage difference between the theoretical and actual values.
2. **Fitted Functions**: The actual relationship is fitted to a function of the form a * 2^(b*n + c), which provides a more accurate model than the simple theoretical prediction.

### Key Statistical Findings

1. **Theoretical vs. Actual Relationship**:
   - The theoretical function (2^n) consistently underestimates the actual number of flips required.
   - For 100 runs, the MAPE is 33.95%, indicating significant deviation from the theoretical model.
   - For 1000 runs, the MAPE is 36.24%, showing that the deviation persists with larger sample sizes.

2. **Fitted Models**:
   - For 100 runs: y = 0.47 * 2^(1.06*n - 0.72)
   - For 1000 runs: y = 0.80 * 2^(0.97*n + 0.46)
   - These models show that the actual relationship requires:
     - A scaling factor (a) to adjust the base magnitude
     - A non-linear exponent (b) to account for the changing rate of increase
     - An offset (c) to adjust for the initial conditions

3. **Sample Size Effects**:
   - The 1000-run analysis provides more stable estimates of the true relationship.
   - The fitted parameters are more consistent in the larger sample size.
   - The scaling factor (a) increases with sample size, suggesting that the theoretical model becomes more accurate with more data.

4. **Practical Implications**:
   - The actual number of flips required for longer streaks is significantly higher than the theoretical prediction.
   - The relationship between streak length and required flips is more complex than a simple exponential function.
   - The fitted models provide a more accurate way to predict the number of flips needed for a given streak length.

## Theoretical Background

The theoretical expectation for the number of flips required to achieve a streak of n heads is approximately 2^(n+1) - 2. However, our analysis shows that this is an oversimplification. The actual relationship is better modeled by a function of the form a * 2^(b*n + c), where:

- a: A scaling factor that accounts for the base magnitude of the relationship
- b: A non-linear exponent that captures the changing rate of increase
- c: An offset that adjusts for initial conditions

This more complex model better captures the true nature of streak probabilities in coin flips.

## Dependencies

- Python 3.x
- pandas
- numpy
- matplotlib
- scipy 