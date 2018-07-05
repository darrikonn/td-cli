from sqlite3 import Error

from todo.commands.base import Command
from todo.renderers import RenderOutput


class Add(Command):
    def is_valid_argument(self, arg):
        return bool(arg)

    def run(self, name):
        try:
            group_name = self.service.group.add(name)

            RenderOutput("Created group {blue}{group_name}").render(group_name=group_name)
        except Error as e:
            print('[*] Could not add a group due to "{}"'.format(e))
