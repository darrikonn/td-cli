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
        raise UsageError('Unknown command "todo {}"'.format(" ".join(self.args)))

    def parseopts(self):
        return self.parser.parseopts(self.args)
