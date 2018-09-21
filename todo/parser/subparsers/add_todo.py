from todo.constants import COMMANDS
from todo.parser.base import BaseParser, set_value


class AddTodoParser(BaseParser):
    command = COMMANDS.ADD_TODO

    def _add_arguments(self):
        self.parser.add_argument("name", action="store")
        self.parser.add_argument("--complete", "-c", dest="state", nargs=0, action=set_value(True))
        self.parser.add_argument(
            "--uncomplete", "-u", dest="state", nargs=0, action=set_value(False)
        )
        self.parser.add_argument("--group", "-g", action="store")

        exclusive_parser = self.parser.add_mutually_exclusive_group()
        exclusive_parser.add_argument("--edit", "-e", action="store_true")
        exclusive_parser.add_argument("--details", "-d", action="store")
