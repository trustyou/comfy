# comfy

Comfy lets you define schemata for config files, compatible with [mypy](http://mypy.readthedocs.io) type checking, and
IDE autocompletion. Example:

*Config schema:*

```python
from comfy import *

class MyConfig(Schema):
    class Server(Section):
        host = Option()
        port = IntOption()
    server: Server
    
    # In Python 3.5 or lower, write as:
    server = None  # type: Server
```

*Config file:*

```ini
[server]
host=api.trustyou.com
port=8080
```

Now to parse our beautiful config file:

```python
from configparser import ConfigParser

config_parser = ConfigParser()
# Read actual config files …

config = MyConfig(config_parser)

print(config.server.host)
# prints api.trustyou.com

print(config.server.hsot)  # Note the typo
# mypy error: "Server" has no attribute "hsot"

print(config.server.port.lower())
# mypy error: "int" has no attribute "lower"
```