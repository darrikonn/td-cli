import sys

from todo.commands.todo.list import STATES
from todo.parsers.base import BaseParser, set_value


class TodosParser(BaseParser):
    def _normalize(self, parsed_args):
        if len(sys.argv[1:]) == 0:
            setattr(parsed_args, 'list_todos', STATES.UNCOMPLETED)
        elif parsed_args.interactive:
            setattr(parsed_args, 'interactive', parsed_args.list_todos or True)
            setattr(parsed_args, 'list_todos', None)
        return parsed_args

    def _add_arguments(self):
        self.parser.add_argument('--interactive', '-i', action='store_true')

        parser_group = self.parser.add_mutually_exclusive_group()
        parser_group.add_argument(
            '--completed',
            '-c',
            dest='list_todos',
            nargs=0,
            action=set_value(STATES.COMPLETED),
        )
        parser_group.add_argument(
            '--uncompleted',
            '-u',
            dest='list_todos',
            nargs=0,
            action=set_value(STATES.UNCOMPLETED),
        )
        parser_group.add_argument('--add', '-a', dest='add_todo', action='store')
