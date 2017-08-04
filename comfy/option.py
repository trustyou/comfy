from typing import List, Optional, Text, Any

from comfy.schema import BaseOption, Section


class Option(BaseOption):

    def unserialize(self, value):
        # type: (Text) -> Text
        return value

    def serialize(self, new_value):
        # type: (Text) -> Text
        if not isinstance(new_value, str):
            raise ValueError("New value should be a string.")
        return str(new_value)


class IntOption(BaseOption):

    def unserialize(self, raw_value):
        # type: (Text) -> int
        return int(raw_value)

    def serialize(self, new_value):
        # type: (int) -> Text
        if not isinstance(new_value, int):
            raise ValueError("New value should be an int.")

        return str(new_value)


class BoolOption(BaseOption):

    truth_values = {"1", "yes", "true"}

    def unserialize(self, raw_value):
        # type: (Text) -> bool
        return raw_value.lower() in self.truth_values

    def serialize(self, new_value):
        # type: (bool) -> Text
        if not isinstance(new_value, bool):
            raise ValueError("New value should be a boolean.")

        return str(new_value).lower()


class ListOption(BaseOption):

    def unserialize(self, raw_value):
        # type: (Text) -> List[Any]
        if raw_value.strip() == "":
            return []
        return [value.strip() for value in raw_value.split(",")]

    def serialize(self, new_value):
        # type: (List[Any]) -> Text
        if not isinstance(new_value, list):
            raise ValueError("New value should be a list.")

        return ','.join(str(val) for val in new_value)
