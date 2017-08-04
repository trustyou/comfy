try:
    from configparser import ConfigParser, NoOptionError
except ImportError:
    # Python 2
    from ConfigParser import ConfigParser, NoOptionError

from inspect import getmembers, isclass
from typing import Any, Optional, Type, Text

from comfy.util import camel_case_to_lower


class Schema:
    """
    Base class for config file schema definition.

    Inherit from this class, and define sections and options::

        class MySchema(Schema):

            class MySection(Section):
                my_opt = Option()
            my_section: MySection  # this is optional, but enables mypy checking and IDE type hints

    The use your schema to wrap a config parser::

        config = MySchema(config_parser)
        print(config.my_section.my_opt)
    """

    def __init__(self, config_parser):
        # type: (ConfigParser) -> None
        self.config_parser = config_parser

        # Find any sections in this class, and instantiate them, binding them to this config parser
        for name, value in getmembers(self, isclass):
            if issubclass(value, Section):
                section_class = value  # type: Type[Section]
                section_name = camel_case_to_lower(name)
                section = section_class(section_name, config_parser)
                setattr(self, section_name, section)


class Section:
    """
    Corresponds to a [section] in a config file.

    The class name gets converted to lower case automatically! I.e. for a config section database_options, declare::

        class DatabaseOptions(Section):
            # ...
    """

    def __init__(self, name, config_parser):
        # type: (str, ConfigParser) -> None
        self.name = name
        self.config_parser = config_parser

        # Find any options in this section, and let them know about their name in this section
        # This is a poor man's __set_name__ :)
        for name, value in getmembers(type(self)):
            if isinstance(value, BaseOption):
                option = value  # type: BaseOption
                option.set_name(name)
                self.validate(option)

    def validate(self, option):
        # type: (BaseOption) -> None

        try:
            option.__get__(self)
        except (ValueError, TypeError, NoOptionError) as e: 
            message = "Validation error ({}.{}).\nDetails: {}".format(self.name, option.name, e)
            e.args = (message, ) + e.args[1:]
            raise 


class BaseOption:
    """
    Base class for options.

    Subclass this and override unserialize() and serialize() to define new option types.
    """

    def __init__(self):
        self.name = None  # type: str

    def unserialize(self, value):
        # type: (Text) -> Any
        # Override in sub classes.
        raise NotImplementedError()

    def serialize(self, new_value):
        # type: (Any) -> Text
        """Checks if the value corresponds to the type of option.

        Returns a string, which will be stored in the config_parser instance.

        Raises ValueError if new_value does not meet expectations.
        """
        raise NotImplementedError()

    def __get__(self, section, type=None):
        # type: (Section, Optional[type]) -> Any
        config_parser = section.config_parser

        raw_value = config_parser.get(section.name, self.name)

        return self.unserialize(raw_value)

    def __set__(self, section, new_value):
        # type: (Section, Any) -> None
        config_parser = section.config_parser

        raw_value = self.serialize(new_value)

        config_parser.set(section.name, self.name, raw_value)

    def __delete__(self, section):
        config_parser = section.config_parser

        config_parser.remove_option(section.name, self.name)

    def set_name(self, name):
        # type: (str) -> None
        """
        Set the name under which this option is to be found in its section.
        """
        self.name = name
