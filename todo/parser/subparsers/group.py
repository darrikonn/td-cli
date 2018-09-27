import argparse

from todo.constants import COMMANDS
from todo.parser.base import BaseParser, set_value


class GroupParser(BaseParser):
    """
    usage: td group [name] {get,delete,preset} ...
           td g [name] {g,d,p} ...

    positional arguments:
      name                  name of the group
      {...}                 commands
        get (g)             list group's todos
        delete (d)          delete group and its todos
        preset (p)          set group as the default group when listing todos

    optional arguments:
      -h, --help  show this help message and exit

    `td group [name]` defaults to `td group [name] get`
    """

    command = COMMANDS.GET_GROUP

    def _set_defaults(self, args):
        self.parser.set_default_subparser("list", args, 2)

    def _add_arguments(self):
        self.parser.add_argument("name", action="store", help="name of the group")
        subparser = self.parser.add_subparsers(dest="command", help=argparse.SUPPRESS)

        delete_parser = self._add_parser(
            subparser, "delete", aliases=["d"], help="delete group and its todos"
        )
        delete_parser.add_argument(
            "--yes",
            "-y",
            dest="skip_prompt",
            action="store_true",
            help="skip yes/no prompt when deleting group",
        )
        delete_parser.set_defaults(command=COMMANDS.DELETE_GROUP)
        delete_parser.usage = "td group [name] delete [--yes]\n       td group [name] d [-y]"

        preset_parser = self._add_parser(
            subparser,
            "preset",
            aliases=["p"],
            help="set group as the default group when listing todos",
        )
        preset_parser.set_defaults(command=COMMANDS.PRESET_GROUP)
        preset_parser.usage = "td group [name] preset\n       td group [name] p"

        get_parser = self._add_parser(subparser, "get", aliases=["g"], help="list group's todos")
        get_parser.add_argument(
            "--completed",
            "-c",
            dest="state",
            nargs=0,
            action=set_value(True),
            help="filter by completed todos",
        )
        get_parser.add_argument(
            "--uncompleted",
            "-u",
            dest="state",
            nargs=0,
            action=set_value(False),
            help="filter by uncompleted todos",
        )
        get_parser.add_argument(
            "--interactive", "-i", action="store_true", help="toggle interactive mode"
        )
        get_parser.set_defaults(command=COMMANDS.GET_GROUP)
        get_parser.usage = "td group [name]\n       td group [name] get\n       td group [name] g"
        get_parser.epilog = "`td group [name]` is the shortcut to `td group [name] get`"
