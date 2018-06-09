import configparser
import sqlite3

from .utils import generate_random_hex


class Service(object):
    __slots__ = ('connection', 'cursor')

    def __init__(self):
        config = configparser.SafeConfigParser({'name': 'todo.db'})
        config.read('todo/todo.cfg')  # TODO: get full path
        database_name = config.get('Database', 'name')
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()
        if not self._database_is_initialized():
            self._initialise_database()

    def _database_is_initialized(self):
        table = self.cursor.execute(
            'SELECT name FROM sqlite_master WHERE type="table" AND name="todo"')
        return table.fetchone() is not None

    def _initialise_database(self):
        self.cursor.execute(
            '''CREATE TABLE todo (
                id TEXT NOT NULL PRIMARY KEY,
                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                title TEXT NOT NULL,
                description TEXT,
                completed BOOLEAN NOT NULL DEFAULT 0
            );''')
        self.cursor.execute(
            '''CREATE TRIGGER update_modify_on_todo_update AFTER UPDATE ON todo
             BEGIN
                UPDATE todo SET modified = datetime('now') WHERE id = NEW.id;
             END;
            ''')
        self.connection.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            return False
        self.connection.close()

    """ API """
    # POST
    def add_todo(self, title, description):
        id = generate_random_hex()
        self.cursor.execute('INSERT INTO todo (id, title, description) VALUES (?, ?, ?);',
                (id, title, description))
        self.connection.commit()
        return id

    # DELETE
    def delete_todo(self, id):
        self.cursor.execute('DELETE FROM todo WHERE id = ?;', (id, ))
        self.connection.commit()

    # PUT
    def complete_todo(self, id):
        self.cursor.execute('UPDATE todo SET completed = 1 WHERE id = ?;', (id, ))
        self.connection.commit()

    def uncomplete_todo(self, id):
        self.cursor.execute('UPDATE todo SET completed = 0 WHERE id = ?;', (id, ))
        self.connection.commit()

    def edit_todo(self, id, description):
        self.cursor.execute('UPDATE todo SET description = ? WHERE id = ?;', (description, id))
        self.connection.commit()

    # GET
    def get_todo(self, id):
        self.cursor.execute("SELECT id, title, description FROM todo WHERE id LIKE ('%' || ? || '%');", (id, ))
        return self.cursor.fetchone()

    def get_uncompleted_todos(self):
        self.cursor.execute('SELECT id, title FROM todo WHERE completed = 0 ORDER BY modified DESC;')
        return self.cursor.fetchall()

    def get_completed_todos(self):
        self.cursor.execute('SELECT id, title FROM todo WHERE completed = 1 ORDER BY modified DESC;')
        return self.cursor.fetchall()
