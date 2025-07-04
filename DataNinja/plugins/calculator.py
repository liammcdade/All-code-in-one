import logging
import math

class CalculatorProcessor:
    def __init__(self):
        """
        Initializes the CalculatorProcessor.
        """
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.logger.info("CalculatorProcessor initialized.")

    def sin(self, value: float) -> float:
        """Calculates the sine of a value (in radians)."""
        self.logger.info(f"Calculating sin({value})")
        return math.sin(value)

    def cos(self, value: float) -> float:
        """Calculates the cosine of a value (in radians)."""
        self.logger.info(f"Calculating cos({value})")
        return math.cos(value)

    def tan(self, value: float) -> float:
        """Calculates the tangent of a value (in radians)."""
        self.logger.info(f"Calculating tan({value})")
        # Add handling for tan(pi/2 + k*pi) if necessary, though math.tan handles it by returning large values.
        return math.tan(value)

    def log(self, value: float, base: float = None) -> float:
        """Calculates the logarithm of a value. Natural log if base is None, else log to the given base."""
        self.logger.info(f"Calculating log({value}) with base {base if base else 'e'}")
        if value <= 0:
            self.logger.error("Logarithm input must be positive.")
            raise ValueError("Logarithm input must be positive.")
        if base is None:
            return math.log(value)
        else:
            if base <= 0 or base == 1:
                self.logger.error("Logarithm base must be positive and not equal to 1.")
                raise ValueError("Logarithm base must be positive and not equal to 1.")
            return math.log(value, base)

    def sqrt(self, value: float) -> float:
        """Calculates the square root of a value."""
        self.logger.info(f"Calculating sqrt({value})")
        if value < 0:
            self.logger.error("Square root input must be non-negative.")
            raise ValueError("Square root input must be non-negative.")
        return math.sqrt(value)

    def convert_unit(self, value: float, from_unit: str, to_unit: str, category: str) -> float:
        """Converts a value between units within a given category."""
        self.logger.info(f"Converting {value} from {from_unit} to {to_unit} in category {category}")

        if category == "temperature":
            # Normalize to Celsius first
            if from_unit == "F":
                celsius = (value - 32) * 5/9
            elif from_unit == "K":
                celsius = value - 273.15
            elif from_unit == "C":
                celsius = value
            else:
                raise ValueError(f"Unknown from_unit '{from_unit}' in temperature category.")

            # Convert from Celsius to target unit
            if to_unit == "F":
                return (celsius * 9/5) + 32
            elif to_unit == "K":
                return celsius + 273.15
            elif to_unit == "C":
                return celsius
            else:
                raise ValueError(f"Unknown to_unit '{to_unit}' in temperature category.")

        # For length and weight, define base units and conversion factors
        # Base unit for length: meter (m)
        # Base unit for weight: kilogram (kg)
        conversions = {
            "length": {
                "m": 1.0,
                "km": 1000.0,
                "ft": 0.3048,
                "mile": 1609.34
            },
            "weight": {
                "kg": 1.0,
                "g": 0.001,
                "lb": 0.453592,
                "oz": 0.0283495
            }
        }

        if category not in conversions:
            raise ValueError(f"Unknown conversion category: {category}")

        cat_conv = conversions[category]
        if from_unit not in cat_conv or to_unit not in cat_conv:
            raise ValueError(f"Units '{from_unit}' or '{to_unit}' not recognized in category '{category}'.")

        # Convert from_unit to base unit, then base unit to to_unit
        value_in_base_unit = value * cat_conv[from_unit]
        result = value_in_base_unit / cat_conv[to_unit]

        self.logger.info(f"Conversion result: {result}")
        return result

if __name__ == "__main__":
    # Basic logging setup for standalone execution
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    calc_proc = CalculatorProcessor()

    # Test scientific functions
    print(f"sin(pi/2) = {calc_proc.sin(math.pi/2)}")
    print(f"cos(pi) = {calc_proc.cos(math.pi)}")
    print(f"tan(pi/4) = {calc_proc.tan(math.pi/4)}")
    print(f"log(10) = {calc_proc.log(10)}")
    print(f"log(100, 10) = {calc_proc.log(100, 10)}")
    print(f"sqrt(16) = {calc_proc.sqrt(16)}")

    try:
        calc_proc.log(0)
    except ValueError as e:
        print(f"Caught expected error for log(0): {e}")
    try:
        calc_proc.sqrt(-1)
    except ValueError as e:
        print(f"Caught expected error for sqrt(-1): {e}")

    # Test unit conversions
    print("\n--- Unit Conversion Tests ---")
    # Length
    print(f"10 km to m: {calc_proc.convert_unit(10, 'km', 'm', 'length')}")
    print(f"3280.84 ft to km: {calc_proc.convert_unit(3280.84, 'ft', 'km', 'length')}")
    # Weight
    print(f"5 kg to lb: {calc_proc.convert_unit(5, 'kg', 'lb', 'weight')}")
    print(f"16 oz to g: {calc_proc.convert_unit(16, 'oz', 'g', 'weight')}")
    # Temperature
    print(f"100 C to F: {calc_proc.convert_unit(100, 'C', 'F', 'temperature')}")
    print(f"32 F to C: {calc_proc.convert_unit(32, 'F', 'C', 'temperature')}")
    print(f"0 C to K: {calc_proc.convert_unit(0, 'C', 'K', 'temperature')}")

    try:
        calc_proc.convert_unit(10, 'km', 'lb', 'length') # Mismatch category
    except ValueError as e:
        print(f"Caught expected error for mismatched units: {e}")
    try:
        calc_proc.convert_unit(10, 'C', 'F', 'distance') # Invalid category
    except ValueError as e:
        print(f"Caught expected error for invalid category: {e}")


    print("\nCalculatorProcessor standalone tests complete.")
