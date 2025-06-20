import unittest
import sys
import os

# Add the parent directory to the Python path to import the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from case_converter import (
    to_uppercase,
    to_lowercase,
    to_titlecase,
)


class TestCaseConversions(unittest.TestCase):

    def test_to_uppercase(self):
        self.assertEqual(to_uppercase("hello"), "HELLO")
        self.assertEqual(to_uppercase("Hello World"), "HELLO WORLD")
        self.assertEqual(to_uppercase("already UPPERCASE"), "ALREADY UPPERCASE")
        self.assertEqual(to_uppercase("123 numbers"), "123 NUMBERS")
        self.assertEqual(to_uppercase(""), "")  # Empty string
        self.assertEqual(to_uppercase("mIxEdCaSe"), "MIXEDCASE")

    def test_to_lowercase(self):
        self.assertEqual(to_lowercase("HELLO"), "hello")
        self.assertEqual(to_lowercase("Hello World"), "hello world")
        self.assertEqual(to_lowercase("already lowercase"), "already lowercase")
        self.assertEqual(to_lowercase("123 NUMBERS"), "123 numbers")
        self.assertEqual(to_lowercase(""), "")  # Empty string
        self.assertEqual(to_lowercase("mIxEdCaSe"), "mixedcase")

    def test_to_titlecase(self):
        self.assertEqual(to_titlecase("hello world"), "Hello World")
        self.assertEqual(to_titlecase("already Titled"), "Already Titled")
        self.assertEqual(to_titlecase("PYTHON programming"), "Python Programming")
        self.assertEqual(
            to_titlecase("1st an example"), "1St An Example"
        )  # Numbers and letters
        self.assertEqual(to_titlecase(""), "")  # Empty string
        self.assertEqual(to_titlecase("mixedCASE example"), "Mixedcase Example")
        self.assertEqual(
            to_titlecase("title with 'apostrophe"), "Title With 'Apostrophe"
        )
        self.assertEqual(to_titlecase("a-dash-example"), "A-Dash-Example")


if __name__ == "__main__":
    unittest.main()
