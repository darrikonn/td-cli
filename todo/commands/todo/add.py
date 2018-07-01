from sqlite3 import Error

from todo.commands.base import Command
from todo.utils import get_user_input


class Add(Command):
    def is_valid_argument(self, arg):
        return bool(arg)

    def run(self, title, edit_description=None):
        try:
            if edit_description:
                description = get_user_input('nvim')
            else:
                description = title

            active_group = self.service.group.get_active_group()
            todo_id = self.service.todo.add(title, description, *active_group)
            print(u'[*] Added todo "{}"'.format(todo_id))
        except Error as e:
            print(u'[*] Could not add a todo due to "{}"'.format(e))
