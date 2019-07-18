import argparse

from todo.exceptions import TodoException
from todo.parser.subparsers import (
    AddGroupParser,
    AddTodoParser,
    CountTodosParser,
    GroupParser,
    InitializeConfigParser,
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
      {...}                   commands
        add (a)               add todo
        add-group (ag)        add group
        count (c)             count todos
        [id]                  manage todo
        group (g)             manage group
        init-config (ig)      initialize config
        list (ls, l)          list todos       *DEFAULT*
        list-groups (lg, lsg) list groups

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
        "add-group": AddGroupParser,
        # count todos
        "c": CountTodosParser,
        "count": CountTodosParser,
        # get group
        "g": GroupParser,
        "group": GroupParser,
        # initialize config
        "ic": InitializeConfigParser,
        "init-config": InitializeConfigParser,
        # list groups
        "lg": ListGroupsParser,
        "lsg": ListGroupsParser,
        "list-groups": ListGroupsParser,
        # list todos
        "l": ListTodosParser,
        "ls": ListTodosParser,
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
            if command == "list_groups":
                raise TodoException(
                    "`{bold}list_groups{reset}` is deprecated, use `{bold}list-groups{reset} instead",
                    type="DeprecatedException",
                )
            if command == "add_group":
                raise TodoException(
                    "`{bold}add_group{reset}` is deprecated, use `{bold}add-group{reset} instead",
                    type="DeprecatedException",
                )

            raise TodoException(
                "Unknown command `{bold}td %s{reset}`" % " ".join(args), type="UsageError"
            )

        return parser(command)

    def parseopts(self, args):
        parser = self._get_parser(args)
        return parser.parseopts(args)
