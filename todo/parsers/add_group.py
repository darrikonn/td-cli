from todo.constants import COMMANDS
from todo.parsers.base import BaseParser


class AddGroupParser(BaseParser):
    command = COMMANDS.ADD_GROUP

    def _add_arguments(self):
        self.parser.add_argument("name", action="store")
