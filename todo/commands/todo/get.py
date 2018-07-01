from sqlite3 import Error

from todo.commands.base import Command


class Get(Command):
    def run(self, id):
        try:
            todo = self._get_todo_or_raise(id)
            print(todo[2])
        except Error as e:
            print(u'[*] Could not get a todo due to "{}"'.format(e))
