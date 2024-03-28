from api.helpers import InvalidString


class StringValidator:
    def check_empty_string(self, input_string: str, field_name):
        """Check if string is empty or not."""
        if not input_string or not input_string.strip():
            raise InvalidString(f"Empty string is not valid for {field_name}.")

        if input_string is None:
            raise InvalidString(f"{field_name} cannot be none.")
