def first_year_without_leap(current_year: int, drift_threshold_days: float) -> int:
    tropical_year = 365.24219042
    gregorian_year = 365.2425
    annual_drift = gregorian_year - tropical_year

    years_until_drift = drift_threshold_days / annual_drift
    first_no_leap_year = int(current_year + years_until_drift)
    return first_no_leap_year


current_year = 2025
drift_threshold = 1  # 1 day drift

year_to_skip_leap = first_year_without_leap(current_year, drift_threshold)
print(f"Leap years might start being skipped from year {year_to_skip_leap} onward.")
