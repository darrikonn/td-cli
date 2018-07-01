from sqlite3 import Error

from todo.commands.base import Command


class Complete(Command):
    def run(self, id):
        try:
            todo = self._get_todo_or_raise(id)
            self.service.todo.complete(todo[0])
            print(u'[*] {} completed'.format(todo[0]))
        except Error as e:
            print(u'[*] Could not complete a todo due to "{}"'.format(e))
