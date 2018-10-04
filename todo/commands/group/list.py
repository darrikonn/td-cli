from todo.commands.base import Command
from todo.renderers import RenderOutput
from todo.utils import interpret_state, singular_or_plural


class List(Command):
    def run(self, args):
        groups = self.service.group.get_all(args.state)
        if not groups:
            return RenderOutput("No{state} {bold}{blue}groups{reset} exist").render(
                state=interpret_state(args.state)
            )

        for group in groups:
            RenderOutput(
                "{bold}{blue}{group_name}{reset}: {items} item{singular_or_plural}: "
                "{completed} completed, {uncompleted} left"
            ).render(
                group_name=group[0],
                items=group[1],
                singular_or_plural=singular_or_plural(group[1]),
                uncompleted=group[2],
                completed=group[3],
            )

        self._print_footer(groups)

    def _print_footer(self, groups):
        group_count = len(groups)
        summary = [res for res in zip(*groups)][2:]
        completed_groups_count = sum(1 for x in summary[0] if x == 0)

        RenderOutput(
            "\n{grey}{group_count} group{singular_or_plural}: {completed} completed, {uncompleted} left"
        ).render(
            group_count=group_count,
            singular_or_plural=singular_or_plural(group_count),
            completed=completed_groups_count,
            uncompleted=group_count - completed_groups_count,
        )
