from sqlite3 import Error

from todo.commands.base import Command


class Uncomplete(Command):
    def run(self, id):
        try:
            todo = self._get_todo_or_raise(id)
            self.service.todo.uncomplete(todo[0])
            print(u'[*] {} uncompleted'.format(todo[0]))
        except Error as e:
            print(u'[*] Could not uncomplete a todo due to "{}"'.format(e))
