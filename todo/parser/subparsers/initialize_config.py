from todo.constants import COMMANDS
from todo.parser.base import BaseParser


class InitializeConfigParser(BaseParser):
    """
    usage: td init-config
           td ic

    initialize config

    optional arguments:
      -h, --help         show this help message and exit
    """

    command = COMMANDS.INITIALIZE_CONFIG
