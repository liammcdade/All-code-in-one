# --- Odds (fractional format) ---
premier_league_odds = {
    "Liverpool": "2/1",
    "Arsenal": "9/4",
    "Manchester City": "5/2",
    "Chelsea": "12/1",
    "Newcastle United": "20/1",
    "Manchester United": "25/1",
    "Tottenham": "50/1",
    "Aston Villa": "66/1",
    "Nottingham Forest": "200/1",
    "AFC Bournemouth": "250/1",
    "Brighton": "250/1",
    "Everton": "250/1",
    "Brentford": "500/1",
    "Crystal Palace": "500/1",
    "Fulham": "500/1",
    "West Ham United": "500/1",
    "Wolverhampton Wanderers": "500/1",
    "Leeds United": "750/1",
    "Burnley": "1000/1",
    "Sunderland": "1000/1"
}

top4_odds = {
    "Liverpool": "1/6",
    "Arsenal": "1/5",
    "Manchester City": "2/9",
    "Newcastle United": "6/5",
    "Chelsea": "6/4",
    "Aston Villa": "7/2",
    "Manchester United": "9/2",
    "Tottenham": "5/1",
    "Brighton": "12/1",
    "Nottingham Forest": "20/1",
    "AFC Bournemouth": "25/1",
    "Crystal Palace": "25/1",
    "Everton": "25/1",
    "Fulham": "33/1",
    "West Ham United": "33/1",
    "Brentford": "40/1",
    "Wolverhampton Wanderers": "50/1",
    "Leeds United": "100/1",
    "Burnley": "150/1",
    "Sunderland": "200/1"
}

relegation_odds = {
    "Sunderland": "1/4",
    "Burnley": "2/5",
    "Leeds United": "10/11",
    "Brentford": "7/2",
    "Wolverhampton Wanderers": "7/2",
    "West Ham United": "6/1",
    "Everton": "7/1",
    "Fulham": "7/1",
    "Crystal Palace": "8/1",
    "AFC Bournemouth": "9/1",
    "Nottingham Forest": "10/1",
    "Brighton": "14/1",
    "Manchester United": "20/1",
    "Manchester City": "20/1",
    "Tottenham": "40/1",
    "Arsenal": "100/1",
    "Aston Villa": "100/1",
    "Chelsea": "100/1",
    "Liverpool": "100/1",
    "Newcastle United": "100/1"
}

def fractional_to_probability(fraction):
    num, denom = map(int, fraction.split('/'))
    return denom / (num + denom)

# --- Title: normalize because only one winner ---
title_probs = {team: fractional_to_probability(odds) for team, odds in premier_league_odds.items()}
title_total = sum(title_probs.values())
title_normalized = {team: prob / title_total for team, prob in title_probs.items()}

# --- Top 4: do not normalize ---
top4_probs = {team: fractional_to_probability(odds) for team, odds in top4_odds.items()}

# --- Relegation: do not normalize ---
relegation_probs = {team: fractional_to_probability(odds) for team, odds in relegation_odds.items()}

# --- Output ---
print("\nPremier League title probabilities (normalized):")
for team, prob in sorted(title_normalized.items(), key=lambda x: x[1], reverse=True):
    print(f"{team:25}: {prob*100:.2f}%")

print("\nTop 4 finish probabilities (raw implied):")
for team, prob in sorted(top4_probs.items(), key=lambda x: x[1], reverse=True):
    print(f"{team:25}: {prob*100:.2f}%")

print("\nTop 5 most likely to be relegated (raw implied):")
for team, prob in sorted(relegation_probs.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"{team:25}: {prob*100:.2f}%")
