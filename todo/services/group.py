from todo.exceptions import TodoException
from todo.services.base import GLOBAL, BaseService
from todo.settings import config, get_git_project_config


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
            raise TodoException("`{bold}<Group: %s>{reset}` already exists." % GLOBAL)

        self.cursor.execute(
            """
            INSERT INTO "group" (name)
            VALUES (?);
            """,
            (group_name,),
        )
        self.connection.commit()
        return group_name

    # DELETE
    def delete(self, name):
        group_name = self._interpret_group_name(name)
        if group_name is None:
            raise TodoException("`{bold}<Group: %s>{reset}` can't be deleted." % GLOBAL)
        self.cursor.execute(
            """
            DELETE FROM "group"
            WHERE name = ?;
            """,
            (group_name,),
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
            (self._interpret_group_name(new_name), self._interpret_group_name(old_name)),
        )
        self.connection.commit()

    def use(self, name):
        group = self.get(name)

        if group is None:
            raise TodoException("<Group: {name}> not found".format(name=name))

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
            (group[0],),
        )
        self.connection.commit()

    # GET
    def get(self, name):
        group_name = self._interpret_group_name(name)
        if group_name is None:
            group = (None,)
        else:
            group = self.cursor.execute(
                """
                SELECT IFNULL(?, ?)
                FROM "group"
                WHERE name = ? OR ? IS NULL;
                """,
                (group_name, GLOBAL, group_name, group_name),
            ).fetchone()
            if group is None:
                return None

        self.cursor.execute(
            """
            SELECT COUNT(id) AS items,
               COALESCE(SUM(completed = 0), 0) AS uncompleted,
               COALESCE(SUM(completed = 1), 0) AS completed
            FROM todo
            WHERE group_name = ? OR ? IS NULL;
            """,
            (group_name, group_name),
        )
        return group + self.cursor.fetchone()

    def get_active_group(self):
        if config["group"]:
            group = self.get(config["group"])
            if group is None:
                raise TodoException(
                    "{bold}<Group: %s>{reset} does not exist, falling back to currently active group"
                    % config["group"],
                    "Your config file at {bold}%s{reset} tries to\noverride the "
                    % (get_git_project_config() or "~")
                    + "default group with `{bold}%s{reset}`, but " % config["group"]
                    + "{bold}<Group: %s>{reset} does not exist." % config["group"],
                    "WARNING",
                )
            return group
        self.cursor.execute(
            """
            SELECT name
            FROM "group"
            WHERE in_use = 1;
            """
        )
        active_group = self.cursor.fetchone() or (None,)
        return self.get(*active_group)

    def get_all(self, completed=None):
        self.cursor.execute(
            """
            SELECT IFNULL(todos.group_name, 'UNGROUPED'), todos.items, todos.uncompleted, todos.completed
            FROM (
                SELECT group_name,
                   COUNT(*) as items,
                   SUM(completed = 0) as uncompleted,
                   SUM(completed = 1) as completed
                FROM todo
                GROUP BY group_name
            ) todos
            WHERE (todos.uncompleted > 0 AND ? = 0)
               OR (todos.uncompleted = 0 AND ? = 1)
               OR ? IS NULL
            UNION ALL
            SELECT g2.name, 0, 0, 0
            FROM "group" g2
            LEFT OUTER JOIN todo ON todo.group_name = g2.name
            WHERE todo.group_name IS NULL
               AND (? = 1 OR ? IS NULL);
            """,
            (completed,) * 5,
        )
        return self.cursor.fetchall()
