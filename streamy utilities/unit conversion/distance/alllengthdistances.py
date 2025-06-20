class UniversalDistanceConverter:
    """
    A universal distance converter that supports conversions between:
    - Sub-millimeter: micron (µm), nanometer (nm), angstrom (Å)
    - Metric: millimeter (mm), centimeter (cm), meter (m), kilometer (km)
    - Imperial: inch (in), foot (ft), yard (yd), mile (mi)
    - Astronomical: astronomical unit (au), light year (ly), parsec (pc)
    """
    
    # Conversion factors to meters (base unit)
    CONVERSION_FACTORS = {
        # Sub-millimeter units
        'nm': 1e-9,
        'µm': 1e-6,
        'mm': 1e-3,
        # Metric units
        'cm': 1e-2,
        'm': 1,
        'km': 1e3,
        # Imperial units
        'in': 0.0254,
        'ft': 0.3048,
        'yd': 0.9144,
        'mi': 1609.344,
        # Astronomical units
        'au': 149597870700,  # astronomical unit
        'ly': 9460730472580800,  # light year
        'pc': 3.08567758149137e16  # parsec
    }
    
    # Unit aliases for user-friendly input
    UNIT_ALIASES = {
        'nanometer': 'nm', 'nanometers': 'nm',
        'micron': 'µm', 'microns': 'µm', 'micrometer': 'µm', 'micrometers': 'µm',
        'millimeter': 'mm', 'millimeters': 'mm',
        'centimeter': 'cm', 'centimeters': 'cm',
        'meter': 'm', 'meters': 'm',
        'kilometer': 'km', 'kilometers': 'km',
        'inch': 'in', 'inches': 'in',
        'foot': 'ft', 'feet': 'ft',
        'yard': 'yd', 'yards': 'yd',
        'mile': 'mi', 'miles': 'mi',
        'astronomical unit': 'au', 'astronomical units': 'au',
        'light year': 'ly', 'light years': 'ly',
        'parsec': 'pc', 'parsecs': 'pc'
    }
    
    @classmethod
    def convert(cls, value, from_unit, to_unit):
        """
        Convert a distance from one unit to another.
        
        Parameters:
        - value: The numerical value to convert
        - from_unit: The unit to convert from (e.g., 'cm', 'au', 'light years')
        - to_unit: The unit to convert to (e.g., 'mm', 'ft', 'ly')
        
        Returns:
        - The converted value
        """
        # Normalize unit strings
        from_unit = cls._normalize_unit(from_unit)
        to_unit = cls._normalize_unit(to_unit)
        
        # Validate units
        valid_units = cls.CONVERSION_FACTORS.keys()
        if from_unit not in valid_units or to_unit not in valid_units:
            raise ValueError(f"Invalid unit. Supported units are: {', '.join(valid_units)}")
        
        # Convert to meters first, then to target unit
        meters = value * cls.CONVERSION_FACTORS[from_unit]
        return meters / cls.CONVERSION_FACTORS[to_unit]
    
    @classmethod
    def _normalize_unit(cls, unit):
        """Convert unit string to standard form (lowercase, no plurals)"""
        unit = unit.lower().strip()
        return cls.UNIT_ALIASES.get(unit, unit)
    
    @classmethod
    def get_all_units(cls):
        """Return a list of all supported units"""
        return list(cls.CONVERSION_FACTORS.keys())
    
    @classmethod
    def get_conversion_examples(cls):
        """Print some common conversion examples"""
        examples = [
            ("1 km", "mi"),
            ("1 au", "km"),
            ("1 ly", "km"),
            ("1 pc", "ly"),
            ("1 mm", "µm")
        ]
        
        print("Conversion Examples:")
        for value_str, to_unit in examples:
            value, from_unit = value_str.split()
            result = cls.convert(float(value), from_unit, to_unit)
            print(f"{value_str} = {result:.2f} {to_unit}")

# Example usage
if __name__ == "__main__":
    converter = UniversalDistanceConverter()
    
    # Convert 1 light year to kilometers
    ly_to_km = converter.convert(1, 'ly', 'km')
    print(f"1 light year = {ly_to_km:.2f} km")
    
    # Convert 1 astronomical unit to miles
    au_to_mi = converter.convert(1, 'au', 'mi')
    print(f"1 astronomical unit = {au_to_mi:.2f} miles")
    
    # Convert 1 nanometer to angstroms
    nm_to_angstrom = converter.convert(1, 'nm', 'Å')
    print(f"1 nanometer = {nm_to_angstrom} angstroms")
    
    # Show some examples
    converter.get_conversion_examples()