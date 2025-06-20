def celsius_to_fahrenheit(c):
    return c * 9 / 5 + 32


def fahrenheit_to_celsius(f):
    return (f - 32) * 5 / 9


def celsius_to_kelvin(c):
    return c + 273.15


def kelvin_to_celsius(k):
    return k - 273.15


def fahrenheit_to_kelvin(f):
    return celsius_to_kelvin(fahrenheit_to_celsius(f))


def kelvin_to_fahrenheit(k):
    return celsius_to_fahrenheit(kelvin_to_celsius(k))


if __name__ == "__main__":
    print("Choose conversion:")
    print("1. Celsius to Fahrenheit")
    print("2. Fahrenheit to Celsius")
    print("3. Celsius to Kelvin")
    print("4. Kelvin to Celsius")
    print("5. Fahrenheit to Kelvin")
    print("6. Kelvin to Fahrenheit")

    choice = input("Enter choice (1-6): ")

    if choice == "1":
        celsius = float(input("Enter temperature in Celsius: "))
        result = celsius_to_fahrenheit(celsius)
        print(f"Result: {result}°F")
    elif choice == "2":
        fahrenheit = float(input("Enter temperature in Fahrenheit: "))
        result = fahrenheit_to_celsius(fahrenheit)
        print(f"Result: {result}°C")
    elif choice == "3":
        celsius = float(input("Enter temperature in Celsius: "))
        result = celsius_to_kelvin(celsius)
        print(f"Result: {result}K")
    elif choice == "4":
        kelvin = float(input("Enter temperature in Kelvin: "))
        result = kelvin_to_celsius(kelvin)
        print(f"Result: {result}°C")
    elif choice == "5":
        fahrenheit = float(input("Enter temperature in Fahrenheit: "))
        result = fahrenheit_to_kelvin(fahrenheit)
        print(f"Result: {result}K")
    elif choice == "6":
        kelvin = float(input("Enter temperature in Kelvin: "))
        result = kelvin_to_fahrenheit(kelvin)
        print(f"Result: {result}°F")
    else:
        print("Invalid choice.")
