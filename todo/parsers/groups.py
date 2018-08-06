from todo.constants import COMMANDS
from todo.parsers.base import BaseParser


class GroupsParser(BaseParser):
    has_command_prefix = True

    def _interpret(self, parsed_args):
        if parsed_args.add_group:
            return {COMMANDS.ADD_GROUP: {"name": parsed_args.add_group}}
        return {COMMANDS.LIST_GROUPS: {}}

    def _add_arguments(self):
        self.parser.add_argument("--add", "-a", dest=COMMANDS.ADD_GROUP, action="store")
