#!/usr/bin/python3

import sys

if sys.version_info < (3,):
    sys.exit("Sorry, td-cli only supports Python >= 3")


def main(args=None):
    from todo.commands import Commands
    from todo.exceptions import TodoException
    from todo.parser import Parser
    from todo.renderers import RenderError

    if args is None:
        args = sys.argv[1:]
    verbose = any(verbose in args for verbose in ("--verbose", "-v"))

    try:
        command, arguments = Parser().parseopts(args)
        Commands(command).run(arguments)
    except TodoException as exc:
        RenderError(exc.message, exc.details, verbose, exc.type).render()
    except Exception as exc:
        RenderError(
            "An unknown error occurred when running `{bold}{command}{reset}`",
            exc,
            verbose,
            "Exception",
        ).render(command=("td " + " ".join(args)).strip())
