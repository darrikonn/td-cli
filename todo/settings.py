import configparser
import os
from functools import lru_cache
from pathlib import Path
from typing import Optional, Tuple

from todo.exceptions import TodoException

CONFIG_SECTION = "settings"
DEFAULT_CONFIG = {"database_name": "todo", "editor": "vi", "group": None, "format": "tmp"}
EXAMPLE_CONFIG = """[settings]
group: {group}
completed: 0
"""


@lru_cache()
def get_project_config(filepath):
    """returns the absolute path of nearest config"""
    config_file = Path.joinpath(filepath, ".td.cfg")

    if Path.home() >= filepath:
        return None
    elif Path.exists(config_file):
        return config_file
    else:
        return get_project_config(filepath.parent)


@lru_cache()
def get_home() -> Tuple[Path, str]:
    # try from TD_CLI_HOME environment variable
    td_cli_env: Optional[str] = os.environ.get("TD_CLI_HOME")
    if td_cli_env:
        td_cli_env_dir: Path = Path.expanduser(Path(td_cli_env))
        if not Path.exists(td_cli_env_dir):
            raise TodoException(
                f'TD_CLI_HOME environment variable set to "{td_cli_env_dir}", but directory does not exist'
            )

        return (td_cli_env_dir, "")

    # try from XDG_CONFIG_HOME environment variable
    xdg_config_home: Optional[str] = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config_home:
        xdg_config_home_dir: Path = Path.expanduser(Path(xdg_config_home))
        if not Path.exists(xdg_config_home_dir):
            raise TodoException(
                f'XDG_CONFIG_HOME environment variable set to "{xdg_config_home}", but directory does not exist'
            )

        config_dir = Path.joinpath(xdg_config_home_dir, "td-cli")
        if not config_dir.exists():
            Path.mkdir(config_dir)
        return (config_dir, "")

    # fallback to home directory
    return (Path.home(), ".")


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
    home_dir, prefix = get_home()
    config_file = Path.joinpath(home_dir, f"{prefix}todo.cfg")
    if Path.exists(config_file):
        _update_from_config(config_file)

    settings["group"] = None

    # from project config
    project_config_file = get_project_config(Path.cwd())
    if project_config_file:
        _update_from_config(project_config_file)

    return settings


config = _get_config()
