"""
Analyze how the probability of heads converges to 0.5 as the number of flips increases.

This script simulates multiple coin flip sequences and calculates the proportion of heads
for each sequence, showing how the distribution of probabilities narrows around 0.5
as the number of flips increases.
"""

import numpy as np
import pandas as pd
from datetime import datetime
import os
import argparse
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def run_convergence_analysis(runs=100000, max_flips=100):
    """
    Run the convergence analysis for different flip counts.
    
    Args:
        runs (int): Number of simulations to run
        max_flips (int): Maximum number of flips
        
    Returns:
        pd.DataFrame: Results of all simulations
    """
    results = []
    flip_counts = range(2, max_flips + 1)
    
    # Print progress header
    print("\nRunning simulations:")
    print("-" * 50)
    
    for flip_count in flip_counts:
        print(f"Processing {flip_count} flips...", end='\r')
        
        # Generate random flips (0 for tails, 1 for heads)
        flips = np.random.randint(0, 2, size=(runs, flip_count))
        
        # Calculate probability (proportion of heads) for each run
        probabilities = np.sum(flips, axis=1) / flip_count
        
        # Store results
        for run_idx in range(runs):
            results.append({
                'Run': run_idx + 1,
                'Flips': flip_count,
                'Probability': probabilities[run_idx]
            })
    
    print("\nSimulations complete!")
    return pd.DataFrame(results)

def calculate_statistics(df):
    """
    Calculate statistics for each flip count.
    
    Args:
        df (pd.DataFrame): Results dataframe
        
    Returns:
        pd.DataFrame: Statistical summary
    """
    stats = df.groupby('Flips').agg({
        'Probability': [
            'mean',
            'std',
            lambda x: np.percentile(x, 25),  # Q1
            'median',
            lambda x: np.percentile(x, 75),  # Q3
            'min',
            'max',
            'count'
        ]
    }).reset_index()
    
    # Flatten column names
    stats.columns = [
        'Flips', 'Mean', 'Std', 'Q1', 'Median', 'Q3', 'Min', 'Max', 'Count'
    ]
    
    # Ensure Flips is integer type
    stats['Flips'] = stats['Flips'].astype(int)
    
    # Calculate distance from 0.5
    stats['Mean_Distance_from_0.5'] = abs(stats['Mean'] - 0.5)
    stats['Max_Distance_from_0.5'] = np.maximum(
        abs(stats['Min'] - 0.5),
        abs(stats['Max'] - 0.5)
    )
    
    return stats

def save_results(df, stats):
    """
    Save results to CSV files in the results directory.
    
    Args:
        df (pd.DataFrame): Full results dataframe
        stats (pd.DataFrame): Statistical summary dataframe
        
    Returns:
        str: Path to results directory
    """
    # Create main results directory if it doesn't exist
    os.makedirs('results', exist_ok=True)
    
    # Create timestamped subdirectory for this analysis
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_dir = os.path.join('results', f'probability_convergence_{timestamp}')
    os.makedirs(results_dir, exist_ok=True)
    
    # Save full results
    df.to_csv(os.path.join(results_dir, 'convergence_full.csv'), index=False)
    
    # Save statistics
    stats.to_csv(os.path.join(results_dir, 'convergence_stats.csv'), index=False)
    
    return results_dir

def print_statistics(stats):
    """
    Print statistical summary.
    
    Args:
        stats (pd.DataFrame): Statistical summary dataframe
    """
    print("\nProbability Convergence Statistics:")
    print("-" * 100)
    print(f"{'Flips':>6} | {'Mean':>8} | {'Std':>8} | {'Median':>8} | "
          f"{'Q1':>8} | {'Q3':>8} | {'Min':>8} | {'Max':>8} | {'Dist':>8}")
    print("-" * 100)
    
    for _, row in stats.iterrows():
        print(f"{int(row['Flips']):6} | {row['Mean']:8.4f} | {row['Std']:8.4f} | "
              f"{row['Median']:8.4f} | {row['Q1']:8.4f} | {row['Q3']:8.4f} | "
              f"{row['Min']:8.4f} | {row['Max']:8.4f} | {row['Mean_Distance_from_0.5']:8.4f}")

def theoretical_probability(n):
    """
    Calculate theoretical probability of getting exactly 50% heads in n flips.
    
    Args:
        n (int): Number of flips
        
    Returns:
        float: Probability of exactly 50% heads
    """
    if n % 2 != 0:  # Odd number of flips can't give exactly 50%
        return 0
    k = n // 2  # Number of heads needed for 50%
    return math.comb(n, k) * (0.5 ** n)

def theoretical_convergence(n):
    """
    Calculate theoretical standard deviation for n flips.
    
    Args:
        n (int): Number of flips
        
    Returns:
        float: Expected standard deviation
    """
    return 1 / (2 * np.sqrt(n))

def create_empirical_exact_plot(stats_df, results_df, results_dir):
    """
    Create plot showing empirical probability of getting exactly p = 0.5
    """
    plt.figure(figsize=(10, 6))
    flips = stats_df['Flips']
    
    # Calculate proportion of runs with exactly 0.5
    exact_50_percent = []
    for flip_count in flips:
        exact_50_percent.append(
            len(results_df[(results_df['Flips'] == flip_count) & 
                         (results_df['Probability'] == 0.5)]) / args.runs
        )
    
    plt.plot(flips, exact_50_percent, 'b-', linewidth=2, label='Empirical P(50%)')
    plt.xlabel('Number of Flips')
    plt.ylabel('Probability of Exactly 50% Heads')
    plt.title('Empirical Probability of Getting Exactly 50% Heads')
    plt.grid(True)
    plt.legend()
    
    plt.savefig(os.path.join(results_dir, 'empirical_exact_probability.png'))
    plt.close()
    
    return exact_50_percent

def create_empirical_convergence_plot(stats_df, results_dir):
    """
    Create plot showing empirical standard deviation convergence
    """
    plt.figure(figsize=(10, 6))
    flips = stats_df['Flips']
    
    plt.plot(flips, stats_df['Std'], 'b-', linewidth=2, label='Empirical σ')
    plt.xlabel('Number of Flips')
    plt.ylabel('Standard Deviation')
    plt.title('Empirical Convergence of Probability')
    plt.grid(True)
    plt.legend()
    
    plt.savefig(os.path.join(results_dir, 'empirical_convergence.png'))
    plt.close()

def create_even_flips_exact_plot(stats_df, results_df, results_dir):
    """
    Create plot showing empirical probability of getting exactly p = 0.5,
    only for even numbers of flips (since odd numbers cannot achieve exactly 50%).
    """
    plt.figure(figsize=(10, 6))
    
    # Filter for even numbers of flips
    even_flips = stats_df[stats_df['Flips'] % 2 == 0]['Flips']
    
    # Calculate proportion of runs with exactly 0.5 for even flips
    exact_50_percent_even = []
    for flip_count in even_flips:
        exact_50_percent_even.append(
            len(results_df[(results_df['Flips'] == flip_count) & 
                         (results_df['Probability'] == 0.5)]) / args.runs
        )
    
    # Empirical probability for even flips
    plt.plot(even_flips, exact_50_percent_even, 'g-', linewidth=2, 
             label='Empirical P(50%) - Even Flips')
    
    # Theoretical probability for even flips
    theoretical_exact_even = [theoretical_probability(n) for n in even_flips]
    plt.plot(even_flips, theoretical_exact_even, 'r--', linewidth=2,
             label='Theoretical P(50%) - Even Flips')
    
    plt.xlabel('Number of Flips (Even Only)')
    plt.ylabel('Probability of Exactly 50% Heads')
    plt.title('Probability of Exactly 50% Heads (Even Flips Only)')
    plt.grid(True)
    plt.legend()
    
    plt.savefig(os.path.join(results_dir, 'even_flips_exact_probability.png'))
    plt.close()
    
    return exact_50_percent_even, even_flips

def create_combined_theoretical_plot(stats_df, exact_50_percent, results_dir):
    """
    Create combined plot with both empirical and theoretical results
    """
    plt.figure(figsize=(12, 10))
    flips = stats_df['Flips']
    
    # Plot 1: Convergence
    plt.subplot(2, 1, 1)
    
    # Empirical standard deviation
    plt.plot(flips, stats_df['Std'], 'b-', linewidth=2, label='Empirical σ')
    
    # Theoretical convergence
    theoretical_std = [theoretical_convergence(n) for n in flips]
    plt.plot(flips, theoretical_std, 'r--', linewidth=2, label='Theoretical σ (1/2√n)')
    
    plt.xlabel('Number of Flips')
    plt.ylabel('Standard Deviation')
    plt.title('Convergence of Probability: Empirical vs Theoretical')
    plt.legend()
    plt.grid(True)
    
    # Plot 2: Exact 50% Probability
    plt.subplot(2, 1, 2)
    
    # Empirical probability of exactly 50%
    plt.plot(flips, exact_50_percent, 'b-', linewidth=2, label='Empirical P(50%)')
    
    # Theoretical probability of exactly 50%
    theoretical_exact = [theoretical_probability(n) for n in flips]
    plt.plot(flips, theoretical_exact, 'r--', linewidth=2, label='Theoretical P(50%)')
    
    plt.xlabel('Number of Flips')
    plt.ylabel('Probability of Exactly 50% Heads')
    plt.title('Probability of Exactly 50% Heads: Empirical vs Theoretical')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'combined_analysis.png'))
    plt.close()

def calculate_fit_statistics(stats_df, results_dir):
    """
    Calculate and save statistical analysis of the fits.
    
    Args:
        stats_df (pd.DataFrame): Statistical summary dataframe
        results_dir (str): Directory to save results
    """
    flips = stats_df['Flips'].values
    
    # Convergence Analysis
    empirical_std = stats_df['Std'].values
    theoretical_std = np.array([theoretical_convergence(n) for n in flips])
    
    # Calculate error metrics for convergence
    std_mape = np.mean(np.abs((empirical_std - theoretical_std) / theoretical_std)) * 100
    std_rmse = np.sqrt(np.mean((empirical_std - theoretical_std) ** 2))
    
    # Fit empirical standard deviation to power law
    def power_law(x, a, b):
        return a * (x ** b)
    
    popt_std, _ = curve_fit(power_law, flips, empirical_std)
    
    # Exact 50% Analysis
    empirical_exact = np.array([
        len(results_df[(results_df['Flips'] == f) & 
            (results_df['Probability'] == 0.5)]) / args.runs
        for f in flips
    ])
    theoretical_exact = np.array([theoretical_probability(n) for n in flips])
    
    # Calculate error metrics for exact 50%
    # Only include non-zero theoretical values to avoid division by zero
    mask = theoretical_exact != 0
    exact_mape = np.mean(np.abs(
        (empirical_exact[mask] - theoretical_exact[mask]) / theoretical_exact[mask]
    )) * 100
    exact_rmse = np.sqrt(np.mean((empirical_exact - theoretical_exact) ** 2))
    
    # Save statistical analysis
    with open(os.path.join(results_dir, 'statistical_analysis.md'), 'w') as f:
        f.write("# Statistical Analysis of Convergence\n\n")
        
        f.write("## Standard Deviation Convergence\n")
        f.write(f"- MAPE: {std_mape:.2f}%\n")
        f.write(f"- RMSE: {std_rmse:.4f}\n")
        f.write(f"- Fitted power law: σ = {popt_std[0]:.4f} * n^({popt_std[1]:.4f})\n")
        f.write(f"- Theoretical model: σ = 1/(2√n)\n\n")
        
        f.write("## Exact 50% Probability\n")
        f.write(f"- MAPE: {exact_mape:.2f}%\n")
        f.write(f"- RMSE: {exact_rmse:.4f}\n")
        f.write("- Theoretical model: P(exactly 50%) = C(n,n/2) * (1/2)^n\n\n")
        
        f.write("## Key Findings\n")
        f.write("1. Standard Deviation Convergence:\n")
        f.write(f"   - The empirical standard deviation follows a power law with exponent {popt_std[1]:.4f}\n")
        f.write("   - This is close to the theoretical -0.5 exponent from the 1/2√n relationship\n\n")
        
        f.write("2. Exact 50% Probability:\n")
        f.write("   - The probability of getting exactly 50% heads decreases with the number of flips\n")
        f.write("   - This matches the theoretical prediction that it becomes increasingly unlikely\n")
        f.write("     to get exactly half heads as the number of flips increases\n")

def fit_power_law(x, y):
    """
    Fit data to a power law function y = ax^b
    """
    def power_law(x, a, b):
        return a * (x ** b)
    
    popt, _ = curve_fit(power_law, x, y)
    return popt[0], popt[1]

def create_comprehensive_plot(stats_df, results_df, results_dir):
    """
    Create a comprehensive plot showing all measures for even flips only,
    including fitted functions and deviations from theoretical values.
    """
    # Filter for even numbers of flips
    even_stats = stats_df[stats_df['Flips'] % 2 == 0].copy()
    even_flips = even_stats['Flips'].values
    
    # Calculate empirical values
    empirical_std = even_stats['Std'].values
    empirical_exact = np.array([
        len(results_df[(results_df['Flips'] == f) & 
            (results_df['Probability'] == 0.5)]) / args.runs
        for f in even_flips
    ])
    
    # Calculate theoretical values
    theoretical_std = np.array([theoretical_convergence(n) for n in even_flips])
    theoretical_exact = np.array([theoretical_probability(n) for n in even_flips])
    
    # Fit functions
    # For standard deviation
    a_std, b_std = fit_power_law(even_flips, empirical_std)
    fitted_std = a_std * (even_flips ** b_std)
    
    # For exact probability (try exponential fit)
    def exp_decay(x, a, b, c):
        return a * np.exp(-b * x) + c
    
    popt_exact, _ = curve_fit(exp_decay, even_flips, empirical_exact, 
                             p0=[0.5, 0.1, 0], bounds=([0, 0, -1], [1, 1, 1]))
    fitted_exact = exp_decay(even_flips, *popt_exact)
    
    # Create plot
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Standard Deviation
    plt.subplot(2, 1, 1)
    plt.plot(even_flips, empirical_std, 'b-', linewidth=2, 
             label='Empirical σ')
    plt.plot(even_flips, theoretical_std, 'r--', linewidth=2, 
             label='Theoretical σ (1/2√n)')
    plt.plot(even_flips, fitted_std, 'g:', linewidth=2,
             label=f'Fitted σ ({a_std:.4f}n^{b_std:.4f})')
    
    plt.xlabel('Number of Flips (Even Only)')
    plt.ylabel('Standard Deviation')
    plt.title('Convergence Analysis (Even Flips Only)')
    plt.grid(True)
    plt.legend()
    
    # Plot 2: Exact Probability
    plt.subplot(2, 1, 2)
    plt.plot(even_flips, empirical_exact, 'b-', linewidth=2,
             label='Empirical P(50%)')
    plt.plot(even_flips, theoretical_exact, 'r--', linewidth=2,
             label='Theoretical P(50%)')
    plt.plot(even_flips, fitted_exact, 'g:', linewidth=2,
             label=f'Fitted P(50%) ({popt_exact[0]:.4f}e^(-{popt_exact[1]:.4f}n) + {popt_exact[2]:.4f})')
    
    plt.xlabel('Number of Flips (Even Only)')
    plt.ylabel('Probability of Exactly 50% Heads')
    plt.title('Exact 50% Probability (Even Flips Only)')
    plt.grid(True)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'comprehensive_analysis.png'))
    plt.close()
    
    # Calculate deviations and statistics
    std_mape = np.mean(np.abs((empirical_std - theoretical_std) / theoretical_std)) * 100
    std_rmse = np.sqrt(np.mean((empirical_std - theoretical_std) ** 2))
    
    exact_mape = np.mean(np.abs((empirical_exact - theoretical_exact) / theoretical_exact)) * 100
    exact_rmse = np.sqrt(np.mean((empirical_exact - theoretical_exact) ** 2))
    
    # Save comprehensive analysis
    with open(os.path.join(results_dir, 'comprehensive_analysis.md'), 'w') as f:
        f.write("# Comprehensive Analysis of Even Flips\n\n")
        
        f.write("## Standard Deviation Convergence\n")
        f.write(f"- Empirical function: σ = {a_std:.4f}n^{b_std:.4f}\n")
        f.write("- Theoretical function: σ = 1/(2√n)\n")
        f.write(f"- MAPE: {std_mape:.2f}%\n")
        f.write(f"- RMSE: {std_rmse:.4f}\n")
        f.write(f"- Power law exponent deviation: {abs(b_std + 0.5):.4f} from theoretical -0.5\n\n")
        
        f.write("## Exact 50% Probability\n")
        f.write(f"- Empirical function: P(50%) = {popt_exact[0]:.4f}e^(-{popt_exact[1]:.4f}n) + {popt_exact[2]:.4f}\n")
        f.write("- Theoretical function: P(50%) = C(n,n/2) * (1/2)^n\n")
        f.write(f"- MAPE: {exact_mape:.2f}%\n")
        f.write(f"- RMSE: {exact_rmse:.4f}\n\n")
        
        f.write("## Key Findings\n")
        f.write("1. Standard Deviation:\n")
        f.write(f"   - The empirical power law exponent ({b_std:.4f}) closely matches\n")
        f.write("     the theoretical -0.5, with only small deviation\n")
        f.write(f"   - The empirical coefficient ({a_std:.4f}) is very close to\n")
        f.write("     the theoretical 0.5\n\n")
        
        f.write("2. Exact 50% Probability:\n")
        f.write("   - The empirical probability follows an exponential decay plus offset\n")
        f.write("   - This matches the theoretical prediction that exact 50% becomes\n")
        f.write("     increasingly rare with more flips\n")
        f.write(f"   - The decay rate ({popt_exact[1]:.4f}) indicates how quickly the\n")
        f.write("     probability approaches the asymptotic value\n")
    
    return std_mape, std_rmse, exact_mape, exact_rmse

def main():
    parser = argparse.ArgumentParser(
        description='Analyze probability convergence to 0.5 with increasing flips.'
    )
    parser.add_argument('--runs', type=int, default=100000,
                      help='Number of simulations to run (default: 100000)')
    parser.add_argument('--max_flips', type=int, default=100,
                      help='Maximum number of flips (default: 100)')
    
    global args
    args = parser.parse_args()
    
    try:
        # Run analysis
        print(f"\nStarting analysis with {args.runs:,} runs and {args.max_flips} max flips...")
        global results_df
        results_df = run_convergence_analysis(args.runs, args.max_flips)
        
        # Calculate statistics
        stats_df = calculate_statistics(results_df)
        
        # Save results
        results_dir = save_results(results_df, stats_df)
        print(f"\nResults saved in: {results_dir}")
        
        # Create individual empirical plots
        exact_50_percent = create_empirical_exact_plot(stats_df, results_df, results_dir)
        create_empirical_convergence_plot(stats_df, results_dir)
        
        # Create even-only exact probability plot
        exact_50_percent_even, even_flips = create_even_flips_exact_plot(stats_df, results_df, results_dir)
        
        # Create combined theoretical plot
        create_combined_theoretical_plot(stats_df, exact_50_percent, results_dir)
        
        # Create comprehensive analysis for even flips
        std_mape, std_rmse, exact_mape, exact_rmse = create_comprehensive_plot(stats_df, results_df, results_dir)
        print(f"Plots saved in: {results_dir}")
        
        # Calculate and save statistical analysis
        calculate_fit_statistics(stats_df, results_dir)
        print(f"Statistical analysis saved in: {results_dir}")
        
        # Print statistics
        print_statistics(stats_df)
        
        # Print key findings
        print("\nKey Findings:")
        print("-" * 50)
        
        # Standard findings
        stable_point = stats_df[stats_df['Std'] < 0.05]['Flips'].min()
        if pd.notna(stable_point):
            print(f"- Probability stabilizes (std < 0.05) after {stable_point} flips")
        
        max_dev_row = stats_df.loc[stats_df['Max_Distance_from_0.5'].idxmax()]
        print(f"- Maximum deviation from 0.5 occurs at {max_dev_row['Flips']} flips")
        print(f"  (range: {max_dev_row['Min']:.4f} to {max_dev_row['Max']:.4f})")
        
        q1_close = stats_df['Q1'] >= 0.4
        q3_close = stats_df['Q3'] <= 0.6
        convergence_point = stats_df[q1_close & q3_close]['Flips'].min()
        if pd.notna(convergence_point):
            print(f"- 50% of results within ±0.1 of 0.5 after {convergence_point} flips")
        
        # Even flips findings
        if len(even_flips) > 0:
            max_even_prob = max(exact_50_percent_even)
            max_even_idx = exact_50_percent_even.index(max_even_prob)
            max_even_flips = even_flips.iloc[max_even_idx]
            print(f"- For even flips, highest probability of exactly 50% occurs at {max_even_flips} flips")
            print(f"  (probability: {max_even_prob:.4f})")
        
        # Print comprehensive analysis results
        print("\nComprehensive Analysis (Even Flips Only):")
        print("-" * 50)
        print(f"Standard Deviation MAPE: {std_mape:.2f}%")
        print(f"Exact 50% Probability MAPE: {exact_mape:.2f}%")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 