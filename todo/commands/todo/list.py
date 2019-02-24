from todo.commands.base import Command
from todo.exceptions import TodoException
from todo.renderers import RenderOutput, RenderOutputWithTextwrap
from todo.utils import singular_or_plural

from .list_interactive import ListInteractive


class List(Command):
    def run(self, args):
        if args.interactive:
            return ListInteractive(self.service).run(args)

        if args.group is None:
            group = self.service.group.get_active_group()
        else:
            group = self.service.group.get(args.group)

        if group is None:
            raise TodoException("<Group: {name}> not found".format(name=args.group))

        todos = self.service.todo.get_all(group[0], args.state)

        RenderOutput("{subsequent_indent}{bold}{blue}{group_name}{reset}\n").render(
            subsequent_indent=" " * 4, group_name=group[0] or "global"
        )

        for todo in todos:
            RenderOutputWithTextwrap("{completed} {bold}{todo_id}{reset}: ", "{name}").render(
                completed="✓" if todo[3] else "x", name=todo[1], todo_id=todo[0]
            )

        RenderOutput(
            "{prefix}{grey}{items} item{singular_or_plural}: {completed} completed, {uncompleted} left"
        ).render(
            prefix="\n" if group[1] > 0 else "",
            items=group[1],
            singular_or_plural=singular_or_plural(group[1]),
            uncompleted=group[2],
            completed=group[3],
        )
