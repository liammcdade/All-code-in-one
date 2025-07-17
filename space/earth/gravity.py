import math

def calculate_earth_gravity(latitude_deg, altitude_m=0):
    """
    Calculate Earth's surface gravity at a given latitude using the International Gravity Formula (IGF).
    Optionally adjust for altitude (simplified free-air correction).
    
    Args:
        latitude_deg (float): Latitude in degrees (-90 to 90)
        altitude_m (float, optional): Altitude above sea level in meters. Default is 0 (sea level).
    
    Returns:
        float: Gravitational acceleration in m/s², or None if inputs are invalid.
    """
    # Validate latitude
    if not isinstance(latitude_deg, (int, float)) or latitude_deg < -90 or latitude_deg > 90:
        return None
    
    # Convert latitude to radians
    phi = math.radians(latitude_deg)
    
    # International Gravity Formula (IGF)
    sin_phi_sq = math.sin(phi) ** 2
    sin_2phi_sq = math.sin(2 * phi) ** 2
    g = 9.780326771 + 0.0053024 * sin_phi_sq - 0.0000058 * sin_2phi_sq
    
    # Optional altitude correction (free-air correction, approximate)
    if altitude_m != 0:
        if not isinstance(altitude_m, (int, float)) or altitude_m < 0:
            return None
        g -= 0.0003086 * (altitude_m / 1000)  # Convert altitude to km
    
    return g

# Compare gravity at two coordinates in Darlington with altitude
if __name__ == "__main__":
    # Define coordinates (latitude, longitude, altitude)
    coords_1 = (54.539855, -1.548613, 45)  # Darlington, estimated 45m altitude
    coords_2 = (54.525236, -1.555423, 45)  # Darlington, estimated 45m altitude
    
    # Calculate gravity
    gravity_1 = calculate_earth_gravity(coords_1[0], coords_1[2])
    gravity_2 = calculate_earth_gravity(coords_2[0], coords_2[2])
    
    # Print results
    print("Gravity Comparison in Darlington:")
    print(f"Coordinates 1: Latitude {coords_1[0]}°, Longitude {coords_1[1]}°, Altitude {coords_1[2]}m")
    print(f"Gravity: {gravity_1:.6f} m/s²" if gravity_1 is not None else "Invalid coordinates")
    print(f"Coordinates 2: Latitude {coords_2[0]}°, Longitude {coords_2[1]}°, Altitude {coords_2[2]}m")
    print(f"Gravity: {gravity_2:.6f} m/s²" if gravity_2 is not None else "Invalid coordinates")
    
    # Calculate and display differences
    if gravity_1 is not None and gravity_2 is not None:
        gravity_diff = abs(gravity_1 - gravity_2)
        avg_gravity = (gravity_1 + gravity_2) / 2
        percentage_diff = (gravity_diff / avg_gravity) * 100
        print(f"\nAbsolute Difference in gravity: {gravity_diff:.6f} m/s² ({gravity_diff * 1e6:.1f} µGal)")
        print(f"Percentage Difference in gravity: {percentage_diff:.8f}%")
    else:
        print("Cannot compare: One or both coordinates are invalid.")