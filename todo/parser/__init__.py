import argparse

from todo.parser.subparsers import (
    AddGroupParser,
    AddTodoParser,
    GroupParser,
    ListGroupsParser,
    ListTodosParser,
    TodoParser,
)
from todo.renderers import RenderHelp


class Parser:
    """
    usage: td {add,add_group,[id],group,list,list_groups} ...

    positional arguments:
      {...}                 commands
        add (a)             add todo
        add_group (ag)      add group
        [id]                todo commands
        group (g)           group commands
        list (l)            list todos       *DEFAULT*
        list_groups (lg)    list groups

    optional arguments:
      -h, --help            show this help message and exit

    `td` defaults to `td list`
    """

class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.print_help = self._print_help
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

    def _print_help(self):
        RenderHelp(self.__doc__).render()

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
