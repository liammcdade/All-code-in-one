def convert_unit(value, from_unit, to_unit):
    conversions = {
        'miles_to_km': lambda x: x * 1.60934,
        'km_to_miles': lambda x: x / 1.60934 
    }
    key = f"{from_unit}_to_{to_unit}"
    if key in conversions:
        return conversions[key](value)
    else:
        raise ValueError("Conversion not supported.")