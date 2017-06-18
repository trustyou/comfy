from typing import List, Optional

from comfy.schema import BaseOption, Section


class Option(BaseOption):

    def __get__(self, section, type=None):
        # type: (Section, Optional[type]) -> str
        config_parser = section.config_parser
        return config_parser.get(section.name, self.name)


class IntOption(BaseOption):

    def __get__(self, section, type=None):
        # type: (Section, Optional[type]) -> int
        config_parser = section.config_parser
        return config_parser.getint(section.name, self.name)


class BoolOption(BaseOption):

    truth_values = {"1", "yes", "true"}

    def __get__(self, section, type=None):
        # type: (Section, Optional[type]) -> bool
        config_parser = section.config_parser
        value = config_parser.get(section.name, self.name)
        return value.lower() in self.truth_values


class ListOption(BaseOption):

    def __get__(self, section, type=None):
        # type: (Section, Optional[type]) -> List[str]
        config_parser = section.config_parser
        values = config_parser.get(section.name, self.name)
        if values.strip() == "":
            return []
        return [value.strip() for value in values.split(",")]
