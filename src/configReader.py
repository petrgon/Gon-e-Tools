import configparser
from helper import tlog
from window import Window

CONFIG_PATH = "config.ini"

# Reads config
class ConfigReader:
    _window: Window = None

    def __init__(self, director):
        self._window = director._window
        return None

    def GetSection(self, section):
        config = configparser.ConfigParser()
        config.optionxform = str
        try:
            config.read(CONFIG_PATH)
            items = config.items(section)
            return map(lambda i : i[0], items)
        except Exception as e:
            self._window.Log(tlog(self.__class__.__name__, e))
            return None

    def Get(self, section, key):
        config = configparser.ConfigParser()
        config.optionxform = str
        try:
            config.read(CONFIG_PATH)
            config.sections()
            if not section in config or not key in config[section]:
                return None
            return config[section][key]
        except Exception as e:
            self._window.Log(tlog(self.__class__.__name__, e))
            return None
        
