import argparse
from abc import ABCMeta, abstractproperty

from todo.renderers import RenderHelp
from todo.utils import get_version


def set_value(value):
    class Action(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            setattr(args, self.dest, value)

    return Action


def set_default_subparser(self, name, args, positional_args):
    for arg in args:
        if arg in ["-h", "--help"]:
            break
    else:
        for x in self._subparsers._actions:
            if not isinstance(x, argparse._SubParsersAction):
                continue
            for sp_name in x._name_parser_map.keys():
                if sp_name in args:
                    return
            if len(args) < positional_args:
                return args
            return args.insert(positional_args, name)


setattr(argparse.ArgumentParser, "set_default_subparser", set_default_subparser)


class BaseParser:
    __metaclass__ = ABCMeta

    @abstractproperty
    def command(self):
        raise NotImplementedError

    def __init__(self, command=None):
        self.parent = argparse.ArgumentParser(add_help=False)
        self.parent.add_argument(
            "--verbose", "-v", dest="verbose", action="store_true", help=argparse.SUPPRESS
        )
        self.parent.add_argument(
            "--version",
            action="version",
            help=argparse.SUPPRESS,
            version="td version {version} - (C) Darri Steinn Konn Konradsson".format(
                version=get_version()
            ),
        )

        self.root_parser = argparse.ArgumentParser(parents=[self.parent])
        if command is None:
            self.parser = self.root_parser
        else:
            self.parser = self.root_parser.add_subparsers().add_parser(
                command, parents=[self.parent]
            )
        self.parser.print_help = self.print_help

    def _add_parser(self, parent, *args, **kwargs):
        parser = parent.add_parser(parents=[self.parent], *args, **kwargs)
        if "help" not in kwargs:
            parser.print_help = self.print_help
        return parser

    def _add_arguments(self):
        pass

    def _set_defaults(self, args):
        pass

    def print_help(self):
        RenderHelp(self.__doc__).render()

    def parseopts(self, args):
        self._add_arguments()
        self._set_defaults(args)
        parsed_args = self.root_parser.parse_args(args)
        return (getattr(parsed_args, "command", None) or self.command, parsed_args)
