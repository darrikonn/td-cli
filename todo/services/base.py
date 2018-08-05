from abc import ABC, abstractmethod

from todo.utils import to_lower

GLOBAL = "global"


class BaseService(ABC):
    __slots__ = ("connection", "cursor")

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    @abstractmethod
    def initialise_table(self):
        pass

    def _interpret_group_name(self, name):
        if self._is_global(name):
            return None
        return to_lower(name)

    def _is_global(self, name):
        return name is None or to_lower(name) == GLOBAL
