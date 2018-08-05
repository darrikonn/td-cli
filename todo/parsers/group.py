import sys

from todo.commands.group.get import STATES
from todo.parsers.base import BaseParser, set_value


class GroupParser(BaseParser):
    arguments = ('name', )
    has_command_prefix = True

    def _normalize(self, parsed_args):
        if len(sys.argv[2:]) == 1:
            setattr(parsed_args, 'get_group', STATES.UNCOMPLETED)
        return parsed_args

    def _add_arguments(self):
        parser_group = self.parser.add_mutually_exclusive_group()
        parser_group.add_argument('--delete', '-d', dest='delete_group', action='store_true')
        parser_group.add_argument(
            '--completed',
            '-c',
            dest='get_group',
            nargs=0,
            action=set_value(STATES.COMPLETED),
        )
        parser_group.add_argument('--add', '-a', action='store')
        parser_group.add_argument("--preset", "-p", action="store_true", dest="preset_group")
