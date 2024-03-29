import re

from api.helpers import InvalidString


class StringValidator:
    def __init__(self, field_name, input_string) -> None:
        self.input_string = input_string
        self.field_name = field_name

    def check_empty_string(self):
        """Check if string is empty or not."""

        if self.input_string is None:
            raise InvalidString(f"{self.field_name} cannot be none.")

        regex = r"^[^\s].*$"
        # * if matched so the field is not empty
        if not re.match(regex, self.input_string):
            raise InvalidString(f"{self.field_name} cannot be none.")
