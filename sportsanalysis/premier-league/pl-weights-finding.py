"""
Premier League Weights Finding Analysis

This script analyzes Premier League player data to find optimal weights for
different performance metrics in player evaluation.

DATA SOURCE: This script requires Premier League player data from FBRef.com
- Player statistics: https://fbref.com/en/comps/9/stats/players/
- Squad statistics: https://fbref.com/en/comps/9/stats/squads/
"""

import pandas as pd
import numpy as np
from pathlib import Path
import os
from typing import Dict, List, Tuple
import logging


def setup_logging() -> None:
    """Setup logging configuration."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def get_file_path() -> str:
    """Get file path from user with helpful guidance."""
    print("=" * 80)
    print("⚽ PREMIER LEAGUE WEIGHTS FINDING ANALYSIS")
    print("=" * 80)
    print("\nThis analysis requires Premier League player data from FBRef.com")
    print("📊 DATA SOURCE: https://fbref.com/en/comps/9/stats/players/ (Premier League)")
    print("\nRequired CSV columns: Player, Squad, Pos, MP, Min, Gls, Ast, xG, xAG, etc.")
    print("\nPlease provide the path to your Premier League player statistics CSV file:")
    print("💡 Suggestion: premier_league_player_stats.csv")
    print("📁 Please enter the full path to your CSV file:")
    
    while True:
        file_path = input("File path: ").strip().strip('"')
        
        if not file_path:
            print("❌ Please provide a file path.")
            continue
            
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            print("Please check the path and try again.")
            continue
            
        if not file_path.lower().endswith('.csv'):
            print("❌ Please provide a CSV file.")
            continue
            
        return file_path


def load_data(file_path: str) -> pd.DataFrame:
    """Load Premier League player data from CSV file."""
    try:
        data_path = Path(file_path)
        df = pd.read_csv(data_path)
        return df
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except Exception as e:
        logging.error(f"Error loading file: {e}")
        raise


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare the dataset."""
    # Remove rows with missing critical data
    df = df.dropna(subset=['Player', 'Squad', 'Pos', 'MP', 'Min'])
    
    # Convert numeric columns
    numeric_cols = ['MP', 'Min', 'Gls', 'Ast', 'xG', 'xAG', 'PrgC', 'PrgP']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Filter for players with minimum playing time
    df = df[df['Min'] >= 270]  # At least 3 full matches
    
    return df


def calculate_performance_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate per-90 performance metrics."""
    # Calculate per-90 statistics
    per_90_cols = ['Gls', 'Ast', 'xG', 'xAG', 'PrgC', 'PrgP']
    for col in per_90_cols:
        if col in df.columns:
            df[f'{col}_per_90'] = df[col] / (df['Min'] / 90)
    
    # Calculate combined metrics
    if 'Gls_per_90' in df.columns and 'Ast_per_90' in df.columns:
        df['G+A_per_90'] = df['Gls_per_90'] + df['Ast_per_90']
    
    if 'xG_per_90' in df.columns and 'xAG_per_90' in df.columns:
        df['xG+xAG_per_90'] = df['xG_per_90'] + df['xAG_per_90']
    
    return df


def find_optimal_weights(df: pd.DataFrame) -> Dict[str, float]:
    """Find optimal weights for different performance metrics."""
    # Define metrics to analyze
    metrics = ['Gls_per_90', 'Ast_per_90', 'xG_per_90', 'xAG_per_90', 'PrgC_per_90', 'PrgP_per_90']
    available_metrics = [m for m in metrics if m in df.columns]
    
    if not available_metrics:
        raise ValueError("No valid performance metrics found in the dataset.")
    
    # Normalize metrics
    normalized_df = df[available_metrics].copy()
    for col in available_metrics:
        normalized_df[col] = (normalized_df[col] - normalized_df[col].mean()) / normalized_df[col].std()
    
    # Calculate correlation matrix
    corr_matrix = normalized_df.corr()
    
    # Find optimal weights based on correlation with goals
    if 'Gls_per_90' in available_metrics:
        goal_correlations = corr_matrix['Gls_per_90'].abs()
        weights = goal_correlations / goal_correlations.sum()
    else:
        # If no goals data, use equal weights
        weights = pd.Series(1/len(available_metrics), index=available_metrics)
    
    return weights.to_dict()


def calculate_player_scores(df: pd.DataFrame, weights: Dict[str, float]) -> pd.DataFrame:
    """Calculate weighted player scores."""
    df_scored = df.copy()
    
    # Normalize metrics for scoring
    for metric in weights.keys():
        if metric in df.columns:
            df_scored[f'{metric}_norm'] = (df[metric] - df[metric].mean()) / df[metric].std()
    
    # Calculate weighted score
    score_components = []
    for metric, weight in weights.items():
        norm_col = f'{metric}_norm'
        if norm_col in df_scored.columns:
            score_components.append(df_scored[norm_col] * weight)
    
    if score_components:
        df_scored['Performance_Score'] = sum(score_components)
    else:
        df_scored['Performance_Score'] = 0
    
    return df_scored


def display_results(weights: Dict[str, float], top_players: pd.DataFrame) -> None:
    """Display analysis results."""
    print("\n" + "="*60)
    print("⚽ PREMIER LEAGUE WEIGHTS ANALYSIS RESULTS")
    print("="*60)
    
    print(f"\n📊 OPTIMAL WEIGHTS FOR PERFORMANCE METRICS:")
    for metric, weight in sorted(weights.items(), key=lambda x: x[1], reverse=True):
        print(f"   {metric}: {weight:.3f}")
    
    print(f"\n🏆 TOP 10 PLAYERS BY PERFORMANCE SCORE:")
    display_cols = ['Player', 'Squad', 'Pos', 'Performance_Score']
    available_cols = [col for col in display_cols if col in top_players.columns]
    print(top_players[available_cols].head(10).to_string(index=False))


def main() -> None:
    """Main function to run the Premier League weights analysis."""
    setup_logging()
    
    try:
        # Get file path from user
        file_path = get_file_path()
        
        # Load and clean data
        df = load_data(file_path)
        df = clean_data(df)
        
        if df.empty:
            print("❌ No valid data found after cleaning.")
            return
        
        # Calculate performance metrics
        df = calculate_performance_metrics(df)
        
        # Find optimal weights
        weights = find_optimal_weights(df)
        
        # Calculate player scores
        df_scored = calculate_player_scores(df, weights)
        
        # Get top players
        top_players = df_scored.nlargest(20, 'Performance_Score')
        
        # Display results
        display_results(weights, top_players)
        
    except Exception as e:
        logging.error(f"Analysis failed: {e}")
        return


if __name__ == "__main__":
    main()