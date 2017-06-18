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

    # Assignment and deletion are currently unsupported!
    with pytest.raises(AttributeError):
        my_config.tmp_directories.vid_tmp = "/tmp/videos"
    with pytest.raises(AttributeError):
        del my_config.tmp_directories.vid_tmp


@pytest.fixture
def broken_config():
    # type: () -> MyConfig
    config_parser = ConfigParser()
    read_config_string(config_parser, """
[tmp_directories]
img_tmp=/tmp/img
# vid_tmp is missing
max_files=hundreds  # not an int
    """)
    config = MyConfig(config_parser)
    return config


def test_error_handling(broken_config):
    # type: (MyConfig) -> None

    # Unexpected section
    with pytest.raises(AttributeError):
        print(broken_config.nonexistent_section)

    # Unexpected option
    with pytest.raises(AttributeError):
        print(broken_config.tmp_directories.wav_tmp)

    # Missing option value
    with pytest.raises(NoOptionError):
        val = broken_config.tmp_directories.vid_tmp

    # Wrong type
    with pytest.raises(ValueError):
        val = broken_config.tmp_directories.max_files