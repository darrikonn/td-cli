import os
from collections import namedtuple


class VerticalTracker:
    __slots__ = ("_rows", "_todos", "_group", "_current_pos", "_cursor", "_deleted_todos")

    PADDING = 15

    Group = namedtuple("Group", ("name", "items", "uncompleted", "completed"))
    Todo = namedtuple("Todo", ("id", "name", "details", "completed"))

    def __init__(self, todos, group):
        _, rows = os.get_terminal_size()
        start_pos = 0 if len(todos) > 0 else -1
        self._rows = rows - self.PADDING
        self._todos = todos
        self._group = group
        self._current_pos = start_pos
        self._cursor = start_pos
        self._deleted_todos = set()

    @property
    def _current_todo(self):
        return self._todos[self._current_pos]

    @property
    def todos_count(self):
        return len(self._todos)

    @property
    def todos(self):
        start_pos = self._current_pos - self._cursor
        return self._todos[start_pos : (start_pos + self._rows)]

    @property
    def current_todo(self):
        if self.todos_count > 0:
            return self.Todo(*self._current_todo)
        return self.Todo(*((None,) * len(self.Todo._fields)))

    @property
    def group(self):
        return self.Group(*self._group)

    @property
    def commands_offset(self):
        return min(self._rows, self.todos_count)

    @property
    def index(self):
        return self._cursor

    @property
    def rows(self):
        return self._rows

    def is_deleted(self, id):
        return id in self._deleted_todos

    def move_down(self):
        self._current_pos += 1
        if self._current_pos == self.todos_count:  # on last todo
            self._cursor = 0
            self._current_pos = 0
        elif not (self._cursor + 2 == self._rows and self._current_pos != self.todos_count - 1):
            self._cursor += 1

    def move_up(self):
        self._current_pos -= 1
        if self._current_pos < 0:
            self._cursor = self.commands_offset - 1
            self._current_pos = self.todos_count - 1
        elif not (self._cursor - 1 == 0 and self._current_pos != 0):
            self._cursor -= 1

    def recover(self):
        self._deleted_todos.discard(self._current_todo[0])
        if self._current_todo[3]:
            self._group = (self._group[0], self._group[1] + 1, self._group[2], self._group[3] + 1)
        else:
            self._group = (self._group[0], self._group[1] + 1, self._group[2] + 1, self._group[3])

    def toggle(self, todo_service):
        # toggle todo
        if self._current_todo[3]:
            # uncomplete todo
            todo_service.uncomplete(self._current_todo[0])
            self._group = self._group[:2] + (self._group[2] + 1, self._group[3] - 1)
        else:
            # complete todo
            todo_service.complete(self._current_todo[0])
            self._group = self._group[:2] + (self._group[2] - 1, self._group[3] + 1)
        # update list
        self._todos[self._current_pos] = self._current_todo[:3] + (not self._current_todo[3],)

    def add(self, todo):
        # add empty line
        self._current_pos += 1
        self._todos = self._todos[: self._current_pos] + [todo] + self._todos[self._current_pos :]
        if self._cursor + 2 < self._rows:
            self._cursor += 1

    def remove(self):
        self._todos = self._todos[: self._current_pos] + self._todos[self._current_pos + 1 :]
        self._current_pos -= 1
        if self._cursor + 2 < self._rows:
            self._cursor -= 1

    def update(self, name, todo_service):
        id = todo_service.add(name, name, self._group[0], False)
        self._todos[self._current_pos] = (id, name, name, False)
        self._group = (self._group[0], self._group[1] + 1, self._group[2] + 1, self._group[3])

    def edit(self, new_name, todo_service):
        if new_name is not None:
            todo_service.edit_name(self._current_todo[0], new_name)
            self._todos[self._current_pos] = (self._current_todo[0], new_name) + self._current_todo[
                2:
            ]

    def mark_deleted(self):
        self._deleted_todos.add(self._current_todo[0])
        if self._current_todo[3]:
            self._group = (self._group[0], self._group[1] - 1, self._group[2], self._group[3] - 1)
        else:
            self._group = (self._group[0], self._group[1] - 1, self._group[2] - 1, self._group[3])

    def delete_todos(self, todo_service):
        for deleted_todo in self._deleted_todos:
            todo_service.delete(deleted_todo)
