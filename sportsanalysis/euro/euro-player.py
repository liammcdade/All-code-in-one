import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from pathlib import Path
import logging
from typing import List

def pick_best(df: pd.DataFrame, pos_substring: str, n: int) -> pd.DataFrame:
    """Selects the top n players for a given position substring based on AdjScore."""
    return df[df["Pos"].str.contains(pos_substring)].nlargest(n, "AdjScore")

def main() -> None:
    """Compute and display the EURO 2024 Best XI based on player and team metrics."""
    logging.basicConfig(level=logging.INFO)
    player_path = Path("euro/euro2024-player.csv")
    team_path = Path("euro/euro2024-country.csv")
    try:
        players = pd.read_csv(player_path)
        teams = pd.read_csv(team_path)
    except FileNotFoundError as e:
        logging.error(f"File not found: {e.filename}")
        return
    except Exception as e:
        logging.error(f"Error loading file: {e}")
        return

    players.columns = players.columns.str.strip()
    teams.columns = teams.columns.str.strip()

    numeric_team_cols = [
        "Age", "Poss", "MP", "Starts", "Min", "90s", "Gls", "Ast", "G+A", "G-PK", "PK", "PKatt",
        "CrdY", "CrdR", "xG", "npxG", "xAG", "npxG+xAG", "PrgC", "PrgP"
    ]
    teams[numeric_team_cols] = teams[numeric_team_cols].apply(pd.to_numeric, errors="coerce")
    teams = teams[teams["Min"] > 0].dropna(subset=["Squad"])

    # Derived team metrics
    teams["Goals_per_90"] = teams["Gls"] / (teams["Min"] / 90)
    teams["Assists_per_90"] = teams["Ast"] / (teams["Min"] / 90)
    teams["xG_diff"] = teams["Gls"] - teams["xG"]
    teams["xGA_diff"] = teams["G+A"] - (teams["xG"] + teams["xAG"])
    teams["npxGxAG_per_90"] = teams["npxG+xAG"] / (teams["Min"] / 90)
    teams["Discipline"] = (teams["CrdY"] + 2 * teams["CrdR"]) / teams["Min"]
    teams["PrgC_per_90"] = teams["PrgC"] / (teams["Min"] / 90)
    teams["PrgP_per_90"] = teams["PrgP"] / (teams["Min"] / 90)

    # Squad-level stats normalization
    team_metrics = [
        "Goals_per_90", "Assists_per_90", "xG_diff", "xGA_diff", "npxGxAG_per_90",
        "Poss", "PrgC_per_90", "PrgP_per_90", "Discipline"
    ]
    scaler = MinMaxScaler()
    teams[team_metrics] = scaler.fit_transform(teams[team_metrics])
    teams["Discipline"] *= -1
    teams["SquadScore"] = teams[team_metrics].sum(axis=1)

    # Adjust for number of matches played in the squad level
    teams["AvgMatches"] = teams.groupby("Squad")["MP"].transform("mean")
    teams["MatchFactor"] = 1 - MinMaxScaler().fit_transform(teams[["AvgMatches"]])

    # PLAYER PERFORMANCE: Clean and preprocess player data
    players = players[players["Min"] > 0].dropna(subset=["Player", "Squad", "Pos"])

    # Derived player metrics
    players["Goals_per_90"] = players["Gls"] / (players["Min"] / 90)
    players["Assists_per_90"] = players["Ast"] / (players["Min"] / 90)
    players["xG_diff"] = players["Gls"] - players["xG"]
    players["xGA_diff"] = players["G+A"] - (players["xG"] + players["xAG"])
    players["npxGxAG_per_90"] = players["npxG+xAG"] / (players["Min"] / 90)
    players["Discipline"] = (players["CrdY"] + 2 * players["CrdR"]) / players["Min"]
    players["PrgC_per_90"] = players["PrgC"] / (players["Min"] / 90)
    players["PrgP_per_90"] = players["PrgP"] / (players["Min"] / 90)

    # Normalize player metrics
    player_metrics = [
        "Goals_per_90", "Assists_per_90", "xG_diff", "xGA_diff", "npxGxAG_per_90",
        "PrgC_per_90", "PrgP_per_90", "Discipline"
    ]
    scaler = MinMaxScaler()
    players[player_metrics] = scaler.fit_transform(players[player_metrics])
    players["Discipline"] *= -1
    players["RawScore"] = players[player_metrics].sum(axis=1)

    # MERGE squad performance data into players dataset
    players = players.merge(
        teams[["Squad", "SquadScore", "MatchFactor"]], on="Squad", how="left"
    )

    # ESTIMATE player performance relative to match played
    players["PlayerMatchWeight"] = players["MP"] / players["MP"].max()

    # Adjusted player score (individual performance + squad quality + match factor)
    players["AdjScore"] = (
        players["RawScore"]
        * (1 + players["SquadScore"])
        * (1 + players["MatchFactor"])
        * players["PlayerMatchWeight"]
    )

    # SELECT BEST XI (4-3-3 formation as default)
    goalkeepers = pick_best(players, "GK", 1)
    defenders = pick_best(players, "DF", 4)
    midfielders = pick_best(players, "MF", 3)
    forwards = pick_best(players, "FW", 3)

    # Combine selected players
    best11 = pd.concat([goalkeepers, defenders, midfielders, forwards])
    best11 = best11.drop_duplicates(subset="Player", keep="first")

    print("🏆 EURO 2024 BEST XI (Adjusted for Team Quality and Tournament Progress):\n")
    print(
        best11[["Player", "Pos", "Squad", "AdjScore"]]
        .sort_values("AdjScore", ascending=False)
        .to_string(index=False)
    )

if __name__ == "__main__":
    main()
