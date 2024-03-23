from ast import literal_eval

from todo.constants import COMMANDS
from todo.parser.base import BaseParser, set_value
from todo.settings import config


class ListTodosParser(BaseParser):
    """
    usage: td [--completed] [--uncompleted] [--raw] [--group GROUP] [--interactive]
           td l [-c] [-u] [-r] [-g GROUP] [-i]
           td ls [-c] [-u] [-r] [-g GROUP] [-i]
           td list [-c] [-u] [-r] [-g GROUP] [-i]

    list todos

    optional arguments:
      -h, --help            show this help message and exit
      --raw, -r             only show todos
      --completed, -c       filter by completed todos
      --uncompleted, -u     filter by uncompleted todos
      --group GROUP, -g GROUP
                            filter by name of group
      --interactive, -i     toggle interactive mode

    `td` is the shortcut to `td list`
    """

    command = COMMANDS.LIST_TODOS

    def _add_arguments(self):
        self.parser.add_argument(
            "--completed",
            "-c",
            dest="state",
            nargs=0,
            default=bool(literal_eval(config["completed"])) if config.get("completed") else None,
            action=set_value(True),
            help="filter by completed todos",
        )
        self.parser.add_argument(
            "--uncompleted",
            "-u",
            dest="state",
            nargs=0,
            action=set_value(False),
            help="filter by uncompleted todos",
        )
        self.parser.add_argument(
            "--raw",
            "-r",
            dest="raw",
            nargs=0,
            action=set_value(True),
            help="only show todos",
        )
        self.parser.add_argument("--group", "-g", action="store", help="filter by name of group")
        self.parser.add_argument(
            "--interactive", "-i", action="store_true", help="toggle interactive mode"
        )
        self.parser.usage = "td [--completed] [--uncompleted] [--group GROUP] [--interactive]"
