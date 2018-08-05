from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self, service):
        self.service = service

    def _get_todo_or_raise(self, id):
        todo = self.service.todo.get(id)
        if todo is None:
            raise Exception("not found")

        return todo

    def _get_group_or_raise(self, name):
        group = self.service.group.get(name)
        if group is None and name != "global":
            raise Exception("not found")

        return group

    @abstractmethod
    def run(self, *args, **kwargs):
        pass
