import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np
# === Load player-level season stats ===
df = pd.read_csv("sports analysis/premier-league/football analytics - player_data (4).csv")

df.columns = df.columns.str.strip()
df = df.drop(columns=["Player", "Pos", "Squad"], errors="ignore")
df = df.apply(pd.to_numeric, errors="coerce")
df = df.dropna(axis=1, how='all')
df = df.loc[:, df.nunique() > 1]

if "MP" not in df.columns:
    raise ValueError("'MP' (Matches Played) column is required.")

df = df.dropna(subset=["MP"])
weights = df["MP"].values
X = df.drop(columns=["MP"])
X = X.fillna(0)

# Standardize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# === Manually apply sample weighting ===
# Weighted mean center
weighted_mean = np.average(X_scaled, axis=0, weights=weights)
X_weighted_centered = (X_scaled - weighted_mean) * np.sqrt(weights[:, np.newaxis])

# PCA on weighted/centered matrix
pca = PCA(n_components=1)
pca.fit(X_weighted_centered)

# Normalize component to get weights summing to 1
components = pd.Series(np.abs(pca.components_[0]), index=X.columns)
weights_normalized = components / components.sum()

print("\n=== Inferred Feature Weights (Unsupervised, MP-weighted manually, sum=1) ===")
print(weights_normalized.sort_values(ascending=False))
print(f"\nTotal sum: {weights_normalized.sum():.4f}")