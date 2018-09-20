from todo.constants import COMMANDS
from todo.parsers.base import BaseParser


class TodoParser(BaseParser):
    command = COMMANDS.GET_TODO

    def _add_arguments(self):
        self.parser.add_argument("id", action="store")
        subparser = self.parser.add_subparsers(dest="command")

        delete_parser = subparser.add_parser("delete", aliases=["d"])
        delete_parser.add_argument("--yes", "-y", dest="skip_prompt", action="store_true")
        delete_parser.set_defaults(command=COMMANDS.DELETE_TODO)

        uncomplete_parser = subparser.add_parser("uncomplete", aliases=["uc", "u"])
        uncomplete_parser.set_defaults(command=COMMANDS.NAME_TODO)

        complete_parser = subparser.add_parser("complete", aliases=["c"])
        complete_parser.set_defaults(command=COMMANDS.COMPLETE_TODO)

        edit_parser = subparser.add_parser("edit", aliases=["e"])
        edit_parser.add_argument("--name", "-n", action="store")
        edit_parser.add_argument("--details", "-d", action="store")
        edit_parser.set_defaults(command=COMMANDS.EDIT_TODO)
