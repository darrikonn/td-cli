from sqlite3 import Error

from todo.commands.base import Command
from todo.exceptions import TodoException
from todo.renderers import RenderOutput
from todo.settings import config
from todo.utils import get_user_input


class Edit(Command):
    def run(self, args):
        try:
            todo = self._get_todo_or_raise(args.id)
            if not (args.name or args.details or args.group):
                details = get_user_input(config["editor"], str.encode(todo[3]))
                self.service.todo.edit_details(todo[0], details)
            else:
                if args.group:
                    group = self._get_group_or_raise(args.group)
                    self.service.todo.set_group(todo[0], group[0])
                if args.name:
                    self.service.todo.edit_name(todo[0], args.name)
                if args.details:
                    self.service.todo.edit_details(todo[0], args.details)

            RenderOutput("Edited {bold}{todo_id}{reset}: {name}").render(
                todo_id=todo[0], name=args.name or todo[2]
            )
        except Error as e:
            raise TodoException("Error occurred, could not edit <Todo: %s>" % args.id, e)
