import argparse

from todo.constants import COMMANDS
from todo.parser.base import BaseParser


class TodoParser(BaseParser):
    """
    usage: td [id] {get,delete,uncomplete,complete,edit} ...

    manage todo

    positional arguments:
      id                    the id of the todo
      {...}                 commands
        get (g)             show todo's details
        delete (d)          delete todo
        uncomplete (u)      uncomplete todo
        complete (c)        complete todo
        edit (e)            edit todo

    optional arguments:
      -h, --help            show this help message and exit

    `td [id]` defaults to `td [id] get`
    You don't have to specify the whole `id`, a substring will do
    """

    command = COMMANDS.GET_TODO

    def _add_arguments(self):
        self.parser.add_argument("id", action="store", help="the id of the todo")
        subparser = self.parser.add_subparsers(dest="command", help="commands")

        get_parser = self._add_parser(subparser, "get", aliases=["g"], help="get todo")
        get_parser.set_defaults(command=COMMANDS.GET_TODO)
        get_parser.usage = "td [id]\n       td [id] get\n       td [id] g"
        get_parser.epilog = "`td [id]` is the shortcut to `td [id] get`"
        get_parser.description = "show todo's details"

        delete_parser = self._add_parser(subparser, "delete", aliases=["d"], help="delete todo")
        delete_parser.add_argument(
            "--yes",
            "-y",
            dest="skip_prompt",
            action="store_true",
            help="skip yes/no prompt when deleting todo",
        )
        delete_parser.set_defaults(command=COMMANDS.DELETE_TODO)
        delete_parser.usage = "td [id] delete [-yes]\n       td [id] d [-y]"
        delete_parser.description = "delete todo"

        uncomplete_parser = self._add_parser(
            subparser, "uncomplete", aliases=["u"], help="uncomplete todo"
        )
        uncomplete_parser.set_defaults(command=COMMANDS.UNCOMPLETE_TODO)
        uncomplete_parser.usage = "td [id] uncomplete\n       td [id] u"
        uncomplete_parser.description = "uncomplete todo"

        complete_parser = self._add_parser(
            subparser, "complete", aliases=["c"], help="complete todo"
        )
        complete_parser.set_defaults(command=COMMANDS.COMPLETE_TODO)
        complete_parser.usage = "td [id] complete\n       td [id] c"
        complete_parser.description = "complete todo"

        edit_parser = self._add_parser(
            subparser,
            "edit",
            aliases=["e"],
            help="edit todo",
            formatter_class=argparse.RawTextHelpFormatter,
            epilog="""If no optional arguments are provided, the todo will be
opened in your editor where you can edit the todo's details.
The editor defaults to `vi`, but you can choose your preferred one be setting:
```
[settings]
editor: <your_editor>
```
in ~/.td.cfg
""",
        )
        edit_parser.add_argument("--name", "-n", action="store", help="update todo's name")
        edit_parser.add_argument("--details", "-d", action="store", help="update todo's detail")
        edit_parser.add_argument("--group", "-g", action="store", help="set todo's group")
        edit_parser.set_defaults(command=COMMANDS.EDIT_TODO)
        edit_parser.usage = "td [id] edit [--name NAME] [--details DETAILS]\n       td [id] e [-n NAME] [-d DETAILS]"
        edit_parser.description = "edit todo"
