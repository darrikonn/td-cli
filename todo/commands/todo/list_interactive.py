from todo.commands.base import Command
from todo.constants import COMMAND_MODES
from todo.constants import INTERACTIVE_COMMANDS as COMMANDS
from todo.exceptions import TodoException
from todo.utils import singular_or_plural
from todo.utils.menu.vertical_tracker import VerticalTracker


class ListInteractive(Command):
    DELETE_MODE_COMMANDS = (
        COMMANDS.ADD,
        COMMANDS.QUIT,
        COMMANDS.RECOVER,
        COMMANDS.UP,
        COMMANDS.DOWN,
    )
    EMPTY_MODE_COMMANDS = (COMMANDS.ADD, COMMANDS.QUIT)
    DEFAULT_MODE_COMMANDS = (
        COMMANDS.ADD,
        COMMANDS.QUIT,
        COMMANDS.DELETE,
        COMMANDS.EDIT,
        COMMANDS.TOGGLE,
        COMMANDS.UP,
        COMMANDS.DOWN,
    )
    # ADD_MODE_COMMANDS is a special case outside of this scope
    # EDIT_MODE_COMMANDS is a special case outside of this scope

    def run(self, args):  # noqa: C901
        try:
            from todo.utils.menu import Menu
        except ImportError as e:
            raise TodoException("Sorry! The interactive mode is not supported by your system", e)

        if args.group is None:
            group = self.service.group.get_active_group()
        else:
            group = self.service.group.get(args.group)

        if group is None:
            raise TodoException("<Group: {name}> not found".format(name=args.group))

        todos = self.service.todo.get_all(group[0], args.state)

        with Menu() as menu:
            menu.clear()

            tracker = VerticalTracker(todos, group)
            while True:
                menu.refresh()
                menu.render_header("{group_name}".format(group_name=tracker.group.name or "global"))
                menu.render_subheader(
                    "{items} item{singular_or_plural}: {completed} completed, {uncompleted} left".format(
                        items=tracker.group.items,
                        singular_or_plural=singular_or_plural(tracker.group.items),
                        completed=tracker.group.completed,
                        uncompleted=tracker.group.uncompleted,
                    )
                )

                self._render_todos(menu, tracker)

                mode = self._get_mode(tracker)
                if mode == COMMAND_MODES.EMPTY:
                    menu.render_commands(tracker.commands_offset, mode=COMMAND_MODES.EMPTY)
                elif mode == COMMAND_MODES.DELETE:
                    menu.render_commands(tracker.commands_offset, mode=COMMAND_MODES.DELETE)
                else:
                    menu.render_commands(tracker.commands_offset)

                command = self._interpret_command(menu.get_command(), mode)

                if command == COMMANDS.DOWN:
                    tracker.move_down()
                elif command == COMMANDS.UP:
                    tracker.move_up()
                elif command == COMMANDS.RECOVER:
                    tracker.recover()
                elif command == COMMANDS.TOGGLE:
                    tracker.toggle(self.service.todo)
                elif command == COMMANDS.ADD:
                    # add empty line
                    tracker.add(("??????", "", "", None))

                    # rerender todos
                    self._render_todos(menu, tracker)

                    # render add commands
                    menu.render_commands(tracker.commands_offset, mode=COMMAND_MODES.ADD)

                    new_todo_name = menu.edit_text("", tracker.index)
                    if new_todo_name is not None:
                        tracker.update(new_todo_name, self.service.todo)
                    else:
                        tracker.remove()
                        menu.clear()
                elif command == COMMANDS.EDIT:
                    menu.render_commands(tracker.commands_offset, mode=COMMAND_MODES.EDIT)
                    new_todo_name = menu.edit_text(tracker.current_todo.name, tracker.index)
                    tracker.edit(new_todo_name, self.service.todo)
                elif command == COMMANDS.DELETE:
                    tracker.mark_deleted()
                elif command == COMMANDS.QUIT:
                    break

            tracker.delete_todos(self.service.todo)

    def _get_mode(self, tracker):
        if tracker.todos_count == 0:
            return COMMAND_MODES.EMPTY
        elif tracker.is_deleted(tracker.current_todo.id):
            return COMMAND_MODES.DELETE
        return COMMAND_MODES.DEFAULT

    def _interpret_command(self, command, mode):
        if mode == COMMAND_MODES.DELETE and command in self.DELETE_MODE_COMMANDS:
            return command
        elif mode == COMMAND_MODES.EMPTY and command in self.EMPTY_MODE_COMMANDS:
            return command
        elif mode == COMMAND_MODES.DEFAULT and command in self.DEFAULT_MODE_COMMANDS:
            return command
        return None

    def _render_todos(self, menu, tracker):
        for index, todo in enumerate(tracker.todos):
            menu.render_todo(todo, index, tracker.index, tracker.is_deleted(todo[0]))
