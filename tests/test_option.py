try:
    from configparser import ConfigParser
except ImportError:
    # Python 2
    from ConfigParser import ConfigParser

import pytest

from comfy import BoolOption, IntOption, ListOption, Option, Section


@pytest.fixture
def section():
    # type: () -> Section
    config_parser = ConfigParser()
    config_parser.add_section("performance")
    return Section("performance", config_parser)


def test_option(section):
    # type: (Section) -> None
    opt = Option()
    opt.set_name("log_prefix")
    section.config_parser.set("performance", "log_prefix", "DEBUG")
    assert opt.__get__(section) == "DEBUG"


def test_int_option(section):
    # type: (Section) -> None
    opt = IntOption()
    opt.set_name("max_threads")

    section.config_parser.set("performance", "max_threads", "200")
    assert opt.__get__(section) == 200

    section.config_parser.set("performance", "max_threads", "as many as cores")
    with pytest.raises(ValueError):
        opt.__get__(section)


def test_bool_option(section):
    # type: (Section) -> None
    opt = BoolOption()
    opt.set_name("resize_pool")

    for val in BoolOption.truth_values:
        section.config_parser.set("performance", "resize_pool", val)
        assert opt.__get__(section) is True

    for val in {"no", "false", "0", ""}:
        section.config_parser.set("performance", "resize_pool", val)
        assert opt.__get__(section) is False


def test_list_option(section):
    # type: (Section) -> None

    opt = ListOption()
    opt.set_name("schedulers")

    section.config_parser.set("performance", "schedulers", "priority,fifo")
    assert opt.__get__(section) == ["priority", "fifo"]

    section.config_parser.set("performance", "schedulers", "priority")
    assert opt.__get__(section) == ["priority"]

    section.config_parser.set("performance", "schedulers", "")
    assert opt.__get__(section) == []