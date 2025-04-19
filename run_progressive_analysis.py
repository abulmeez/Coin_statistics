import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

def flip_until_streak_numpy(streak_target):
    max_batch = 10_000_000  # process in big batches
    total_flips = 0
    current_streak = 1

    # Start with a random flip
    last_flip = np.random.randint(1, 3)

    while current_streak < streak_target:
        # Generate a large batch of random flips
        flips = np.random.randint(1, 3, size=max_batch)
        for flip in flips:
            total_flips += 1
            if flip == last_flip:
                current_streak += 1
                if current_streak == streak_target:
                    return total_flips
            else:
                current_streak = 1
                last_flip = flip

    return total_flips

def run_progressive_simulations(max_runs=100, max_streak=15):
    # Create results directory if it doesn't exist
    results_dir = os.path.join("results", "results_20250419_progressive")
    os.makedirs(results_dir, exist_ok=True)
    
    # Create CSV filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(results_dir, f'progressive_simulation_results_{timestamp}.csv')
    
    # Initialize DataFrame to store results
    results = []
    
    # Run simulations for each number of runs
    for num_runs in range(1, max_runs + 1):
        print(f"\nRunning {num_runs} runs...")
        
        # Run simulations for current number of runs
        for run in range(1, num_runs + 1):
            for streak_target in range(1, max_streak + 1):
                total_flips = flip_until_streak_numpy(streak_target)
                theoretical_flips = 2 ** streak_target
                difference = total_flips - theoretical_flips
                percentage_diff = (difference / theoretical_flips) * 100
                
                results.append({
                    'Total Runs': num_runs,
                    'Current Run': run,
                    'Streak Target': streak_target,
                    'Flips Required': total_flips,
                    'Theoretical Flips': theoretical_flips,
                    'Absolute Difference': difference,
                    'Percentage Difference': percentage_diff
                })
    
    # Convert results to DataFrame and save to CSV
    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)
    print(f"\nResults have been saved to {filename}")
    
    return df

def analyze_progressive_results(df):
    # Group by number of runs and calculate statistics
    stats = df.groupby('Total Runs').agg({
        'Absolute Difference': ['mean', 'std', 'min', 'max'],
        'Percentage Difference': ['mean', 'std', 'min', 'max']
    }).reset_index()
    
    # Flatten column names
    stats.columns = ['_'.join(col).strip() for col in stats.columns.values]
    
    # Create directory for plots if it doesn't exist
    results_dir = os.path.join("results", "results_20250419_progressive")
    os.makedirs(results_dir, exist_ok=True)
    
    # Plot mean absolute difference vs number of runs
    plt.figure(figsize=(12, 8))
    plt.plot(stats['Total Runs_'], stats['Absolute Difference_mean'], 
             label='Mean Absolute Difference')
    plt.fill_between(stats['Total Runs_'], 
                    stats['Absolute Difference_mean'] - stats['Absolute Difference_std'],
                    stats['Absolute Difference_mean'] + stats['Absolute Difference_std'],
                    alpha=0.2)
    
    plt.title('Mean Absolute Difference from Theoretical vs Number of Runs')
    plt.xlabel('Number of Runs')
    plt.ylabel('Absolute Difference (Flips)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig(os.path.join(results_dir, 'absolute_difference_vs_runs.png'))
    plt.close()
    
    # Plot mean percentage difference vs number of runs
    plt.figure(figsize=(12, 8))
    plt.plot(stats['Total Runs_'], stats['Percentage Difference_mean'], 
             label='Mean Percentage Difference')
    plt.fill_between(stats['Total Runs_'], 
                    stats['Percentage Difference_mean'] - stats['Percentage Difference_std'],
                    stats['Percentage Difference_mean'] + stats['Percentage Difference_std'],
                    alpha=0.2)
    
    plt.title('Mean Percentage Difference from Theoretical vs Number of Runs')
    plt.xlabel('Number of Runs')
    plt.ylabel('Percentage Difference (%)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig(os.path.join(results_dir, 'percentage_difference_vs_runs.png'))
    plt.close()
    
    return stats

def main():
    # Run progressive simulations
    df = run_progressive_simulations(max_runs=100, max_streak=15)
    
    # Analyze results
    stats = analyze_progressive_results(df)
    
    # Save statistics to CSV
    results_dir = os.path.join("results", "results_20250419_progressive")
    stats.to_csv(os.path.join(results_dir, 'progressive_analysis_stats.csv'), index=False)
    
    print("\nAnalysis complete. Results and plots have been saved.")

if __name__ == "__main__":
    main() 