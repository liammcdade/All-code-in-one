def convert_weight(value, from_unit, to_unit):
    """
    Converts between different weight units.

    Supported units: kg, g, lb, oz
    """
    # Normalize input units to lowercase
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    # Conversion factors to grams
    to_grams = {"kg": 1000, "g": 1, "lb": 453.592, "oz": 28.3495}

    # Check if units are supported
    if from_unit not in to_grams or to_unit not in to_grams:
        raise ValueError(f"Unsupported unit(s): {from_unit}, {to_unit}")

    # Convert from original unit to grams
    value_in_grams = value * to_grams[from_unit]

    # Convert from grams to target unit
    converted_value = value_in_grams / to_grams[to_unit]

    return round(converted_value, 4)


def kg_to_lb(kg):
    return kg * 2.20462


def lb_to_kg(lb):
    return lb / 2.20462


def g_to_kg(g):
    return g / 1000


def kg_to_g(kg):
    return kg * 1000


def main():
    print("⚖️ Welcome to the Weight Converter!")
    print("Supported units: kg (kilogram), g (gram), lb (pound), oz (ounce)")

    try:
        value = float(input("Enter the value to convert: "))
        from_unit = input("From unit (kg/g/lb/oz): ")
        to_unit = input("To unit (kg/g/lb/oz): ")

        result = convert_weight(value, from_unit, to_unit)
        print(f"\n✅ {value} {from_unit} = {result} {to_unit}")
    except ValueError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"⚠️ An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
