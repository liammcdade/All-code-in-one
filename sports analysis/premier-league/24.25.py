import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import copy

# === Step 1: Load and clean main player data ===
player_file = "sports analysis/premier-league/football analytics - player_data (4).csv"
df = pd.read_csv(player_file)
df = df.dropna(how='all')
df = df[df['Player'] != 'Player']
df = df.reset_index(drop=True)

df['Min'] = pd.to_numeric(df['Min'], errors='coerce')
df = df[df['Min'] >= 180]

non_numeric_cols = ['Player', 'Nation', 'Pos', 'Squad']
numeric_cols = [col for col in df.columns if col not in non_numeric_cols]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
df = df.fillna(0)

# Remove players who have minutes but no other stats
stats_cols = [col for col in df.columns if col not in ['Player', 'Nation', 'Pos', 'Squad', 'Min']]
df['StatsSum'] = df[stats_cols].sum(axis=1)
df = df[~((df['Min'] > 0) & (df['StatsSum'] == 0))].copy()
df.drop(columns=['StatsSum'], inplace=True)

# === Step 2: Load and merge additional stats ===
additional_stats_file = "sports analysis\premier-league\epl_player_stats_24_25.csv"
add_stats_df = pd.read_csv(additional_stats_file)
add_stats_df = add_stats_df.dropna(how='all')

header_rows = add_stats_df[add_stats_df.iloc[:, 0].astype(str).str.lower() == 'player'].index
add_stats_df = add_stats_df.drop(header_rows, errors='ignore').reset_index(drop=True)

possible_player_cols = ['Player', 'Player Name', 'Name']
player_col = None
for col in possible_player_cols:
    if col in add_stats_df.columns:
        player_col = col
        break
if player_col is None:
    raise ValueError("No player identifier column found in additional stats file.")
if player_col != 'Player':
    add_stats_df = add_stats_df.rename(columns={player_col: 'Player'})

existing_cols = set(df.columns)
new_stat_cols = [col for col in add_stats_df.columns if col not in existing_cols and col != 'Player']

df = df.merge(add_stats_df[['Player'] + new_stat_cols], on='Player', how='left')
df[new_stat_cols] = df[new_stat_cols].fillna(0)

# === Step 3: Define position groups and stats ===
pos_groups = {
    'GK': ['Saves', 'Saves %', 'Goals Prevented', 'Clean Sheets'],
    'DF': ['Tackles', 'Clearances', 'Interceptions', 'Blocks', 'Aerial Duels', 'aDuels Won', 'aDuels %', 'Ground Duels', 'gDuels Won'],
    'MF': ['Passes', 'Successful Passes', 'Passes%', 'PrgP', 'PrgC', 'PrgR', 'Carries', 'Progressive Carries', 'Through Balls', 'Crosses', 'Successful Crosses'],
    'FW': ['Gls', 'Ast', 'G+A', 'Shots', 'Shots On Target', 'Conversion %', 'Big Chances Missed', 'xG', 'npxG', 'xAG', 'npxG+xAG'],
}
card_stats = ['CrdY', 'CrdR']
for c in card_stats:
    df[c] = -df[c]

# === Step 3.1: Define stat weights and negative stats ===
stat_weights = {
    'GK': {
        'Saves': 2, 'Saves %': 2, 'Goals Prevented': 3, 'Clean Sheets': 3, 'CrdY': -1, 'CrdR': -2
    },
    'DF': {
        'Tackles': 2, 'Clearances': 2, 'Interceptions': 2, 'Blocks': 2, 'Aerial Duels': 1, 'aDuels Won': 1, 'aDuels %': 1, 'Ground Duels': 1, 'gDuels Won': 1, 'CrdY': -1, 'CrdR': -2
    },
    'MF': {
        'Passes': 1, 'Successful Passes': 2, 'Passes%': 1, 'PrgP': 1, 'PrgC': 1, 'PrgR': 1, 'Carries': 1, 'Progressive Carries': 1, 'Through Balls': 2, 'Crosses': 1, 'Successful Crosses': 2, 'CrdY': -1, 'CrdR': -2
    },
    'FW': {
        'Gls': 3, 'Ast': 2, 'G+A': 2, 'Shots': 1, 'Shots On Target': 1, 'Conversion %': 1, 'Big Chances Missed': -2, 'xG': 2, 'npxG': 2, 'xAG': 1, 'npxG+xAG': 1, 'CrdY': -1, 'CrdR': -2
    }
}

# === Step 3.2: Exclude stats with too many zeros per position ===
def get_valid_stats(df, pos):
    stats = list(stat_weights[pos].keys())
    valid = []
    for stat in stats:
        if stat in df.columns:
            nonzero = (df[df['Pos'] == pos][stat] != 0).sum()
            total = (df['Pos'] == pos).sum()
            if total > 0 and nonzero / total > 0.2:  # keep if >20% nonzero
                valid.append(stat)
    return valid

# === Step 4: Explode multi-position players and clean % fields ===
df_exp = df.assign(Pos=df['Pos'].str.split(',')).explode('Pos')
df_exp['Pos'] = df_exp['Pos'].str.strip()
df_exp = df_exp[df_exp['Pos'].isin(pos_groups.keys())]

for col in df_exp.columns:
    if df_exp[col].dtype == 'object' and df_exp[col].astype(str).str.contains('%').any():
        df_exp[col] = df_exp[col].astype(str).str.replace('%', '', regex=False)
        df_exp[col] = pd.to_numeric(df_exp[col], errors='coerce').fillna(0)

df_exp['90s'] = pd.to_numeric(df_exp['90s'], errors='coerce').fillna(0)

# === Step 4.5: Keep only players with at least one nonzero value in relevant stats ===
def has_any_stats(row):
    pos = row['Pos']
    required = pos_groups[pos] + card_stats
    required = [s for s in required if s in row.index]
    if not required:
        return False
    return any(row[stat] > 0 for stat in required)

df_exp = df_exp[df_exp.apply(has_any_stats, axis=1)].copy()

# === Step 4.5: Keep only players with enough nonzero stats ===
def has_enough_stats(row):
    pos = row['Pos']
    valid_stats = get_valid_stats(df_exp, pos)
    nonzero_count = sum(row.get(stat, 0) != 0 for stat in valid_stats)
    return nonzero_count >= max(2, len(valid_stats) // 2)  # at least half nonzero

df_exp = df_exp[df_exp.apply(has_enough_stats, axis=1)].copy()

# After filtering, ensure all columns are unique (remove duplicates by name)
df_exp = df_exp.loc[:, ~df_exp.columns.duplicated()]

# === Step 5: Score players with weights, negatives, and stat normalization ===
def score_player(row):
    pos = row['Pos']
    valid_stats = get_valid_stats(df_exp, pos)
    if not valid_stats:
        return 0.0
    values = []
    weights = []
    zero_penalty_count = 0
    for stat in valid_stats:
        val = pd.to_numeric(row.get(stat, 0), errors='coerce')
        stat_vals = pd.to_numeric(df_exp[df_exp['Pos'] == pos][stat], errors='coerce').fillna(0)
        minv, maxv = stat_vals.min(), stat_vals.max()
        if maxv > minv:
            norm_val = (val - minv) / (maxv - minv)
        else:
            norm_val = 0
        w = stat_weights[pos][stat]
        values.append(norm_val * w)
        weights.append(abs(w))
        # Penalize for zero in positive-weighted stats
        if w > 0 and val == 0:
            zero_penalty_count += 1
    if not weights or sum(weights) == 0:
        return 0.0
    base_score = sum(values) / sum(weights)
    # Slight penalty: 2% per zero in positive stat
    penalty = max(0, 1 - 0.02 * zero_penalty_count)
    return penalty * base_score

raw_scores = df_exp.apply(score_player, axis=1)
df_exp['RawScore'] = raw_scores

# === Step 6: Weight score by games played ===
df_exp['WeightedScore'] = df_exp['RawScore'] * np.log1p(df_exp['90s'])

# === Step 7: Normalize per position ===
df_exp['NormalizedScore'] = 0.0
for pos in pos_groups.keys():
    mask = df_exp['Pos'] == pos
    subset = df_exp.loc[mask, ['WeightedScore']]
    if subset.shape[0] == 0:
        continue
    scaler = MinMaxScaler()
    df_exp.loc[mask, 'NormalizedScore'] = scaler.fit_transform(subset)

# === Step 8: Best position per player ===
idx = df_exp.groupby('Player')['NormalizedScore'].idxmax()
df_best_pos = df_exp.loc[idx].copy()

# === Step 9: Convert to 1–10 scale ===
mean = df_best_pos['NormalizedScore'].mean()
std = df_best_pos['NormalizedScore'].std()
if std == 0:
    df_best_pos['Rating'] = 5.0
else:
    z = (df_best_pos['NormalizedScore'] - mean) / std
    df_best_pos['Rating'] = np.clip(z * 2 + 5, 1, 10)
df_best_pos['Rating'] = df_best_pos['Rating'].round(3)

# === Step 10: Display results ===
for pos in pos_groups.keys():
    print(f"\nTop 5 Players at position {pos}:")
    top5 = df_best_pos[df_best_pos['Pos'] == pos].sort_values('Rating', ascending=False).head(5)
    print(top5[['Player', 'Squad', 'Rating']].to_string(index=False))

    print(f"\nBottom 5 Players at position {pos}:")
    bottom5 = df_best_pos[df_best_pos['Pos'] == pos].sort_values('Rating', ascending=True).head(5)
    print(bottom5[['Player', 'Squad', 'Rating']].to_string(index=False))

N_RUNS = 1000
all_scores = {pos: {} for pos in pos_groups.keys()}

for run in range(N_RUNS):
    # Randomize weights for this run
    run_weights = copy.deepcopy(stat_weights)
    for pos in run_weights:
        for stat in run_weights[pos]:
            base = stat_weights[pos][stat]
            # Only randomize if not zero
            if base != 0:
                run_weights[pos][stat] = base * np.random.uniform(0.7, 1.3)

    def get_valid_stats_run(df, pos):
        stats = list(run_weights[pos].keys())
        valid = []
        for stat in stats:
            if stat in df.columns:
                nonzero = (df[df['Pos'] == pos][stat] != 0).sum()
                total = (df['Pos'] == pos).sum()
                if total > 0 and nonzero / total > 0.2:
                    valid.append(stat)
        return valid

    def score_player_run(row):
        pos = row['Pos']
        valid_stats = get_valid_stats_run(df_exp, pos)
        if not valid_stats:
            return 0.0
        values = []
        weights = []
        zero_penalty_count = 0
        for stat in valid_stats:
            val = pd.to_numeric(row.get(stat, 0), errors='coerce')
            stat_vals = pd.to_numeric(df_exp[df_exp['Pos'] == pos][stat], errors='coerce').fillna(0)
            minv, maxv = stat_vals.min(), stat_vals.max()
            if maxv > minv:
                norm_val = (val - minv) / (maxv - minv)
            else:
                norm_val = 0
            w = run_weights[pos][stat]
            values.append(norm_val * w)
            weights.append(abs(w))
            if w > 0 and val == 0:
                zero_penalty_count += 1
        if not weights or sum(weights) == 0:
            return 0.0
        base_score = sum(values) / sum(weights)
        penalty = max(0, 1 - 0.02 * zero_penalty_count)
        return penalty * base_score

    raw_scores = df_exp.apply(score_player_run, axis=1)
    weighted_scores = raw_scores * np.log1p(df_exp['90s'])
    # Normalize per position
    norm_scores = np.zeros_like(weighted_scores)
    for pos in pos_groups.keys():
        mask = df_exp['Pos'] == pos
        subset = weighted_scores[mask]
        if subset.shape[0] == 0:
            continue
        scaler = MinMaxScaler()
        normed = scaler.fit_transform(subset.values.reshape(-1, 1)).flatten()
        norm_scores[mask] = normed
    # Store scores for each player/position
    for i, row in df_exp.iterrows():
        player = row['Player']
        pos = row['Pos']
        if player not in all_scores[pos]:
            all_scores[pos][player] = []
        all_scores[pos][player].append(norm_scores[i])

# Compute average score for each player/position
avg_scores = {pos: {} for pos in pos_groups.keys()}
for pos in all_scores:
    for player in all_scores[pos]:
        avg_scores[pos][player] = np.mean(all_scores[pos][player])

# Build DataFrame for ranking
rank_rows = []
for pos in avg_scores:
    for player in avg_scores[pos]:
        # Get squad for display
        squad = df_exp[(df_exp['Player'] == player) & (df_exp['Pos'] == pos)]['Squad'].iloc[0]
        rank_rows.append({'Player': player, 'Squad': squad, 'Pos': pos, 'AvgScore': avg_scores[pos][player]})
rank_df = pd.DataFrame(rank_rows)

# === Step 10: Display results ===
for pos in pos_groups.keys():
    print(f"\nTop 5 Players at position {pos} (robust avg):")
    top5 = rank_df[rank_df['Pos'] == pos].sort_values('AvgScore', ascending=False).head(5)
    print(top5[['Player', 'Squad', 'AvgScore']].to_string(index=False))

    print(f"\nBottom 5 Players at position {pos} (robust avg):")
    bottom5 = rank_df[rank_df['Pos'] == pos].sort_values('AvgScore', ascending=True).head(5)
    print(bottom5[['Player', 'Squad', 'AvgScore']].to_string(index=False))
