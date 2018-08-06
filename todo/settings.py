import configparser
import os
from functools import lru_cache

from todo.constants import STATES

CONFIG_FILE_NAME = "~/.td.cfg"
CONFIG_SECTION = "settings"
DEFAULT_CONFIG = {"database_name": "todo", "editor": "vi", "default_state": None}


@lru_cache()
def _get_config():
    config_file = CONFIG_FILE_NAME and os.path.expanduser(CONFIG_FILE_NAME)
    settings = DEFAULT_CONFIG
    if os.path.exists(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        if config.has_section(CONFIG_SECTION):
            user_settings = dict(config.items(CONFIG_SECTION))
            if "default_state" in user_settings:
                if user_settings["default_state"] == STATES.COMPLETED:
                    user_settings["default_state"] = True
                elif user_settings["default_state"] == STATES.UNCOMPLETED:
                    user_settings["default_state"] = False
                else:
                    user_settings["default_state"] = None
            settings.update(user_settings)
    return settings


config = _get_config()
