import numpy as np
import csv
from datetime import datetime

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

def run_multiple_simulations(num_runs=100, max_streak=25):
    # Create CSV filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'streak_simulation_results_{timestamp}.csv'
    
    # Open CSV file for writing
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(['Run', 'Streak Target', 'Flips Required'])
        
        # Run multiple simulations
        for run in range(1, num_runs + 1):
            print(f"\nRun {run}:")
            for streak_target in range(1, max_streak + 1):
                total_flips = flip_until_streak_numpy(streak_target)
                print(f"Streak of {streak_target}: {total_flips:,} flips")
                writer.writerow([run, streak_target, total_flips])
    
    print(f"\nResults have been saved to {filename}")

# Run the simulations
run_multiple_simulations() 