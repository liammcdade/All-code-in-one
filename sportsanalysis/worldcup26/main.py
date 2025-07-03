import importlib
import math
import random
from collections import defaultdict

# --- FIFA Rankings (used for all confederations) ---
FIFA_RANKINGS = {
    "Argentina": 1886.16, "Spain": 1854.64, "France": 1852.71, "England": 1819.2, "Brazil": 1776.03,
    "Netherlands": 1752.44, "Portugal": 1750.08, "Belgium": 1735.75, "Italy": 1718.31, "Germany": 1716.98,
    "Croatia": 1698.66, "Morocco": 1694.24, "Uruguay": 1679.49, "Colombia": 1679.04, "Japan": 1652.64,
    "USA": 1648.81, "Mexico": 1646.94, "IR Iran": 1637.39, "Senegal": 1630.32, "Switzerland": 1624.75,
    "Denmark": 1617.54, "Austria": 1580.22, "Korea Republic": 1574.93, "Ecuador": 1567.95, "Ukraine": 1559.81,
    "Australia": 1554.55, "Türkiye": 1551.47, "Sweden": 1536.05, "Wales": 1535.57, "Canada": 1531.58,
    "Serbia": 1523.91, "Egypt": 1518.79, "Panama": 1517.66, "Poland": 1517.35, "Russia": 1516.27,
    "Algeria": 1507.17, "Hungary": 1503.34, "Norway": 1497.18, "Czechia": 1491.43, "Greece": 1489.82,
    "Côte d'Ivoire": 1487.27, "Peru": 1483.48, "Nigeria": 1481.35, "Scotland": 1480.3, "Romania": 1479.22,
    "Slovakia": 1477.78, "Venezuela": 1476.84, "Paraguay": 1475.93, "Tunisia": 1474.1, "Cameroon": 1465.72,
    "Slovenia": 1462.66, "Chile": 1461.91, "Mali": 1460.23, "Costa Rica": 1459.13, "Qatar": 1456.58,
    "South Africa": 1445.01, "Uzbekistan": 1437.02, "Saudi Arabia": 1418.96, "Iraq": 1413.4,
    "Republic of Ireland": 1412.23, "North Macedonia": 1406.87, "Bosnia and Herzegovina": 1400.99,
    "Ghana": 1399.78, "DR Congo": 1395.2, "Finland": 1393.77, "Burkina Faso": 1385.61, "Iceland": 1383.07,
    "Albania": 1374.88, "Honduras": 1373.07, "United Arab Emirates": 1368.14, "Jordan": 1283.48,
    "New Zealand": 1221.75, "New Caledonia": 1058.0, "Kuwait": 1109.81, "India": 1132.03, "Afghanistan": 919.32,
    "Kyrgyz Republic": 1297.05, "Oman": 1307.72, "Palestine": 1269.83, "Indonesia": 1102.26, "China PR": 1275.25,
    "Bahrain": 1128.53, "Congo": 1204.68, "Tanzania": 1184.28, "Niger": 1072.07, "Zambia": 1241.65,
    "Cuba": 1291.68, "Bermuda": 1198.81, "Cayman Islands": 951.18, "Antigua and Barbuda": 1040.69,
    "Grenada": 1150.77, "Saint Kitts and Nevis": 998.67, "Bahamas": 872.2, "Aruba": 978.89, "Barbados": 940.33,
    "Saint Lucia": 1026.83, "Guyana": 1069.95, "Montserrat": 1061.5, "Belize": 1007.41, "Dominican Republic": 1181.82,
    "Dominica": 927.87, "British Virgin Islands": 809.8, "Saint Vincent and the Grenadines": 1039.67, "Anguilla": 786.9,
    "Puerto Rico": 1083.3, "Bolivia": 1302.2, "Mauritania": 1206.18, "Togo": 1162.77, "Sudan": 1120.35,
    "South Sudan": 948.33, "Benin": 1146.43, "Zimbabwe": 1092.36, "Rwanda": 1080.35, "Lesotho": 1047.88,
    "Cape Verde": 1435.32, "Angola": 1276.46, "Libya": 1182.26, "Eswatini": 966.86, "Mauritius": 903.07,
    "Gabon": 1290.35, "Kenya": 1166.19, "The Gambia": 1127.32, "Burundi": 1089.47, "Seychelles": 834.61,
    "Guinea": 1345.86, "Uganda": 1184.2, "Mozambique": 1166.7, "Botswana": 1083.56, "Somalia": 822.45,
    "Equatorial Guinea": 1238.19, "Namibia": 1152.06, "Malawi": 1109.84, "Liberia": 1039.69, "Sao Tome and Principe": 878.0,
    "Djibouti": 863.09, "Ethiopia": 1060.03, "Guinea-Bissau": 1218.4, "Sierra Leone": 1087.72, "North Korea": 1153.25,
    "Thailand": 1176.4, "Vietnam": 1169.96, "Syria": 1088.19, "Lebanon": 1010.42, "Tajikistan": 1100.91,
    "Bulgaria": 1365.17, "Israel": 1358.33, "Georgia": 1302.26, "Luxembourg": 1285.44, "Cyprus": 1155.24,
    "Kosovo": 1119.5, "Lithuania": 1062.24, "Estonia": 1007.41, "Latvia": 986.79, "Azerbaijan": 1159.26,
    "Kazakhstan": 1117.84, "Armenia": 1111.45, "Malta": 955.51, "Moldova": 909.11, "Gibraltar": 822.61,
    "San Marino": 743.08, "Liechtenstein": 724.87, "Andorra": 894.49, "Faroe Islands": 1037.13, "Madagascar": 1165.75,
    "Comoros": 1137.9, "Central African Republic": 1086.56, "Chad": 903.07, "Northern Ireland": 1300.0,
    "Belarus": 1250.0, "Trinidad and Tobago": 1350.0, "Curacao": 1300.0, "Haiti": 1280.0, "Nicaragua": 1270.0,
    "Guatemala": 1320.0, "Jamaica": 1400.0, "Suriname": 1250.0, "El Salvador": 1200.0, "Greenland": 500.0,
}

# --- UEFA Qualification ---
def get_uefa_qualified_teams():
    # Direct: top 16, Playoff: next 3
    uefa_teams = [
        "Spain", "France", "England", "Germany", "Italy", "Netherlands", "Portugal", "Belgium",
        "Croatia", "Switzerland", "Denmark", "Austria", "Ukraine", "Türkiye", "Sweden", "Wales",
        "Poland", "Serbia", "Scotland"
    ]
    direct = uefa_teams[:16]
    playoff = uefa_teams[16:]
    return direct, playoff

# --- CAF (Africa) Qualification ---
from collections import defaultdict

# FIFA Ranking points for CAF teams (June 2024 FIFA World Ranking)
caf_team_strengths = {
    "Morocco": 1676.99, "Senegal": 1623.34, "Egypt": 1515.1, "Tunisia": 1502.8, "Algeria": 1493.59,
    "Mali": 1475.29, "Ivory Coast": 1447.65, "Nigeria": 1445.69, "Burkina Faso": 1435.59, "Cameroon": 1421.93,
    "Ghana": 1399.79, "DR Congo": 1378.1, "South Africa": 1361.32, "Cape Verde": 1345.54, "Zambia": 1297.2,
    "Gabon": 1294.61, "Equatorial Guinea": 1269.83, "Uganda": 1238.16, "Benin": 1228.61, "Mauritania": 1226.54,
    "Madagascar": 1205.86, "Guinea-Bissau": 1184.28, "Namibia": 1179.94, "Angola": 1177.37, "Mozambique": 1168.04,
    "Gambia": 1166.5, "Sierra Leone": 1162.77, "Togo": 1150.14, "Tanzania": 1141.51, "Libya": 1133.09,
    "Zimbabwe": 1122.97, "Malawi": 1120.73, "Comoros": 1111.46, "Sudan": 1081.76, "Rwanda": 1060.03,
    "Burundi": 1050.21, "Ethiopia": 1032.54, "Botswana": 1021.93, "Eswatini": 1007.82, "Lesotho": 989.15,
    "Liberia": 982.72, "Central African Republic": 962.19, "Niger": 959.08, "Chad": 906.91,
    "Sao Tome and Principe": 864.03, "South Sudan": 841.48, "Djibouti": 821.57, "Seychelles": 800.74, "Somalia": 799.04, "Eritrea": 794.75,
}

# Current Group Standings after Matchday 6 (June 2025)
caf_current_group_standings = {
    "Group A": [("Morocco", 13), ("South Africa", 10), ("Zimbabwe", 5), ("Libya", 4)],
    "Group B": [("Senegal", 16), ("Egypt", 13), ("Ghana", 7), ("Angola", 3)],
    "Group C": [("Nigeria", 15), ("Ivory Coast", 12), ("Mali", 8), ("Mauritania", 1)],
    "Group D": [("Cameroon", 14), ("Burkina Faso", 11), ("DR Congo", 7), ("Togo", 3)],
    "Group E": [("Tunisia", 15), ("Algeria", 10), ("Morocco", 7), ("Zimbabwe", 0)],
    "Group F": [("Senegal", 18), ("Egypt", 12), ("Ghana", 6), ("Angola", 0)],
}

# Helper and simulation functions for CAF
def get_africa_qualified_teams():
    # Direct qualifiers based on current standings
    direct_qualifiers = []
    playoff_teams = []

    # Top 2 teams from each group qualify directly
    for group, teams in caf_current_group_standings.items():
        sorted_teams = sorted(teams, key=lambda x: -x[1])  # Sort by points, descending
        direct_qualifiers.extend([team[0] for team in sorted_teams[:2]])  # Top 2 teams

    # Placeholder: Last team from each group to playoff
    for group, teams in caf_current_group_standings.items():
        sorted_teams = sorted(teams, key=lambda x: -x[1])  # Sort by points, descending
        playoff_teams.append(sorted_teams[-1][0])  # Last team

    return list(set(direct_qualifiers)), list(set(playoff_teams))

# --- AFC (Asia) Qualification ---
from collections import defaultdict

afc_team_strengths = {
    "Japan": 1652.64, "IR Iran": 1637.39, "Korea Republic": 1575.0, "Australia": 1488.89, "Qatar": 1445.01,
    "Saudi Arabia": 1418.96, "Iraq": 1413.40, "Uzbekistan": 1437.02, "Jordan": 1389.15, "United Arab Emirates": 1382.70,
    "Oman": 1332.96, "Bahrain": 1290.00, "China PR": 1250.95, "Palestine": 1224.65, "Kyrgyzstan": 1205.68,
    "North Korea": 1153.38, "Indonesia": 1142.92, "Kuwait": 1109.91,
}

# Placeholder for group standings and fixtures (should be replaced with real data for full simulation)
afc_current_standings = {
    "Group A": ["Japan", "IR Iran", "Qatar", "Uzbekistan"],
    "Group B": ["Korea Republic", "Australia", "Saudi Arabia", "Iraq"],
    "Group C": ["Jordan", "United Arab Emirates", "Oman", "Bahrain"],
}

def get_asia_qualified_teams():
    # Direct qualifiers: top 2 from each group
    direct_qualifiers = []
    playoff_teams = []
    for group, teams in afc_current_standings.items():
        direct_qualifiers.extend(teams[:2])
        playoff_teams.append(teams[2])  # 3rd place to playoff
    return list(set(direct_qualifiers)), list(set(playoff_teams))

# --- CONCACAF (North America) Qualification ---
from collections import defaultdict

concacaf_groups = {
    "Group A": ["USA", "Canada", "Panama", "Honduras"],
    "Group B": ["Mexico", "Costa Rica", "Jamaica", "El Salvador"],
    "Group C": ["Trinidad and Tobago", "Guatemala", "Haiti", "Curaçao"],
}

def get_northamerica_qualified_teams():
    # Direct: group winners
    direct_qualifiers = []
    playoff_teams = []
    for group, teams in concacaf_groups.items():
        direct_qualifiers.append(teams[0])
        playoff_teams.append(teams[1])  # 2nd place to playoff
    return list(set(direct_qualifiers)), list(set(playoff_teams))

# --- CONMEBOL (South America) Qualification ---
from collections import defaultdict

conmebol_teams = [
    "Argentina", "Brazil", "Uruguay", "Colombia", "Ecuador", "Peru", "Venezuela", "Paraguay", "Chile", "Bolivia"
]
conmebol_points = {
    "Argentina": 34, "Ecuador": 24, "Paraguay": 24, "Brazil": 22, "Uruguay": 21, "Colombia": 21,
    "Venezuela": 18, "Bolivia": 14, "Peru": 11, "Chile": 10
}

def get_southamerica_qualified_teams():
    # Direct: top 6, Playoff: 7th
    sorted_teams = sorted(conmebol_points.items(), key=lambda x: -x[1])
    direct = [team for team, _ in sorted_teams[:6]]
    playoff = [sorted_teams[6][0]]
    return direct, playoff

# --- OFC (Oceania) Qualification ---
def get_ofc_qualified_teams():
    # OFC: New Zealand direct, New Caledonia to playoff
    return ["New Zealand"], ["New Caledonia"]

# --- Aggregate all direct and playoff teams ---
direct_teams = set()
playoff_teams = set()

direct, playoff = get_uefa_qualified_teams()
direct_teams.update(direct)
playoff_teams.update(playoff)

direct, playoff = get_africa_qualified_teams()
direct_teams.update(direct)
playoff_teams.update(playoff)

direct, playoff = get_asia_qualified_teams()
direct_teams.update(direct)
playoff_teams.update(playoff)

direct, playoff = get_northamerica_qualified_teams()
direct_teams.update(direct)
playoff_teams.update(playoff)

direct, playoff = get_southamerica_qualified_teams()
direct_teams.update(direct)
playoff_teams.update(playoff)

direct, playoff = get_ofc_qualified_teams()
direct_teams.update(direct)
playoff_teams.update(playoff)

# --- Inter-confederation playoff simulation ---
def simulate_interconf_playoff(playoff_teams, num_slots=2, sims=200):
    # For 48-team World Cup, usually 6 teams, 2 slots (format: 2 seeded, 4 play-off, then winners face seeds)
    # We'll do a simple knockout: random pairings, winners qualify
    playoff_teams = list(playoff_teams)
    qual_counts = defaultdict(int)
    for _ in range(sims):
        teams = playoff_teams[:]
        random.shuffle(teams)
        # If more than 2 slots, adjust logic
        while len(teams) > num_slots:
            next_round = []
            for i in range(0, len(teams), 2):
                if i+1 >= len(teams):
                    next_round.append(teams[i])
                    continue
                t1, t2 = teams[i], teams[i+1]
                # Use FIFA ranking as tiebreaker
                r1 = FIFA_RANKINGS.get(t1, 1000)
                r2 = FIFA_RANKINGS.get(t2, 1000)
                g1 = random.gauss(r1/500, 1)
                g2 = random.gauss(r2/500, 1)
                winner = t1 if g1 > g2 or (g1 == g2 and r1 >= r2) else t2
                next_round.append(winner)
            teams = next_round
        for t in teams:
            qual_counts[t] += 1
    # Return the most frequent qualifiers
    qualified = sorted(qual_counts, key=lambda t: -qual_counts[t])[:num_slots]
    return qualified

# --- Add interconf playoff winners to World Cup field ---
interconf_qualifiers = simulate_interconf_playoff(playoff_teams, num_slots=2, sims=200)
qualified_teams = list(direct_teams) + interconf_qualifiers

# --- World Cup Draw and Simulation (as before) ---
NUM_GROUPS = 8
TEAMS_PER_GROUP = 6
random.shuffle(qualified_teams)
groups = [qualified_teams[i::NUM_GROUPS] for i in range(NUM_GROUPS)]

NUM_SIMULATIONS = 100
stage_counts = {team: {"groups": 0, "R32": 0, "R16": 0, "QF": 0, "SF": 0, "Final": 0, "Winner": 0} for team in qualified_teams}

class Team:
    def __init__(self, name):
        self.name = name
        self.ranking_points = FIFA_RANKINGS.get(name, 1000)
    def __repr__(self):
        return f"{self.name} ({self.ranking_points})"
_team_cache = {}
def get_team(name):
    if name not in _team_cache:
        _team_cache[name] = Team(name)
    return _team_cache[name]
def simulate_match(team1, team2):
    elo_diff = team1.ranking_points - team2.ranking_points
    base_expected_goals = 1.3
    scale_factor = 0.002
    expected_goals_team1 = base_expected_goals * math.exp(scale_factor * elo_diff)
    expected_goals_team2 = base_expected_goals * math.exp(scale_factor * -elo_diff)
    goals_team1 = max(0, int(random.gauss(expected_goals_team1, 1.0) + 0.5))
    goals_team2 = max(0, int(random.gauss(expected_goals_team2, 1.0) + 0.5))
    return goals_team1, goals_team2

for _ in range(NUM_SIMULATIONS):
    random.shuffle(qualified_teams)
    sim_groups = [qualified_teams[i::NUM_GROUPS] for i in range(NUM_GROUPS)]
    knockout_teams = []
    # Group stage: top 2 from each group advance
    for group in sim_groups:
        group_results = []
        for team in group:
            points = 0
            gd = 0
            for opponent in group:
                if team == opponent:
                    continue
                t1 = get_team(team)
                t2 = get_team(opponent)
                g1, g2 = simulate_match(t1, t2)
                if g1 > g2:
                    points += 3
                elif g1 == g2:
                    points += 1
                gd += g1 - g2
            group_results.append((team, points, gd, t1.ranking_points))
        group_results.sort(key=lambda x: (x[1], x[2], x[3]), reverse=True)
        for idx, (team, *_ ) in enumerate(group_results):
            stage_counts[team]["groups"] += 1
            if idx < 2:
                knockout_teams.append(team)
                stage_counts[team]["R32"] += 1
    # R32
    next_round = knockout_teams[:]
    random.shuffle(next_round)
    # R16
    r16 = []
    for i in range(0, len(next_round), 2):
        t1 = get_team(next_round[i])
        t2 = get_team(next_round[i+1])
        g1, g2 = simulate_match(t1, t2)
        winner = next_round[i] if g1 > g2 or (g1 == g2 and t1.ranking_points >= t2.ranking_points) else next_round[i+1]
        r16.append(winner)
        stage_counts[winner]["R16"] += 1
    # QF
    qf = []
    random.shuffle(r16)
    for i in range(0, len(r16), 2):
        t1 = get_team(r16[i])
        t2 = get_team(r16[i+1])
        g1, g2 = simulate_match(t1, t2)
        winner = r16[i] if g1 > g2 or (g1 == g2 and t1.ranking_points >= t2.ranking_points) else r16[i+1]
        qf.append(winner)
        stage_counts[winner]["QF"] += 1
    # SF
    sf = []
    random.shuffle(qf)
    for i in range(0, len(qf), 2):
        t1 = get_team(qf[i])
        t2 = get_team(qf[i+1])
        g1, g2 = simulate_match(t1, t2)
        winner = qf[i] if g1 > g2 or (g1 == g2 and t1.ranking_points >= t2.ranking_points) else qf[i+1]
        sf.append(winner)
        stage_counts[winner]["SF"] += 1
    # Final
    final = []
    random.shuffle(sf)
    for i in range(0, len(sf), 2):
        t1 = get_team(sf[i])
        t2 = get_team(sf[i+1]) if i+1 < len(sf) else t1
        g1, g2 = simulate_match(t1, t2)
        winner = sf[i] if g1 > g2 or (g1 == g2 and t1.ranking_points >= t2.ranking_points) else (sf[i+1] if i+1 < len(sf) else sf[i])
        final.append(winner)
        stage_counts[winner]["Final"] += 1
    # Winner
    if len(final) >= 2:
        t1 = get_team(final[0])
        t2 = get_team(final[1])
        g1, g2 = simulate_match(t1, t2)
        winner = final[0] if g1 > g2 or (g1 == g2 and t1.ranking_points >= t2.ranking_points) else final[1]
        stage_counts[winner]["Winner"] += 1
    elif len(final) == 1:
        stage_counts[final[0]]["Winner"] += 1

# --- Output Results ---
print("\n--- World Cup 2026 Stage-by-Stage Simulation Results (100 runs) ---\n")
print("| Team                 | R32 (%) | R16 (%) | QF (%) | SF (%) | Final (%) | Winner (%) |")
print("|----------------------|---------|---------|--------|--------|-----------|------------|")
for team in sorted(qualified_teams, key=lambda t: -FIFA_RANKINGS.get(t, 0)):
    print(f"| {team:<20} | {stage_counts[team]['R32']:>7.1f} | {stage_counts[team]['R16']:>7.1f} | {stage_counts[team]['QF']:>6.1f} | {stage_counts[team]['SF']:>6.1f} | {stage_counts[team]['Final']:>9.1f} | {stage_counts[team]['Winner']:>10.1f} |")

# --- Simulate and print qualifying for each confederation ---
print("\n--- Confederation Qualifying Results ---")
confed_results = {}
for name, func in [
    ("UEFA", get_uefa_qualified_teams),
    ("CAF", get_africa_qualified_teams),
    ("AFC", get_asia_qualified_teams),
    ("CONCACAF", get_northamerica_qualified_teams),
    ("CONMEBOL", get_southamerica_qualified_teams),
    ("OFC", get_ofc_qualified_teams),
]:
    direct, playoff = func()
    confed_results[name] = (direct, playoff)
    print(f"{name}:\n  Direct: {sorted(direct)}\n  Playoff: {sorted(playoff)}\n")
