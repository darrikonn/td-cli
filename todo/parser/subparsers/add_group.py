from todo.constants import COMMANDS
from todo.parser.base import BaseParser


class AddGroupParser(BaseParser):
    """
    usage: td add-group [name]
           td ag [name]

    add group

    positional arguments:
      name        the new group's name

    optional arguments:
      -h, --help  show this help message and exit
    """

    command = COMMANDS.ADD_GROUP

    def _add_arguments(self):
        self.parser.add_argument("name", action="store", help="the new group's name")
