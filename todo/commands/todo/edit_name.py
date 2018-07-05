from sqlite3 import Error

from todo.commands.base import Command
from todo.renderers import RenderOutput


class EditName(Command):
    def is_valid_argument(self, arg):
        return bool(arg)

    def run(self, name, id):
        try:
            todo = self._get_todo_or_raise(id)
            self.service.todo.edit_name(todo[0], name)

            RenderOutput("[*] {todo_id} named").render(todo_id=todo[0])
        except Error as e:
            print(u'[*] Could not edit a todo due to "{}"'.format(e))
