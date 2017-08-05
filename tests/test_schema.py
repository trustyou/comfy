try:
    from configparser import ConfigParser, NoOptionError
except ImportError:
    # Python 2
    from ConfigParser import ConfigParser, NoOptionError

import pytest

from comfy import Schema, Section, Option, IntOption
from comfy.util import read_config_string


class MyConfig(Schema):

    class TmpDirectories(Section):
        img_tmp = Option()
        vid_tmp = Option()
        max_files = IntOption()
    tmp_directories = None  # type: TmpDirectories


@pytest.fixture
def my_config():
    # type: () -> MyConfig
    config_parser = ConfigParser()
    read_config_string(config_parser, """
[tmp_directories]
img_tmp=/tmp/img
vid_tmp=/tmp/vid
max_files=1024
    """)
    config = MyConfig(config_parser)
    return config


def test_smoke(my_config):
    # type: (MyConfig) -> None

    # TODO Fix for Python 2, fails with: AssertionError: assert <comfy.option.Option instance at ...> == '/tmp/img'
    # Why doesn't the descriptor __get__ get invoked in Python 2?
    assert my_config.tmp_directories.img_tmp == "/tmp/img"
    assert my_config.tmp_directories.vid_tmp == "/tmp/vid"
    assert my_config.tmp_directories.max_files == 1024

    new_val = "/tmp/videos"
    my_config.tmp_directories.vid_tmp = new_val
    assert my_config.tmp_directories.vid_tmp == new_val
    assert my_config.config_parser.get("tmp_directories", "vid_tmp") == new_val

    del my_config.tmp_directories.vid_tmp
    with pytest.raises(NoOptionError):
        assert my_config.tmp_directories.vid_tmp == new_val


def _test_error(config, Error):
    # type: (str, Exception) -> None

    config_parser = ConfigParser()
    read_config_string(config_parser, config)
    with pytest.raises(Error):
        config = MyConfig(config_parser)


def test_missing_option():
    config = """
[tmp_directories]
img_tmp=/tmp/img
# vid_tmp is missing
max_files=1024
    """
    _test_error(config, NoOptionError)

def test_wrong_int_value():
    config = """
[tmp_directories]
img_tmp=/tmp/img
vid_tmp=/tmp/vid
max_files=not_a_int  
    """
    _test_error(config, ValueError)
