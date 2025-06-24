import pandas as pd
import matplotlib.pyplot as plt
import re

# Load CSV with correct date parsing
df = pd.read_csv("sports analysis/kaggle/wfp_food_prices_egy.csv", parse_dates=["date"], dayfirst=True)

# Filter for Egypt national average market
df_egypt = df[df['market'] == 'National Average']

# Drop rows with missing price or unit
df_egypt = df_egypt[['date', 'category', 'usdprice', 'unit']].dropna()

# Normalize unit column to lowercase and strip spaces
unit_conversion = {
    'kg': 1,
    'g': 0.001,
    'ton': 1000,
    'litre': 1,
    'ml': 0.001,
    '100 g': 0.1,
    '800 g': 0.8,  # Added for your CSV
    '1000 g': 1,
    '500 g': 0.5,
    '200 g': 0.2,
    '250 g': 0.25,
    'piece': None,
    'dozen': None,
    'bag (50kg)': 50,
    'sack (50kg)': 50,
    'sack (25kg)': 25,
    'bag (25kg)': 25,
    'bottle (1 litre)': 1,
    'bottle (500ml)': 0.5,
    # Add more mappings as needed
}

# Normalize units in the DataFrame
# Lowercase and strip spaces for robust matching
# Also replace multiple spaces with a single space
def normalize_unit(u):
    if pd.isnull(u):
        return u
    u = u.lower().strip()
    u = re.sub(r'\s+', ' ', u)
    return u

df_egypt['unit'] = df_egypt['unit'].apply(normalize_unit)

df_egypt['conversion_factor'] = df_egypt['unit'].map(unit_conversion)
df_egypt = df_egypt.dropna(subset=['conversion_factor'])

# Normalize prices to per kg or litre
df_egypt['usd_per_kg'] = df_egypt['usdprice'] / df_egypt['conversion_factor']

# Extract month for aggregation
df_egypt['month'] = df_egypt['date'].dt.to_period('M')

# Group by category and month
monthly_avg = df_egypt.groupby(['category', 'month'])['usd_per_kg'].mean().reset_index()

# Pivot table for price comparison over time
pivot = monthly_avg.pivot(index='month', columns='category', values='usd_per_kg')

if pivot.shape[0] < 2:
    print("Not enough data to compute price change (need at least two months after filtering).")
else:
    # Calculate percentage price change
    price_change = (pivot.iloc[-1] - pivot.iloc[0]) / pivot.iloc[0] * 100
    price_change = price_change.sort_values(ascending=False)

    # Display results
    print("Price Change by Category (% increase from first to last month):")
    print(price_change.round(2).to_string())

    # Plot
    price_change.plot(kind='barh', title="Normalized Food Price Increase by Category in Egypt")
    plt.xlabel('% Price Increase (USD per kg or litre)')
    plt.tight_layout()
    plt.show()
