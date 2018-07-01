from todo.parsers.base import BaseParser


class ConfigParser(BaseParser):
    arguments = ('name', )
    has_command_prefix = True

    def _normalize(self, parsed_args):
        setattr(parsed_args, 'use_group', True)
        return parsed_args

    def _add_arguments(self):
        self.parser.add_argument('--create', '-c', action='store_true')
