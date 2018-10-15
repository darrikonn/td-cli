from abc import ABC, abstractmethod

from todo.exceptions import TodoException


class Command(ABC):
    def __init__(self, service):
        self.service = service

    def _get_todo_or_raise(self, id):
        group = self.service.group.get_active_group()
        todo = self.service.todo.get(id, group[0])
        if todo is None:
            raise TodoException("{bold}<Todo: %s>{reset} not found" % id)

        return todo

    def _get_group_or_raise(self, name):
        group = self.service.group.get(name)
        if group is None and name != "global":
            raise TodoException("<Group: {name}> not found".format(name=name))

        return group

    @abstractmethod
    def run(self, *args, **kwargs):
        pass
