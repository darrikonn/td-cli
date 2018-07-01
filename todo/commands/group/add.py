from sqlite3 import Error

from todo.commands.base import Command


class Add(Command):
    def is_valid_argument(self, arg):
        return bool(arg)

    def run(self, name):
        try:
            group_name = self.service.group.add(name)
            print(u'[*] Added group "{}"'.format(group_name))
        except Error as e:
            print(u'[*] Could not add a group due to "{}"'.format(e))
