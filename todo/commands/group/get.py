from todo.commands.base import Command
from todo.renderers import RenderOutput, RenderOutputWithTextwrap


class STATES:
    COMPLETED = "completed"
    UNCOMPLETED = "uncompleted"


class Get(Command):
    arguments = (STATES.COMPLETED, STATES.UNCOMPLETED)

    def run(self, state, name):
        group = self._get_group_or_raise(name)
        completed_todos = self.service.todo.get_all(group[0], completed=True)
        uncompleted_todos = self.service.todo.get_all(group[0])
        todos = completed_todos if state == STATES.COMPLETED else uncompleted_todos

        RenderOutput("{subsequent_indent}{bold}{blue}{group_name}{reset}\n").render(
            subsequent_indent=" " * 8, group_name=group[0] or "global"
        )

        for todo in todos:
            RenderOutputWithTextwrap("{bold}{todo_id}{reset}  ", "{name}").render(name=todo[1], todo_id=todo[0])

        completed = len(completed_todos)
        uncompleted = len(uncompleted_todos)
        RenderOutput("{prefix}{grey}{items} items: {completed} completed, {uncompleted} uncompleted").render(
            prefix="\n" if len(todos) > 0 else "",
            items=completed + uncompleted,
            completed=completed,
            uncompleted=uncompleted,
        )
