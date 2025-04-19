"""
Analyze the probability of getting exactly half heads in a sequence of coin flips.

This script simulates multiple coin flip sequences and calculates the empirical
probability of getting exactly half heads for different sequence lengths.
Results are saved to CSV and probabilities are printed to stdout.
"""

import numpy as np
import pandas as pd
from datetime import datetime
import os
import argparse
import math

def run_equal_probability_analysis(runs=100000, max_flips=100):
    """
    Run the equal probability analysis for different flip counts.
    
    Args:
        runs (int): Number of simulations to run
        max_flips (int): Maximum number of flips (must be even)
        
    Returns:
        pd.DataFrame: Results of all simulations
    """
    if max_flips % 2 != 0:
        raise ValueError("max_flips must be even")
        
    results = []
    flip_counts = range(2, max_flips + 2, 2)
    
    # Print progress header
    print("\nRunning simulations:")
    print("-" * 50)
    
    for flip_count in flip_counts:
        print(f"Processing {flip_count} flips...", end='\r')
        
        # Generate random flips (0 for tails, 1 for heads)
        flips = np.random.randint(0, 2, size=(runs, flip_count))
        
        # Convert to sequences of 'H' and 'T'
        sequences = np.where(flips == 1, 'H', 'T')
        sequences = [''.join(seq) for seq in sequences]
        
        # Count heads and check for equality
        heads_count = np.sum(flips, axis=1)
        is_equal = heads_count == flip_count // 2
        
        # Store results
        for run_idx in range(runs):
            results.append({
                'Run': run_idx + 1,
                'Flips': flip_count,
                'Sequence': sequences[run_idx],
                'IsEqual': is_equal[run_idx]
            })
    
    print("\nSimulations complete!")
    return pd.DataFrame(results)

def save_results(df):
    """
    Save results to a CSV file in the results directory.
    
    Args:
        df (pd.DataFrame): Results dataframe to save
        
    Returns:
        tuple: (filepath, results_dir) - Path to saved file and results directory
    """
    # Create main results directory if it doesn't exist
    os.makedirs('results', exist_ok=True)
    
    # Create timestamped subdirectory for this analysis
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_dir = os.path.join('results', f'equal_probability_{timestamp}')
    os.makedirs(results_dir, exist_ok=True)
    
    # Save full results
    filename = 'equal_heads_tails_full.csv'
    filepath = os.path.join(results_dir, filename)
    df.to_csv(filepath, index=False)
    
    # Calculate and save summary statistics
    summary = df.groupby('Flips')['IsEqual'].agg(['count', 'mean', 'std']).reset_index()
    summary.columns = ['Flips', 'Total_Runs', 'Empirical_Probability', 'Standard_Deviation']
    
    # Add theoretical probability
    summary['Theoretical_Probability'] = summary['Flips'].apply(
        lambda n: math.comb(n, n//2) * (0.5 ** n)
    )
    
    # Calculate absolute and relative differences
    summary['Absolute_Difference'] = abs(
        summary['Empirical_Probability'] - summary['Theoretical_Probability']
    )
    summary['Relative_Difference_Percent'] = (
        summary['Absolute_Difference'] / summary['Theoretical_Probability'] * 100
    )
    
    # Save summary
    summary_filepath = os.path.join(results_dir, 'probability_summary.csv')
    summary.to_csv(summary_filepath, index=False)
    
    return filepath, results_dir

def print_probabilities(df, results_dir):
    """
    Print empirical probabilities for each flip count.
    
    Args:
        df (pd.DataFrame): Results dataframe
        results_dir (str): Directory where results are saved
    """
    print("\nEmpirical Probabilities of Equal Heads and Tails:")
    print("-" * 75)
    print(f"{'Flips':>6} | {'Probability':>10} | {'Theoretical':>10} | {'Diff %':>8} | {'Std Dev':>8}")
    print("-" * 75)
    
    # Create data for plotting
    plot_data = []
    
    for flips in sorted(df['Flips'].unique()):
        mask = df['Flips'] == flips
        empirical_prob = df[mask]['IsEqual'].mean()
        std_dev = df[mask]['IsEqual'].std()
        
        # Calculate theoretical probability using binomial coefficient
        n = flips
        k = flips // 2
        theoretical_prob = math.comb(n, k) * (0.5 ** n)
        
        # Calculate percentage difference
        diff_percent = abs(empirical_prob - theoretical_prob) / theoretical_prob * 100
        
        print(f"{flips:6d} | {empirical_prob:10.4f} | {theoretical_prob:10.4f} | "
              f"{diff_percent:8.2f} | {std_dev:8.4f}")
        
        plot_data.append({
            'Flips': flips,
            'Empirical': empirical_prob,
            'Theoretical': theoretical_prob,
            'StdDev': std_dev
        })
    
    # Save plot data for potential future visualization
    plot_df = pd.DataFrame(plot_data)
    plot_df.to_csv(os.path.join(results_dir, 'plot_data.csv'), index=False)

def main():
    parser = argparse.ArgumentParser(description='Analyze probability of equal heads and tails.')
    parser.add_argument('--runs', type=int, default=100000,
                      help='Number of simulations to run (default: 100000)')
    parser.add_argument('--max_flips', type=int, default=100,
                      help='Maximum number of flips, must be even (default: 100)')
    
    args = parser.parse_args()
    
    try:
        # Run analysis
        print(f"\nStarting analysis with {args.runs:,} runs and {args.max_flips} max flips...")
        results_df = run_equal_probability_analysis(args.runs, args.max_flips)
        
        # Save results
        filepath, results_dir = save_results(results_df)
        print(f"\nResults directory: {results_dir}")
        print(f"Full results saved to: {filepath}")
        
        # Print probabilities
        print_probabilities(results_df, results_dir)
        
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 