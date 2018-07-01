from sqlite3 import Error

from todo.commands.base import Command
from todo.utils import get_user_input


class Edit(Command):
    def run(self, id):
        try:
            todo = self._get_todo_or_raise(id)
            description = get_user_input('nvim', str.encode(todo[2]))
            self.service.todo.edit_description(todo[0], description)
            print(u'[*] {} edited'.format(todo[0]))
        except Error as e:
            print(u'[*] Could not edit a todo due to "{}"'.format(e))
