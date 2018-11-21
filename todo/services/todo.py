from __future__ import absolute_import

from todo.services.base import BaseService
from todo.utils import generate_random_int


class TodoService(BaseService):
    def initialise_table(self):
        self.cursor.execute(
            """
            CREATE TABLE todo(
                id TEXT PRIMARY KEY NOT NULL,
                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                name TEXT NOT NULL,
                details TEXT,
                completed BOOLEAN NOT NULL DEFAULT 0,
                group_name TEXT,
                FOREIGN KEY (group_name) REFERENCES "group" (name) ON DELETE CASCADE
            );
            """
        )
        self.cursor.execute(
            """
            CREATE TRIGGER update_modify_on_todo_update AFTER UPDATE ON todo
             BEGIN
                UPDATE todo
                SET modified = datetime('now')
                WHERE id = NEW.id;
             END;
            """
        )

    # POST
    def add(self, name, details, group, completed):
        id = generate_random_int()
        group_name = self._interpret_group_name(group)
        self.cursor.execute(
            """
            INSERT INTO todo (id, name, details, group_name, completed)
            VALUES (?, ?, ?, ?, ?);
            """,
            (id, name, details, group_name, completed),
        )
        self.connection.commit()
        return id

    # DELETE
    def delete(self, id):
        self.cursor.execute(
            """
            DELETE FROM todo
            WHERE id = ?;
            """,
            (id,),
        )
        self.connection.commit()

    # PUT
    def complete(self, id):
        self.cursor.execute(
            """
            UPDATE todo
            SET completed = 1
            WHERE id = ?;
            """,
            (id,),
        )
        self.connection.commit()

    def uncomplete(self, id):
        self.cursor.execute(
            """
            UPDATE todo
            SET completed = 0
            WHERE id = ?;
            """,
            (id,),
        )
        self.connection.commit()

    def set_group(self, id, group):
        group_name = self._interpret_group_name(group)
        self.cursor.execute(
            """
            UPDATE todo
            SET group_name = ?
            WHERE id = ?;
            """,
            (group_name, id),
        )
        self.connection.commit()

    def edit_details(self, id, details):
        self.cursor.execute(
            """
            UPDATE todo
            SET details = ?
            WHERE id = ?;
            """,
            (details, id),
        )
        self.connection.commit()

    def edit_name(self, id, name):
        self.cursor.execute(
            """
            UPDATE todo
            SET name = ?
            WHERE id = ?;
            """,
            (name, id),
        )
        self.connection.commit()

    # GET
    def get(self, id, group):
        self.cursor.execute(
            """
            SELECT id, group_name, name, details, completed
            FROM todo
            WHERE id LIKE ('%' || ? || '%')
            ORDER BY group_name = ? DESC, completed, modified DESC;
            """,
            (id, group),
        )
        return self.cursor.fetchone()

    def get_all(self, group=None, completed=None):
        group_name = self._interpret_group_name(group)
        self.cursor.execute(
            """
            SELECT id, name, details, completed
            FROM todo
            WHERE (completed = ? OR ? IS NULL) AND
                  (group_name = ? OR ? IS NULL)
            ORDER BY completed, modified DESC;
            """,
            (completed, completed, group_name, group_name),
        )
        return self.cursor.fetchall()
