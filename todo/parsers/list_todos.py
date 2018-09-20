from todo.constants import COMMANDS
from todo.parsers.base import BaseParser, set_value


class ListTodosParser(BaseParser):
    command = COMMANDS.LIST_TODOS

    def _add_arguments(self):
        self.parser.add_argument("--completed", "-c", dest="state", nargs=0, action=set_value(True))
        self.parser.add_argument(
            "--uncompleted", "-u", dest="state", nargs=0, action=set_value(False)
        )
        self.parser.add_argument("--group", "-g", action="store")
        self.parser.add_argument("--interactive", "-i", action="store_true")
