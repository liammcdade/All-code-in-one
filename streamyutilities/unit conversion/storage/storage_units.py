# Define conversion factors with respect to Bytes
CONVERSION_FACTORS = {
    "B": 1,
    "KB": 1024,
    "MB": 1024**2,
    "GB": 1024**3,
    "TB": 1024**4,
}

def convert_storage(value, from_unit, to_unit):
  """Converts a storage value from one unit to another.

  Args:
    value: The numerical value to convert.
    from_unit: The unit to convert from (e.g., "B", "KB", "MB", "GB", "TB").
    to_unit: The unit to convert to (e.g., "B", "KB", "MB", "GB", "TB").

  Returns:
    The converted value, or None if units are invalid.
  """
  from_unit = from_unit.upper()
  to_unit = to_unit.upper()

  if from_unit not in CONVERSION_FACTORS or to_unit not in CONVERSION_FACTORS:
    return None

  # Convert the value to Bytes (the base unit)
  value_in_bytes = value * CONVERSION_FACTORS[from_unit]

  # Convert from Bytes to the target unit
  converted_value = value_in_bytes / CONVERSION_FACTORS[to_unit]
  return converted_value

if __name__ == "__main__":
  try:
    value_str = input("Enter value: ")
    value = float(value_str)

    from_unit_input = input("Enter unit to convert from (B, KB, MB, GB, TB): ").strip()
    to_unit_input = input("Enter unit to convert to (B, KB, MB, GB, TB): ").strip()

    result = convert_storage(value, from_unit_input, to_unit_input)

    if result is not None:
      print(f"Result: {result} {to_unit_input.upper()}")
    else:
      print("Error: Invalid unit input. Please use B, KB, MB, GB, or TB.")

  except ValueError:
    print("Error: Invalid numerical input for value.")
  except Exception as e:
    print(f"An unexpected error occurred: {e}")
