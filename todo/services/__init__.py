import os
import sqlite3
from pathlib import Path
from urllib.request import pathname2url

from todo.settings import config

from .group import GroupService
from .todo import TodoService


class Service:
    __slots__ = ("connection", "cursor")

    service_dict = {"todo": TodoService, "group": GroupService}

    def __init__(self):
        db_uri = "file:{}".format(pathname2url(self._get_database_path()))

        try:
            self.connection = sqlite3.connect("{}?mode=rw".format(db_uri), uri=True)
            self.cursor = self.connection.cursor()
        except sqlite3.OperationalError:
            self._initialise_database(db_uri)
        self._link_services()

        self.cursor.execute("PRAGMA foreign_keys = ON")

    def _get_database_path(self):
        return os.path.expanduser(Path("~/.{}.db".format(config["database_name"])))

    def _initialise_database(self, db_uri):
        self.connection = sqlite3.connect(db_uri, uri=True)
        self.cursor = self.connection.cursor()
        for _, cls in self.service_dict.items():
            cls.initialise_table(self)
        self.connection.commit()

    def _link_services(self):
        for prop, service in self.service_dict.items():
            setattr(Service, prop, service(self.connection, self.cursor))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            return False
        self.connection.close()
