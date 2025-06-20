def convert_weight(value, from_unit, to_unit):
    """
    Converts between different weight/mass units.
    Supported units: kg, g, mg, lb, oz, st, t, ton, µg
    """
    # Conversion factors to grams
    to_grams = {
        'kg': 1000,           # Kilogram
        'g': 1,               # Gram
        'mg': 0.001,          # Milligram
        'lb': 453.592,        # Pound
        'oz': 28.3495,        # Ounce
        'st': 6350.29,        # Stone
        't': 1_000_000,       # Metric Ton
        'ton': 907_184.74,    # US Ton
        'µg': 0.000001        # Microgram
    }

    # Normalize input units to lowercase
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    # Check if units are valid
    if from_unit not in to_grams:
        raise ValueError(f"Unsupported source unit: {from_unit}")
    if to_unit not in to_grams:
        raise ValueError(f"Unsupported target unit: {to_unit}")

    # Convert from original unit to grams
    value_in_grams = value * to_grams[from_unit]

    # Convert from grams to target unit
    converted_value = value_in_grams / to_grams[to_unit]

    return round(converted_value, 6)


def main():
    print("⚖️ Welcome to the All-in-One Weight Converter!")
    print("Supported units: kg, g, mg, lb, oz, st, t, ton, µg")

    try:
        value = float(input("Enter the weight value: "))
        from_unit = input("From unit: ").strip().lower()
        to_unit = input("To unit: ").strip().lower()

        result = convert_weight(value, from_unit, to_unit)
        print(f"\n✅ {value} {from_unit} = {result} {to_unit}")
    
    except ValueError as ve:
        print(f"⚠️ Error: {ve}")
    except Exception as e:
        print(f"⚠️ An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()