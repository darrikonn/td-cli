from __future__ import absolute_import

from todo.services.base import BaseService
from todo.utils import generate_random_hex


class TodoService(BaseService):
    def initialise_table(self):
        self.cursor.execute(
            """
            CREATE TABLE todo(
                id TEXT PRIMARY KEY NOT NULL,
                created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                title TEXT NOT NULL,
                description TEXT,
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
    def add(self, title, description, group):
        id = generate_random_hex()
        self.cursor.execute(
            """
            INSERT INTO todo (id, title, description, group_name)
            VALUES (?, ?, ?, ?);
            """,
            (id, title, description, group)
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
            (id, )
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
            (id, )
        )
        self.connection.commit()

    def uncomplete(self, id):
        self.cursor.execute(
            """
            UPDATE todo
            SET completed = 0
            WHERE id = ?;
            """,
            (id, )
        )
        self.connection.commit()

    def edit_description(self, id, description):
        self.cursor.execute(
            """
            UPDATE todo
            SET description = ?
            WHERE id = ?;
            """,
            (description, id)
        )
        self.connection.commit()

    def edit_title(self, id, title):
        self.cursor.execute(
            """
            UPDATE todo
            SET title = ?
            WHERE id = ?;
            """,
            (title, id)
        )
        self.connection.commit()

    # GET
    def get(self, id):
        self.cursor.execute(
            """
            SELECT id, title, description
            FROM todo
            WHERE id LIKE ('%' || ? || '%');
            """,
            (id, )
        )
        return self.cursor.fetchone()

    def get_all(self, group=None, completed=False):
        self.cursor.execute(
            """
            SELECT id, title
            FROM todo
            WHERE completed = ? AND
                  (group_name = ? OR ? IS NULL)
            ORDER BY modified DESC;
            """,
            (completed, group, group)
        )
        return self.cursor.fetchall()
