from todo.constants import COMMANDS
from todo.parser.base import BaseParser, set_value


class GroupParser(BaseParser):
    command = COMMANDS.GET_GROUP

    def _set_defaults(self, args):
        self.parser.set_default_subparser("list", args, 2)

    def _add_arguments(self):
        self.parser.add_argument("name", action="store")
        subparser = self.parser.add_subparsers(dest="command")

        delete_parser = subparser.add_parser("delete", aliases=["d"])
        delete_parser.add_argument("--yes", "-y", dest="skip_prompt", action="store_true")
        delete_parser.set_defaults(command=COMMANDS.DELETE_GROUP)

        preset_parser = subparser.add_parser("preset", aliases=["ps", "p"])
        preset_parser.set_defaults(command=COMMANDS.PRESET_GROUP)

        list_parser = subparser.add_parser("list")
        list_parser.add_argument("--completed", "-c", dest="state", nargs=0, action=set_value(True))
        list_parser.add_argument(
            "--uncompleted", "-u", dest="state", nargs=0, action=set_value(False)
        )
        list_parser.add_argument("--interactive", "-i", action="store_true")
        list_parser.set_defaults(command=COMMANDS.GET_GROUP)
