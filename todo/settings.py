import configparser
import os
from functools import lru_cache
from pathlib import Path
from subprocess import check_output

CONFIG_FILE_NAME = "~/.td.cfg"
CONFIG_SECTION = "settings"
DEFAULT_CONFIG = {"database_name": "todo", "editor": "vi", "group": None}
EXAMPLE_CONFIG = """[settings]
group: {group}
"""


@lru_cache()
def get_git_project_config():
    """ returns the absolute path of the repository root """
    try:
        base = check_output("git rev-parse --show-toplevel 2> /dev/null", shell=True)
        path = base.decode("utf-8").strip()
        return "{path}/.td.cfg".format(path=path)
    except Exception:
        return ""


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
    config_file = os.path.expanduser(Path(CONFIG_FILE_NAME))
    if os.path.exists(config_file):
        _update_from_config(config_file)

    settings["group"] = None

    # from git project config
    git_config_file = get_git_project_config()
    if os.path.exists(git_config_file):
        _update_from_config(git_config_file)

    return settings


config = _get_config()
