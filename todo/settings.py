import configparser
import os
from functools import lru_cache
from pathlib import Path

CONFIG_SECTION = "settings"
DEFAULT_CONFIG = {"database_name": "todo", "editor": "vi", "group": None}
EXAMPLE_CONFIG = """[settings]
group: {group}
"""


@lru_cache()
def get_project_config(filepath):
    """ returns the absolute path of nearest config """
    config_file = Path.joinpath(filepath, ".td.cfg")

    if Path.home() >= filepath:
        return None
    elif Path.exists(config_file):
        return config_file
    else:
        return get_project_config(filepath.parent)


@lru_cache()
def _get_config():
    settings = DEFAULT_CONFIG

    def _update_from_config(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        if config.has_section(CONFIG_SECTION):
            user_settings = dict(config.items(CONFIG_SECTION))
            settings.update(user_settings)

    # from environment
    environment_editor = os.environ.get("EDITOR")
    if environment_editor:
        settings["editor"] = environment_editor

    # from root config
    config_file = Path.joinpath(Path.home(), ".config", "td-cli", "td.cfg")
    if Path.exists(config_file):
        _update_from_config(config_file)

    settings["group"] = None

    # from project config
    project_config_file = get_project_config(Path.cwd())
    if project_config_file:
        _update_from_config(project_config_file)

    return settings


config = _get_config()
