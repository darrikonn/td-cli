import argparse

from todo.exceptions import TodoException
from todo.parser.subparsers import (
    AddGroupParser,
    AddTodoParser,
    GroupParser,
    ListGroupsParser,
    ListTodosParser,
    TodoParser,
)
from todo.renderers import RenderHelp
from todo.utils import docstring, get_version


@docstring(get_version())
class Parser:
    """
    usage: td {add,add_group,[id],group,list,list_groups} ...

    td-cli %s
    Darri Steinn Konn Konradsson <darrikonn@gmail.com>
    https://github.com/darrikonn/td-cli

    td-cli (td) is a command line todo manager,
    where you can organize and manage your todos across multiple projects.

    positional arguments:
      {...}                 commands
        add (a)             add todo
        add_group (ag)      add group
        [id]                manage todo
        group (g)           manage group
        list (l)            list todos       *DEFAULT*
        list_groups (lg)    list groups

    optional arguments:
      -h, --help            show this help message and exit

    `td` defaults to `td list`
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.print_help = self._print_help
        self.parser.add_argument("command", nargs="?")

    _subparsers = {
        # add todo
        "a": AddTodoParser,
        "add": AddTodoParser,
        # add group
        "ag": AddGroupParser,
        "add_group": AddGroupParser,
        # get group
        "g": GroupParser,
        "group": GroupParser,
        # list groups
        "lg": ListGroupsParser,
        "list_groups": ListGroupsParser,
        # list todos
        "l": ListTodosParser,
        "list": ListTodosParser,
    }

    def _print_help(self):
        RenderHelp(self.__doc__).render()

    def _get_parser(self, args):
        command = self.parser.parse_known_args(args[:1])[0].command
        if command is None:
            return ListTodosParser()
        if command.isdigit() and len(command) <= 6:
            return TodoParser()

        parser = self._subparsers.get(command)
        if parser is None:
            raise TodoException(
                "Unknown command `{bold}td %s{reset}`" % " ".join(args), type="UsageError"
            )

        return parser(command)

    def parseopts(self, args):
        parser = self._get_parser(args)
        return parser.parseopts(args)
