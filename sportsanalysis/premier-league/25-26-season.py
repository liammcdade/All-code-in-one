import pandas as pd
import numpy as np
import random
from itertools import product
from tqdm import tqdm
from tabulate import tabulate

def fractional_to_probability(frac_odds):
    """
    Converts fractional odds (e.g., '5/1' or '2/5') to implied probability
    """
    try:
        if frac_odds == "∞":
            return 0.001  # Very low chance
        num, den = map(float, frac_odds.split('/'))
        decimal_odds = num / den + 1
        return 1 / decimal_odds
    except Exception as e:
        raise ValueError(f"Invalid fractional odds format: {frac_odds}")

def simulate_premier_league_with_fractional_odds(custom_odds, num_simulations=50):
    """
    Simulates Premier League using custom team odds given as fractions.
    custom_odds: dict of {team_name: fractional_odds} e.g. {"Team A": "5/1"}
    """

    teams = list(custom_odds.keys())

    # Convert fractional odds to strength scores (implied probabilities)
    strength_dict = {t: fractional_to_probability(o) for t, o in custom_odds.items()}

    # Generate fixtures
    matches = [(home, away) for home, away in product(teams, repeat=2) if home != away]

    # Initialize tracking
    all_results = {team: {'Points': [], 'GF': [], 'GA': []} for team in teams}
    champion_count = {team: 0 for team in teams}
    relegation_count = {team: 0 for team in teams}

    # Run simulations
    total_games = num_simulations * len(matches)
    with tqdm(total=total_games, desc="Simulating Matches", unit="match") as pbar:
        for sim_num in range(num_simulations):

            standings = {team: {'Points': 0, 'GF': 0, 'GA': 0} for team in teams}

            for home, away in matches:
                home_strength = strength_dict[home]
                away_strength = strength_dict[away]

                # Add small home advantage
                home_advantage = 0.05
                total = home_strength + home_advantage + away_strength

                home_win_prob = (home_strength + home_advantage) / total
                away_win_prob = away_strength / total
                draw_prob = 1 - home_win_prob - away_win_prob

                # Randomly pick result based on probability
                r = random.random()
                if r < home_win_prob:
                    outcome = 'home_win'
                elif r < home_win_prob + draw_prob:
                    outcome = 'draw'
                else:
                    outcome = 'away_win'

                # Simulate goals based on team strength
                base_home_goals = round(np.random.normal(home_strength * 2, 0.5))
                base_away_goals = round(np.random.normal(away_strength * 2, 0.5))

                # Apply outcome
                if outcome == 'home_win':
                    hg = max(1, base_home_goals)
                    ag = max(0, base_away_goals - 1)
                    standings[home]['Points'] += 3
                elif outcome == 'away_win':
                    ag = max(1, base_away_goals)
                    hg = max(0, base_home_goals - 1)
                    standings[away]['Points'] += 3
                else:
                    hg = max(0, base_home_goals - 1)
                    ag = max(0, base_away_goals - 1)
                    standings[home]['Points'] += 1
                    standings[away]['Points'] += 1

                # Update goal stats
                standings[home]['GF'] += hg
                standings[home]['GA'] += ag
                standings[away]['GF'] += ag
                standings[away]['GA'] += hg

                pbar.update(1)

            # Record results of this simulation
            for team in teams:
                all_results[team]['Points'].append(standings[team]['Points'])
                all_results[team]['GF'].append(standings[team]['GF'])
                all_results[team]['GA'].append(standings[team]['GA'])

            # Record champion and relegated teams
            sorted_standings = sorted(
                [{'Team': t, 'Points': standings[t]['Points'], 'GD': standings[t]['GF'] - standings[t]['GA']} for t in teams],
                key=lambda x: (x['Points'], x['GD']),
                reverse=True
            )
            champion_count[sorted_standings[0]['Team']] += 1
            for i in range(len(sorted_standings)-3, len(sorted_standings)):
                team = sorted_standings[i]['Team']
                relegation_count[team] += 1

    # Step 5: Build summary table
    summary = []
    for team in teams:
        avg_points = round(np.mean(all_results[team]['Points']), 1)
        avg_gf = round(np.mean(all_results[team]['GF']))
        avg_ga = round(np.mean(all_results[team]['GA']))
        avg_gd = avg_gf - avg_ga
        summary.append({
            'Team': team,
            'Expected Points': avg_points,
            'Expected GF': avg_gf,
            'Expected GA': avg_ga,
            'Expected GD': avg_gd
        })

    summary_df = pd.DataFrame(summary)
    summary_df = summary_df.sort_values(by=['Expected Points', 'Expected GD'], ascending=False)
    summary_df['Position'] = range(1, len(summary_df)+1)

    # Step 6: Add odds
    def prob_to_fractional(prob):
        if prob <= 0.001:
            return "∞"
        odds_decimal = 1 / prob
        num = round((odds_decimal - 1) * 10)
        den = 10
        gcd = np.gcd(int(num), int(den))
        return f"{int(num // gcd)} / {int(den // gcd)}"

    champion_prob = {t: round(champion_count[t] / num_simulations, 4) for t in teams}
    relegation_prob = {t: round(relegation_count[t] / num_simulations, 4) for t in teams}

    summary_df['Champion Probability'] = summary_df['Team'].map(lambda t: champion_prob[t])
    summary_df['Relegation Probability'] = summary_df['Team'].map(lambda t: relegation_prob[t])
    summary_df['Win Odds (Fractional)'] = summary_df['Team'].map(lambda t: prob_to_fractional(champion_prob[t]))
    summary_df['Relegation Odds (Fractional)'] = summary_df['Team'].map(lambda t: prob_to_fractional(relegation_prob[t]))

    return summary_df

custom_odds = {
    'Manchester City': '1/2',
    'Arsenal': '5/1',
    'Liverpool': '6/1',
    'Chelsea': '10/1',
    'Tottenham': '12/1',
    'Manchester Utd': '14/1',
    'Newcastle Utd': '20/1',
    'Brighton': '25/1',
    'Fulham': '40/1',
    'Crystal Palace': '50/1',
    'Wolves': '60/1',
    'Everton': '66/1',
    'Brentford': '80/1',
    'West Ham': '100/1',
    'Aston Villa': '100/1',
    'Leicester City': '100/1',
    "Nott'ham Forest": '100/1',
    'Burnley': '200/1',
    'Luton Town': '250/1',
    'Sheffield United': '300/1'
}

# Run simulation
print("Running Premier League Season Simulations...")
final_table = simulate_premier_league_with_fractional_odds(custom_odds, num_simulations=100)

# Print final table with nice formatting
print(tabulate(final_table, headers='keys', tablefmt='fancy_grid', showindex=False))