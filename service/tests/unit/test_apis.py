import unittest

from api.helpers import handle_error_response, write_into_file


class TestHandleErrorResponse(unittest.TestCase):
    def test_default_response(self):
        response = handle_error_response("error", 500, 1, 500, msg=None)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.mimetype, "application/json")
        self.assertIn("type", response.data.decode())
        self.assertIn("code", response.data.decode())
        self.assertIn("subcode", response.data.decode())

    def test_custom_response(self):
        response = handle_error_response(
            "custom_error", 404, 2, 404, msg="Resource not found"
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.mimetype, "application/json")
        self.assertIn("type", response.data.decode())
        self.assertIn("code", response.data.decode())
        self.assertIn("subcode", response.data.decode())
        self.assertIn("msg", response.data.decode())
        self.assertIn("Resource not found", response.data.decode())


class TestWriteIntoFile(unittest.TestCase):
    def test_write_content(self):
        # Test writing content to a file
        location = "../static/test_output.txt"
        content = "Hello, world!"
        write_into_file(location, content)

        # Read the content from the file
        with open(location, "r") as file:
            written_content = file.read()

        self.assertEqual(written_content, content)

    def test_empty_content(self):
        # Test writing empty content to a file
        location = "test_empty_output.txt"
        content = ""
        write_into_file(location, content)

        # Read the content from the file
        with open(location, "r") as file:
            written_content = file.read()

        self.assertEqual(written_content, content)
