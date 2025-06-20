def celsius_to_fahrenheit(celsius):
  """Converts Celsius to Fahrenheit.

  Args:
    celsius: Temperature in Celsius.

  Returns:
    Temperature in Fahrenheit.
  """
  return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
  """Converts Fahrenheit to Celsius.

  Args:
    fahrenheit: Temperature in Fahrenheit.

  Returns:
    Temperature in Celsius.
  """
  return (fahrenheit - 32) * 5/9

def celsius_to_kelvin(celsius):
  """Converts Celsius to Kelvin.

  Args:
    celsius: Temperature in Celsius.

  Returns:
    Temperature in Kelvin.
  """
  return celsius + 273.15

def kelvin_to_celsius(kelvin):
  """Converts Kelvin to Celsius.

  Args:
    kelvin: Temperature in Kelvin.

  Returns:
    Temperature in Celsius.
  """
  return kelvin - 273.15

def fahrenheit_to_kelvin(fahrenheit):
  """Converts Fahrenheit to Kelvin.

  Args:
    fahrenheit: Temperature in Fahrenheit.

  Returns:
    Temperature in Kelvin.
  """
  celsius = fahrenheit_to_celsius(fahrenheit)
  return celsius_to_kelvin(celsius)

def kelvin_to_fahrenheit(kelvin):
  """Converts Kelvin to Fahrenheit.

  Args:
    kelvin: Temperature in Kelvin.

  Returns:
    Temperature in Fahrenheit.
  """
  celsius = kelvin_to_celsius(kelvin)
  return celsius_to_fahrenheit(celsius)

if __name__ == "__main__":
  print("Choose conversion:")
  print("1. Celsius to Fahrenheit")
  print("2. Fahrenheit to Celsius")
  print("3. Celsius to Kelvin")
  print("4. Kelvin to Celsius")
  print("5. Fahrenheit to Kelvin")
  print("6. Kelvin to Fahrenheit")

  choice = input("Enter choice (1-6): ")

  if choice == '1':
    celsius = float(input("Enter temperature in Celsius: "))
    result = celsius_to_fahrenheit(celsius)
    print(f"Result: {result}°F")
  elif choice == '2':
    fahrenheit = float(input("Enter temperature in Fahrenheit: "))
    result = fahrenheit_to_celsius(fahrenheit)
    print(f"Result: {result}°C")
  elif choice == '3':
    celsius = float(input("Enter temperature in Celsius: "))
    result = celsius_to_kelvin(celsius)
    print(f"Result: {result}K")
  elif choice == '4':
    kelvin = float(input("Enter temperature in Kelvin: "))
    result = kelvin_to_celsius(kelvin)
    print(f"Result: {result}°C")
  elif choice == '5':
    fahrenheit = float(input("Enter temperature in Fahrenheit: "))
    result = fahrenheit_to_kelvin(fahrenheit)
    print(f"Result: {result}K")
  elif choice == '6':
    kelvin = float(input("Enter temperature in Kelvin: "))
    result = kelvin_to_fahrenheit(kelvin)
    print(f"Result: {result}°F")
  else:
    print("Invalid choice.")
