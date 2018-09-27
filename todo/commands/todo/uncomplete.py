from sqlite3 import Error

from todo.commands.base import Command
from todo.exceptions import TodoException
from todo.renderers import RenderOutput


class Uncomplete(Command):
    def run(self, args):
        try:
            todo = self._get_todo_or_raise(args.id)
            self.service.todo.uncomplete(todo[0])
            RenderOutput("{bold}{red}x {reset}{todo_id}{normal}: {name}").render(
                todo_id=todo[0], name=todo[2]
            )
        except Error as e:
            raise TodoException("Error occurred, could not uncomplete <Todo: %s>" % args.id, e)
