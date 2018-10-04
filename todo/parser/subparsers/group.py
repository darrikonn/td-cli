from todo.constants import COMMANDS
from todo.parser.base import BaseParser, set_value


class GroupParser(BaseParser):
    """
    usage: td group [name] {list,delete,preset} ...
           td g [name] {l,d,p} ...

    manage group

    positional arguments:
      name                  name of the group
      {...}                 commands
        list (ls, l)        list group's todos
        delete (d)          delete group and its todos
        preset (p)          set group as the default group when listing todos

    optional arguments:
      -h, --help  show this help message and exit

    `td group [name]` defaults to `td group [name] ls`
    """

    command = COMMANDS.GET_GROUP

    def _set_defaults(self, args):
        self.parser.set_default_subparser("list", args, 2)

    def _add_arguments(self):
        self.parser.add_argument("name", action="store", help="name of the group")
        subparser = self.parser.add_subparsers(dest="command", help="commands")

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
        delete_parser.description = "delete group and its todos"

        preset_parser = self._add_parser(
            subparser,
            "preset",
            aliases=["p"],
            help="set group as the default group when listing todos",
        )
        preset_parser.set_defaults(command=COMMANDS.PRESET_GROUP)
        preset_parser.usage = "td group [name] preset\n       td group [name] p"
        preset_parser.description = "set group as the default group when listing todos"

        list_parser = self._add_parser(
            subparser, "list", aliases=["ls", "l"], help="list group's todos"
        )
        list_parser.add_argument(
            "--completed",
            "-c",
            dest="state",
            nargs=0,
            action=set_value(True),
            help="filter by completed todos",
        )
        list_parser.add_argument(
            "--uncompleted",
            "-u",
            dest="state",
            nargs=0,
            action=set_value(False),
            help="filter by uncompleted todos",
        )
        list_parser.add_argument(
            "--interactive", "-i", action="store_true", help="toggle interactive mode"
        )
        list_parser.set_defaults(command=COMMANDS.GET_GROUP)
        list_parser.usage = (
            "td group [name]\n       td group [name] list\n       "
            "td group [name] ls\n       td group [name] l"
        )
        list_parser.epilog = "`td group [name]` is the shortcut to `td group [name] list`"
        list_parser.description = "list group's todos"
