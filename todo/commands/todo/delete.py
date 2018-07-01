from sqlite3 import Error

from todo.commands.base import Command


class Delete(Command):
    def run(self, id, skip_prompt=False):
        try:
            todo = self._get_todo_or_raise(id)
            if not skip_prompt:
                choice = input(
                    '[?] Are you sure you want to delete todo \033[34m{}\033[37m? [Y|n] '.format('darri')
                ).lower()
                if choice not in ('y', 'yes', ''):
                    raise Exception('Abort!')
            self.service.todo.delete(todo[0])
            print(u'[-] {} deleted'.format(todo[0]))
        except Error as e:
            print(u'[*] Could not delete a todo due to "{}"'.format(e))
