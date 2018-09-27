from sqlite3 import Error

from todo.commands.base import Command
from todo.exceptions import TodoException
from todo.renderers import RenderOutput


class Complete(Command):
    def run(self, args):
        try:
            todo = self._get_todo_or_raise(args.id)
            self.service.todo.complete(todo[0])

            RenderOutput("{bold}{green}✓ {reset}{bold}{todo_id}{reset}: {name}").render(
                todo_id=todo[0], name=todo[2]
            )
        except Error as e:
            raise TodoException("Error occurred, could not complete <Todo: %s>" % args.id, e)
