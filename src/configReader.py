import configparser

CONFIG_PATH = "config.ini"

# Reads config
class ConfigReader:
    def __init__(self):
        return

    def GetSection(self, section):
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        items = config.items(section)
        return map(lambda i : i[0], items)

    def Get(self, section, key):
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        config.sections()
        if not section in config or not key in config[section]:
            return None
        return config[section][key]
        
