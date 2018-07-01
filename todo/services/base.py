from abc import ABC, abstractmethod


class BaseService(ABC):
    __slots__ = ('connection', 'cursor')

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    @abstractmethod
    def initialise_table(self):
        pass
