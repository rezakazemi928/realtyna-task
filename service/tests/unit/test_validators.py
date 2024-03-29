import unittest

from api.helpers import (  # Replace with the actual module name
    InvalidString,
    StringValidator,
)


class TestStringValidator(unittest.TestCase):
    def test_non_empty_string(self):
        # Test with a non-empty string
        validator = StringValidator("Name", "John Doe")
        self.assertIsNone(validator.check_empty_string())

    def test_empty_string(self):
        # Test with an empty string
        validator = StringValidator("Address", "")
        with self.assertRaises(InvalidString) as context:
            validator.check_empty_string()
        self.assertEqual(str(context.exception), "Address cannot be none.")

    def test_none_string(self):
        # Test with None input
        validator = StringValidator("Email", None)
        with self.assertRaises(InvalidString) as context:
            validator.check_empty_string()
        self.assertEqual(str(context.exception), "Email cannot be none.")
