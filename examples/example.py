from configparser import ConfigParser

from comfy import *


class MyConfig(Schema):

    class Server(Section):
        host = Option()
        port = IntOption()
    server = None  # type: Server


if __name__ == "__main__":

    config_parser = ConfigParser()
    config_parser.read_string("""
[server]
host=api.trustyou.com
port=8080
""")
    config = MyConfig(config_parser)

    print("Host:", config.server.host)
    print("Port:", config.server.port)

