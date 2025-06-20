import logging
import math # For basic type checking, not actual geo calcs yet

# from ..core.utils import setup_logging # If a centralized logging setup is used

# Basic module-level logger configuration
# This will be overridden if __main__ configures logging more specifically.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class GeoProcessor:
    def __init__(self, data=None):
        """
        Initializes the GeoProcessor.

        Args:
            data (pd.DataFrame, optional): DataFrame with geographic data.
                                           Not used in this basic implementation.
        """
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.data = data
        self.logger.info("GeoProcessor initialized.")
        if self.data is not None:
            self.logger.info(f"GeoProcessor received data with shape: {self.data.shape}")


    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float, unit: str = 'km') -> float:
        """
        Calculates the distance between two geographic points using the Haversine formula.

        Args:
            lat1 (float): Latitude of the first point in degrees.
            lon1 (float): Longitude of the first point in degrees.
            lat2 (float): Latitude of the second point in degrees.
            lon2 (float): Longitude of the second point in degrees.
            unit (str, optional): Unit for distance ('km' or 'miles'). Defaults to 'km'.

        Returns:
            float: The calculated distance in the specified unit.

        Raises:
            TypeError: If any coordinate is not a number.
            ValueError: If unit is not 'km' or 'miles' (basic validation).
        """
        self.logger.info(
            f"Calculating distance between ({lat1},{lon1}) and ({lat2},{lon2}) in {unit}."
        )

        for coord, name in [(lat1, "lat1"), (lon1, "lon1"), (lat2, "lat2"), (lon2, "lon2")]:
            if not isinstance(coord, (int, float)):
                self.logger.error(f"Invalid type for coordinate {name}: {type(coord)}. Must be numeric.")
                raise TypeError(f"Coordinate {name} must be a number (int or float).")

        if unit not in ['km', 'miles']:
            self.logger.error(f"Invalid unit specified: {unit}. Must be 'km' or 'miles'.")
            raise ValueError("Unit must be 'km' or 'miles'.")

        # Earth radius
        if unit == 'km':
            R = 6371.0
        else: # unit == 'miles'
            R = 3959.0

        # Convert latitude and longitude from degrees to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        # Differences in coordinates
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad

        # Haversine formula
        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c

        self.logger.info(f"Calculated distance: {distance:.2f} {unit}")
        return distance

    def geocode_address(self, address: str, api_key: str = None) -> dict:
        """
        Placeholder for geocoding an address to latitude/longitude coordinates.
        Returns a fixed dummy dictionary and logs a warning.

        Args:
            address (str): The address to geocode.
            api_key (str, optional): API key for the geocoding service (currently unused).
                                     Defaults to None.
        Returns:
            dict: A dictionary with dummy geocoded information.

        Raises:
            TypeError: If address is not a string.
            ValueError: If address is an empty string.
        """
        self.logger.info(f"Attempting to geocode address: '{address}'")

        if api_key:
            self.logger.info(f"Received API key: {'*' * (len(api_key) - 3) + api_key[-3:] if len(api_key) > 3 else '***'}") # Basic masking

        if not isinstance(address, str):
            self.logger.error(f"Invalid type for address: {type(address)}. Must be a string.")
            raise TypeError("Address must be a string.")
        if not address.strip():
            self.logger.error("Address cannot be an empty string.")
            raise ValueError("Address cannot be an empty or whitespace-only string.")

        # Return a more realistic, but still fixed, dummy dictionary
        mock_coordinates = {
            'latitude': 34.0522,
            'longitude': -118.2437,
            'address_found': '123 Main St, Anytown, USA', # Mocked part of the response
            'confidence': 'mocked_high' # Mocked part of the response
        }
        self.logger.warning(
            f"Geocoding is mocked for '{address}'. Returning fixed dummy data: {mock_coordinates}"
        )
        return mock_coordinates

if __name__ == '__main__':
    # Setup a more specific logger for the __main__ execution if needed
    # The module-level basicConfig might be sufficient for simple scripts.
    # If handlers are added here, ensure they don't duplicate if basicConfig already ran.
    main_exec_logger = logging.getLogger(__name__) # Corresponds to 'DataNinja.plugins.geo' if run as module

    # Ensure the logger for __main__ execution has a handler and appropriate level
    # Using force=True to reconfigure if basicConfig was already called by module import
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', force=True)
    main_exec_logger.setLevel(logging.DEBUG) # Set level for this specific logger

    main_exec_logger.info("--- GeoProcessor Example Usage ---")

    geo_proc = GeoProcessor()

    # Test calculate_distance
    main_exec_logger.info("\n--- Testing calculate_distance ---")
    # Coordinates for San Francisco (SF) and Los Angeles (LA)
    sf_lat, sf_lon = 37.7749, -122.4194
    la_lat, la_lon = 34.0522, -118.2437
    # Expected distance SF to LA is ~559 km or ~347 miles

    try:
        dist_km = geo_proc.calculate_distance(lat1=sf_lat, lon1=sf_lon, lat2=la_lat, lon2=la_lon, unit='km')
        main_exec_logger.info(f"Distance SF to LA: {dist_km:.2f} km (Expected ~559 km)")

        dist_miles = geo_proc.calculate_distance(lat1=sf_lat, lon1=sf_lon, lat2=la_lat, lon2=la_lon, unit='miles')
        main_exec_logger.info(f"Distance SF to LA: {dist_miles:.2f} miles (Expected ~347 miles)")

        # Test with known points: London to Paris
        # London: 51.5074° N, 0.1278° W
        # Paris: 48.8566° N, 2.3522° E
        lon_lat, lon_lon = 51.5074, -0.1278
        par_lat, par_lon = 48.8566, 2.3522
        # Expected distance ~344 km or ~214 miles

        dist_km_lp = geo_proc.calculate_distance(lon_lat, lon_lon, par_lat, par_lon, unit='km')
        main_exec_logger.info(f"Distance London to Paris: {dist_km_lp:.2f} km (Expected ~344 km)")

        dist_miles_lp = geo_proc.calculate_distance(lon_lat, lon_lon, par_lat, par_lon, unit='miles')
        main_exec_logger.info(f"Distance London to Paris: {dist_miles_lp:.2f} miles (Expected ~214 miles)")


        # Test with invalid unit
        try:
            geo_proc.calculate_distance(sf_lat, sf_lon, la_lat, la_lon, unit='lightyears')
        except ValueError as e:
            main_exec_logger.info(f"Caught expected ValueError for invalid unit: {e}")

        # Test with invalid coordinate type
        try:
            geo_proc.calculate_distance("not_a_float", sf_lon, la_lat, la_lon)
        except TypeError as e:
            main_exec_logger.info(f"Caught expected TypeError for invalid coordinate: {e}")

    except Exception as e:
        main_exec_logger.error(f"Error during calculate_distance test: {e}", exc_info=True)


    # Test geocode_address
    main_exec_logger.info("\n--- Testing geocode_address ---")
    try:
        address1 = "1600 Amphitheatre Parkway, Mountain View, CA"
        coords1 = geo_proc.geocode_address(address=address1)
        main_exec_logger.info(f"Geocoding result for '{address1}': {coords1}")

        address2 = "Eiffel Tower, Paris, France"
        coords2 = geo_proc.geocode_address(address=address2, api_key="DUMMY_API_KEY_12345")
        main_exec_logger.info(f"Geocoding result for '{address2}' (with API key): {coords2}")

        # Test with invalid address type
        try:
            geo_proc.geocode_address(12345)
        except TypeError as e:
            main_exec_logger.info(f"Caught expected TypeError for invalid address type: {e}")

        # Test with empty address
        try:
            geo_proc.geocode_address("   ")
        except ValueError as e:
            main_exec_logger.info(f"Caught expected ValueError for empty address: {e}")

    except Exception as e:
        main_exec_logger.error(f"Error during geocode_address test: {e}", exc_info=True)

    main_exec_logger.info("\n--- GeoProcessor tests finished ---")
