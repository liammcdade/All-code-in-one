import random

# --- Example initial table (in-memory, editable, labeled) ---
INITIAL_TABLE = [
    {'Group': 'A', 'Team': 'Norway',      'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
    {'Group': 'A', 'Team': 'Switzerland','P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
    {'Group': 'A', 'Team': 'Iceland',    'P': 1, 'W': 0, 'D': 0, 'L': 1, 'GF': 0, 'GA': 1, 'GD': -1, 'Pts': 0},
    {'Group': 'A', 'Team': 'Finland',    'P': 1, 'W': 1, 'D': 0, 'L': 0, 'GF': 1, 'GA': 0, 'GD': 1, 'Pts': 0},
    {'Group': 'B', 'Team': 'Spain',      'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
    {'Group': 'B', 'Team': 'Italy',      'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
    {'Group': 'B', 'Team': 'Belgium',    'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
    {'Group': 'B', 'Team': 'Portugal',   'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
    {'Group': 'C', 'Team': 'Germany',    'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
    {'Group': 'C', 'Team': 'Sweden',     'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
    {'Group': 'C', 'Team': 'Denmark',    'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
    {'Group': 'C', 'Team': 'Poland',     'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
    {'Group': 'D', 'Team': 'England',    'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 6, 'GA': 0, 'GD': 0, 'Pts': 0},
    {'Group': 'D', 'Team': 'France',     'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
    {'Group': 'D', 'Team': 'Netherlands','P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
    {'Group': 'D', 'Team': 'Wales',      'P': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0},
]

# --- All group stage fixtures (edit as needed) ---
GROUP_FIXTURES = [
    # Group A
    ("Norway", "Switzerland"), ("Norway", "Iceland"), ("Switzerland", "Finland"), ("Norway", "Finland"), ("Switzerland", "Iceland"),
    # Group B
    ("Spain", "Italy"), ("Belgium", "Portugal"), ("Spain", "Belgium"), ("Italy", "Portugal"), ("Spain", "Portugal"), ("Italy", "Belgium"),
    # Group C
    ("Germany", "Sweden"), ("Denmark", "Poland"), ("Germany", "Denmark"), ("Sweden", "Poland"), ("Germany", "Poland"), ("Sweden", "Denmark"),
    # Group D
    ("England", "France"), ("Netherlands", "Wales"), ("England", "Netherlands"), ("France", "Wales"), ("England", "Wales"), ("France", "Netherlands"),
]

# --- FIFA/UEFA Women's Rankings (example, update as needed) ---
FIFA_UEFA_RANKINGS = {
    'England': 1, 'Spain': 2, 'France': 3, 'Germany': 4, 'Sweden': 5, 'Netherlands': 6, 'Italy': 7, 'Norway': 8,
    'Denmark': 9, 'Belgium': 10, 'Switzerland': 11, 'Portugal': 12, 'Iceland': 13, 'Finland': 14, 'Poland': 15, 'Wales': 16
}
# Lower number = stronger team

# --- In-memory table helpers ---
def make_table():
    table = {}
    for row in INITIAL_TABLE:
        team = row['Team']
        table[team] = row.copy()
    return table

def reset_table(table):
    for team in table:
        table[team].update({'P':0,'W':0,'D':0,'L':0,'GF':0,'GA':0,'GD':0,'Pts':0})

# --- Print table ---
def print_table(table: dict) -> None:
    """Prints the table in a simple format."""
    columns = ['P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']
    print("Group, Team, " + ", ".join(columns))
    for team, stats in table.items():
        stat_str = " ".join([f"{col}:{stats[col]}" for col in columns])
        print(f"{stats['Group']}, {team}, {stat_str}")

# --- Print table sorted by group and points ---
def print_full_table(table: dict) -> None:
    """Prints the table sorted by group, points, goal difference, and goals for."""
    columns = ['P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']
    print("Group, Team, " + ", ".join(columns))
    teams = list(table.items())
    teams.sort(key=lambda x: (x[1]['Group'], -x[1]['Pts'], -x[1]['GD'], -x[1]['GF'], x[0]))
    for team, stats in teams:
        stat_str = " ".join([f"{col}:{stats[col]}" for col in columns])
        print(f"{stats['Group']}, {team}, {stat_str}")

# --- Update match result in the table ---
def update_match(table, team1, team2, goals1, goals2):
    for team in [team1, team2]:
        table[team]['P'] += 1
    table[team1]['GF'] += goals1
    table[team1]['GA'] += goals2
    table[team2]['GF'] += goals2
    table[team2]['GA'] += goals1
    table[team1]['GD'] = table[team1]['GF'] - table[team1]['GA']
    table[team2]['GD'] = table[team2]['GF'] - table[team2]['GA']
    if goals1 > goals2:
        table[team1]['W'] += 1
        table[team2]['L'] += 1
        table[team1]['Pts'] += 3
    elif goals1 < goals2:
        table[team2]['W'] += 1
        table[team1]['L'] += 1
        table[team2]['Pts'] += 3
    else:
        table[team1]['D'] += 1
        table[team2]['D'] += 1
        table[team1]['Pts'] += 1
        table[team2]['Pts'] += 1

# (Removed duplicate print_full_table definition)

# --- Simulate a single match using rankings ---
def simulate_match_result_strength(team1, team2):
    r1 = FIFA_UEFA_RANKINGS.get(team1, 20)
    r2 = FIFA_UEFA_RANKINGS.get(team2, 20)
    diff = r2 - r1
    p1 = 0.5 + 0.12 * diff
    p1 = max(0.05, min(0.9, p1))
    p2 = 1 - p1
    outcome = random.choices(['win1', 'draw', 'win2'], weights=[p1, 0.18, p2])[0]
    if outcome == 'win1':
        g1, g2 = random.randint(1, 3), random.randint(0, 1)
    elif outcome == 'win2':
        g1, g2 = random.randint(0, 1), random.randint(1, 3)
    else:
        g1 = g2 = random.randint(0, 2)
    return g1, g2

# --- Simulate full group stage using rankings ---
def simulate_group_stage_strength(table):
    for team1, team2 in GROUP_FIXTURES:
        g1, g2 = simulate_match_result_strength(team1, team2)
        update_match(table, team1, team2, g1, g2)

# --- Get group standings as list of lists ---
def get_group_standings(table):
    groups = {}
    for team, stats in table.items():
        groups.setdefault(stats['Group'], []).append((team, stats))
    standings = {}
    for group, teams in groups.items():
        teams.sort(key=lambda x: (-x[1]['Pts'], -x[1]['GD'], -x[1]['GF'], x[0]))
        standings[group] = teams
    return standings

# --- Full tournament simulation with win probabilities ---
def simulate_full_tournament_prob(num_sims=1000):
    win_counts = {team: 0 for team in FIFA_UEFA_RANKINGS}
    for _ in range(num_sims):
        table = make_table()
        simulate_group_stage_strength(table)
        standings = get_group_standings(table)
        qualifiers = []
        for group in sorted(standings):
            qualifiers.extend([standings[group][0][0], standings[group][1][0]])
        next_round = qualifiers[:]
        random.shuffle(next_round)
        while len(next_round) > 1:
            winners = []
            for i in range(0, len(next_round), 2):
                if i+1 >= len(next_round):
                    winners.append(next_round[i])
                else:
                    t1, t2 = next_round[i], next_round[i+1]
                    r1 = FIFA_UEFA_RANKINGS.get(t1, 20)
                    r2 = FIFA_UEFA_RANKINGS.get(t2, 20)
                    p1 = 0.5 + 0.12 * (r2 - r1)
                    p1 = max(0.05, min(0.9, p1))
                    winner = t1 if random.random() < p1 else t2
                    winners.append(winner)
            next_round = winners
        win_counts[next_round[0]] += 1
    print("\n--- Tournament Win Probabilities ({} sims) ---".format(num_sims))
    for team, count in sorted(win_counts.items(), key=lambda x: -x[1]):
        print(f"{team:15}: {count/num_sims:.2%}")

# --- Usage Example ---
if __name__ == "__main__":
    simulate_full_tournament_prob(1000)
