from todo.constants import COMMANDS
from todo.parsers.base import BaseParser


class GroupParser(BaseParser):
    command = COMMANDS.GET_GROUP

    def _add_arguments(self):
        self.parser.add_argument("name", action="store")
        subparser = self.parser.add_subparsers(dest="command")

        delete_parser = subparser.add_parser("delete", aliases=["d"])
        delete_parser.add_argument("--yes", "-y", dest="skip_prompt", action="store_true")
        delete_parser.set_defaults(command=COMMANDS.DELETE_GROUP)

        preset_parser = subparser.add_parser("preset", aliases=["ps", "p"])
        preset_parser.set_defaults(command=COMMANDS.PRESET_GROUP)
