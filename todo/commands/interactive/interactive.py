from todo.commands.base import Command
from todo.constants import INTERACTIVE_COMMAND as COMMAND
from todo.utils.menu import Menu


class STATES:
    COMPLETED = "completed"
    UNCOMPLETED = "uncompleted"


class Interactive(Command):
    arguments = (STATES.COMPLETED, STATES.UNCOMPLETED)

    def run(self, state=None, group_name=None):
        if group_name is None:
            group = self.service.group.get_active_group()
        else:
            group = self.service.group.get(group_name)

        todos = self.service.todo.get_all(
            group[0],
            True if state == STATES.COMPLETED else False if state == STATES.UNCOMPLETED else None  # TODO
        )
        todos_count = len(todos)

        with Menu() as menu:
            menu.clear()
            menu.render_header("{group_name}".format(group_name=group[0]))

            current_pos = 0
            while True:
                menu.refresh()
                menu.render_subheader(
                    "{items} items: {completed} completed, {uncompleted} left".format(
                        items=todos_count, completed=group[2], uncompleted=group[1]
                    )
                )

                for index, todo in enumerate(todos):
                    menu.render_todo(todo, index, current_pos)

                menu.render_commands(todos_count)

                command = menu.get_command()

                if command == COMMAND.DOWN:
                    current_pos = current_pos + 1 if current_pos + 1 < todos_count else 0
                elif command == COMMAND.UP:
                    current_pos = current_pos - 1 if current_pos > 0 else todos_count - 1

                todo = todos[current_pos]
                if command == COMMAND.TOGGLE:
                    # toggle todo
                    if todo[3]:
                        # uncomplete todo
                        self.service.todo.uncomplete(todo[0])
                        group = group[:1] + (group[1] + 1, group[2] - 1)
                    else:
                        # complete todo
                        self.service.todo.complete(todo[0])
                        group = group[:1] + (group[1] - 1, group[2] + 1)
                    # update list
                    todos[current_pos] = todo[:3] + (not todo[3],)
                elif command == COMMAND.QUIT:
                    break
