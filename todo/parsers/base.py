import argparse
from abc import ABCMeta, abstractproperty


def set_value(value):
    class Action(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            setattr(args, self.dest, value)

    return Action


class BaseParser:
    __metaclass__ = ABCMeta

    @abstractproperty
    def command(self):
        raise NotImplementedError

    def __init__(self, command=None):
        self.root_parser = argparse.ArgumentParser()
        if command is None:
            self.parser = self.root_parser
        else:
            self.parser = self.root_parser.add_subparsers().add_parser(command)

    def _add_arguments(self):
        pass

    def parseopts(self, args):
        self._add_arguments()
        parsed_args = self.root_parser.parse_args(args)
        return (getattr(parsed_args, "command", None) or self.command, parsed_args)
