from sqlite3 import Error

from todo.commands.base import Command


class Delete(Command):
    def run(self, name, skip_prompt=False):
        try:
            group = self._get_group_or_raise(name)
            if group[0] is None:
                raise Exception('Cannot delete group global')
            if not skip_prompt:
                completed_todos = self.service.todo.get_all(*group, completed=True)
                uncompleted_todos = self.service.todo.get_all(*group)
                todo_count = len(completed_todos) + len(uncompleted_todos)
                if todo_count > 0:
                    print("By deleting {}, you'll also delete {} todo{} in that group".format(
                        name, todo_count, 's' if todo_count > 1 else '')
                    )
                choice = input(
                    '[?] Are you sure you want to delete group \033[34m{}\033[37m? [Y|n] '.format(group[0])
                ).lower()
                if choice not in ('y', 'yes', ''):
                    raise Exception('Abort!')
            self.service.group.delete(group[0])
            print(u'[-] {} deleted'.format(group[0]))
        except Error as e:
            print(u'[*] Could not delete a group due to "{}"'.format(e))
