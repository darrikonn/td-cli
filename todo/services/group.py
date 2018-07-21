from todo.services.base import GLOBAL, BaseService


class GroupService(BaseService):
    def initialise_table(self):
        self.cursor.execute(
            """
            CREATE TABLE "group"(
                name TEXT PRIMARY KEY NOT NULL,
                in_use BOOLEAN NOT NULL DEFAULT 0
            );
            """
        )

    # POST
    def add(self, name):
        group_name = self._interpret_group_name(name)
        if group_name is None:
            raise Exception('"{}" is a reserved group name. You can`t create that group'.format(GLOBAL))

        self.cursor.execute(
            """
            INSERT INTO "group" (name)
            VALUES (?);
            """,
            (group_name, )
        )
        self.connection.commit()
        return group_name

    # DELETE
    def delete(self, name):
        group_name = self._interpret_group_name(name)
        if group_name is None:
            raise Exception('"{}" is a reserved group name. You can`t delete that group'.format(GLOBAL))
        self.cursor.execute(
            """
            DELETE FROM "group"
            WHERE name = ?;
            """,
            (group_name, )
        )
        self.connection.commit()

    # PUT
    def edit_name(self, new_name, old_name):
        self.cursor.execute(
            """
            UPDATE "group"
            SET name = ?
            WHERE name = ?;
            """,
            (self._interpret_group_name(new_name), self._interpret_group_name(old_name))
        )
        self.connection.commit()

    def use(self, name):
        group = self.get(name)

        if group is None:
            raise Exception('Group "{}" not found'.format(name))

        self.cursor.execute(
            """
            UPDATE "group"
            SET in_use = 0
            """
        )

        self.cursor.execute(
            """
            UPDATE "group"
            SET in_use = 1
            WHERE name = ?;
            """,
            (group[0], )
        )
        self.connection.commit()

    # GET
    def get(self, name):
        group_name = self._interpret_group_name(name)
        self.cursor.execute(
            """
            SELECT IFNULL(group_name, ?), sum(completed = False) as uncompleted, sum(completed = True) as completed
            FROM todo
            WHERE group_name = ? OR ? IS NULL;
            """,
            (GLOBAL, group_name, group_name, )
        )
        return self.cursor.fetchone()

    def get_active_group(self):
        self.cursor.execute(
            """
            SELECT name
            FROM "group"
            WHERE in_use = 1;
            """
        )
        active_group = self.cursor.fetchone() or (None, )
        return self.get(*active_group)

    def get_all(self):
        self.cursor.execute(
            """
            SELECT IFNULL(g.name, ?), todos.items, todos.completed, todos.uncompleted
            FROM (
                SELECT group_name,
                   COUNT(*) as items,
                   SUM(completed = 1) as completed,
                   SUM(completed = 0) as uncompleted
                FROM todo
                GROUP BY group_name
            ) todos
            LEFT OUTER JOIN "group" g ON todos.group_name = g.name
            UNION ALL
            SELECT g2.name, 0, 0, 0
            FROM "group" g2
            LEFT OUTER JOIN todo ON todo.group_name = g2.name
            WHERE todo.group_name IS NULL;
            """,
            (GLOBAL, )
        )
        return self.cursor.fetchall()
