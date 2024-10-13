import configparser
import os

config = configparser.ConfigParser()

config_file_path = os.path.join(os.path.dirname(__file__), 'config.ini')

config.read(config_file_path)
# config.read('config.ini')

if not config.sections():
    raise FileNotFoundError(f"Config file not found: {config_file_path}")


def reload_config():
    config.read('config.ini')
