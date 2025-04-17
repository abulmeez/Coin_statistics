import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

def load_latest_csv():
    # Find the most recent CSV file
    csv_files = glob.glob('streak_simulation_results_*.csv')
    if not csv_files:
        raise FileNotFoundError("No simulation results CSV files found")
    
    latest_file = max(csv_files, key=os.path.getctime)
    return pd.read_csv(latest_file)

def create_individual_runs_plot(df, max_streak, suffix=''):
    plt.figure(figsize=(12, 8))
    
    # Filter data for the specified range
    df_filtered = df[df['Streak Target'] <= max_streak]
    
    # Plot each run
    for run in df_filtered['Run'].unique():
        run_data = df_filtered[df_filtered['Run'] == run]
        plt.plot(run_data['Streak Target'], run_data['Flips Required'], 
                color='lightblue', alpha=0.3, linewidth=1)
    
    plt.title(f'Number of Flips Required for Each Streak Length\n(All 100 Runs, n=1 to {max_streak})')
    plt.xlabel('Streak Length (n)')
    plt.ylabel('Number of Flips Required')
    plt.grid(True, alpha=0.3)
    plt.savefig(f'individual_runs{suffix}.png')
    plt.close()

def create_median_plot(df, max_streak, suffix=''):
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
    plt.savefig(f'median_plot{suffix}.png')
    plt.close()

def create_combined_plot(df, max_streak, suffix=''):
    plt.figure(figsize=(12, 8))
    
    # Filter data for the specified range
    df_filtered = df[df['Streak Target'] <= max_streak]
    
    # Plot all individual runs
    for run in df_filtered['Run'].unique():
        run_data = df_filtered[df_filtered['Run'] == run]
        plt.plot(run_data['Streak Target'], run_data['Flips Required'], 
                color='lightblue', alpha=0.3, linewidth=1)
    
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
    plt.savefig(f'combined_plot{suffix}.png')
    plt.close()

def create_trimmed_plot(df, max_streak, suffix=''):
    plt.figure(figsize=(12, 8))
    
    # Filter data for the specified range
    df_filtered = df[df['Streak Target'] <= max_streak]
    
    # Calculate trimmed mean (excluding 5 highest and 5 lowest values) for each streak length
    trimmed_means = []
    for n in range(1, max_streak + 1):
        values = df_filtered[df_filtered['Streak Target'] == n]['Flips Required'].values
        # Sort values and remove 5 highest and 5 lowest
        sorted_values = np.sort(values)
        trimmed_values = sorted_values[5:-5]  # Remove first and last 5 values
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
    
    plt.title(f'Comparison of Theoretical, Median, and Trimmed Mean\n(n=1 to {max_streak}, excluding 10 most extreme values)')
    plt.xlabel('Streak Length (n)')
    plt.ylabel('Number of Flips Required')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig(f'trimmed_plot{suffix}.png')
    plt.close()

def main():
    # Load the data
    df = load_latest_csv()
    
    # Create plots for n=1 to 25
    print("Creating plots for n=1 to 25...")
    create_individual_runs_plot(df, 25)
    create_median_plot(df, 25)
    create_combined_plot(df, 25)
    create_trimmed_plot(df, 25)
    
    # Create plots for n=1 to 10
    print("\nCreating plots for n=1 to 10...")
    create_individual_runs_plot(df, 10, '_n10')
    create_median_plot(df, 10, '_n10')
    create_combined_plot(df, 10, '_n10')
    create_trimmed_plot(df, 10, '_n10')
    
    print("\nAll plots have been saved as PNG files:")
    print("\nFor n=1 to 25:")
    print("- individual_runs.png: Shows all 100 runs")
    print("- median_plot.png: Shows the median values and theoretical function")
    print("- combined_plot.png: Shows individual runs, median, and theoretical function")
    print("- trimmed_plot.png: Shows theoretical, median, and trimmed mean (excluding 10 extreme values)")
    
    print("\nFor n=1 to 10:")
    print("- individual_runs_n10.png: Shows all 100 runs")
    print("- median_plot_n10.png: Shows the median values and theoretical function")
    print("- combined_plot_n10.png: Shows individual runs, median, and theoretical function")
    print("- trimmed_plot_n10.png: Shows theoretical, median, and trimmed mean (excluding 10 extreme values)")

if __name__ == "__main__":
    main() 