from sqlite3 import Error, IntegrityError

from todo.commands.base import Command
from todo.exceptions import TodoException
from todo.renderers import RenderOutput


class Add(Command):
    def run(self, args):
        try:
            group_name = self.service.group.add(args.name)

            RenderOutput("Created group {blue}{group_name}").render(group_name=group_name)
        except IntegrityError as e:
            raise TodoException("`{bold}<Group: %s>{reset}` already exists." % args.name, e)
        except Error as e:
            raise TodoException("Error occurred, could not create a new group", e)
