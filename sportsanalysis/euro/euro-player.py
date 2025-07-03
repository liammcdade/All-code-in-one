"""
EURO 2024 Best XI Analysis

This script computes and displays the EURO 2024 Best XI based on player and team metrics.
It combines individual player performance with team quality and tournament progress.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from pathlib import Path
import logging
from typing import List, Dict, Any


# Configuration
PLAYER_DATA_FILE = "euro/euro2024-player.csv"
TEAM_DATA_FILE = "euro/euro2024-country.csv"
FORMATION = {"GK": 1, "DF": 4, "MF": 3, "FW": 3}  # 4-3-3 formation


def setup_logging() -> None:
    """Setup logging configuration."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def load_data(player_path: str, team_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load and validate player and team data."""
    try:
        players = pd.read_csv(player_path)
        teams = pd.read_csv(team_path)
        return players, teams
    except FileNotFoundError as e:
        logging.error(f"File not found: {e.filename}")
        raise
    except Exception as e:
        logging.error(f"Error loading file: {e}")
        raise


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare dataframe."""
    df.columns = df.columns.str.strip()
    return df


def get_numeric_columns() -> List[str]:
    """Get list of numeric columns for processing."""
    return [
        "Age", "Poss", "MP", "Starts", "Min", "90s", "Gls", "Ast", "G+A", "G-PK", 
        "PK", "PKatt", "CrdY", "CrdR", "xG", "npxG", "xAG", "npxG+xAG", "PrgC", "PrgP"
    ]


def process_team_data(teams: pd.DataFrame) -> pd.DataFrame:
    """Process and calculate team-level metrics."""
    numeric_cols = get_numeric_columns()
    teams[numeric_cols] = teams[numeric_cols].apply(pd.to_numeric, errors="coerce")
    teams = teams[teams["Min"] > 0].dropna(subset=["Squad"])
    
    # Calculate per-90 metrics
    per_90_metrics = ["Gls", "Ast", "PrgC", "PrgP"]
    for col in per_90_metrics:
        teams[f"{col}_per_90"] = teams[col] / (teams["Min"] / 90)
    
    # Calculate derived metrics
    teams["xG_diff"] = teams["Gls"] - teams["xG"]
    teams["xGA_diff"] = teams["G+A"] - (teams["xG"] + teams["xAG"])
    teams["npxGxAG_per_90"] = teams["npxG+xAG"] / (teams["Min"] / 90)
    teams["Discipline"] = (teams["CrdY"] + 2 * teams["CrdR"]) / teams["Min"]
    
    # Normalize team metrics
    team_metrics = [
        "Goals_per_90", "Assists_per_90", "xG_diff", "xGA_diff", "npxGxAG_per_90",
        "Poss", "PrgC_per_90", "PrgP_per_90", "Discipline"
    ]
    
    scaler = MinMaxScaler()
    teams[team_metrics] = scaler.fit_transform(teams[team_metrics])
    teams["Discipline"] *= -1  # Lower is better
    teams["SquadScore"] = teams[team_metrics].sum(axis=1)
    
    # Adjust for number of matches played
    teams["AvgMatches"] = teams.groupby("Squad")["MP"].transform("mean")
    teams["MatchFactor"] = 1 - MinMaxScaler().fit_transform(teams[["AvgMatches"]])
    
    return teams


def process_player_data(players: pd.DataFrame, teams: pd.DataFrame) -> pd.DataFrame:
    """Process and calculate player-level metrics."""
    players = players[players["Min"] > 0].dropna(subset=["Player", "Squad", "Pos"])
    
    # Calculate per-90 metrics
    per_90_metrics = ["Gls", "Ast", "PrgC", "PrgP"]
    for col in per_90_metrics:
        players[f"{col}_per_90"] = players[col] / (players["Min"] / 90)
    
    # Calculate derived metrics
    players["xG_diff"] = players["Gls"] - players["xG"]
    players["xGA_diff"] = players["G+A"] - (players["xG"] + players["xAG"])
    players["npxGxAG_per_90"] = players["npxG+xAG"] / (players["Min"] / 90)
    players["Discipline"] = (players["CrdY"] + 2 * players["CrdR"]) / players["Min"]
    
    # Normalize player metrics
    player_metrics = [
        "Goals_per_90", "Assists_per_90", "xG_diff", "xGA_diff", "npxGxAG_per_90",
        "PrgC_per_90", "PrgP_per_90", "Discipline"
    ]
    
    scaler = MinMaxScaler()
    players[player_metrics] = scaler.fit_transform(players[player_metrics])
    players["Discipline"] *= -1  # Lower is better
    players["RawScore"] = players[player_metrics].sum(axis=1)
    
    # Merge squad performance data
    players = players.merge(
        teams[["Squad", "SquadScore", "MatchFactor"]], on="Squad", how="left"
    )
    
    # Calculate adjusted score
    players["PlayerMatchWeight"] = players["MP"] / players["MP"].max()
    players["AdjScore"] = (
        players["RawScore"]
        * (1 + players["SquadScore"])
        * (1 + players["MatchFactor"])
        * players["PlayerMatchWeight"]
    )
    
    return players


def select_best_players(players: pd.DataFrame, formation: Dict[str, int]) -> pd.DataFrame:
    """Select the best players for each position based on formation."""
    def pick_best(df: pd.DataFrame, pos_substring: str, n: int) -> pd.DataFrame:
        """Select the top n players for a given position substring based on AdjScore."""
        return df[df["Pos"].str.contains(pos_substring)].nlargest(n, "AdjScore")
    
    selected_players = []
    
    for position, count in formation.items():
        position_players = pick_best(players, position, count)
        selected_players.append(position_players)
    
    best_xi = pd.concat(selected_players)
    best_xi = best_xi.drop_duplicates(subset="Player", keep="first")
    
    return best_xi


def display_results(best_xi: pd.DataFrame) -> None:
    """Display the Best XI results."""
    print("🏆 EURO 2024 BEST XI (Adjusted for Team Quality and Tournament Progress):\n")
    
    # Sort by adjusted score and display
    display_df = best_xi[["Player", "Pos", "Squad", "AdjScore"]].sort_values(
        "AdjScore", ascending=False
    )
    
    print(display_df.to_string(index=False))
    
    # Print formation summary
    print(f"\nFormation: {FORMATION['DF']}-{FORMATION['MF']}-{FORMATION['FW']}")
    print(f"Total players selected: {len(best_xi)}")


def main() -> None:
    """Main function to run the EURO 2024 Best XI analysis."""
    setup_logging()
    
    try:
        # Load data
        players, teams = load_data(PLAYER_DATA_FILE, TEAM_DATA_FILE)
        
        # Clean data
        players = clean_dataframe(players)
        teams = clean_dataframe(teams)
        
        # Process team data
        teams = process_team_data(teams)
        
        # Process player data
        players = process_player_data(players, teams)
        
        # Select Best XI
        best_xi = select_best_players(players, FORMATION)
        
        # Display results
        display_results(best_xi)
        
    except Exception as e:
        logging.error(f"Analysis failed: {e}")
        return


if __name__ == "__main__":
    main()
