import sys

from todo.parsers.base import BaseParser


class TodoParser(BaseParser):
    arguments = ('id', )

    def _normalize(self, parsed_args):
        if len(sys.argv[1:]) == 1:
            setattr(parsed_args, 'get_todo', True)
        return parsed_args

    def _add_arguments(self):
        self.parser.add_argument('--yes', '-y', action='store_true')

        parser_group_1 = self.parser.add_mutually_exclusive_group()
        parser_group_1.add_argument('--complete', '-c', dest='complete_todo', action='store_true')
        parser_group_1.add_argument('--uncomplete', '-u', dest='uncomplete_todo', action='store_true')

        parser_group_2 = self.parser.add_mutually_exclusive_group()
        parser_group_2.add_argument('--delete', dest='delete_todo', action='store_true')
        parser_group_2.add_argument('--name', '-n', dest='name_todo', action='store')
        parser_group_2.add_argument('--edit', '-e', dest='edit_todo', action='store_true')
