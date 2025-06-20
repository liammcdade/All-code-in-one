import unittest
import sys
import os

# Add the parent directory to the Python path to import the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from storage_units import convert_storage

class TestStorageConversions(unittest.TestCase):

    def test_convert_storage_basic(self):
        self.assertAlmostEqual(convert_storage(1024, "B", "KB"), 1.0)
        self.assertAlmostEqual(convert_storage(1, "KB", "B"), 1024.0)
        self.assertAlmostEqual(convert_storage(1, "MB", "KB"), 1024.0)
        self.assertAlmostEqual(convert_storage(1, "GB", "MB"), 1024.0)
        self.assertAlmostEqual(convert_storage(1, "TB", "GB"), 1024.0)

    def test_convert_storage_multi_step(self):
        self.assertAlmostEqual(convert_storage(1, "GB", "B"), 1024*1024*1024.0)
        self.assertAlmostEqual(convert_storage(1, "TB", "MB"), 1024*1024.0)
        self.assertAlmostEqual(convert_storage(1048576, "KB", "TB"), 1048576 / (1024*1024*1024)) # 1 KB is 1/(1024^3) TB

    def test_convert_to_same_unit(self):
        self.assertAlmostEqual(convert_storage(500, "MB", "MB"), 500.0)
        self.assertAlmostEqual(convert_storage(100, "B", "B"), 100.0)
        self.assertAlmostEqual(convert_storage(2, "TB", "TB"), 2.0)

    def test_convert_with_zero_value(self):
        self.assertAlmostEqual(convert_storage(0, "GB", "MB"), 0.0)
        self.assertAlmostEqual(convert_storage(0, "B", "TB"), 0.0)

    def test_invalid_units(self):
        self.assertIsNone(convert_storage(1, "ZB", "MB")) # ZB is not a valid unit
        self.assertIsNone(convert_storage(1, "MB", "YB")) # YB is not a valid unit
        self.assertIsNone(convert_storage(1, "BYTES", "KB")) # BYTES is not valid, should be B
        self.assertIsNone(convert_storage(1, "kb", "megabytes")) # megabytes is not valid

    def test_case_insensitivity_for_units(self):
        self.assertAlmostEqual(convert_storage(1, "gb", "mb"), 1024.0)
        self.assertAlmostEqual(convert_storage(1024, "b", "kb"), 1.0)
        self.assertAlmostEqual(convert_storage(1, "Tb", "gB"), 1024.0)

if __name__ == '__main__':
    unittest.main()
