from sqlite3 import Error

from todo.commands.base import Command
from todo.renderers import RenderOutput


class EditName(Command):
    def run(self, name, id):
        try:
            todo = self._get_todo_or_raise(id)
            self.service.todo.edit_name(todo[0], name)

            RenderOutput("Named {bold}{todo_id}{reset} to: {name}").render(todo_id=todo[0], name=name)
        except Error as e:
            print(u'[*] Could not edit a todo due to "{}"'.format(e))
