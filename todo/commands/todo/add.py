from sqlite3 import Error

from todo.commands.base import Command
from todo.exceptions import TodoException
from todo.renderers import RenderOutput
from todo.settings import config
from todo.utils import get_user_input


class Add(Command):
    def run(self, args):
        try:
            if args.edit:
                details = get_user_input(config["editor"])
            else:
                details = args.details or args.name

            if args.group is None:
                group = self.service.group.get_active_group()
            else:
                group = self.service.group.get(args.group)
            todo_id = self.service.todo.add(args.name, details, group[0], completed=args.state)

            RenderOutput("Created todo {bold}{todo_id}").render(todo_id=todo_id)
        except Error as e:
            raise TodoException("Error occurred, could not create a new todo", e)
