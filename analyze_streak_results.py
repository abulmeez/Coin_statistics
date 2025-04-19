import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

def load_latest_csv(results_dir):
    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(results_dir) if f.endswith('.csv')]
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {results_dir}")
    
    # Sort by modification time and get the latest
    latest_file = max(csv_files, key=lambda x: os.path.getmtime(os.path.join(results_dir, x)))
    return pd.read_csv(os.path.join(results_dir, latest_file))

def create_individual_runs_plot(df, results_dir, max_streak):
    plt.figure(figsize=(12, 8))
    for run in df['Run'].unique():
        run_data = df[df['Run'] == run]
        plt.plot(run_data['Streak'], run_data['Flips'], alpha=0.1, color='blue')
    
    plt.title('Individual Runs: Flips Required vs Streak Length')
    plt.xlabel('Streak Length')
    plt.ylabel('Number of Flips')
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(results_dir, f'individual_runs_{max_streak}.png'))
    plt.close()

def create_median_plot(df, results_dir, max_streak):
    median_flips = df.groupby('Streak')['Flips'].median()
    theoretical = [2**n for n in range(1, max_streak + 1)]
    
    plt.figure(figsize=(12, 8))
    plt.plot(range(1, max_streak + 1), median_flips, 'o-', label='Median Flips')
    plt.plot(range(1, max_streak + 1), theoretical, 'r--', label='Theoretical')
    plt.title('Median Flips Required vs Streak Length')
    plt.xlabel('Streak Length')
    plt.ylabel('Number of Flips')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig(os.path.join(results_dir, f'median_plot_{max_streak}.png'))
    plt.close()

def create_combined_plot(df, results_dir, max_streak):
    mean_flips = df.groupby('Streak')['Flips'].mean()
    std_flips = df.groupby('Streak')['Flips'].std()
    theoretical = [2**n for n in range(1, max_streak + 1)]
    
    plt.figure(figsize=(12, 8))
    plt.errorbar(range(1, max_streak + 1), mean_flips, yerr=std_flips, 
                fmt='o-', capsize=5, label='Mean Flips')
    plt.plot(range(1, max_streak + 1), theoretical, 'r--', label='Theoretical')
    plt.title('Mean Flips Required vs Streak Length')
    plt.xlabel('Streak Length')
    plt.ylabel('Number of Flips')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig(os.path.join(results_dir, f'combined_plot_{max_streak}.png'))
    plt.close()

def create_trimmed_plot(df, results_dir, max_streak):
    # Calculate trimmed mean (excluding top and bottom 5%)
    trimmed_mean = df.groupby('Streak')['Flips'].apply(
        lambda x: x.sort_values().iloc[int(0.05*len(x)):int(0.95*len(x))].mean()
    )
    theoretical = [2**n for n in range(1, max_streak + 1)]
    
    plt.figure(figsize=(12, 8))
    plt.plot(range(1, max_streak + 1), trimmed_mean, 'o-', label='Trimmed Mean')
    plt.plot(range(1, max_streak + 1), theoretical, 'r--', label='Theoretical')
    plt.title('Trimmed Mean Flips Required vs Streak Length')
    plt.xlabel('Streak Length')
    plt.ylabel('Number of Flips')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig(os.path.join(results_dir, f'trimmed_plot_{max_streak}.png'))
    plt.close()

def main():
    # Create results directory
    results_dir = os.path.join("results", f"results_{datetime.now().strftime('%Y%m%d')}")
    os.makedirs(results_dir, exist_ok=True)
    
    # Analyze both 100 and 1000 runs
    for num_runs in [100, 1000]:
        run_dir = os.path.join(results_dir, f"results_{num_runs}")
        os.makedirs(run_dir, exist_ok=True)
        
        # Load the latest CSV file for this number of runs
        df = load_latest_csv(run_dir)
        
        # Create plots for different streak ranges
        for max_streak in [10, 20]:
            streak_df = df[df['Streak'] <= max_streak]
            
            create_individual_runs_plot(streak_df, run_dir, max_streak)
            create_median_plot(streak_df, run_dir, max_streak)
            create_combined_plot(streak_df, run_dir, max_streak)
            create_trimmed_plot(streak_df, run_dir, max_streak)

if __name__ == "__main__":
    main() 