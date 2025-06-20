import unittest
import sys
import os

# Add the parent directory to the Python path to import the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from celsius_fahrenheit_kelvin import (
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    celsius_to_kelvin,
    kelvin_to_celsius,
    fahrenheit_to_kelvin,
    kelvin_to_fahrenheit,
)

class TestTemperatureConversions(unittest.TestCase):

    def test_celsius_to_fahrenheit(self):
        self.assertAlmostEqual(celsius_to_fahrenheit(0), 32.0)
        self.assertAlmostEqual(celsius_to_fahrenheit(100), 212.0)
        self.assertAlmostEqual(celsius_to_fahrenheit(-40), -40.0)
        self.assertAlmostEqual(celsius_to_fahrenheit(25), 77.0)

    def test_fahrenheit_to_celsius(self):
        self.assertAlmostEqual(fahrenheit_to_celsius(32), 0.0)
        self.assertAlmostEqual(fahrenheit_to_celsius(212), 100.0)
        self.assertAlmostEqual(fahrenheit_to_celsius(-40), -40.0)
        self.assertAlmostEqual(fahrenheit_to_celsius(77), 25.0)

    def test_celsius_to_kelvin(self):
        self.assertAlmostEqual(celsius_to_kelvin(0), 273.15)
        self.assertAlmostEqual(celsius_to_kelvin(-273.15), 0.0)
        self.assertAlmostEqual(celsius_to_kelvin(25), 298.15)

    def test_kelvin_to_celsius(self):
        self.assertAlmostEqual(kelvin_to_celsius(273.15), 0.0)
        self.assertAlmostEqual(kelvin_to_celsius(0), -273.15)
        self.assertAlmostEqual(kelvin_to_celsius(298.15), 25.0)

    def test_fahrenheit_to_kelvin(self):
        self.assertAlmostEqual(fahrenheit_to_kelvin(32), 273.15) # 0°C
        self.assertAlmostEqual(fahrenheit_to_kelvin(212), 373.15) # 100°C
        self.assertAlmostEqual(fahrenheit_to_kelvin(-40), 233.15) # -40°C

    def test_kelvin_to_fahrenheit(self):
        self.assertAlmostEqual(kelvin_to_fahrenheit(273.15), 32.0) # 0°C
        self.assertAlmostEqual(kelvin_to_fahrenheit(373.15), 212.0) # 100°C
        self.assertAlmostEqual(kelvin_to_fahrenheit(233.15), -40.0) # -40°C

if __name__ == '__main__':
    unittest.main()
