from todo.commands.base import Command
from todo.commands.group import Get as GetGroup


class STATES:
    COMPLETED = "completed"
    UNCOMPLETED = "uncompleted"


class List(Command):
    arguments = (STATES.COMPLETED, STATES.UNCOMPLETED)

    def run(self, state):
        active_group = self.service.group.get_active_group()
        GetGroup.run(self, state, *active_group)
