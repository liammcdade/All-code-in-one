import pandas as pd
import numpy as np

# Constants
G = 6.67430e-11       # m^3 kg^-1 s^-2
au = 1.495978707e11   # meters
M_sun = 1.98847e30    # kg

# Load data
df = pd.read_csv("space/exoplanet/exoplanet.csv")

# Save original missing count and total cells
original_na = df.isna().sum().sum()
total_cells = df.size

def calc_orbital_period(a_au, m_star_sol):
    if pd.isna(a_au) or pd.isna(m_star_sol):
        return np.nan
    a_m = a_au * au
    m_star_kg = m_star_sol * M_sun
    period_sec = 2 * np.pi * np.sqrt(a_m**3 / (G * m_star_kg))
    return period_sec / 86400  # seconds to days

def spectype_to_teff(s):
    if not isinstance(s, str):
        return np.nan
    s = s.strip().upper()
    if s.startswith("O"): return 35000
    if s.startswith("B"): return 15000
    if s.startswith("A"): return 9000
    if s.startswith("F"): return 7000
    if s.startswith("G"): return 5700
    if s.startswith("K"): return 4500
    if s.startswith("M"): return 3200
    return np.nan

def teff_to_spectype(teff):
    if pd.isna(teff):
        return np.nan
    if teff > 30000: return "O"
    if teff > 10000: return "B"
    if teff > 7500: return "A"
    if teff > 6000: return "F"
    if teff > 5200: return "G"
    if teff > 3700: return "K"
    return "M"

def mass_to_radius(mass_jupiter):
    if pd.isna(mass_jupiter):
        return np.nan
    return 1.0 * (mass_jupiter ** 0.5)

def radius_to_mass(radius_jupiter):
    if pd.isna(radius_jupiter):
        return np.nan
    return (radius_jupiter ** 2)

# Fill missing pl_eqt
mask = df['pl_eqt'].isna() & df['st_teff'].notna() & df['st_rad'].notna() & df['pl_orbsmax'].notna()
df.loc[mask, 'pl_eqt'] = df.loc[mask].apply(lambda r: r['st_teff'] * np.sqrt(r['st_rad'] / (2 * r['pl_orbsmax'])), axis=1)

# Fill missing pl_insol
mask = df['pl_insol'].isna() & df['st_rad'].notna() & df['st_teff'].notna() & df['pl_orbsmax'].notna()
df.loc[mask, 'pl_insol'] = df.loc[mask].apply(lambda r: (r['st_rad']**2) * (r['st_teff']**4) / (r['pl_orbsmax']**2), axis=1)

# Fill missing pl_orbper
mask = df['pl_orbper'].isna() & df['pl_orbsmax'].notna() & df['st_mass'].notna()
df.loc[mask, 'pl_orbper'] = df.loc[mask].apply(lambda r: calc_orbital_period(r['pl_orbsmax'], r['st_mass']), axis=1)

# Fill missing st_teff
mask = df['st_teff'].isna() & df['st_spectype'].notna()
df.loc[mask, 'st_teff'] = df.loc[mask, 'st_spectype'].apply(spectype_to_teff)

# Fill missing st_spectype
mask = df['st_spectype'].isna() & df['st_teff'].notna()
df.loc[mask, 'st_spectype'] = df.loc[mask, 'st_teff'].apply(teff_to_spectype)

# Fill missing pl_rade from pl_bmassj
mask = df['pl_rade'].isna() & df['pl_bmassj'].notna()
df.loc[mask, 'pl_rade'] = df.loc[mask, 'pl_bmassj'].apply(mass_to_radius)

# Fill missing pl_bmassj from pl_rade
mask = df['pl_bmassj'].isna() & df['pl_rade'].notna()
df.loc[mask, 'pl_bmassj'] = df.loc[mask, 'pl_rade'].apply(radius_to_mass)

# Fill missing pl_bmasse from pl_bmassj (Jupiter masses to Earth masses)
mask = df['pl_bmasse'].isna() & df['pl_bmassj'].notna()
df.loc[mask, 'pl_bmasse'] = df.loc[mask, 'pl_bmassj'] * 317.8

# Fill missing pl_bmassj from pl_bmasse (Earth masses to Jupiter masses)
mask = df['pl_bmassj'].isna() & df['pl_bmasse'].notna()
df.loc[mask, 'pl_bmassj'] = df.loc[mask, 'pl_bmasse'] / 317.8

# Save output
df.to_csv("filled_exoplanets_formulas.csv", index=False)

# Calculate and print how many cells were filled (percentage)
new_na = df.isna().sum().sum()
filled_cells = original_na - new_na
percent_filled = (filled_cells / total_cells) * 100

print(f"Filled {filled_cells} cells ({percent_filled:.2f}%) of total {total_cells} cells.")
