import math
import random

# Constants (all in SI units)
EARTH_GRAVITY = 9.78152969 # m/s^2
MOON_GRAVITY = 1.62   # m/s^2
EARTH_ESCAPE_VELOCITY = 11200  # m/s
MOON_ESCAPE_VELOCITY = 2380   # m/s
MOON_ORBITAL_VELOCITY = 1680   # m/s (low lunar orbit)
EARTH_ROTATION_SPEED = 465     # m/s at equator
G0 = 9.81                     # Standard gravity for specific impulse (m/s^2)

# Delta-v requirements for mission phases (approximate, in m/s)
DELTA_V_EARTH_LAUNCH = 9400   # To low Earth orbit
DELTA_V_EARTH_ESCAPE = 3200   # To escape Earth's gravity from LEO
DELTA_V_LUNAR_ORBIT = 1400    # Lunar orbit insertion
DELTA_V_LUNAR_LANDING = 2000   # Lunar landing
DELTA_V_LUNAR_TAKEOFF = 2000   # Lunar ascent to orbit
DELTA_V_EARTH_REENTRY = 1000   # Controlled re-entry burn

def cape_canaveral_initial_velocity(latitude_deg=28.5):
    """Calculate initial velocity due to Earth's rotation at Cape Canaveral."""
    return EARTH_ROTATION_SPEED * math.cos(math.radians(latitude_deg))

def rocket_equation_delta_v(mass_initial, mass_final, isp):
    """Calculate delta-v using the Tsiolkovsky rocket equation."""
    if mass_final <= 0 or mass_initial <= mass_final:
        return 0
    return isp * G0 * math.log(mass_initial / mass_final)

def thrust_to_weight_ratio(thrust, mass, gravity):
    """Calculate thrust-to-weight ratio for a given gravity."""
    return thrust / (mass * gravity)

def mission_progress(params):
    """Calculate mission progress for a staged rocket mission."""
    isp = params["isp"]  # Specific impulse in seconds
    stages = params["stages"]  # List of (initial_mass, fuel_mass, thrust, burn_time)

    current_velocity = cape_canaveral_initial_velocity()
    total_delta_v_required = (DELTA_V_EARTH_LAUNCH + DELTA_V_EARTH_ESCAPE +
                             DELTA_V_LUNAR_ORBIT + DELTA_V_LUNAR_LANDING +
                             DELTA_V_LUNAR_TAKEOFF + DELTA_V_EARTH_REENTRY)
    total_delta_v = 0
    current_mass = stages[0]["initial_mass"]  # Start with first stage mass

    # Earth launch (to LEO and escape)
    for i, stage in enumerate(stages[:2]):  # First two stages for Earth launch
        twr = thrust_to_weight_ratio(stage["thrust"], current_mass, EARTH_GRAVITY)
        if twr < 1.2:  # Require TWR > 1.2 for liftoff
            return 0.0
        mass_final = current_mass - stage["fuel_mass"]
        if mass_final <= 0:
            return 0.0
        delta_v = rocket_equation_delta_v(current_mass, mass_final, isp)
        total_delta_v += delta_v
        current_mass = mass_final
        if i == 0:
            current_mass -= stage["structural_mass"]  # Jettison first stage

    earth_progress = min(total_delta_v / (DELTA_V_EARTH_LAUNCH + DELTA_V_EARTH_ESCAPE), 1.0)
    if earth_progress < 1.0:
        return 0.0

    # Lunar orbit insertion
    twr = thrust_to_weight_ratio(stages[2]["thrust"], current_mass, MOON_GRAVITY)
    if twr < 1.0:
        return 0.0
    mass_final = current_mass - stages[2]["fuel_mass"]
    if mass_final <= 0:
        return 0.0
    delta_v = rocket_equation_delta_v(current_mass, mass_final, isp)
    total_delta_v += delta_v
    lunar_orbit_progress = min(delta_v / DELTA_V_LUNAR_ORBIT, 1.0)
    current_mass = mass_final
    if lunar_orbit_progress < 1.0:
        return 0.0

    # Lunar landing
    twr = thrust_to_weight_ratio(stages[3]["thrust"], current_mass, MOON_GRAVITY)
    if twr < 1.5:  # Higher TWR for precise landing
        return 0.0
    mass_final = current_mass - stages[3]["fuel_mass"]
    if mass_final <= 0:
        return 0.0
    delta_v = rocket_equation_delta_v(current_mass, mass_final, isp)
    total_delta_v += delta_v
    lunar_landing_progress = min(delta_v / DELTA_V_LUNAR_LANDING, 1.0)
    current_mass = mass_final
    if lunar_landing_progress < 1.0:
        return 0.0

    # Lunar takeoff
    twr = thrust_to_weight_ratio(stages[4]["thrust"], current_mass, MOON_GRAVITY)
    if twr < 1.5:
        return 0.0
    mass_final = current_mass - stages[4]["fuel_mass"]
    if mass_final <= 0:
        return 0.0
    delta_v = rocket_equation_delta_v(current_mass, mass_final, isp)
    total_delta_v += delta_v
    lunar_takeoff_progress = min(delta_v / DELTA_V_LUNAR_TAKEOFF, 1.0)
    current_mass = mass_final
    if lunar_takeoff_progress < 1.0:
        return 0.0

    # Earth re-entry
    twr = thrust_to_weight_ratio(stages[5]["thrust"], current_mass, EARTH_GRAVITY)
    if twr < 1.0:
        return 0.0
    mass_final = current_mass - stages[5]["fuel_mass"]
    if mass_final <= 0:
        return 0.0
    delta_v = rocket_equation_delta_v(current_mass, mass_final, isp)
    total_delta_v += delta_v
    earth_reentry_progress = min(delta_v / DELTA_V_EARTH_REENTRY, 1.0)
    if earth_reentry_progress < 1.0:
        return 0.0

    # Overall mission progress
    return (earth_progress * lunar_orbit_progress * lunar_landing_progress *
            lunar_takeoff_progress * earth_reentry_progress)

def random_variation(value, scale=0.05, min_val=1, max_val=None):
    """Apply random variation to a parameter within a scale."""
    factor = 1 + random.uniform(-scale, scale)
    new_val = value * factor
    if max_val is not None:
        new_val = min(new_val, max_val)
    return max(new_val, min_val)

# Initialize realistic parameters
initial_params = {
    "isp": 350,  # Specific impulse (s), typical for chemical rockets
    "stages": [
        # Stage 1: Earth launch (booster)
        {"initial_mass": 500000, "fuel_mass": 400000, "structural_mass": 50000, "thrust": 7.5e6, "burn_time": 150},
        # Stage 2: Earth escape
        {"initial_mass": 120000, "fuel_mass": 90000, "structural_mass": 15000, "thrust": 1.5e6, "burn_time": 300},
        # Stage 3: Lunar orbit insertion
        {"initial_mass": 30000, "fuel_mass": 20000, "structural_mass": 5000, "thrust": 4e5, "burn_time": 200},
        # Stage 4: Lunar landing
        {"initial_mass": 15000, "fuel_mass": 10000, "structural_mass": 3000, "thrust": 2e5, "burn_time": 150},
        # Stage 5: Lunar takeoff
        {"initial_mass": 10000, "fuel_mass": 6000, "structural_mass": 2000, "thrust": 1.5e5, "burn_time": 100},
        # Stage 6: Earth re-entry
        {"initial_mass": 5000, "fuel_mass": 2000, "structural_mass": 1000, "thrust": 1e5, "burn_time": 50},
    ]
}

best_params = initial_params.copy()
best_progress = mission_progress(best_params)
print(f"Initial progress: {best_progress*100:.2f}%")

# Optimization loop
for i in range(10000):
    trial_params = {
        "isp": random_variation(best_params["isp"], scale=0.05, min_val=300, max_val=450),
        "stages": []
    }
    current_mass = 0
    for stage in best_params["stages"]:
        trial_stage = {
            "initial_mass": random_variation(stage["initial_mass"], scale=0.05, min_val=5000),
            "fuel_mass": random_variation(stage["fuel_mass"], scale=0.05, min_val=1000),
            "structural_mass": random_variation(stage["structural_mass"], scale=0.05, min_val=500),
            "thrust": random_variation(stage["thrust"], scale=0.05, min_val=5e4),
            "burn_time": random_variation(stage["burn_time"], scale=0.05, min_val=10, max_val=600)
        }
        # Ensure fuel mass doesn't exceed initial mass
        trial_stage["fuel_mass"] = min(trial_stage["fuel_mass"], trial_stage["initial_mass"] * 0.9)
        trial_stage["structural_mass"] = min(trial_stage["structural_mass"], trial_stage["initial_mass"] * 0.2)
        trial_params["stages"].append(trial_stage)
        current_mass += trial_stage["initial_mass"] if not trial_params["stages"] else 0

    progress = mission_progress(trial_params)

    if progress > best_progress:
        best_progress = progress
        best_params = trial_params
        print(f"Iteration {i}: Progress: {progress*100:.2f}%, ISP: {best_params['isp']:.2f}, Stages: {[s['initial_mass'] for s in best_params['stages']]}")

    if best_progress >= 0.99:  # Allow near-100% due to numerical precision
        print("Mission parameters found for near-full success.")
        break

print("\nBest parameters found:")
print(f"ISP: {best_params['isp']:.2f} s")
for i, stage in enumerate(best_params["stages"], 1):
    print(f"Stage {i}: Initial Mass: {stage['initial_mass']:.0f} kg, Fuel Mass: {stage['fuel_mass']:.0f} kg, "
          f"Structural Mass: {stage['structural_mass']:.0f} kg, Thrust: {stage['thrust']:.0f} N, "
          f"Burn Time: {stage['burn_time']:.1f} s")
print(f"Best mission progress: {best_progress*100:.2f}%")