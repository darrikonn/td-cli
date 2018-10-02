import configparser
import os
from functools import lru_cache

CONFIG_FILE_NAME = "~/.td.cfg"
CONFIG_SECTION = "settings"
DEFAULT_CONFIG = {"database_name": "todo", "editor": "vi"}


@lru_cache()
def _get_config():
    config_file = CONFIG_FILE_NAME and os.path.expanduser(CONFIG_FILE_NAME)
    settings = DEFAULT_CONFIG
    environment_editor = os.environ.get("EDITOR")
    if environment_editor:
        settings["editor"] = environment_editor
    if os.path.exists(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        if config.has_section(CONFIG_SECTION):
            user_settings = dict(config.items(CONFIG_SECTION))
            settings.update(user_settings)
    return settings


config = _get_config()
