import argparse


def set_value(value):
    class Action(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            setattr(args, self.dest, value)
    return Action


class BaseParser:
    arguments = tuple()
    has_command_prefix = False

    def __init__(self, command):
        self._parser = argparse.ArgumentParser()
        if self.has_command_prefix:
            self.parser = self._parser.add_subparsers().add_parser(command)
        else:
            self.parser = self._parser

        for arg in self.arguments:
            self.parser.add_argument(arg)

    def _add_arguments(self):
        pass

    def _normalize(self, parsed_args):
        return parsed_args

    def parseopts(self, args):
        self._add_arguments()
        return self._normalize(self._parser.parse_args(args))
