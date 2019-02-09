from sqlite3 import Error

from todo.commands.base import Command
from todo.exceptions import TodoException
from todo.renderers import RenderInput, RenderOutput, RenderOutputWithTextwrap


class Delete(Command):
    def run(self, args):
        try:
            todo = self._get_todo_or_raise(args.id)
            if not args.skip_prompt:
                choice = RenderInput(
                    "[?] Are you sure you want to delete todo {bold}{todo_id}{normal}? [Y|n] "
                ).render(todo_id=todo[0])
                if choice not in ("", "y", "ye", "yes"):
                    return RenderOutput("Abort!").render()
            self.service.todo.delete(todo[0])

            RenderOutputWithTextwrap(
                "{red}Deleted{reset} {bold}{todo_id}{reset}: ", "{name}"
            ).render(name=todo[2], todo_id=todo[0], subsequent_indent=" " * 16)
        except Error as e:
            raise TodoException("Error occurred, could not delete <Todo: %s>" % args.id, e)
