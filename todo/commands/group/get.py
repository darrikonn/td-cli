from todo.commands.base import Command
from todo.renderers import RenderOutput, RenderOutputWithTextwrap


class Get(Command):
    def run(self, state, name):
        group = self._get_group_or_raise(name)
        todos = self.service.todo.get_all(group[0], state)

        RenderOutput("{subsequent_indent}{bold}{blue}{group_name}{reset}\n").render(
            subsequent_indent=" " * 8, group_name=group[0] or "global"
        )

        for todo in todos:
            RenderOutputWithTextwrap("{bold}{todo_id}{reset}  ", "{name}").render(name=todo[1], todo_id=todo[0])

        RenderOutput("{prefix}{grey}{items} items: {completed} completed, {uncompleted} uncompleted").render(
            prefix="\n" if group[1] > 0 else "",
            items=group[1],
            uncompleted=group[2],
            completed=group[3],
        )
