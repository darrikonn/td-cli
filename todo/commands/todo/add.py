from sqlite3 import Error

from todo.commands.base import Command
from todo.renderers import RenderOutput
from todo.settings import config
from todo.utils import get_user_input


class Add(Command):
    def is_valid_argument(self, arg):
        return bool(arg)

    def run(self, name, group_name, edit_details=None):
        try:
            if edit_details:
                details = get_user_input(config["editor"])
            else:
                details = name

            if group_name is None:
                group = self.service.group.get_active_group()
            else:
                group = self.service.group.get(group_name)
            todo_id = self.service.todo.add(name, details, group[0])

            RenderOutput("Created todo {bold}{todo_id}").render(todo_id=todo_id)
        except Error as e:
            print(u'[*] Could not add a todo due to "{}"'.format(e))
