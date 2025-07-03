"""
Formula 1 Championship Probability Analysis

This script analyzes Formula 1 race data to calculate driver performance scores and
simulates championship win probabilities using Monte Carlo simulation.

The script reads race results from a CSV file, cleans the data, calculates
various driver statistics (average finish, DNF rate, points, etc.),
assigns a score to each driver based on these stats, and then runs a
Monte Carlo simulation to estimate each driver's chance of winning a
hypothetical championship.
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path
from typing import Optional, Dict, List, Tuple


# Configuration
RESULTS_CSV_FILE = Path("sportsanalysis/F1/Formula1.csv")
OUTPUT_CSV_FILE = Path("f1_championship_probabilities.csv")
N_SIMULATIONS: int = 100_000
RANDOM_SEED: int = 42

# Scoring weights for driver performance calculation
SCORING_WEIGHTS = {
    'avg_finish': -50,      # Higher average finish position is worse
    'avg_grid': -2,         # Higher average grid position is generally worse
    'dnf_rate': -200,       # Higher DNF rate is significantly worse
    'total_points': 5,      # More points are better
    'fastest_laps': 10      # More fastest laps are better
}

# DNF keywords for detecting non-finishes
DNF_KEYWORDS = [
    "DNF", "Accident", "Engine", "Gearbox", "Hydraulics", "Retired", 
    "Electrical", "Crash", "Suspension", "Overheating", "Collision", 
    "Puncture", "Disqualified", "Withdrew", "Power unit", "Brakes"
]


def setup_logging() -> None:
    """Setup basic logging configuration."""
    import logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def load_f1_data(file_path: Path) -> pd.DataFrame:
    """Load F1 race data from CSV file."""
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The data file '{file_path}' was not found.")
        raise
    except (pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        print(f"Error: Could not parse the data file '{file_path}'. Details: {e}")
        raise


def clean_f1_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare F1 data for analysis."""
    # Convert numeric columns
    df["Position"] = pd.to_numeric(df["Position"], errors="coerce")
    df["Starting Grid"] = pd.to_numeric(df["Starting Grid"], errors="coerce")
    df["Points"] = pd.to_numeric(df["Points"], errors="coerce").fillna(0)
    
    # Convert fastest lap to binary
    df["Set Fastest Lap"] = df["Set Fastest Lap"].map({"Yes": 1, "No": 0}).fillna(0)
    
    # Detect DNFs
    dnf_pattern = "|".join(DNF_KEYWORDS)
    df["DNF"] = (
        df["Time/Retired"]
        .fillna("DNF")
        .str.contains(dnf_pattern, case=False, na=False)
        .astype(int)
    )
    
    return df


def calculate_driver_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate aggregated statistics for each driver."""
    driver_stats = df.groupby("Driver").agg(
        Races=("Position", "count"),
        AvgFinish=("Position", "mean"),
        AvgGrid=("Starting Grid", "mean"),
        TotalPoints=("Points", "sum"),
        FastestLaps=("Set Fastest Lap", "sum"),
        DNFs=("DNF", "sum"),
    )
    
    # Calculate DNF rate
    driver_stats["DNFRate"] = 0.0
    driver_stats.loc[driver_stats["Races"] > 0, "DNFRate"] = (
        driver_stats["DNFs"] / driver_stats["Races"]
    )
    
    return driver_stats


def calculate_driver_scores(driver_stats: pd.DataFrame) -> pd.DataFrame:
    """Calculate performance scores for each driver."""
    # Fill NaN values with mean for scoring
    driver_stats["Score"] = (
        driver_stats["AvgFinish"].fillna(driver_stats["AvgFinish"].mean()) * SCORING_WEIGHTS['avg_finish'] +
        driver_stats["AvgGrid"].fillna(driver_stats["AvgGrid"].mean()) * SCORING_WEIGHTS['avg_grid'] +
        driver_stats["DNFRate"] * SCORING_WEIGHTS['dnf_rate'] +
        driver_stats["TotalPoints"] * SCORING_WEIGHTS['total_points'] +
        driver_stats["FastestLaps"] * SCORING_WEIGHTS['fastest_laps']
    )
    
    return driver_stats


def calculate_win_probabilities(driver_stats: pd.DataFrame) -> pd.Series:
    """Calculate win probabilities from driver scores."""
    # Shift scores to be positive for probability calculation
    min_score = driver_stats["Score"].min()
    scores_shifted = driver_stats["Score"] - min_score + 1e-3
    
    # Handle edge cases
    if scores_shifted.sum() == 0:
        probabilities = pd.Series(
            1 / len(scores_shifted) if len(scores_shifted) > 0 else 0,
            index=scores_shifted.index,
        )
    else:
        probabilities = scores_shifted / scores_shifted.sum()
    
    # Ensure probabilities sum to 1
    if not np.isclose(probabilities.sum(), 1.0):
        probabilities = probabilities / probabilities.sum()
    
    return probabilities


def run_monte_carlo_simulation(probabilities: pd.Series, num_simulations: int) -> pd.Series:
    """Run Monte Carlo simulation to estimate championship win probabilities."""
    np.random.seed(RANDOM_SEED)
    drivers = probabilities.index.tolist()
    
    if not drivers:
        raise ValueError("No drivers found to simulate.")
    
    # Prepare weights for simulation
    if probabilities.empty or probabilities.sum() == 0:
        print("Warning: Probabilities are zero or empty. Assigning equal weights.")
        weights = [1 / len(drivers)] * len(drivers) if len(drivers) > 0 else []
    else:
        weights = probabilities.values
    
    if not weights:
        raise ValueError("No weights available for simulation.")
    
    # Run simulation
    sim_results = np.random.choice(drivers, size=num_simulations, p=weights)
    sim_counts_percent = pd.Series(sim_results).value_counts(normalize=True) * 100
    
    return sim_counts_percent


def display_results(final_probabilities: pd.Series) -> None:
    """Display simulation results."""
    print("\n--- Championship Win Probabilities ---")
    print(final_probabilities.round(2))
    
    # Show top 3 drivers
    top_drivers = final_probabilities.head(3)
    print(f"\n🏆 Top Contenders:")
    for i, (driver, prob) in enumerate(top_drivers.items(), 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
        print(f"{medal} {driver}: {prob:.2f}%")


def save_results(final_probabilities: pd.Series, output_file: Path) -> None:
    """Save results to CSV file."""
    try:
        final_probabilities.round(2).to_csv(output_file)
        print(f"\nResults saved to {output_file}")
    except Exception as e:
        print(f"\nError saving results to CSV: {e}")


def main() -> None:
    """Main function to run F1 championship probability analysis."""
    setup_logging()
    
    try:
        # Load and clean data
        df = load_f1_data(RESULTS_CSV_FILE)
        df = clean_f1_data(df)
        
        # Calculate driver statistics
        driver_stats = calculate_driver_stats(df)
        
        # Calculate driver scores
        driver_stats = calculate_driver_scores(driver_stats)
        
        # Calculate win probabilities
        probabilities = calculate_win_probabilities(driver_stats)
        
        # Run Monte Carlo simulation
        final_probabilities = run_monte_carlo_simulation(probabilities, N_SIMULATIONS)
        final_probabilities = final_probabilities.rename("WinChance (%)").sort_values(ascending=False)
        
        # Display and save results
        display_results(final_probabilities)
        save_results(final_probabilities, OUTPUT_CSV_FILE)
        
    except Exception as e:
        print(f"Analysis failed: {e}")
        return


if __name__ == "__main__":
    main()
