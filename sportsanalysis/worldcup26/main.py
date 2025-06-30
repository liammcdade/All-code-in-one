import importlib
import math
import random
from collections import defaultdict

# --- Minimal team and match logic for World Cup simulation ---
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

# --- Import confederation simulation modules ---
confed_modules = {
    "UEFA": "sports analysis.worldcup26.qualifying.uefa",
    "CAF": "sports analysis.worldcup26.qualifying.Africa",
    "AFC": "sports analysis.worldcup26.qualifying.Asia",
    "CONCACAF": "sports analysis.worldcup26.qualifying.NorthAmerica",
    "CONMEBOL": "sports analysis.worldcup26.qualifying.Southamerica",
    "OFC": "sports analysis.worldcup26.qualifying.ofc",
}

def get_confed_qualified(confed_name):
    mod = importlib.import_module(confed_modules[confed_name])
    return mod.get_qualified_teams()

# --- Get all direct and playoff teams ---
direct_teams = set()
playoff_teams = set()
for confed in confed_modules:
    direct, playoff = get_confed_qualified(confed)
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
        t2 = get_team(sf[i+1])
        g1, g2 = simulate_match(t1, t2)
        winner = sf[i] if g1 > g2 or (g1 == g2 and t1.ranking_points >= t2.ranking_points) else sf[i+1]
        final.append(winner)
        stage_counts[winner]["Final"] += 1
    # Winner
    if final:
        t1 = get_team(final[0])
        t2 = get_team(final[1]) if len(final) > 1 else t1
        g1, g2 = simulate_match(t1, t2)
        winner = final[0] if g1 > g2 or (g1 == g2 and t1.ranking_points >= t2.ranking_points) else final[1]
        stage_counts[winner]["Winner"] += 1

# --- Output Results ---
print("\n--- World Cup 2026 Stage-by-Stage Simulation Results (100 runs) ---\n")
print("| Team                 | R32 (%) | R16 (%) | QF (%) | SF (%) | Final (%) | Winner (%) |")
print("|----------------------|---------|---------|--------|--------|-----------|------------|")
for team in sorted(qualified_teams, key=lambda t: -FIFA_RANKINGS.get(t, 0)):
    print(f"| {team:<20} | {stage_counts[team]['R32']:>7.1f} | {stage_counts[team]['R16']:>7.1f} | {stage_counts[team]['QF']:>6.1f} | {stage_counts[team]['SF']:>6.1f} | {stage_counts[team]['Final']:>9.1f} | {stage_counts[team]['Winner']:>10.1f} |")
