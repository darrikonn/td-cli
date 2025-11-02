from abc import ABC, abstractmethod

from todo.exceptions import TodoException


class Command(ABC):
    def __init__(self, service):
        self.service = service

    def _get_todo_or_raise(self, id):
        group = self.service.group.get_active_group()
        todos = self.service.todo.get_all_matching(id, group[0])
        if not todos:
            raise TodoException("{bold}<Todo: %s>{reset} not found" % id)
        if len(todos) > 1:
            raise TodoException(
                "{bold}<Todo: %s>{reset} matches multiple todos. Please provide a more specific ID."
                % id
            )

        return todos[0]

    def _get_group_or_raise(self, name):
        group = self.service.group.get(name)
        if group is None and name != "global":
            raise TodoException("<Group: {name}> not found".format(name=name))

        return group

    @abstractmethod
    def run(self, *args, **kwargs):
        pass
