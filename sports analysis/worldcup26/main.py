import random
import math
from collections import defaultdict
from tqdm.auto import tqdm  # <-- Add tqdm for progress bars
import argparse
from typing import List, Tuple

# FIFA_RANKINGS updated as of April 3, 2025, based on publicly available data.
FIFA_RANKINGS = {
    "Argentina": 1886.16,
    "Spain": 1854.64,
    "France": 1852.71,
    "England": 1819.2,
    "Brazil": 1776.03,
    "Netherlands": 1752.44,
    "Portugal": 1750.08,
    "Belgium": 1735.75,
    "Italy": 1718.31,
    "Germany": 1716.98,
    "Croatia": 1698.66,
    "Morocco": 1694.24,
    "Uruguay": 1679.49,
    "Colombia": 1679.04,
    "Japan": 1652.64,
    "USA": 1648.81,
    "Mexico": 1646.94,
    "IR Iran": 1637.39,
    "Senegal": 1630.32,
    "Switzerland": 1624.75,
    "Denmark": 1617.54,
    "Austria": 1580.22,
    "Korea Republic": 1574.93,
    "Ecuador": 1567.95,
    "Ukraine": 1559.81,
    "Australia": 1554.55,
    "Türkiye": 1551.47,
    "Sweden": 1536.05,
    "Wales": 1535.57,
    "Canada": 1531.58,
    "Serbia": 1523.91,
    "Egypt": 1518.79,
    "Panama": 1517.66,
    "Poland": 1517.35,
    "Russia": 1516.27,
    "Algeria": 1507.17,
    "Hungary": 1503.34,
    "Norway": 1497.18,
    "Czechia": 1491.43,
    "Greece": 1489.82,
    "Côte d'Ivoire": 1487.27,
    "Peru": 1483.48,
    "Nigeria": 1481.35,
    "Scotland": 1480.3,
    "Romania": 1479.22,
    "Slovakia": 1477.78,
    "Venezuela": 1476.84,
    "Paraguay": 1475.93,
    "Tunisia": 1474.1,
    "Cameroon": 1465.72,
    "Slovenia": 1462.66,
    "Chile": 1461.91,
    "Mali": 1460.23,
    "Costa Rica": 1459.13,
    "Qatar": 1456.58,
    "South Africa": 1445.01,
    "Uzbekistan": 1437.02,
    "Saudi Arabia": 1418.96,
    "Iraq": 1413.4,
    "Republic of Ireland": 1412.23,
    "North Macedonia": 1406.87,
    "Bosnia and Herzegovina": 1400.99,
    "Ghana": 1399.78,
    "DR Congo": 1395.2,
    "Finland": 1393.77,
    "Burkina Faso": 1385.61,
    "Iceland": 1383.07,
    "Albania": 1374.88,
    "Honduras": 1373.07,
    "United Arab Emirates": 1368.14,
    "Jordan": 1283.48,
    "New Zealand": 1221.75,
    "New Caledonia": 1058.0,
    "Kuwait": 1109.81,
    "India": 1132.03,
    "Afghanistan": 919.32,
    "Kyrgyz Republic": 1297.05,
    "Oman": 1307.72,
    "Palestine": 1269.83,
    "Indonesia": 1102.26,
    "China PR": 1275.25,
    "Bahrain": 1128.53,
    "Congo": 1204.68,
    "Tanzania": 1184.28,
    "Niger": 1072.07,
    "Zambia": 1241.65,
    "Cuba": 1291.68,
    "Bermuda": 1198.81,
    "Cayman Islands": 951.18,
    "Antigua and Barbuda": 1040.69,
    "Grenada": 1150.77,
    "Saint Kitts and Nevis": 998.67,
    "Bahamas": 872.2,
    "Aruba": 978.89,
    "Barbados": 940.33,
    "Saint Lucia": 1026.83,
    "Guyana": 1069.95,
    "Montserrat": 1061.5,
    "Belize": 1007.41,
    "Dominican Republic": 1181.82,
    "Dominica": 927.87,
    "British Virgin Islands": 809.8,
    "Saint Vincent and the Grenadines": 1039.67,
    "Anguilla": 786.9,
    "Puerto Rico": 1083.3,
    "Bolivia": 1302.2,
    "Mauritania": 1206.18,
    "Togo": 1162.77,
    "Sudan": 1120.35,
    "South Sudan": 948.33,
    "Benin": 1146.43,
    "Zimbabwe": 1092.36,
    "Rwanda": 1080.35,
    "Lesotho": 1047.88,
    "Cape Verde": 1435.32,
    "Angola": 1276.46,
    "Libya": 1182.26,
    "Eswatini": 966.86,
    "Mauritius": 903.07,
    "Gabon": 1290.35,
    "Kenya": 1166.19,
    "The Gambia": 1127.32,
    "Burundi": 1089.47,
    "Seychelles": 834.61,
    "Guinea": 1345.86,
    "Uganda": 1184.2,
    "Mozambique": 1166.7,
    "Botswana": 1083.56,
    "Somalia": 822.45,
    "Equatorial Guinea": 1238.19,
    "Namibia": 1152.06,
    "Malawi": 1109.84,
    "Liberia": 1039.69,
    "Sao Tome and Principe": 878.0,
    "Djibouti": 863.09,
    "Ethiopia": 1060.03,
    "Guinea-Bissau": 1218.4,
    "Sierra Leone": 1087.72,
    "North Korea": 1153.25,
    "Thailand": 1176.4,
    "Vietnam": 1169.96,
    "Syria": 1088.19,
    "Lebanon": 1010.42,
    "Tajikistan": 1100.91,
    "Bulgaria": 1365.17,
    "Israel": 1358.33,
    "Georgia": 1302.26,
    "Luxembourg": 1285.44,
    "Cyprus": 1155.24,
    "Kosovo": 1119.5,
    "Lithuania": 1062.24,
    "Estonia": 1007.41,
    "Latvia": 986.79,
    "Azerbaijan": 1159.26,
    "Kazakhstan": 1117.84,
    "Armenia": 1111.45,
    "Malta": 955.51,
    "Moldova": 909.11,
    "Gibraltar": 822.61,
    "San Marino": 743.08,
    "Liechtenstein": 724.87,
    "Andorra": 894.49,
    "Faroe Islands": 1037.13,
    "Madagascar": 1165.75,
    "Comoros": 1137.9,
    "Central African Republic": 1086.56,
    "Chad": 903.07,
    "Northern Ireland": 1300.0,
    "Belarus": 1250.0,
    "Trinidad and Tobago": 1350.0,
    "Curacao": 1300.0,
    "Haiti": 1280.0,
    "Nicaragua": 1270.0,
    "Guatemala": 1320.0,
    "Jamaica": 1400.0,
    "Suriname": 1250.0,
    "El Salvador": 1200.0,
    "Greenland": 500.0,
}


class Team:
    def __init__(self, name, confederation, ranking_points):
        self.name = name
        self.confederation = confederation
        self.ranking_points = ranking_points
        self.group_stats = {
            "Pld": 0,
            "W": 0,
            "D": 0,
            "L": 0,
            "GF": 0,
            "GA": 0,
            "GD": 0,
            "Pts": 0,
        }

    def __repr__(self):
        return f"Team({self.name}, {self.ranking_points:.2f})"


teams = {}


def get_team(name):
    """Retrieves a Team object by name, creating it if it doesn't exist."""
    if name not in teams:
        ranking_points = FIFA_RANKINGS.get(name, 500.0)
        teams[name] = Team(name, "Unknown", ranking_points)
    return teams[name]


def simulate_match(team1, team2):
    """Simulates a single football match between two teams based on their FIFA ranking points."""
    elo_diff = team1.ranking_points - team2.ranking_points
    base_expected_goals = 1.3
    scale_factor = 0.002
    expected_goals_team1 = base_expected_goals * math.exp(scale_factor * elo_diff)
    expected_goals_team2 = base_expected_goals * math.exp(scale_factor * -elo_diff)
    goals_team1 = max(0, int(random.gauss(expected_goals_team1, 1.0) + 0.5))
    goals_team2 = max(0, int(random.gauss(expected_goals_team2, 1.0) + 0.5))
    return goals_team1, goals_team2


def update_group_standings(standings, team_name, goals_for, goals_against):
    """Updates a team's statistics in a group standings dictionary after a match."""
    team_stats = standings[team_name]
    team_stats["Pld"] += 1
    team_stats["GF"] += goals_for
    team_stats["GA"] += goals_against
    team_stats["GD"] = team_stats["GF"] - team_stats["GA"]
    if goals_for > goals_against:
        team_stats["W"] += 1
        team_stats["Pts"] += 3
    elif goals_for == goals_against:
        team_stats["D"] += 1
        team_stats["Pts"] += 1
    else:
        team_stats["L"] += 1


def sort_group(standings_list):
    """Sorts a list of team standings based on points, goal difference, goals scored, and FIFA ranking."""
    return sorted(
        standings_list,
        key=lambda x: (x["Pts"], x["GD"], x["GF"], get_team(x["Team"]).ranking_points),
        reverse=True,
    )


def simulate_group_with_initial_standings(
    group_name,
    group_teams_names,
    initial_standings_data,
    num_qualify_direct=0,
    num_to_playoff=0,
    total_matches_per_team=None,
    verbose=True,
):
    """Simulates a group stage, starting from provided initial standings."""
    if verbose:
        print(f"\n--- Simulating Group: {group_name} (from initial standings) ---")
    standings = {
        team_name: initial_standings_data.get(
            team_name,
            {"Pld": 0, "W": 0, "D": 0, "L": 0, "GF": 0, "GA": 0, "GD": 0, "Pts": 0},
        ).copy()
        for team_name in group_teams_names
    }
    if verbose:
        print(f"Initial Standings for {group_name}:")
        print(
            "{:<20} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5}".format(
                "Team", "Pld", "W", "D", "L", "GF", "GA", "GD", "Pts"
            )
        )
        for team_name in group_teams_names:
            stats = standings[team_name]
            print(
                "{:<20} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5}".format(
                    team_name,
                    stats["Pld"],
                    stats["W"],
                    stats["D"],
                    stats["L"],
                    stats["GF"],
                    stats["GA"],
                    stats["GD"],
                    stats["Pts"],
                )
            )
    if len(group_teams_names) > 1:
        legs_per_pair = 2
        if group_name.startswith(
            "CONCACAF_Second_Round_Group_"
        ) or group_name.startswith("AFC_Fourth_Round_Group_"):
            legs_per_pair = 1
        total_possible_matches_in_group = (
            len(group_teams_names) * (len(group_teams_names) - 1) // 2
        ) * legs_per_pair
        current_total_matches_played = sum(s["Pld"] for s in standings.values()) // 2
        matches_to_simulate_count = (
            total_possible_matches_in_group - current_total_matches_played
        )
        if verbose:
            print(f"Total possible matches in group: {total_possible_matches_in_group}")
            print(f"Current total matches played: {current_total_matches_played}")
            print(f"Matches to simulate: {matches_to_simulate_count}")
        for _ in range(matches_to_simulate_count):
            eligible_teams = [
                t_name
                for t_name in group_teams_names
                if standings[t_name]["Pld"] < total_matches_per_team
            ]
            if len(eligible_teams) < 2:
                if verbose:
                    print(
                        "Not enough eligible teams to simulate remaining matches in this group."
                    )
                break
            team1_name, team2_name = random.sample(eligible_teams, 2)
            t1 = get_team(team1_name)
            t2 = get_team(team2_name)
            goals1, goals2 = simulate_match(t1, t2)
            update_group_standings(standings, team1_name, goals1, goals2)
            update_group_standings(standings, team2_name, goals2, goals1)
    final_standings_list = [
        {"Team": team_name, **stats} for team_name, stats in standings.items()
    ]
    sorted_standings = sort_group(final_standings_list)
    if verbose:
        print(f"--- {group_name} Final Standings (after simulation) ---")
        print(
            "{:<20} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5}".format(
                "Team", "Pld", "W", "D", "L", "GF", "GA", "GD", "Pts"
            )
        )
        for team_stat in sorted_standings:
            print(
                "{:<20} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5}".format(
                    team_stat["Team"],
                    team_stat["Pld"],
                    team_stat["W"],
                    team_stat["D"],
                    team_stat["L"],
                    team_stat["GF"],
                    team_stat["GA"],
                    team_stat["GD"],
                    team_stat["Pts"],
                )
            )
    qualified = [t["Team"] for t in sorted_standings[:num_qualify_direct]]
    playoff = [
        t["Team"]
        for t in sorted_standings[
            num_qualify_direct : num_qualify_direct + num_to_playoff
        ]
    ]
    remaining = [
        t["Team"] for t in sorted_standings[num_qualify_direct + num_to_playoff :]
    ]
    if verbose:
        print(f"\nQualified from {group_name}: {qualified}")
        if playoff:
            print(f"Advance to next round/playoff from {group_name}: {playoff}")
    return qualified, playoff, remaining, standings


def simulate_knockout(teams_for_knockout, round_name="Knockout Round", verbose=True):
    """
    Simulates a knockout tournament recursively.
    Teams are sorted by ranking for pairing (higher ranked plays lower ranked).
    """
    if verbose:
        print(f"\n--- Simulating {round_name} ---")
    if len(teams_for_knockout) < 2:
        if teams_for_knockout:
            if verbose:
                print(
                    f"Only one team left in {round_name}: {teams_for_knockout[0]} advances by default."
                )
            return teams_for_knockout
        if verbose:
            print(f"Not enough teams for {round_name}.")
        return []
    teams_for_knockout.sort(key=lambda x: get_team(x).ranking_points, reverse=True)
    current_round_winners = []
    num_matches = len(teams_for_knockout) // 2
    for i in range(num_matches):
        team1_name = teams_for_knockout[i]
        team2_name = teams_for_knockout[len(teams_for_knockout) - 1 - i]
        if verbose:
            print(f"Match: {team1_name} vs {team2_name}")
        t1 = get_team(team1_name)
        t2 = get_team(team2_name)
        goals1, goals2 = simulate_match(t1, t2)
        if verbose:
            print(f"  {t1.name} {goals1}-{goals2} {t2.name}")
        if goals1 == goals2:
            if verbose:
                print(
                    "  Match drawn, simulating extra time and penalties (higher ranked team wins)."
                )
            if t1.ranking_points > t2.ranking_points:
                current_round_winners.append(t1.name)
                if verbose:
                    print(f"  {t1.name} wins.")
            else:
                current_round_winners.append(t2.name)
                if verbose:
                    print(f"  {t2.name} wins.")
        elif goals1 > goals2:
            current_round_winners.append(t1.name)
        else:
            current_round_winners.append(t2.name)
    if len(teams_for_knockout) % 2 != 0:
        bye_team = teams_for_knockout[num_matches * 2]
        current_round_winners.append(bye_team)
        if verbose:
            print(f"  {bye_team} gets a bye to the next round.")
    if len(current_round_winners) > 1:
        return simulate_knockout(
            current_round_winners,
            round_name=f"Next Stage of {round_name}",
            verbose=verbose,
        )
    else:
        return current_round_winners


# --- Static Qualification Data ---
STATIC_WORLD_CUP_QUALIFIED = {
    "CONCACAF": ["Canada", "Mexico", "USA"],
    "CONMEBOL": ["Argentina"],
    "AFC": ["Japan", "IR Iran", "Uzbekistan", "Korea Republic", "Jordan"],
    "OFC": ["New Zealand"],
}

STATIC_INTER_CONFED_PLAYOFF_TEAMS = {
    "OFC": "New Caledonia",
}

# --- LIVE STANDINGS DATA ---
LIVE_STANDINGS_DATA = {
    "CONMEBOL": {
        "Argentina": {
            "Pld": 16,
            "W": 11,
            "D": 2,
            "L": 3,
            "GF": 28,
            "GA": 9,
            "GD": 19,
            "Pts": 35,
        },
        "Ecuador": {
            "Pld": 16,
            "W": 7,
            "D": 7,
            "L": 2,
            "GF": 13,
            "GA": 5,
            "GD": 8,
            "Pts": 25,
        },
        "Brazil": {
            "Pld": 16,
            "W": 7,
            "D": 4,
            "L": 5,
            "GF": 21,
            "GA": 16,
            "GD": 5,
            "Pts": 25,
        },
        "Uruguay": {
            "Pld": 16,
            "W": 6,
            "D": 6,
            "L": 4,
            "GF": 19,
            "GA": 12,
            "GD": 7,
            "Pts": 24,
        },
        "Paraguay": {
            "Pld": 16,
            "W": 6,
            "D": 6,
            "L": 4,
            "GF": 13,
            "GA": 10,
            "GD": 3,
            "Pts": 24,
        },
        "Colombia": {
            "Pld": 16,
            "W": 5,
            "D": 7,
            "L": 4,
            "GF": 19,
            "GA": 15,
            "GD": 4,
            "Pts": 22,
        },
        "Venezuela": {
            "Pld": 16,
            "W": 4,
            "D": 6,
            "L": 6,
            "GF": 15,
            "GA": 19,
            "GD": -4,
            "Pts": 18,
        },
        "Bolivia": {
            "Pld": 16,
            "W": 5,
            "D": 2,
            "L": 9,
            "GF": 16,
            "GA": 32,
            "GD": -16,
            "Pts": 17,
        },
        "Peru": {
            "Pld": 16,
            "W": 2,
            "D": 6,
            "L": 8,
            "GF": 6,
            "GA": 17,
            "GD": -11,
            "Pts": 12,
        },
        "Chile": {
            "Pld": 16,
            "W": 2,
            "D": 4,
            "L": 10,
            "GF": 9,
            "GA": 24,
            "GD": -15,
            "Pts": 10,
        },
    },
    "CAF": {
        "CAF_Group_A": {
            "Egypt": {
                "Pld": 6,
                "W": 5,
                "D": 1,
                "L": 0,
                "GF": 14,
                "GA": 2,
                "GD": 12,
                "Pts": 16,
            },
            "Burkina Faso": {
                "Pld": 6,
                "W": 3,
                "D": 2,
                "L": 1,
                "GF": 13,
                "GA": 7,
                "GD": 6,
                "Pts": 11,
            },
            "Sierra Leone": {
                "Pld": 6,
                "W": 2,
                "D": 2,
                "L": 2,
                "GF": 7,
                "GA": 7,
                "GD": 0,
                "Pts": 8,
            },
            "Ethiopia": {
                "Pld": 6,
                "W": 1,
                "D": 3,
                "L": 2,
                "GF": 7,
                "GA": 7,
                "GD": 0,
                "Pts": 6,
            },
            "Guinea-Bissau": {
                "Pld": 6,
                "W": 1,
                "D": 3,
                "L": 2,
                "GF": 5,
                "GA": 7,
                "GD": -2,
                "Pts": 6,
            },
            "Djibouti": {
                "Pld": 6,
                "W": 0,
                "D": 1,
                "L": 5,
                "GF": 4,
                "GA": 20,
                "GD": -16,
                "Pts": 1,
            },
        },
        "CAF_Group_B": {
            "DR Congo": {
                "Pld": 6,
                "W": 4,
                "D": 1,
                "L": 1,
                "GF": 7,
                "GA": 2,
                "GD": 5,
                "Pts": 13,
            },
            "Senegal": {
                "Pld": 6,
                "W": 3,
                "D": 3,
                "L": 0,
                "GF": 8,
                "GA": 1,
                "GD": 7,
                "Pts": 12,
            },
            "Sudan": {
                "Pld": 6,
                "W": 3,
                "D": 3,
                "L": 0,
                "GF": 8,
                "GA": 2,
                "GD": 6,
                "Pts": 12,
            },
            "Togo": {
                "Pld": 6,
                "W": 0,
                "D": 4,
                "L": 2,
                "GF": 4,
                "GA": 7,
                "GD": -3,
                "Pts": 4,
            },
            "South Sudan": {
                "Pld": 6,
                "W": 0,
                "D": 3,
                "L": 3,
                "GF": 2,
                "GA": 10,
                "GD": -8,
                "Pts": 3,
            },
            "Mauritania": {
                "Pld": 6,
                "W": 0,
                "D": 2,
                "L": 4,
                "GF": 2,
                "GA": 9,
                "GD": -7,
                "Pts": 2,
            },
        },
        "CAF_Group_C": {
            "South Africa": {
                "Pld": 6,
                "W": 4,
                "D": 1,
                "L": 1,
                "GF": 10,
                "GA": 5,
                "GD": 5,
                "Pts": 13,
            },
            "Rwanda": {
                "Pld": 6,
                "W": 2,
                "D": 2,
                "L": 2,
                "GF": 4,
                "GA": 4,
                "GD": 0,
                "Pts": 8,
            },
            "Benin": {
                "Pld": 6,
                "W": 2,
                "D": 2,
                "L": 2,
                "GF": 6,
                "GA": 7,
                "GD": -1,
                "Pts": 8,
            },
            "Nigeria": {
                "Pld": 6,
                "W": 1,
                "D": 4,
                "L": 1,
                "GF": 7,
                "GA": 6,
                "GD": 1,
                "Pts": 7,
            },
            "Lesotho": {
                "Pld": 6,
                "W": 1,
                "D": 3,
                "L": 2,
                "GF": 4,
                "GA": 5,
                "GD": -1,
                "Pts": 6,
            },
            "Zimbabwe": {
                "Pld": 6,
                "W": 0,
                "D": 4,
                "L": 2,
                "GF": 5,
                "GA": 9,
                "GD": -4,
                "Pts": 4,
            },
        },
        "CAF_Group_D": {
            "Cape Verde": {
                "Pld": 6,
                "W": 4,
                "D": 1,
                "L": 1,
                "GF": 7,
                "GA": 5,
                "GD": 2,
                "Pts": 13,
            },
            "Cameroon": {
                "Pld": 6,
                "W": 3,
                "D": 3,
                "L": 0,
                "GF": 12,
                "GA": 4,
                "GD": 8,
                "Pts": 12,
            },
            "Libya": {
                "Pld": 6,
                "W": 2,
                "D": 2,
                "L": 2,
                "GF": 6,
                "GA": 7,
                "GD": -1,
                "Pts": 8,
            },
            "Angola": {
                "Pld": 6,
                "W": 1,
                "D": 4,
                "L": 1,
                "GF": 4,
                "GA": 4,
                "GD": 0,
                "Pts": 7,
            },
            "Mauritius": {
                "Pld": 6,
                "W": 1,
                "D": 2,
                "L": 3,
                "GF": 6,
                "GA": 10,
                "GD": -4,
                "Pts": 5,
            },
            "Eswatini": {
                "Pld": 6,
                "W": 0,
                "D": 2,
                "L": 4,
                "GF": 4,
                "GA": 9,
                "GD": -5,
                "Pts": 2,
            },
        },
        "CAF_Group_E": {
            "Morocco": {
                "Pld": 5,
                "W": 5,
                "D": 0,
                "L": 0,
                "GF": 14,
                "GA": 2,
                "GD": 12,
                "Pts": 15,
            },
            "Tanzania": {
                "Pld": 5,
                "W": 3,
                "D": 0,
                "L": 2,
                "GF": 5,
                "GA": 4,
                "GD": 1,
                "Pts": 9,
            },
            "Zambia": {
                "Pld": 5,
                "W": 2,
                "D": 0,
                "L": 3,
                "GF": 9,
                "GA": 7,
                "GD": 2,
                "Pts": 6,
            },
            "Niger": {
                "Pld": 4,
                "W": 2,
                "D": 0,
                "L": 2,
                "GF": 6,
                "GA": 4,
                "GD": 2,
                "Pts": 6,
            },
            "Congo": {
                "Pld": 5,
                "W": 0,
                "D": 0,
                "L": 5,
                "GF": 2,
                "GA": 19,
                "GD": -17,
                "Pts": 0,
            },
            "Eritrea": {
                "Pld": 0,
                "W": 0,
                "D": 0,
                "L": 0,
                "GF": 0,
                "GA": 0,
                "GD": 0,
                "Pts": 0,
            },
        },
        "CAF_Group_F": {
            "Ivory Coast": {
                "Pld": 6,
                "W": 5,
                "D": 1,
                "L": 0,
                "GF": 14,
                "GA": 0,
                "GD": 14,
                "Pts": 16,
            },
            "Gabon": {
                "Pld": 6,
                "W": 5,
                "D": 0,
                "L": 1,
                "GF": 12,
                "GA": 6,
                "GD": 6,
                "Pts": 15,
            },
            "Burundi": {
                "Pld": 6,
                "W": 3,
                "D": 1,
                "L": 2,
                "GF": 13,
                "GA": 7,
                "GD": 6,
                "Pts": 10,
            },
            "Kenya": {
                "Pld": 6,
                "W": 1,
                "D": 3,
                "L": 2,
                "GF": 11,
                "GA": 8,
                "GD": 3,
                "Pts": 6,
            },
            "Gambia": {
                "Pld": 6,
                "W": 1,
                "D": 1,
                "L": 4,
                "GF": 12,
                "GA": 13,
                "GD": -1,
                "Pts": 4,
            },
            "Seychelles": {
                "Pld": 6,
                "W": 0,
                "D": 0,
                "L": 6,
                "GF": 2,
                "GA": 30,
                "GD": -28,
                "Pts": 0,
            },
        },
        "CAF_Group_G": {
            "Algeria": {
                "Pld": 6,
                "W": 5,
                "D": 0,
                "L": 1,
                "GF": 16,
                "GA": 6,
                "GD": 10,
                "Pts": 15,
            },
            "Mozambique": {
                "Pld": 6,
                "W": 4,
                "D": 0,
                "L": 2,
                "GF": 10,
                "GA": 11,
                "GD": -1,
                "Pts": 12,
            },
            "Botswana": {
                "Pld": 6,
                "W": 3,
                "D": 0,
                "L": 3,
                "GF": 9,
                "GA": 8,
                "GD": 1,
                "Pts": 9,
            },
            "Uganda": {
                "Pld": 6,
                "W": 3,
                "D": 0,
                "L": 3,
                "GF": 6,
                "GA": 7,
                "GD": -1,
                "Pts": 9,
            },
            "Guinea": {
                "Pld": 6,
                "W": 2,
                "D": 1,
                "L": 3,
                "GF": 4,
                "GA": 5,
                "GD": -1,
                "Pts": 7,
            },
            "Somalia": {
                "Pld": 6,
                "W": 0,
                "D": 1,
                "L": 5,
                "GF": 3,
                "GA": 11,
                "GD": -8,
                "Pts": 1,
            },
        },
        "CAF_Group_H": {
            "Tunisia": {
                "Pld": 6,
                "W": 5,
                "D": 1,
                "L": 0,
                "GF": 9,
                "GA": 0,
                "GD": 9,
                "Pts": 16,
            },
            "Equatorial Guinea": {
                "Pld": 6,
                "W": 2,
                "D": 1,
                "L": 3,
                "GF": 4,
                "GA": 8,
                "GD": -4,
                "Pts": 7,
            },
            "Namibia": {
                "Pld": 6,
                "W": 3,
                "D": 3,
                "L": 0,
                "GF": 8,
                "GA": 2,
                "GD": 6,
                "Pts": 12,
            },
            "Liberia": {
                "Pld": 6,
                "W": 3,
                "D": 1,
                "L": 2,
                "GF": 7,
                "GA": 4,
                "GD": 3,
                "Pts": 10,
            },
            "Malawi": {
                "Pld": 6,
                "W": 2,
                "D": 0,
                "L": 4,
                "GF": 4,
                "GA": 6,
                "GD": -2,
                "Pts": 6,
            },
            "Sao Tome and Principe": {
                "Pld": 6,
                "W": 0,
                "D": 0,
                "L": 6,
                "GF": 2,
                "GA": 14,
                "GD": -12,
                "Pts": 0,
            },
        },
        "CAF_Group_I": {
            "Ghana": {
                "Pld": 6,
                "W": 5,
                "D": 0,
                "L": 1,
                "GF": 15,
                "GA": 5,
                "GD": 10,
                "Pts": 15,
            },
            "Comoros": {
                "Pld": 6,
                "W": 4,
                "D": 0,
                "L": 2,
                "GF": 9,
                "GA": 7,
                "GD": 2,
                "Pts": 12,
            },
            "Madagascar": {
                "Pld": 6,
                "W": 3,
                "D": 1,
                "L": 2,
                "GF": 9,
                "GA": 6,
                "GD": 3,
                "Pts": 10,
            },
            "Mali": {
                "Pld": 6,
                "W": 2,
                "D": 3,
                "L": 1,
                "GF": 8,
                "GA": 4,
                "GD": 4,
                "Pts": 9,
            },
            "Central African Republic": {
                "Pld": 6,
                "W": 1,
                "D": 2,
                "L": 3,
                "GF": 8,
                "GA": 13,
                "GD": -5,
                "Pts": 5,
            },
            "Chad": {
                "Pld": 6,
                "W": 0,
                "D": 0,
                "L": 6,
                "GF": 1,
                "GA": 15,
                "GD": -14,
                "Pts": 0,
            },
        },
    },
    "AFC": {
        "AFC_Third_Round_Group_A": {
            "IR Iran": {
                "Pld": 9,
                "W": 6,
                "D": 2,
                "L": 1,
                "GF": 16,
                "GA": 8,
                "GD": 8,
                "Pts": 20,
            },
            "Uzbekistan": {
                "Pld": 9,
                "W": 5,
                "D": 3,
                "L": 1,
                "GF": 11,
                "GA": 7,
                "GD": 4,
                "Pts": 18,
            },
            "United Arab Emirates": {
                "Pld": 9,
                "W": 4,
                "D": 2,
                "L": 3,
                "GF": 14,
                "GA": 7,
                "GD": 7,
                "Pts": 14,
            },
            "Qatar": {
                "Pld": 9,
                "W": 4,
                "D": 1,
                "L": 4,
                "GF": 17,
                "GA": 21,
                "GD": -4,
                "Pts": 13,
            },
            "Kyrgyz Republic": {
                "Pld": 9,
                "W": 2,
                "D": 1,
                "L": 6,
                "GF": 11,
                "GA": 17,
                "GD": -6,
                "Pts": 7,
            },
            "North Korea": {
                "Pld": 9,
                "W": 0,
                "D": 3,
                "L": 6,
                "GF": 9,
                "GA": 18,
                "GD": -9,
                "Pts": 3,
            },
        },
        "AFC_Third_Round_Group_B": {
            "South Korea": {
                "Pld": 9,
                "W": 5,
                "D": 4,
                "L": 0,
                "GF": 16,
                "GA": 7,
                "GD": 9,
                "Pts": 19,
            },
            "Jordan": {
                "Pld": 9,
                "W": 4,
                "D": 4,
                "L": 1,
                "GF": 16,
                "GA": 7,
                "GD": 9,
                "Pts": 16,
            },
            "Iraq": {
                "Pld": 9,
                "W": 3,
                "D": 3,
                "L": 3,
                "GF": 8,
                "GA": 9,
                "GD": -1,
                "Pts": 12,
            },
            "Oman": {
                "Pld": 9,
                "W": 3,
                "D": 1,
                "L": 5,
                "GF": 8,
                "GA": 13,
                "GD": -5,
                "Pts": 10,
            },
            "Palestine": {
                "Pld": 9,
                "W": 2,
                "D": 3,
                "L": 4,
                "GF": 9,
                "GA": 12,
                "GD": -3,
                "Pts": 9,
            },
            "Kuwait": {
                "Pld": 9,
                "W": 0,
                "D": 5,
                "L": 4,
                "GF": 7,
                "GA": 16,
                "GD": -9,
                "Pts": 5,
            },
        },
        "AFC_Third_Round_Group_C": {
            "Japan": {
                "Pld": 9,
                "W": 6,
                "D": 2,
                "L": 1,
                "GF": 24,
                "GA": 3,
                "GD": 21,
                "Pts": 20,
            },
            "Australia": {
                "Pld": 9,
                "W": 4,
                "D": 4,
                "L": 1,
                "GF": 14,
                "GA": 6,
                "GD": 8,
                "Pts": 16,
            },
            "Saudi Arabia": {
                "Pld": 9,
                "W": 3,
                "D": 4,
                "L": 2,
                "GF": 6,
                "GA": 6,
                "GD": 0,
                "Pts": 13,
            },
            "Indonesia": {
                "Pld": 9,
                "W": 3,
                "D": 3,
                "L": 3,
                "GF": 9,
                "GA": 14,
                "GD": -5,
                "Pts": 12,
            },
            "Bahrain": {
                "Pld": 9,
                "W": 1,
                "D": 3,
                "L": 5,
                "GF": 5,
                "GA": 15,
                "GD": -10,
                "Pts": 6,
            },
            "China PR": {
                "Pld": 9,
                "W": 2,
                "D": 0,
                "L": 7,
                "GF": 6,
                "GA": 20,
                "GD": -14,
                "Pts": 6,
            },
        },
    },
    "CONCACAF_Second_Round": {
        "CONCACAF_Second_Round_Group_A": {
            "Honduras": {
                "Pld": 2,
                "W": 2,
                "D": 0,
                "L": 0,
                "GF": 7,
                "GA": 0,
                "GD": 7,
                "Pts": 6,
            },
            "Cuba": {
                "Pld": 2,
                "W": 1,
                "D": 0,
                "L": 1,
                "GF": 1,
                "GA": 1,
                "GD": 0,
                "Pts": 3,
            },
            "Cayman Islands": {
                "Pld": 2,
                "W": 1,
                "D": 0,
                "L": 1,
                "GF": 2,
                "GA": 2,
                "GD": 0,
                "Pts": 3,
            },
            "Antigua and Barbuda": {
                "Pld": 2,
                "W": 0,
                "D": 1,
                "L": 1,
                "GF": 1,
                "GA": 2,
                "GD": -1,
                "Pts": 1,
            },
            "Bermuda": {
                "Pld": 2,
                "W": 0,
                "D": 1,
                "L": 1,
                "GF": 2,
                "GA": 7,
                "GD": -5,
                "Pts": 1,
            },
        },
        "CONCACAF_Second_Round_Group_B": {
            "Costa Rica": {
                "Pld": 2,
                "W": 2,
                "D": 0,
                "L": 0,
                "GF": 7,
                "GA": 0,
                "GD": 7,
                "Pts": 6,
            },
            "Trinidad and Tobago": {
                "Pld": 2,
                "W": 1,
                "D": 1,
                "L": 0,
                "GF": 6,
                "GA": 0,
                "GD": 6,
                "Pts": 4,
            },
            "Saint Kitts and Nevis": {
                "Pld": 2,
                "W": 1,
                "D": 0,
                "L": 1,
                "GF": 1,
                "GA": 3,
                "GD": -2,
                "Pts": 3,
            },
            "Grenada": {
                "Pld": 2,
                "W": 0,
                "D": 1,
                "L": 1,
                "GF": 1,
                "GA": 3,
                "GD": -2,
                "Pts": 1,
            },
            "Bahamas": {
                "Pld": 2,
                "W": 0,
                "D": 0,
                "L": 2,
                "GF": 0,
                "GA": 7,
                "GD": -7,
                "Pts": 0,
            },
        },
        "CONCACAF_Second_Round_Group_C": {
            "Curacao": {
                "Pld": 2,
                "W": 2,
                "D": 0,
                "L": 0,
                "GF": 5,
                "GA": 0,
                "GD": 5,
                "Pts": 6,
            },
            "Haiti": {
                "Pld": 2,
                "W": 2,
                "D": 0,
                "L": 0,
                "GF": 3,
                "GA": 0,
                "GD": 3,
                "Pts": 6,
            },
            "Saint Lucia": {
                "Pld": 2,
                "W": 0,
                "D": 1,
                "L": 1,
                "GF": 0,
                "GA": 1,
                "GD": -1,
                "Pts": 1,
            },
            "Aruba": {
                "Pld": 2,
                "W": 0,
                "D": 1,
                "L": 1,
                "GF": 0,
                "GA": 2,
                "GD": -2,
                "Pts": 1,
            },
            "Barbados": {
                "Pld": 2,
                "W": 0,
                "D": 0,
                "L": 2,
                "GF": 0,
                "GA": 5,
                "GD": -5,
                "Pts": 0,
            },
        },
        "CONCACAF_Second_Round_Group_D": {
            "Nicaragua": {
                "Pld": 2,
                "W": 2,
                "D": 0,
                "L": 0,
                "GF": 7,
                "GA": 0,
                "GD": 7,
                "Pts": 6,
            },
            "Panama": {
                "Pld": 2,
                "W": 2,
                "D": 0,
                "L": 0,
                "GF": 4,
                "GA": 0,
                "GD": 4,
                "Pts": 6,
            },
            "Guyana": {
                "Pld": 2,
                "W": 1,
                "D": 0,
                "L": 1,
                "GF": 1,
                "GA": 1,
                "GD": 0,
                "Pts": 3,
            },
            "Montserrat": {
                "Pld": 2,
                "W": 0,
                "D": 0,
                "L": 2,
                "GF": 0,
                "GA": 5,
                "GD": -5,
                "Pts": 0,
            },
            "Belize": {
                "Pld": 2,
                "W": 0,
                "D": 0,
                "L": 2,
                "GF": 0,
                "GA": 6,
                "GD": -6,
                "Pts": 0,
            },
        },
        "CONCACAF_Second_Round_Group_E": {
            "Guatemala": {
                "Pld": 2,
                "W": 2,
                "D": 0,
                "L": 0,
                "GF": 9,
                "GA": 0,
                "GD": 9,
                "Pts": 6,
            },
            "Jamaica": {
                "Pld": 2,
                "W": 2,
                "D": 0,
                "L": 0,
                "GF": 2,
                "GA": 0,
                "GD": 2,
                "Pts": 6,
            },
            "Dominican Republic": {
                "Pld": 2,
                "W": 1,
                "D": 0,
                "L": 1,
                "GF": 3,
                "GA": 0,
                "GD": 3,
                "Pts": 3,
            },
            "Dominica": {
                "Pld": 2,
                "W": 0,
                "D": 0,
                "L": 2,
                "GF": 0,
                "GA": 7,
                "GD": -7,
                "Pts": 0,
            },
            "British Virgin Islands": {
                "Pld": 2,
                "W": 0,
                "D": 0,
                "L": 2,
                "GF": 0,
                "GA": 7,
                "GD": -7,
                "Pts": 0,
            },
        },
        "CONCACAF_Second_Round_Group_F": {
            "Suriname": {
                "Pld": 2,
                "W": 2,
                "D": 0,
                "L": 0,
                "GF": 7,
                "GA": 0,
                "GD": 7,
                "Pts": 6,
            },
            "Puerto Rico": {
                "Pld": 2,
                "W": 1,
                "D": 1,
                "L": 0,
                "GF": 8,
                "GA": 0,
                "GD": 8,
                "Pts": 4,
            },
            "El Salvador": {
                "Pld": 2,
                "W": 1,
                "D": 1,
                "L": 0,
                "GF": 2,
                "GA": 0,
                "GD": 2,
                "Pts": 4,
            },
            "Saint Vincent and the Grenadines": {
                "Pld": 2,
                "W": 0,
                "D": 0,
                "L": 2,
                "GF": 0,
                "GA": 5,
                "GD": -5,
                "Pts": 0,
            },
            "Anguilla": {
                "Pld": 2,
                "W": 0,
                "D": 0,
                "L": 2,
                "GF": 0,
                "GA": 12,
                "GD": -12,
                "Pts": 0,
            },
        },
    },
    "UEFA": {
        "UEFA_Group_A": {},
        "UEFA_Group_B": {},
        "UEFA_Group_C": {},
        "UEFA_Group_D": {},
        "UEFA_Group_E": {},
        "UEFA_Group_F": {},
        "UEFA_Group_G": {
            "Poland": {
                "Pld": 2,
                "W": 2,
                "D": 0,
                "L": 0,
                "GF": 3,
                "GA": 0,
                "GD": 3,
                "Pts": 6,
            },
            "Finland": {
                "Pld": 2,
                "W": 1,
                "D": 1,
                "L": 0,
                "GF": 1,
                "GA": 0,
                "GD": 1,
                "Pts": 4,
            },
            "Lithuania": {
                "Pld": 2,
                "W": 0,
                "D": 1,
                "L": 1,
                "GF": 0,
                "GA": 1,
                "GD": -1,
                "Pts": 1,
            },
            "Netherlands": {
                "Pld": 0,
                "W": 0,
                "D": 0,
                "L": 0,
                "GF": 0,
                "GA": 0,
                "GD": 0,
                "Pts": 0,
            },
            "Malta": {
                "Pld": 2,
                "W": 0,
                "D": 0,
                "L": 2,
                "GF": 0,
                "GA": 3,
                "GD": -3,
                "Pts": 0,
            },
        },
        "UEFA_Group_H": {
            "Bosnia and Herzegovina": {
                "Pld": 2,
                "W": 2,
                "D": 0,
                "L": 0,
                "GF": 2,
                "GA": 0,
                "GD": 2,
                "Pts": 6,
            },
            "Romania": {
                "Pld": 2,
                "W": 1,
                "D": 0,
                "L": 1,
                "GF": 3,
                "GA": 0,
                "GD": 3,
                "Pts": 3,
            },
            "Cyprus": {
                "Pld": 2,
                "W": 1,
                "D": 0,
                "L": 1,
                "GF": 1,
                "GA": 0,
                "GD": 1,
                "Pts": 3,
            },
            "Austria": {
                "Pld": 0,
                "W": 0,
                "D": 0,
                "L": 0,
                "GF": 0,
                "GA": 0,
                "GD": 0,
                "Pts": 0,
            },
            "San Marino": {
                "Pld": 2,
                "W": 0,
                "D": 0,
                "L": 2,
                "GF": 0,
                "GA": 6,
                "GD": -6,
                "Pts": 0,
            },
        },
        "UEFA_Group_I": {
            "Norway": {
                "Pld": 2,
                "W": 2,
                "D": 0,
                "L": 0,
                "GF": 7,
                "GA": 0,
                "GD": 7,
                "Pts": 6,
            },
            "Estonia": {
                "Pld": 2,
                "W": 1,
                "D": 0,
                "L": 1,
                "GF": 0,
                "GA": 0,
                "GD": 0,
                "Pts": 3,
            },
            "Israel": {
                "Pld": 2,
                "W": 1,
                "D": 0,
                "L": 1,
                "GF": 0,
                "GA": 1,
                "GD": -1,
                "Pts": 3,
            },
            "Italy": {
                "Pld": 0,
                "W": 0,
                "D": 0,
                "L": 0,
                "GF": 0,
                "GA": 0,
                "GD": 0,
                "Pts": 0,
            },
            "Moldova": {
                "Pld": 2,
                "W": 0,
                "D": 0,
                "L": 2,
                "GF": 0,
                "GA": 6,
                "GD": -6,
                "Pts": 0,
            },
        },
        "UEFA_Group_J": {
            "North Macedonia": {
                "Pld": 2,
                "W": 1,
                "D": 1,
                "L": 0,
                "GF": 3,
                "GA": 0,
                "GD": 3,
                "Pts": 4,
            },
            "Wales": {
                "Pld": 2,
                "W": 1,
                "D": 1,
                "L": 0,
                "GF": 2,
                "GA": 0,
                "GD": 2,
                "Pts": 4,
            },
            "Kazakhstan": {
                "Pld": 2,
                "W": 1,
                "D": 0,
                "L": 1,
                "GF": 0,
                "GA": 0,
                "GD": 0,
                "Pts": 3,
            },
            "Belgium": {
                "Pld": 0,
                "W": 0,
                "D": 0,
                "L": 0,
                "GF": 0,
                "GA": 0,
                "GD": 0,
                "Pts": 0,
            },
            "Liechtenstein": {
                "Pld": 2,
                "W": 0,
                "D": 0,
                "L": 2,
                "GF": 0,
                "GA": 5,
                "GD": -5,
                "Pts": 0,
            },
        },
    },
}


def simulate_afc_qualifying(verbose=True):
    """Simulates the AFC (Asia) World Cup qualifying process."""
    if verbose:
        print(f"\n\n===== Simulating AFC World Cup Qualifying =====")
    afc_qualified_paths = []
    for team_name in STATIC_WORLD_CUP_QUALIFIED["AFC"]:
        afc_qualified_paths.append((team_name, "AFC Direct (Pre-qualified)"))
    afc_third_round_groups = {
        "AFC_Third_Round_Group_A": [
            t
            for t in LIVE_STANDINGS_DATA["AFC"]["AFC_Third_Round_Group_A"].keys()
            if t not in [item[0] for item in afc_qualified_paths]
        ],
        "AFC_Third_Round_Group_B": [
            t
            for t in LIVE_STANDINGS_DATA["AFC"]["AFC_Third_Round_Group_B"].keys()
            if t not in [item[0] for item in afc_qualified_paths]
        ],
        "AFC_Third_Round_Group_C": [
            t
            for t in LIVE_STANDINGS_DATA["AFC"]["AFC_Third_Round_Group_C"].keys()
            if t not in [item[0] for item in afc_qualified_paths]
        ],
    }
    afc_fourth_round_teams = []
    for group_name, teams_in_group in afc_third_round_groups.items():
        if not teams_in_group:
            if verbose:
                print(f"Skipping empty group: {group_name}")
            continue
        initial_group_data = {
            t_name: LIVE_STANDINGS_DATA["AFC"][group_name][t_name]
            for t_name in teams_in_group
        }
        direct_qualifiers, playoff_teams, _, _ = simulate_group_with_initial_standings(
            group_name,
            teams_in_group,
            initial_group_data,
            num_qualify_direct=2,
            num_to_playoff=2,
            total_matches_per_team=10,
            verbose=verbose,
        )
        for team in direct_qualifiers:
            afc_qualified_paths.append((team, "AFC Direct (Third Round)"))
        afc_fourth_round_teams.extend(playoff_teams)
    if verbose:
        print("\n--- AFC Fourth Round ---")
    random.shuffle(afc_fourth_round_teams)
    if len(afc_fourth_round_teams) >= 6:
        afc_fourth_round_groups = {
            "AFC_Fourth_Round_Group_X": afc_fourth_round_teams[0:3],
            "AFC_Fourth_Round_Group_Y": afc_fourth_round_teams[3:6],
        }
    else:
        if verbose:
            print(
                f"Not enough teams ({len(afc_fourth_round_teams)}) for AFC Fourth Round, proceeding with available."
            )
        if len(afc_fourth_round_teams) > 0:
            afc_fourth_round_groups = {
                "AFC_Fourth_Round_Group_X": afc_fourth_round_teams
            }
        else:
            afc_fourth_round_groups = {}
    afc_fifth_round_teams = []
    for group_name, teams_in_group in afc_fourth_round_groups.items():
        if not teams_in_group:
            continue
        direct_qualifiers, playoff_teams, _, _ = simulate_group_with_initial_standings(
            group_name,
            teams_in_group,
            {},
            num_qualify_direct=1,
            num_to_playoff=1,
            total_matches_per_team=2,
            verbose=verbose,
        )
        for team in direct_qualifiers:
            afc_qualified_paths.append((team, "AFC Direct (Fourth Round)"))
        afc_fifth_round_teams.extend(playoff_teams)
    afc_playoff_participant = None
    if verbose:
        print("\n--- AFC Fifth Round ---")
    if len(afc_fifth_round_teams) == 2:
        if verbose:
            print(
                f"AFC Playoff Match: {afc_fifth_round_teams[0]} vs {afc_fifth_round_teams[1]}"
            )
        winner = simulate_knockout(
            afc_fifth_round_teams, round_name="AFC Playoff", verbose=verbose
        )
        if winner:
            afc_playoff_participant = winner[0]
            if verbose:
                print(
                    f"AFC Inter-confederation Playoff participant: {afc_playoff_participant}"
                )
    elif len(afc_fifth_round_teams) == 1:
        afc_playoff_participant = afc_fifth_round_teams[0]
        if verbose:
            print(
                f"AFC Inter-confederation Playoff participant (by default): {afc_playoff_participant}"
            )
    else:
        if verbose:
            print("Not enough teams for AFC Fifth Round playoff or unexpected number.")
    return afc_qualified_paths, afc_playoff_participant


def simulate_caf_qualifying(verbose=True):
    """Simulates the CAF (Africa) World Cup qualifying process."""
    if verbose:
        print(f"\n\n===== Simulating CAF World Cup Qualifying =====")
    caf_qualified_paths = []
    caf_groups_initial_teams = {
        "CAF_Group_A": [
            "Egypt",
            "Burkina Faso",
            "Guinea-Bissau",
            "Sierra Leone",
            "Ethiopia",
            "Djibouti",
        ],
        "CAF_Group_B": [
            "DR Congo",
            "Senegal",
            "Sudan",
            "Togo",
            "South Sudan",
            "Mauritania",
        ],
        "CAF_Group_C": [
            "South Africa",
            "Rwanda",
            "Benin",
            "Nigeria",
            "Lesotho",
            "Zimbabwe",
        ],
        "CAF_Group_D": [
            "Cape Verde",
            "Cameroon",
            "Libya",
            "Angola",
            "Mauritius",
            "Eswatini",
        ],
        "CAF_Group_E": ["Morocco", "Tanzania", "Zambia", "Niger", "Congo"],
        "CAF_Group_F": [
            "Ivory Coast",
            "Gabon",
            "Burundi",
            "Kenya",
            "Gambia",
            "Seychelles",
        ],
        "CAF_Group_G": [
            "Algeria",
            "Mozambique",
            "Botswana",
            "Uganda",
            "Guinea",
            "Somalia",
        ],
        "CAF_Group_H": [
            "Tunisia",
            "Equatorial Guinea",
            "Namibia",
            "Liberia",
            "Malawi",
            "Sao Tome and Principe",
        ],
        "CAF_Group_I": [
            "Ghana",
            "Comoros",
            "Madagascar",
            "Mali",
            "Central African Republic",
            "Chad",
        ],
    }
    group_runners_up_for_selection = []
    for group_name, teams_in_group_list in caf_groups_initial_teams.items():
        if not teams_in_group_list:
            continue
        initial_group_data = LIVE_STANDINGS_DATA["CAF"].get(group_name, {})
        if group_name == "CAF_Group_E":
            total_matches_per_team = 8
        else:
            total_matches_per_team = 10
        qualified_from_group, runner_up, _, _ = simulate_group_with_initial_standings(
            group_name,
            teams_in_group_list,
            initial_group_data,
            num_qualify_direct=1,
            num_to_playoff=1,
            total_matches_per_team=total_matches_per_team,
            verbose=verbose,
        )
        for team in qualified_from_group:
            caf_qualified_paths.append((team, "CAF Direct (Group Winner)"))
        if runner_up:
            group_runners_up_for_selection.append(
                {
                    "team": runner_up[0],
                    "ranking_points": get_team(runner_up[0]).ranking_points,
                }
            )
    group_runners_up_for_selection.sort(key=lambda x: x["ranking_points"], reverse=True)
    caf_playoff_candidates = [s["team"] for s in group_runners_up_for_selection[:4]]
    caf_playoff_participant = None
    if verbose:
        print("\n--- CAF Play-off Stage ---")
    if len(caf_playoff_candidates) >= 2:
        if verbose:
            print(
                f"CAF Playoff participants (top 4 runners-up by ranking): {caf_playoff_candidates}"
            )
        winner = simulate_knockout(
            caf_playoff_candidates, round_name="CAF Playoff", verbose=verbose
        )
        if winner:
            caf_playoff_participant = winner[0]
            if verbose:
                print(
                    f"CAF Inter-confederation Playoff participant: {caf_playoff_participant}"
                )
    elif len(caf_playoff_candidates) == 1:
        caf_playoff_participant = caf_playoff_candidates[0]
        if verbose:
            print(
                f"CAF Inter-confederation Playoff participant (by default): {caf_playoff_participant}"
            )
    else:
        if verbose:
            print("Not enough teams for CAF Playoff stage.")
    return caf_qualified_paths, caf_playoff_participant


def simulate_concacaf_qualifying(verbose=True):
    """Simulates the CONCACAF (North, Central America, and Caribbean) World Cup qualifying process."""
    if verbose:
        print(f"\n\n===== Simulating CONCACAF World Cup Qualifying =====")
    concacaf_qualified_paths = []
    for team_name in STATIC_WORLD_CUP_QUALIFIED["CONCACAF"]:
        concacaf_qualified_paths.append((team_name, "CONCACAF Host Nation"))
    concacaf_second_round_groups_teams = {
        "CONCACAF_Second_Round_Group_A": list(
            LIVE_STANDINGS_DATA["CONCACAF_Second_Round"][
                "CONCACAF_Second_Round_Group_A"
            ].keys()
        ),
        "CONCACAF_Second_Round_Group_B": list(
            LIVE_STANDINGS_DATA["CONCACAF_Second_Round"][
                "CONCACAF_Second_Round_Group_B"
            ].keys()
        ),
        "CONCACAF_Second_Round_Group_C": list(
            LIVE_STANDINGS_DATA["CONCACAF_Second_Round"][
                "CONCACAF_Second_Round_Group_C"
            ].keys()
        ),
        "CONCACAF_Second_Round_Group_D": list(
            LIVE_STANDINGS_DATA["CONCACAF_Second_Round"][
                "CONCACAF_Second_Round_Group_D"
            ].keys()
        ),
        "CONCACAF_Second_Round_Group_E": list(
            LIVE_STANDINGS_DATA["CONCACAF_Second_Round"][
                "CONCACAF_Second_Round_Group_E"
            ].keys()
        ),
        "CONCACAF_Second_Round_Group_F": list(
            LIVE_STANDINGS_DATA["CONCACAF_Second_Round"][
                "CONCACAF_Second_Round_Group_F"
            ].keys()
        ),
    }
    concacaf_third_round_teams = []
    for group_name, teams_in_group_list in concacaf_second_round_groups_teams.items():
        if not teams_in_group_list:
            continue
        initial_group_data = LIVE_STANDINGS_DATA["CONCACAF_Second_Round"].get(
            group_name, {}
        )
        qualified_from_group, runner_up, _, _ = simulate_group_with_initial_standings(
            group_name,
            teams_in_group_list,
            initial_group_data,
            num_qualify_direct=1,
            num_to_playoff=1,
            total_matches_per_team=4,
            verbose=verbose,
        )
        concacaf_third_round_teams.extend(qualified_from_group)
        if runner_up:
            concacaf_third_round_teams.extend(runner_up)
    concacaf_icp_participants = []
    if verbose:
        print("\n--- CONCACAF Third Round ---")
    random.shuffle(concacaf_third_round_teams)
    if len(concacaf_third_round_teams) >= 12:
        concacaf_third_round_groups = {
            "CONCACAF_Third_Round_Group_1": concacaf_third_round_teams[0:4],
            "CONCACAF_Third_Round_Group_2": concacaf_third_round_teams[4:8],
            "CONCACAF_Third_Round_Group_3": concacaf_third_round_teams[8:12],
        }
    else:
        if verbose:
            print(
                f"Not enough teams ({len(concacaf_third_round_teams)}) for CONCACAF Third Round, proceeding with available."
            )
        concacaf_third_round_groups = {}
        for i in range(len(concacaf_third_round_teams) // 4):
            concacaf_third_round_groups[f"CONCACAF_Third_Round_Group_{i+1}"] = (
                concacaf_third_round_teams[i * 4 : (i + 1) * 4]
            )
        if (
            len(concacaf_third_round_teams) % 4 != 0
            and len(concacaf_third_round_teams) > 0
        ):
            concacaf_third_round_groups[f"CONCACAF_Third_Round_Group_X_Remainder"] = (
                concacaf_third_round_teams[-(len(concacaf_third_round_teams) % 4) :]
            )
    concacaf_runners_up_stats = []
    for group_name, teams_in_group in concacaf_third_round_groups.items():
        if not teams_in_group:
            continue
        direct_qualifiers, runner_up, _, _ = simulate_group_with_initial_standings(
            group_name,
            teams_in_group,
            {},
            num_qualify_direct=1,
            num_to_playoff=1,
            total_matches_per_team=6,
            verbose=verbose,
        )
        for team in direct_qualifiers:
            concacaf_qualified_paths.append((team, "CONCACAF Direct (Group Winner)"))
        if runner_up:
            concacaf_runners_up_stats.append(
                {
                    "team": runner_up[0],
                    "ranking_points": get_team(runner_up[0]).ranking_points,
                }
            )
    concacaf_runners_up_stats.sort(key=lambda x: x["ranking_points"], reverse=True)
    concacaf_icp_participants = [s["team"] for s in concacaf_runners_up_stats[:2]]
    if len(concacaf_icp_participants) >= 2:
        if verbose:
            print(
                f"CONCACAF Inter-confederation Playoff participants: {concacaf_icp_participants}"
            )
    elif concacaf_icp_participants:
        if verbose:
            print(
                f"CONCACAF Inter-confederation Playoff participants (partial): {concacaf_icp_participants}"
            )
    else:
        if verbose:
            print("Not enough CONCACAF teams for ICP slots.")
    return concacaf_qualified_paths, concacaf_icp_participants


def simulate_conmebol_qualifying(verbose=True):
    """Simulates the CONMEBOL (South America) World Cup qualifying process."""
    if verbose:
        print(f"\n\n===== Simulating CONMEBOL World Cup Qualifying =====")
    conmebol_qualified_paths = []
    conmebol_playoff_participant = None
    for team_name in STATIC_WORLD_CUP_QUALIFIED["CONMEBOL"]:
        conmebol_qualified_paths.append((team_name, "CONMEBOL Direct (Pre-qualified)"))
    conmebol_teams = list(LIVE_STANDINGS_DATA["CONMEBOL"].keys())
    if verbose:
        print(
            "Simulating CONMEBOL league from current standings (15 matches per team played, 3 remaining)."
        )
    initial_conmebol_standings = LIVE_STANDINGS_DATA["CONMEBOL"]
    _, _, _, final_conmebol_standings_dict = simulate_group_with_initial_standings(
        "CONMEBOL_League",
        conmebol_teams,
        initial_conmebol_standings,
        num_qualify_direct=0,
        num_to_playoff=0,
        total_matches_per_team=18,
        verbose=verbose,
    )
    conmebol_final_standings_list = []
    for team_name in conmebol_teams:
        conmebol_final_standings_list.append(
            {"Team": team_name, **final_conmebol_standings_dict.get(team_name, {})}
        )
    sorted_standings = sort_group(conmebol_final_standings_list)
    for t in sorted_standings[:6]:
        conmebol_qualified_paths.append((t["Team"], "CONMEBOL Direct (Top 6)"))
    if len(sorted_standings) >= 7:
        conmebol_playoff_participant = sorted_standings[6]["Team"]
        if verbose:
            print(
                f"CONMEBOL Inter-confederation Playoff participant: {conmebol_playoff_participant}"
            )
    else:
        if verbose:
            print(
                "Not enough teams in CONMEBOL league to determine 7th place for playoff spot."
            )
    return conmebol_qualified_paths, conmebol_playoff_participant


def simulate_ofc_qualifying(verbose=True):
    """Simulates the OFC (Oceania) World Cup qualifying process."""
    if verbose:
        print(f"\n\n===== Simulating OFC World Cup Qualifying =====")
    ofc_qualified_paths = []
    for team_name in STATIC_WORLD_CUP_QUALIFIED["OFC"]:
        ofc_qualified_paths.append((team_name, "OFC Direct (Pre-qualified)"))
    ofc_playoff_participant = STATIC_INTER_CONFED_PLAYOFF_TEAMS.get("OFC", None)
    if ofc_playoff_participant:
        if verbose:
            print(
                f"OFC Inter-confederation Playoff participant (already known): {ofc_playoff_participant}"
            )
    return ofc_qualified_paths, ofc_playoff_participant


def simulate_uefa_qualifying(verbose=True):
    """Simulates the UEFA (Europe) World Cup qualifying process."""
    if verbose:
        print(f"\n\n===== Simulating UEFA World Cup Qualifying =====")
    uefa_qualified_paths = []
    uefa_teams_pool = [
        "Spain",
        "France",
        "England",
        "Belgium",
        "Italy",
        "Germany",
        "Netherlands",
        "Portugal",
        "Croatia",
        "Switzerland",
        "Denmark",
        "Austria",
        "Ukraine",
        "Türkiye",
        "Sweden",
        "Wales",
        "Serbia",
        "Poland",
        "Russia",
        "Hungary",
        "Norway",
        "Czechia",
        "Greece",
        "Scotland",
        "Romania",
        "Slovakia",
        "Slovenia",
        "Republic of Ireland",
        "North Macedonia",
        "Bosnia and Herzegovina",
        "Finland",
        "Iceland",
        "Albania",
        "Bulgaria",
        "Israel",
        "Georgia",
        "Luxembourg",
        "Cyprus",
        "Kosovo",
        "Lithuania",
        "Estonia",
        "Latvia",
        "Azerbaijan",
        "Kazakhstan",
        "Armenia",
        "Malta",
        "Moldova",
        "Gibraltar",
        "San Marino",
        "Liechtenstein",
        "Andorra",
        "Faroe Islands",
        "Northern Ireland",
        "Belarus",
        "Trinidad and Tobago",
        "Curacao",
        "Haiti",
        "Nicaragua",
        "Guatemala",
        "Jamaica",
        "Suriname",
        "El Salvador",
    ]
    random.shuffle(uefa_teams_pool)
    uefa_groups_teams = {
        "UEFA_Group_A": ["Germany", "Luxembourg", "Northern Ireland", "Slovakia"],
        "UEFA_Group_B": ["Kosovo", "Slovenia", "Sweden", "Switzerland"],
        "UEFA_Group_C": ["Belarus", "Denmark", "Greece", "Scotland"],
        "UEFA_Group_D": ["Azerbaijan", "France", "Iceland", "Ukraine"],
        "UEFA_Group_E": ["Bulgaria", "Georgia", "Spain", "Türkiye"],
        "UEFA_Group_F": ["Armenia", "Hungary", "Portugal", "Republic of Ireland"],
        "UEFA_Group_G": ["Poland", "Finland", "Lithuania", "Netherlands", "Malta"],
        "UEFA_Group_H": [
            "Bosnia and Herzegovina",
            "Romania",
            "Cyprus",
            "Austria",
            "San Marino",
        ],
        "UEFA_Group_I": ["Norway", "Estonia", "Israel", "Italy", "Moldova"],
        "UEFA_Group_J": [
            "North Macedonia",
            "Wales",
            "Kazakhstan",
            "Belgium",
            "Liechtenstein",
        ],
        "UEFA_Group_K": [],
        "UEFA_Group_L": [],
    }
    assigned_teams = set()
    for group_teams in uefa_groups_teams.values():
        assigned_teams.update(group_teams)
    unassigned_uefa_teams = [t for t in uefa_teams_pool if t not in assigned_teams]
    random.shuffle(unassigned_uefa_teams)
    if len(unassigned_uefa_teams) >= 4:
        uefa_groups_teams["UEFA_Group_K"] = unassigned_uefa_teams[0:4]
        unassigned_uefa_teams = unassigned_uefa_teams[4:]
    if len(unassigned_uefa_teams) >= 4:
        uefa_groups_teams["UEFA_Group_L"] = unassigned_uefa_teams[0:4]
        unassigned_uefa_teams = unassigned_uefa_teams[4:]
    elif len(unassigned_uefa_teams) > 0:
        if not uefa_groups_teams["UEFA_Group_L"]:
            uefa_groups_teams["UEFA_Group_L"].extend(unassigned_uefa_teams)
        else:
            uefa_groups_teams["UEFA_Group_K"].extend(unassigned_uefa_teams)
        unassigned_uefa_teams = []
    all_runners_up_stats = []
    for group_name, teams_in_group_list in uefa_groups_teams.items():
        if not teams_in_group_list:
            continue
        initial_group_data = LIVE_STANDINGS_DATA["UEFA"].get(group_name, {})
        if len(teams_in_group_list) == 4:
            total_matches_per_team = 6
        else:
            total_matches_per_team = 8
        direct_qualifier, runner_up, _, _ = simulate_group_with_initial_standings(
            group_name,
            teams_in_group_list,
            initial_group_data,
            num_qualify_direct=1,
            num_to_playoff=1,
            total_matches_per_team=total_matches_per_team,
            verbose=verbose,
        )
        for team in direct_qualifier:
            uefa_qualified_paths.append((team, "UEFA Direct (Group Winner)"))
        if runner_up:
            all_runners_up_stats.append(
                {
                    "team": runner_up[0],
                    "ranking_points": get_team(runner_up[0]).ranking_points,
                }
            )
    all_runners_up_stats.sort(key=lambda x: x["ranking_points"], reverse=True)
    uefa_playoff_candidates = [s["team"] for s in all_runners_up_stats[:12]]
    uefa_icp_participants = []
    if verbose:
        print("\n--- UEFA Play-off Stage ---")
    if len(uefa_playoff_candidates) >= 12:
        random.shuffle(uefa_playoff_candidates)
        playoff_groups = {
            "UEFA_Playoff_Path_A": uefa_playoff_candidates[0:4],
            "UEFA_Playoff_Path_B": uefa_playoff_candidates[4:8],
            "UEFA_Playoff_Path_C": uefa_playoff_candidates[8:12],
        }
        for path_name, teams_in_path in playoff_groups.items():
            if verbose:
                print(f"\nSimulating {path_name}")
            winners = simulate_knockout(
                teams_in_path, round_name=path_name, verbose=verbose
            )
            if winners:
                uefa_qualified_paths.append((winners[0], f"UEFA Playoff ({path_name})"))
    else:
        if verbose:
            print(
                f"Not enough teams ({len(uefa_playoff_candidates)}) for UEFA Playoff, proceeding with available."
            )
        if uefa_playoff_candidates:
            winners = simulate_knockout(
                uefa_playoff_candidates, round_name="UEFA Playoff", verbose=verbose
            )
            if winners:
                uefa_qualified_paths.append((winners[0], "UEFA Playoff"))
    if len(all_runners_up_stats) >= 13:
        uefa_icp_participants = [all_runners_up_stats[12]["team"]]
        if verbose:
            print(
                f"UEFA Inter-confederation Playoff participant: {uefa_icp_participants[0]}"
            )
    return uefa_qualified_paths, uefa_icp_participants


def simulate_inter_confederation_playoffs(
    afc_playoff_team,
    caf_playoff_team,
    concacaf_playoff_teams,
    conmebol_playoff_team,
    ofc_playoff_team,
    uefa_playoff_team,
    verbose=True,
):
    """Simulates the inter-confederation playoffs for two World Cup spots."""
    if verbose:
        print(f"\n\n===== Simulating Inter-confederation Playoffs =====")
    icp_qualified = []
    icp_teams = []
    if afc_playoff_team:
        icp_teams.append(afc_playoff_team)
    if caf_playoff_team:
        icp_teams.append(caf_playoff_team)
    if concacaf_playoff_teams:
        icp_teams.extend(concacaf_playoff_teams)
    if conmebol_playoff_team:
        icp_teams.append(conmebol_playoff_team)
    if ofc_playoff_team:
        icp_teams.append(ofc_playoff_team)
    if uefa_playoff_team:
        icp_teams.append(uefa_playoff_team)
    if verbose:
        print(f"Inter-confederation Playoff participants: {icp_teams}")
    if len(icp_teams) >= 4:
        random.shuffle(icp_teams)
        first_pair = icp_teams[:2]
        second_pair = icp_teams[2:4]
        if verbose:
            print("\nInter-confederation Playoff Matches:")
        for pair in [first_pair, second_pair]:
            if len(pair) == 2:
                if verbose:
                    print(f"Match: {pair[0]} vs {pair[1]}")
                winner = simulate_knockout(
                    pair,
                    round_name="Inter-confederation Playoff Match",
                    verbose=verbose,
                )
                if winner:
                    icp_qualified.append((winner[0], "Inter-confederation Playoff"))
            else:
                if verbose:
                    print(f"Not enough teams in pair: {pair}")
    else:
        if verbose:
            print(
                f"Not enough teams ({len(icp_teams)}) for Inter-confederation Playoffs, simulating with available."
            )
        if len(icp_teams) >= 2:
            winners = simulate_knockout(
                icp_teams, round_name="Inter-confederation Playoff", verbose=verbose
            )
            if winners:
                icp_qualified.append((winners[0], "Inter-confederation Playoff"))
        else:
            if verbose:
                print("Not enough teams for Inter-confederation Playoffs.")
    return icp_qualified


def simulate_qualification_process(num_simulations=1000, verbose=True):
    """
    Runs the entire World Cup 2026 qualification simulation multiple times and aggregates results.
    Ensures that 48 teams qualify in each simulation.
    """
    if verbose:
        print(
            f"\n=== Running {num_simulations} Simulations of World Cup 2026 Qualification ==="
        )
    qualification_counts = defaultdict(int)
    qualification_paths = defaultdict(list)
    total_qualified_teams = set()
    # Use tqdm for progress bar if not verbose, otherwise print every 100
    sim_iter = tqdm(
        range(num_simulations), desc="Simulating World Cups", disable=verbose
    )
    for sim in sim_iter:
        if verbose and sim % 100 == 0:
            print(f"Running simulation {sim + 1}/{num_simulations}...")
        afc_qualified, afc_playoff = simulate_afc_qualifying(verbose=False)
        caf_qualified, caf_playoff = simulate_caf_qualifying(verbose=False)
        concacaf_qualified, concacaf_playoffs = simulate_concacaf_qualifying(
            verbose=False
        )
        conmebol_qualified, conmebol_playoff = simulate_conmebol_qualifying(
            verbose=False
        )
        ofc_qualified, ofc_playoff = simulate_ofc_qualifying(verbose=False)
        uefa_qualified, uefa_playoff = simulate_uefa_qualifying(verbose=False)
        icp_qualified = simulate_inter_confederation_playoffs(
            afc_playoff,
            caf_playoff,
            concacaf_playoffs,
            conmebol_playoff,
            ofc_playoff,
            uefa_playoff,
            verbose=False,
        )
        all_qualified = (
            afc_qualified
            + caf_qualified
            + concacaf_qualified
            + conmebol_qualified
            + ofc_qualified
            + uefa_qualified
            + icp_qualified
        )
        # Ensure only 48 teams qualify (if more, trim by ranking; if less, add next best by ranking)
        qualified_teams_set = set(team for team, _ in all_qualified)
        if len(qualified_teams_set) > 48:
            # Sort by FIFA ranking and keep top 48
            all_qualified_sorted = sorted(
                all_qualified, key=lambda x: FIFA_RANKINGS.get(x[0], 0), reverse=True
            )
            all_qualified = []
            seen = set()
            for team, path in all_qualified_sorted:
                if team not in seen:
                    all_qualified.append((team, path))
                    seen.add(team)
                if len(all_qualified) == 48:
                    break
        elif len(qualified_teams_set) < 48:
            # Add next best teams by FIFA ranking not already qualified
            already_qualified = set(team for team, _ in all_qualified)
            all_teams_sorted = sorted(
                FIFA_RANKINGS.items(), key=lambda x: x[1], reverse=True
            )
            for team, _ in all_teams_sorted:
                if team not in already_qualified:
                    all_qualified.append((team, "FIFA Ranking Filler"))
                    already_qualified.add(team)
                if len(already_qualified) == 48:
                    break
        # Now, exactly 48 teams
        for team, path in all_qualified[:48]:
            qualification_counts[team] += 1
            qualification_paths[team].append(path)
            total_qualified_teams.add(team)
    if verbose:
        print("\n=== Qualification Probabilities ===")
        print("Team".ljust(30) + "Qualification Probability (%)")
        print("-" * 60)
        sorted_teams = sorted(
            qualification_counts.items(), key=lambda x: x[1], reverse=True
        )
        for team, count in sorted_teams:
            probability = (count / num_simulations) * 100
            print(f"{team.ljust(30)} {probability:.2f}%")
        print("\n=== Qualification Paths ===")
        for team in sorted(total_qualified_teams):
            print(f"\n{team}:")
            path_counts = defaultdict(int)
            for path in qualification_paths[team]:
                path_counts[path] += 1
            for path, count in sorted(
                path_counts.items(), key=lambda x: x[1], reverse=True
            ):
                path_probability = (count / num_simulations) * 100
                print(f"  {path}: {path_probability:.2f}%")
    return qualification_counts, qualification_paths


def ensure_48_teams(all_qualified: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """Ensures the qualified teams list is exactly 48, trimming or filling as needed."""
    qualified_teams_set = set(team for team, _ in all_qualified)
    if len(qualified_teams_set) > 48:
        all_qualified_sorted = sorted(
            all_qualified, key=lambda x: FIFA_RANKINGS.get(x[0], 0), reverse=True
        )
        all_qualified_display = []
        seen = set()
        for team, path in all_qualified_sorted:
            if team not in seen:
                all_qualified_display.append((team, path))
                seen.add(team)
            if len(all_qualified_display) == 48:
                break
        return all_qualified_display
    elif len(qualified_teams_set) < 48:
        already_qualified = set(team for team, _ in all_qualified)
        all_qualified_display = list(all_qualified)
        all_teams_sorted = sorted(
            FIFA_RANKINGS.items(), key=lambda x: x[1], reverse=True
        )
        for team, _ in all_teams_sorted:
            if team not in already_qualified:
                all_qualified_display.append((team, "FIFA Ranking Filler"))
                already_qualified.add(team)
            if len(already_qualified) == 48:
                break
        return all_qualified_display
    else:
        return all_qualified


def parse_args():
    parser = argparse.ArgumentParser(
        description="World Cup 2026 Qualification Simulator"
    )
    parser.add_argument(
        "--seed", type=int, default=None, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--simulations",
        type=int,
        default=1000,
        help="Number of simulations for probability estimation",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.seed is not None:
        random.seed(args.seed)
    verbose = args.verbose
    num_simulations = args.simulations

    # Run one detailed simulation for display
    if verbose:
        print("=== Single Detailed Simulation ===")
    afc_qualified, afc_playoff = simulate_afc_qualifying(verbose=verbose)
    caf_qualified, caf_playoff = simulate_caf_qualifying(verbose=verbose)
    concacaf_qualified, concacaf_playoffs = simulate_concacaf_qualifying(
        verbose=verbose
    )
    conmebol_qualified, conmebol_playoff = simulate_conmebol_qualifying(verbose=verbose)
    ofc_qualified, ofc_playoff = simulate_ofc_qualifying(verbose=verbose)
    uefa_qualified, uefa_playoff = simulate_uefa_qualifying(verbose=verbose)
    icp_qualified = simulate_inter_confederation_playoffs(
        afc_playoff,
        caf_playoff,
        concacaf_playoffs,
        conmebol_playoff,
        ofc_playoff,
        uefa_playoff,
        verbose=verbose,
    )
    all_qualified = (
        afc_qualified
        + caf_qualified
        + concacaf_qualified
        + conmebol_qualified
        + ofc_qualified
        + uefa_qualified
        + icp_qualified
    )
    all_qualified_display = ensure_48_teams(all_qualified)

    print("\n=== Teams Qualified for World Cup 2026 (Single Simulation) ===")
    print("Team".ljust(48) + "Qualification Path")
    print("-" * 60)
    for team, path in sorted(all_qualified_display):
        print(f"{team.ljust(48)} {path}")

    # --- Print qualification probabilities for each team over multiple simulations ---
    print(f"\n=== Qualification Probabilities ({num_simulations} Simulations) ===")
    qualification_counts, _ = simulate_qualification_process(
        num_simulations=num_simulations, verbose=False
    )
    sorted_teams = sorted(
        qualification_counts.items(), key=lambda x: x[1], reverse=True
    )

    # --- Confederation mapping for breakdown ---
    CONFED_MAP = {}
    # Manually map teams to confederations based on STATIC_WORLD_CUP_QUALIFIED and FIFA_RANKINGS
    for team in FIFA_RANKINGS:
        if team in STATIC_WORLD_CUP_QUALIFIED.get("AFC", []):
            CONFED_MAP[team] = "AFC"
        elif team in STATIC_WORLD_CUP_QUALIFIED.get("CAF", []):
            CONFED_MAP[team] = "CAF"
        elif team in STATIC_WORLD_CUP_QUALIFIED.get("CONCACAF", []):
            CONFED_MAP[team] = "CONCACAF"
        elif team in STATIC_WORLD_CUP_QUALIFIED.get("CONMEBOL", []):
            CONFED_MAP[team] = "CONMEBOL"
        elif team in STATIC_WORLD_CUP_QUALIFIED.get("OFC", []):
            CONFED_MAP[team] = "OFC"
        elif team in [
            "Spain",
            "France",
            "England",
            "Belgium",
            "Italy",
            "Germany",
            "Netherlands",
            "Portugal",
            "Croatia",
            "Switzerland",
            "Denmark",
            "Austria",
            "Ukraine",
            "Türkiye",
            "Sweden",
            "Wales",
            "Serbia",
            "Poland",
            "Russia",
            "Hungary",
            "Norway",
            "Czechia",
            "Greece",
            "Scotland",
            "Romania",
            "Slovakia",
            "Slovenia",
            "Republic of Ireland",
            "North Macedonia",
            "Bosnia and Herzegovina",
            "Finland",
            "Iceland",
            "Albania",
            "Bulgaria",
            "Israel",
            "Georgia",
            "Luxembourg",
            "Cyprus",
            "Kosovo",
            "Lithuania",
            "Estonia",
            "Latvia",
            "Azerbaijan",
            "Kazakhstan",
            "Armenia",
            "Malta",
            "Moldova",
            "Gibraltar",
            "San Marino",
            "Liechtenstein",
            "Andorra",
            "Faroe Islands",
            "Northern Ireland",
            "Belarus",
        ]:
            CONFED_MAP[team] = "UEFA"
        else:
            # Default fallback for unmapped teams
            CONFED_MAP[team] = "Other"

    # Build confederation breakdowns
    confed_qualified = defaultdict(list)
    confed_probs = defaultdict(list)
    for team, count in sorted_teams:
        confed = CONFED_MAP.get(team, "Other")
        percent = (count / num_simulations) * 100
        confed_qualified[confed].append((team, percent))

    print("\n=== Confederation Qualification Probabilities Breakdown ===")
    for confed in sorted(confed_qualified.keys()):
        print(f"\n[{confed}]")
        print("Team".ljust(48) + "Chance (%)")
        print("-" * 60)
        for team, percent in confed_qualified[confed]:
            print(f"{team.ljust(48)} {percent:.2f}%")
