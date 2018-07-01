from todo.commands.base import Command
from todo.utils import Fore, Style, singular_or_plural


class List(Command):
    def run(self):
        groups = self.service.group.get_all()
        for group in groups:
            print(
                "{bold}{blue}{name}{reset}: {items} item{postfix}: {completed} completed, {uncompleted} left".format(
                    name=group[0],
                    items=group[1],
                    postfix=singular_or_plural(group[1]),
                    completed=group[2],
                    uncompleted=group[3],
                    blue=Fore.BLUE,
                    bold=Style.BOLD,
                    reset=Style.RESET_ALL,
                )
            )

        self._print_footer(groups)

    def _print_footer(self, groups):
        group_count = len(groups)
        summary = [res for res in zip(*groups)][2:]
        print(
            "\n{info}{groups} group{postfix}: {completed} completed, {uncompleted} left".format(
                groups=group_count,
                postfix=singular_or_plural(group_count),
                completed=sum(summary[0]),
                uncompleted=sum(summary[1]),
                info=Fore.INFO,
            )
        )
