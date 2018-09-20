#!/usr/bin/python3

import sys

from todo.parsers import Parser
from todo.commands import Commands


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    command, arguments = Parser().parseopts(args)

    Commands(command).run(arguments)
