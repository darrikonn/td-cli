from todo.parsers.base import BaseParser


class GroupsParser(BaseParser):
    has_command_prefix = True

    def _interpret(self, parsed_args):
        if parsed_args.add_group:
            return {"add_group": {"name": parsed_args.add_group}}
        return {"list_groups": {}}

    def _add_arguments(self):
        self.parser.add_argument('--add', '-a', dest='add_group', action='store')
