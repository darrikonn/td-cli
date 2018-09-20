import argparse

from todo.parsers.add_group import AddGroupParser
from todo.parsers.add_todo import AddTodoParser
from todo.parsers.todo import TodoParser
from todo.parsers.group import GroupParser
from todo.parsers.list_groups import ListGroupsParser
from todo.parsers.list_todos import ListTodosParser


class UsageError(Exception):
    pass


class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("command", nargs="?")

    _subparsers = {
        "a": AddTodoParser,
        "add": AddTodoParser,
        "add_group": AddGroupParser,
        "ag": AddGroupParser,
        "g": GroupParser,
        "group": GroupParser,
        "groups": ListGroupsParser,
        "gs": ListGroupsParser,
    }

    def _get_parser(self, args):
        command = self.parser.parse_known_args(args[:1])[0].command
        if command is None:
            return ListTodosParser()
        elif command.isdigit() and len(command) <= 6:
            return TodoParser()

        parser = self._subparsers.get(command)
        if parser is None:
            raise UsageError('Unknown command "todo {}"'.format(" ".join(args)))

        return parser(command)

    def parseopts(self, args):
        parser = self._get_parser(args)
        return parser.parseopts(args)
