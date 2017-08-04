from typing import List, Optional

from comfy.schema import BaseOption, Section


class Option(BaseOption):

    def unserialize(self, value):
        return value

    def serialize(self, new_value):
        if not isinstance(new_value, str):
            raise ValueError("New value should be a string.")
        return str(new_value)


class IntOption(BaseOption):

    def unserialize(self, raw_value):
        return int(raw_value)

    def serialize(self, new_value):
        if not isinstance(new_value, int):
            raise ValueError("New value should be an int.")

        return str(new_value)


class BoolOption(BaseOption):

    truth_values = {"1", "yes", "true"}

    def unserialize(self, raw_value):
        return raw_value.lower() in self.truth_values

    def serialize(self, new_value):
        if not isinstance(new_value, bool):
            raise ValueError("New value should be a boolean.")

        return str(new_value).lower()


class ListOption(BaseOption):

    def unserialize(self, raw_value):
        if raw_value.strip() == "":
            return []
        return [value.strip() for value in raw_value.split(",")]

    def serialize(self, new_value):
        if not isinstance(new_value, list):
            raise ValueError("New value should be a list.")

        return ','.join(new_value)
