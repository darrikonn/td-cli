from sqlite3 import Error

from todo.commands.base import Command
from todo.renderers import RenderInput, RenderOutputWithTextwrap


class Delete(Command):
    def run(self, id, skip_prompt=False):
        try:
            todo = self._get_todo_or_raise(id)
            if not skip_prompt:
                choice = RenderInput(
                    "[?] Are you sure you want to delete todo {bold}{todo_id}{normal}? [Y|n]"
                ).render(todo_id=todo[0])
                if choice not in ("", "y", "ye", "yes"):
                    raise Exception("Abort!")
            self.service.todo.delete(todo[0])

            RenderOutputWithTextwrap(
                "{red}Deleted{reset} {bold}{todo_id}{reset}: ", "{name}"
            ).render(name=todo[2], todo_id=todo[0], subsequent_indent=" " * 7)
        except Error as e:
            print(u'[*] Could not delete a todo due to "{}"'.format(e))
