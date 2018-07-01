import textwrap
from os import get_terminal_size

from todo.commands.base import Command
from todo.utils import Fore, Style


class STATES:
    COMPLETED = "completed"
    UNCOMPLETED = "uncompleted"


class List(Command):
    arguments = (STATES.COMPLETED, STATES.UNCOMPLETED)

    def run(self, state):
        active_group = self.service.group.get_active_group()
        completed_todos = self.service.todo.get_all(*active_group, completed=True)
        uncompleted_todos = self.service.todo.get_all(*active_group)
        todos = completed_todos if state == STATES.COMPLETED else uncompleted_todos

        cols, _ = get_terminal_size()

        subsequent_indent = " " * 8
        self._print_header(active_group[0] or "global", subsequent_indent)

        for todo in todos:
            prefix = "{bold}{id}{reset}  ".format(id=todo[0], bold=Style.BOLD, reset=Style.RESET_ALL)
            wrapper = textwrap.TextWrapper(initial_indent=prefix, width=cols, subsequent_indent=subsequent_indent)
            print(wrapper.fill(todo[1]))

        self._print_footer(len(completed_todos), len(uncompleted_todos), len(todos))

    def _print_header(self, name, subsequent_indent):
        print(
            "{subsequent_indent}{bold}{blue}{name}{reset}\n".format(
                name=name, subsequent_indent=subsequent_indent, blue=Fore.BLUE, bold=Style.BOLD, reset=Style.RESET_ALL
            )
        )

    def _print_footer(self, completed, uncompleted, listed):
        print(
            "{prefix}{info}{items} items: {completed} completed, {uncompleted} uncompleted".format(
                prefix="\n" if listed > 0 else "",
                items=completed + uncompleted,
                completed=completed,
                uncompleted=uncompleted,
                info=Fore.INFO,
            )
        )
