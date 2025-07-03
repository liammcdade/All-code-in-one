"""
Coriolis Effect Calculator for NFL Kicks

This script calculates the Coriolis effect on NFL field goal kicks at different distances.
The Coriolis effect is the deflection of moving objects due to Earth's rotation.
"""

import numpy as np
from typing import List, Tuple


# Physical constants
EARTH_ANGULAR_VELOCITY = 7.292115e-5  # rad/s
APPROXIMATE_NFL_LATITUDE = 40  # degrees
KICK_SPEED = 25  # m/s, rough average kick speed
YARDS_TO_METERS = 0.9144


def yards_to_meters(yards: float) -> float:
    """Convert yards to meters."""
    return yards * YARDS_TO_METERS


def calculate_flight_time(distance_meters: float) -> float:
    """Calculate flight time for a kick over given distance."""
    return distance_meters / KICK_SPEED if distance_meters > 0 else 0


def calculate_coriolis_displacement(velocity: float, flight_time: float, latitude_rad: float) -> float:
    """Calculate Coriolis displacement in meters."""
    return EARTH_ANGULAR_VELOCITY * velocity * np.sin(latitude_rad) * flight_time**2


def analyze_kick_distances(start_yards: int = 1, end_yards: int = 70) -> Tuple[List[float], List[float]]:
    """Analyze Coriolis effect for a range of kick distances."""
    kick_distances_yards = np.arange(start_yards, end_yards + 1)
    displacements_cm = []
    
    latitude_rad = np.radians(APPROXIMATE_NFL_LATITUDE)
    
    for yards in kick_distances_yards:
        distance_meters = yards_to_meters(yards)
        flight_time = calculate_flight_time(distance_meters)
        displacement_meters = calculate_coriolis_displacement(KICK_SPEED, flight_time, latitude_rad)
        displacements_cm.append(displacement_meters * 100)  # Convert to cm
    
    return kick_distances_yards, displacements_cm


def calculate_percentage_increases(displacements: List[float]) -> Tuple[List[float], int, float]:
    """Calculate percentage increases between consecutive displacements."""
    percent_increases = []
    
    for i in range(1, len(displacements)):
        prev = displacements[i - 1]
        curr = displacements[i]
        
        if prev == 0:
            percent_increases.append(float("inf"))
        else:
            pct_inc = ((curr - prev) / prev) * 100
            percent_increases.append(pct_inc)
    
    # Find biggest percentage increase (ignore infinity at start)
    filtered_increases = [p for p in percent_increases if p != float("inf")]
    if filtered_increases:
        max_increase = max(filtered_increases)
        max_index = percent_increases.index(max_increase) + 2  # +2 to get yard number after 1
        avg_increase = np.mean(filtered_increases)
    else:
        max_increase = 0
        max_index = 0
        avg_increase = 0
    
    return percent_increases, max_index, avg_increase


def print_results(distances: List[float], displacements: List[float], 
                 max_index: int, avg_increase: float) -> None:
    """Print formatted results."""
    print("Kick Distance (yards) | Coriolis Deflection (cm)")
    print("-" * 45)
    
    for yards, displacement_cm in zip(distances, displacements):
        print(f"{yards:>20} | {displacement_cm:.4f}")
    
    avg_deflection_cm = np.mean(displacements)
    print(f"\nAverage Coriolis deflection over {len(distances)}-{max(distances)} yard kicks: {avg_deflection_cm:.4f} cm")
    
    if max_index > 0:
        print(f"Biggest percentage increase: {max_increase:.2f}% from yard {max_index-1} to {max_index}")
    print(f"Average percentage increase per yard: {avg_increase:.2f}%")


def main() -> None:
    """Main function to run the Coriolis effect analysis."""
    print("Coriolis Effect Analysis for NFL Field Goal Kicks\n")
    
    # Analyze kick distances
    distances, displacements = analyze_kick_distances()
    
    # Calculate percentage increases
    percent_increases, max_index, avg_increase = calculate_percentage_increases(displacements)
    
    # Print results
    print_results(distances, displacements, max_index, avg_increase)


if __name__ == "__main__":
    main()
