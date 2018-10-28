try:
    from configparser import ConfigParser, NoOptionError
except ImportError:
    # Python 2
    from ConfigParser import ConfigParser, NoOptionError

from comfy import *


class MyConfig(Schema):

    class TmpDirectories(Section):
        img_tmp = Option()
        vid_tmp = Option()
        max_files = IntOption()
    tmp_directories = None


if __name__ == "__main__":

    config_parser = ConfigParser()

    config_parser.read_string(u"""
[tmp_directories]
img_tmp=/tmp/img
vid_tmp=/tmp/vid
max_files=1024
""")
    config = MyConfig(config_parser)

    print(config.tmp_directories.img_tmp)
