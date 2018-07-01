from todo.parsers.base import BaseParser


class GroupsParser(BaseParser):
    has_command_prefix = True

    def _normalize(self, parsed_args):
        if not parsed_args.add_group:
            setattr(parsed_args, 'list_groups', True)
        return parsed_args

    def _add_arguments(self):
        self.parser.add_argument('--add', '-a', dest='add_group', action='store')
