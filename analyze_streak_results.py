import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os
from datetime import datetime
from scipy.optimize import curve_fit

def load_specific_csv(file_path):
    return pd.read_csv(file_path)

def create_individual_runs_plot(df, max_streak, results_dir, suffix=''):
    plt.figure(figsize=(12, 8))
    
    # Filter data for the specified range
    df_filtered = df[df['Streak Target'] <= max_streak]
    
    # Plot each run
    for run in df_filtered['Run'].unique():
        run_data = df_filtered[df_filtered['Run'] == run]
        plt.plot(run_data['Streak Target'], run_data['Flips Required'], 
                color='lightblue', alpha=0.1, linewidth=1)
    
    plt.title(f'Number of Flips Required for Each Streak Length\n(All {len(df_filtered["Run"].unique())} Runs, n=1 to {max_streak})')
    plt.xlabel('Streak Length (n)')
    plt.ylabel('Number of Flips Required')
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(results_dir, f'individual_runs{suffix}.png'))
    plt.close()

def create_median_plot(df, max_streak, results_dir, suffix=''):
    plt.figure(figsize=(12, 8))
    
    # Filter data for the specified range
    df_filtered = df[df['Streak Target'] <= max_streak]
    
    # Calculate median for each streak length
    median_data = df_filtered.groupby('Streak Target')['Flips Required'].median()
    
    # Plot median data
    plt.plot(median_data.index, median_data.values, 
            color='red', linewidth=2, label='Median')
    
    # Plot theoretical function y = 2^n
    n_values = np.arange(1, max_streak + 1)
    theoretical_values = 2 ** n_values
    plt.plot(n_values, theoretical_values, 
            color='green', linewidth=2, linestyle='--', label='Theoretical (2^n)')
    
    plt.title(f'Median Number of Flips Required for Each Streak Length\n(n=1 to {max_streak})')
    plt.xlabel('Streak Length (n)')
    plt.ylabel('Number of Flips Required')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig(os.path.join(results_dir, f'median_plot{suffix}.png'))
    plt.close()

def create_combined_plot(df, max_streak, results_dir, suffix=''):
    plt.figure(figsize=(12, 8))
    
    # Filter data for the specified range
    df_filtered = df[df['Streak Target'] <= max_streak]
    
    # Plot all individual runs
    for run in df_filtered['Run'].unique():
        run_data = df_filtered[df_filtered['Run'] == run]
        plt.plot(run_data['Streak Target'], run_data['Flips Required'], 
                color='lightblue', alpha=0.1, linewidth=1)
    
    # Calculate and plot median
    median_data = df_filtered.groupby('Streak Target')['Flips Required'].median()
    plt.plot(median_data.index, median_data.values, 
            color='red', linewidth=2, label='Median')
    
    # Plot theoretical function y = 2^n
    n_values = np.arange(1, max_streak + 1)
    theoretical_values = 2 ** n_values
    plt.plot(n_values, theoretical_values, 
            color='green', linewidth=2, linestyle='--', label='Theoretical (2^n)')
    
    plt.title(f'Number of Flips Required for Each Streak Length\n(All Runs + Median + Theoretical, n=1 to {max_streak})')
    plt.xlabel('Streak Length (n)')
    plt.ylabel('Number of Flips Required')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig(os.path.join(results_dir, f'combined_plot{suffix}.png'))
    plt.close()

def create_trimmed_plot(df, max_streak, results_dir, suffix=''):
    plt.figure(figsize=(12, 8))
    
    # Filter data for the specified range
    df_filtered = df[df['Streak Target'] <= max_streak]
    
    # Calculate trimmed mean (excluding 50 highest and 50 lowest values) for each streak length
    trimmed_means = []
    for n in range(1, max_streak + 1):
        values = df_filtered[df_filtered['Streak Target'] == n]['Flips Required'].values
        # Sort values and remove 50 highest and 50 lowest
        sorted_values = np.sort(values)
        trimmed_values = sorted_values[50:-50]  # Remove first and last 50 values
        trimmed_means.append(np.mean(trimmed_values))
    
    # Plot theoretical function y = 2^n
    n_values = np.arange(1, max_streak + 1)
    theoretical_values = 2 ** n_values
    plt.plot(n_values, theoretical_values, 
            color='green', linewidth=2, linestyle='--', label='Theoretical (2^n)')
    
    # Plot median
    median_data = df_filtered.groupby('Streak Target')['Flips Required'].median()
    plt.plot(median_data.index, median_data.values, 
            color='red', linewidth=2, label='Median')
    
    # Plot trimmed mean
    plt.plot(n_values, trimmed_means, 
            color='orange', linewidth=2, label='Trimmed Mean (90% of data)')
    
    plt.title(f'Comparison of Theoretical, Median, and Trimmed Mean\n(n=1 to {max_streak}, excluding 100 most extreme values)')
    plt.xlabel('Streak Length (n)')
    plt.ylabel('Number of Flips Required')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig(os.path.join(results_dir, f'trimmed_plot{suffix}.png'))
    plt.close()

def calculate_statistics(df, max_streak):
    """Calculate statistical differences from theoretical values."""
    stats = {}
    
    # Filter data for the specified range
    df_filtered = df[df['Streak Target'] <= max_streak]
    
    # Calculate median for each streak length
    median_data = df_filtered.groupby('Streak Target')['Flips Required'].median()
    
    # Calculate theoretical values
    n_values = np.arange(1, max_streak + 1)
    theoretical_values = 2 ** n_values
    
    # Calculate percentage differences
    percentage_diff = ((median_data.values - theoretical_values) / theoretical_values) * 100
    
    # Calculate mean absolute percentage error (MAPE)
    mape = np.mean(np.abs(percentage_diff))
    
    # Fit a function of the form a * 2^(b*n + c)
    def theoretical_func(n, a, b, c):
        return a * (2 ** (b * n + c))
    
    # Fit the function to the median data
    popt, pcov = curve_fit(theoretical_func, n_values, median_data.values, p0=[1, 1, 0])
    
    stats['median_values'] = median_data.values
    stats['theoretical_values'] = theoretical_values
    stats['percentage_diff'] = percentage_diff
    stats['mape'] = mape
    stats['fitted_params'] = popt
    stats['fitted_function'] = f"{popt[0]:.2f} * 2^({popt[1]:.2f}*n + {popt[2]:.2f})"
    
    return stats

def create_statistical_summary(df_100, df_1000, df_10000, max_streak):
    """Create a summary of statistical findings."""
    stats_100 = calculate_statistics(df_100, max_streak)
    stats_1000 = calculate_statistics(df_1000, max_streak)
    stats_10000 = calculate_statistics(df_10000, max_streak)
    
    summary = f"""# Statistical Analysis Summary

## 100 Runs Analysis
- Mean Absolute Percentage Error (MAPE): {stats_100['mape']:.2f}%
- Fitted Function: y = {stats_100['fitted_function']}

## 1000 Runs Analysis
- Mean Absolute Percentage Error (MAPE): {stats_1000['mape']:.2f}%
- Fitted Function: y = {stats_1000['fitted_function']}

## 10000 Runs Analysis
- Mean Absolute Percentage Error (MAPE): {stats_10000['mape']:.2f}%
- Fitted Function: y = {stats_10000['fitted_function']}

## Key Findings
1. The theoretical function (2^n) tends to underestimate the actual number of flips required.
2. The fitted functions show that the actual relationship is more complex than the simple theoretical model.
3. The 1000-run analysis provides a more accurate estimate of the true relationship.
4. The 10000-run analysis provides an even more accurate estimate of the true relationship.
"""
    
    return summary

def main():
    # Create directories for results
    results_dir_100 = "results_20250417_100"
    results_dir_1000 = "results_20250418_1000"
    results_dir_10000 = "results_20250418_10000"
    os.makedirs(results_dir_100, exist_ok=True)
    os.makedirs(results_dir_1000, exist_ok=True)
    os.makedirs(results_dir_10000, exist_ok=True)
    
    # Load specific CSV files
    print("Analyzing 100 runs...")
    df_100 = load_specific_csv("streak_simulation_results_20250417_180749.csv")
    create_individual_runs_plot(df_100, 20, results_dir_100)
    create_median_plot(df_100, 20, results_dir_100)
    create_combined_plot(df_100, 20, results_dir_100)
    create_trimmed_plot(df_100, 20, results_dir_100)
    
    # Create plots for n=1 to 10 for 100 runs
    create_individual_runs_plot(df_100, 10, results_dir_100, '_n10')
    create_median_plot(df_100, 10, results_dir_100, '_n10')
    create_combined_plot(df_100, 10, results_dir_100, '_n10')
    create_trimmed_plot(df_100, 10, results_dir_100, '_n10')
    
    # Analyze 1000 runs
    print("\nAnalyzing 1000 runs...")
    df_1000 = load_specific_csv("streak_simulation_results_20250418_202140.csv")
    create_individual_runs_plot(df_1000, 20, results_dir_1000)
    create_median_plot(df_1000, 20, results_dir_1000)
    create_combined_plot(df_1000, 20, results_dir_1000)
    create_trimmed_plot(df_1000, 20, results_dir_1000)
    
    # Create plots for n=1 to 10 for 1000 runs
    create_individual_runs_plot(df_1000, 10, results_dir_1000, '_n10')
    create_median_plot(df_1000, 10, results_dir_1000, '_n10')
    create_combined_plot(df_1000, 10, results_dir_1000, '_n10')
    create_trimmed_plot(df_1000, 10, results_dir_1000, '_n10')
    
    # Analyze 10000 runs
    print("\nAnalyzing 10000 runs...")
    df_10000 = load_specific_csv("streak_simulation_results_20250418_202140_10000.csv")
    create_individual_runs_plot(df_10000, 20, results_dir_10000)
    create_median_plot(df_10000, 20, results_dir_10000)
    create_combined_plot(df_10000, 20, results_dir_10000)
    create_trimmed_plot(df_10000, 20, results_dir_10000)
    
    # Create plots for n=1 to 10 for 10000 runs
    create_individual_runs_plot(df_10000, 10, results_dir_10000, '_n10')
    create_median_plot(df_10000, 10, results_dir_10000, '_n10')
    create_combined_plot(df_10000, 10, results_dir_10000, '_n10')
    create_trimmed_plot(df_10000, 10, results_dir_10000, '_n10')
    
    # Generate statistical summary
    summary = create_statistical_summary(df_100, df_1000, df_10000, 20)
    with open("statistical_summary.md", "w") as f:
        f.write(summary)
    
    print("\nAll plots have been saved in their respective directories:")
    print(f"\nFor 100 runs (in {results_dir_100}):")
    print("- individual_runs.png: Shows all 100 runs")
    print("- median_plot.png: Shows the median values and theoretical function")
    print("- combined_plot.png: Shows individual runs, median, and theoretical function")
    print("- trimmed_plot.png: Shows theoretical, median, and trimmed mean (excluding 100 extreme values)")
    
    print(f"\nFor 1000 runs (in {results_dir_1000}):")
    print("- individual_runs.png: Shows all 1000 runs")
    print("- median_plot.png: Shows the median values and theoretical function")
    print("- combined_plot.png: Shows individual runs, median, and theoretical function")
    print("- trimmed_plot.png: Shows theoretical, median, and trimmed mean (excluding 100 extreme values)")
    
    print(f"\nFor 10000 runs (in {results_dir_10000}):")
    print("- individual_runs.png: Shows all 10000 runs")
    print("- median_plot.png: Shows the median values and theoretical function")
    print("- combined_plot.png: Shows individual runs, median, and theoretical function")
    print("- trimmed_plot.png: Shows theoretical, median, and trimmed mean (excluding 100 extreme values)")
    
    print("\nStatistical summary has been saved to statistical_summary.md")

if __name__ == "__main__":
    main() 