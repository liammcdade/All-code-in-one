###############################################################
# Premier League Title Odds (Winning Odds) - averaged from multiple sources
# Other odds (top4, relegation) remain unchanged
###############################################################
premier_league_odds_raw = {
    "Liverpool": ["9/5", "15/8", "15/8", "2/1", "15/8", "15/8", "9/5", "15/8", "37/20", "15/8"],
    "Arsenal": ["9/4", "9/4", "9/4", "9/4", "9/4", "9/4", "9/4", "9/4", "9/4", "9/4"],
    "Manchester City": ["5/2", "5/2", "5/2", "3/1", "5/2", "5/2", "5/2", "5/2", "5/2", "5/2"],
    "Chelsea": ["13/1", "14/1", "13/1", "13/1", "14/1", "14/1", "13/1", "13/1", "12/1", "13/1"],
    "Newcastle United": ["26/1", "22/1", "26/1", "26/1", "16/1", "22/1", "26/1", "21/1", "25/1", "21/1"],
    "Manchester United": ["26/1", "28/1", "26/1", "34/1", "25/1", "28/1", "26/1", "31/1", "25/1", "31/1"],
    "Tottenham": ["51/1", "50/1", "51/1", "51/1", "50/1", "50/1", "51/1", "51/1", "50/1", "51/1"],
    "Aston Villa": ["67/1", "66/1", "67/1", "81/1", "40/1", "66/1", "67/1", "51/1", "66/1", "51/1"],
    "Brighton": ["151/1", "125/1", "151/1", "251/1", "250/1", "125/1", "151/1", "201/1", "150/1", "201/1"],
    "Nottingham Forest": ["201/1", "175/1", "201/1", "301/1", "150/1", "175/1", "201/1", "201/1", "200/1", "201/1"],
    "AFC Bournemouth": ["351/1", "300/1", "351/1", "501/1", "300/1", "300/1", "351/1", "301/1", "350/1", "301/1"],
    "Everton": ["501/1", "500/1", "501/1", "501/1", "500/1", "500/1", "501/1", "501/1", "500/1", "501/1"],
    "West Ham United": ["751/1", "500/1", "501/1", "751/1", "500/1", "500/1", "751/1", "501/1", "750/1", "501/1"],
    "Crystal Palace": ["751/1", "500/1", "751/1", "501/1", "500/1", "500/1", "751/1", "501/1", "750/1", "501/1"],
    "Fulham": ["751/1", "500/1", "751/1", "751/1", "500/1", "500/1", "751/1", "501/1", "750/1", "501/1"],
    "Wolverhampton Wanderers": ["1000/1", "1000/1", "1001/1", "751/1", "1000/1", "1000/1", "1000/1", "501/1", "1000/1", "501/1"],
    "Brentford": ["1000/1", "1000/1", "1001/1", "1000/1", "750/1", "1000/1", "1000/1", "501/1", "1000/1", "501/1"],
    "Leeds United": ["1000/1", "1000/1", "1001/1", "501/1", "1000/1", "1000/1", "1000/1", "1000/1", "1000/1", "1000/1"],
    "Burnley": ["1500/1", "1000/1", "1501/1", "1000/1", "1500/1", "1000/1", "1500/1", "1000/1", "1500/1", "1000/1"],
    "Sunderland": ["20/21", "1000/1", "20/21", "1000/1", "2000/1", "1000/1", "20/21", "1000/1", "2000/1", "1000/1"]
}

def average_fractional_odds(odds_list):
    # Skip missing or invalid odds
    valid = [o for o in odds_list if o != '-' and '/' in o]
    nums, dens = zip(*[map(int, o.split('/')) for o in valid])
    avg_num = sum(nums) / len(nums)
    avg_den = sum(dens) / len(dens)
    return f"{round(avg_num)}/{round(avg_den)}"

premier_league_odds = {team: average_fractional_odds(odds) for team, odds in premier_league_odds_raw.items()}

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
