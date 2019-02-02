from sqlite3 import Error

from todo.commands.base import Command
from todo.exceptions import TodoException
from todo.renderers import RenderOutput, RenderOutputWithTextwrap


class Get(Command):
    def run(self, args):
        try:
            todo = self._get_todo_or_raise(args.id)
            RenderOutput("{subsequent_indent}{bold}{blue}{group_name}{reset}\n").render(
                group_name=todo[1] or "UNGROUPED", subsequent_indent=" " * 4
            )

            RenderOutput("{details}").render(details=todo[3])

            RenderOutputWithTextwrap(
                "\n{grey}{completed} {bold}{todo_id}{normal}: ", "{details}"
            ).render(details=todo[2], completed="✓" if todo[4] else "x", todo_id=todo[0])
        except Error as e:
            raise TodoException(
                "Error occurred, could not get {bold}<Todo: %s>{reset}" % args.id, e
            )
