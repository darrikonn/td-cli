from todo.commands.base import Command
from todo.commands.group import Get as GetGroup


class List(Command):
    def run(self, state, group_name):
        if group_name is None:
            group = self.service.group.get_active_group()
        else:
            group = self.service.group.get(group_name)
        GetGroup.run(self, state or False, group[0])
