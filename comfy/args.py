from argparse import ArgumentParser
from typing import List, AnyStr


def get_arg_name(section_name, option_name):
    """
    Gets the name of the cli argument based on the name of the section and the name of the option.
    It concats the 2 names using an underline separator and prefixes the results with 2 dashes.

    Ex.
        section: "server"
        option: "port"
            ->
        argument: "--server_port"

    :param section_name: the section name
    :param option_name: the option name
    :return: the argument name
    """
    return "--{}_{}".format(section_name, option_name)


def overwrite_options(argv, schema):
    # type: (List[AnyStr], Schema) -> None
    """
    It overwrites the schema options based on command line parameters.

    :param argv: the cli parameters
    :param schema: the schema
    """

    sections = schema.get_sections()
    argument_parser = ArgumentParser()
    arg_name_to_option = {}
    for section in sections:
        for option_name, option in section.get_options():
            arg_name = get_arg_name(section.name, option_name)
            arg_name_to_option[arg_name] = (section, option)
            argument_parser.add_argument(arg_name)

    args, _ = argument_parser.parse_known_args(argv)
    result = vars(args)

    for arg_name, arg_value in result.items():
        if arg_value is not None:
            key = "--{}".format(arg_name.replace("-", "_"))
            section, option = arg_name_to_option[key]
            section.__setattr__(option.name, option.unserialize(arg_value))
