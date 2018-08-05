import argparse

from todo.parsers.group import GroupParser
from todo.parsers.groups import GroupsParser
from todo.parsers.todo import TodoParser
from todo.parsers.todos import TodosParser


class UsageError(Exception):
    pass


class Parser:
    def __init__(self, args):
        parser = argparse.ArgumentParser()

        parser.add_argument('command', nargs='?')
        parser.add_argument('argument', nargs='?')
        command_root, _ = parser.parse_known_args(args[:1])
        argument_root, _ = parser.parse_known_args(args[:2])

        self.args = args
        self.parser = self._get_root_parser(command_root.command, argument_root.argument)

    def _get_root_parser(self, command, argument):
        if command is None:
            return TodosParser(command)
        elif command == "group":
            if argument is None:
                return GroupsParser(command)
            return GroupParser(command)
        try:
            if int(command, 16) and len(command) <= 6:
                return TodoParser(command)
        except ValueError:
            pass
        raise UsageError('Unknown command "todo {}"'.format(' '.join(self.args)))

    def _get_arguments(self, args):
        return {k: v for k, v in vars(args).items() if k in self.parser.arguments}

    def _get_commands(self, args):
        return {k: v for k, v in vars(args).items() if v and k not in self.parser.arguments}

    def parseopts(self):
        opts = self.parser.parseopts(self.args)
        return (self._get_arguments(opts), self._get_commands(opts))
