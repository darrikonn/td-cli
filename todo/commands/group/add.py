from sqlite3 import Error

from todo.commands.base import Command
from todo.renderers import RenderOutput


class Add(Command):
    def run(self, args):
        try:
            group_name = self.service.group.add(args.name)

            RenderOutput("Created group {blue}{group_name}").render(
                group_name=group_name
            )
        except Error as e:
            print('[*] Could not add a group due to "{}"'.format(e))
