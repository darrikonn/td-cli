from todo.constants import COMMANDS
from todo.parser.base import BaseParser, set_value


class ListGroupsParser(BaseParser):
    """
    usage: td list-groups [--completed] [--uncompleted]
           td lg [-c] [-u]

    list groups

    optional arguments:
      -h, --help         show this help message and exit
      --completed, -c    filter by completed groups
      --uncompleted, -u  filter by uncompleted groups
    """

    command = COMMANDS.LIST_GROUPS

    def _add_arguments(self):
        self.parser.add_argument(
            "--completed",
            "-c",
            dest="state",
            nargs=0,
            action=set_value(True),
            help="filter by completed groups",
        )
        self.parser.add_argument(
            "--uncompleted",
            "-u",
            dest="state",
            nargs=0,
            action=set_value(False),
            help="filter by uncompleted groups",
        )
