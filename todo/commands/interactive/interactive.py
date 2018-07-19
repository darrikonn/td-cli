from todo.commands.base import Command
from todo.constants import INTERACTIVE_COMMAND as COMMAND
from todo.utils.menu import Menu


class Interactive(Command):
    def run(self):
        active_group = self.service.group.get_active_group()
        completed_todos = self.service.todo.get_all(*active_group, completed=True)
        uncompleted_todos = self.service.todo.get_all(*active_group)
        completed = len(completed_todos)
        uncompleted = len(uncompleted_todos)
        completed_count = completed
        uncompleted_count = uncompleted

        with Menu() as menu:
            menu.clear()
            menu.render_header("{group_name}".format(group_name=active_group[0] or "global"))

            current_pos = 0
            while True:
                menu.refresh()
                menu.render_subheader(
                    "{items} items: {completed} completed, {uncompleted} left".format(
                        items=completed + uncompleted, completed=completed_count, uncompleted=uncompleted_count
                    )
                )

                for index, todo in enumerate(uncompleted_todos):
                    menu.render_todo(todo, index, current_pos)

                menu.render_commands(uncompleted)

                command = menu.get_command()

                if command == COMMAND.DOWN:
                    current_pos = current_pos + 1 if current_pos + 1 < uncompleted else 0
                elif command == COMMAND.UP:
                    current_pos = current_pos - 1 if current_pos > 0 else uncompleted - 1

                todo = uncompleted_todos[current_pos]
                if command == COMMAND.TOGGLE:
                    # toggle todo
                    if todo[3]:
                        # uncomplete todo
                        self.service.todo.uncomplete(todo[0])
                        completed_count -= 1
                        uncompleted_count += 1
                    else:
                        # complete todo
                        self.service.todo.complete(todo[0])
                        completed_count += 1
                        uncompleted_count -= 1
                    # update list
                    uncompleted_todos[current_pos] = todo[:3] + (not todo[3],)
                elif command == COMMAND.QUIT:
                    break
