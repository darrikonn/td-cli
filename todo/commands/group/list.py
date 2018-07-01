from todo.commands.base import Command


class List(Command):
    def run(self):
        groups = self.service.group.get_all()
        print(groups)
