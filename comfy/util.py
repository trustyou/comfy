try:
    from configparser import ConfigParser
except ImportError:
    # Python 2
    from ConfigParser import ConfigParser
    from StringIO import StringIO

import re
import sys


def camel_case_to_lower(name):
    # type: (str) -> str
    """
    Convert a string written in CamelCase to lower case, with underscores inserted before capitals.
    :param name: CamelCase string
    :return: camel_case string returned as lower case
    """
    return re.sub("([^A-Z])([A-Z][A-Za-z]*)", r"\1_\2", name).lower()


if sys.version_info[0] == 2:

    def read_config_string(config_parser, string):
        # type: (ConfigParser, str) -> None
        """
        Read config from string. For Python 2.
        """
        buffer = StringIO(string)
        config_parser.readfp(buffer)
else:

    def read_config_string(config_parser, string):
        # type: (ConfigParser, str) -> None
        config_parser.read_string(string)
