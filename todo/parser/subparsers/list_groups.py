from todo.constants import COMMANDS
from todo.parser.base import BaseParser, set_value


class ListGroupsParser(BaseParser):
    command = COMMANDS.LIST_GROUPS

    def _add_arguments(self):
        self.parser.add_argument("--completed", "-c", dest="state", nargs=0, action=set_value(True))
        self.parser.add_argument(
            "--uncompleted", "-u", dest="state", nargs=0, action=set_value(False)
        )
