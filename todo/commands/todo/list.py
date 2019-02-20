from todo.commands.base import Command
from todo.constants import COMMAND_MODES
from todo.constants import INTERACTIVE_COMMANDS as COMMANDS
from todo.exceptions import TodoException
from todo.renderers import RenderOutput, RenderOutputWithTextwrap
from todo.utils import interpret_state, singular_or_plural


class List(Command):
    def run(self, args):
        if args.group is None:
            group = self.service.group.get_active_group()
        else:
            group = self.service.group.get(args.group)

        if group is None:
            raise TodoException("<Group: {name}> not found".format(name=args.group))

        todos = self.service.todo.get_all(group[0], args.state)

        if args.interactive:
            self._render_todos_interactive(todos, group, args.state)
        else:
            self._render_todos(todos, group)

    def _render_todos(self, todos, group):
        RenderOutput("{subsequent_indent}{bold}{blue}{group_name}{reset}\n").render(
            subsequent_indent=" " * 4, group_name=group[0] or "global"
        )

        for todo in todos:
            RenderOutputWithTextwrap("{completed} {bold}{todo_id}{reset}: ", "{name}").render(
                completed="✓" if todo[3] else "x", name=todo[1], todo_id=todo[0]
            )

        RenderOutput(
            "{prefix}{grey}{items} item{singular_or_plural}: {completed} completed, {uncompleted} left"
        ).render(
            prefix="\n" if group[1] > 0 else "",
            items=group[1],
            singular_or_plural=singular_or_plural(group[1]),
            uncompleted=group[2],
            completed=group[3],
        )

    def _render_todos_interactive(self, todos, group, state):  # noqa: C901
        try:
            from todo.utils.menu import Menu
        except ImportError as e:
            raise TodoException("Sorry! The interactive mode is not supported by your system", e)

        if len(todos) == 0:
            return RenderOutput(
                "No{state} {bold}{blue}{name}{reset} {bold}todos{reset} to be listed"
            ).render(state=interpret_state(state), name=group[0] or "global")

        import os
        _, rows = os.get_terminal_size()
        max_rows = rows - 15
        deleted_todos = set()
        with Menu() as menu:
            menu.clear()

            current_pos = 0
            cursor = 0
            while True:
                menu.refresh()
                menu.render_header("{group_name}".format(group_name=group[0]))
                menu.render_subheader(
                    "{items} item{singular_or_plural}: {completed} completed, {uncompleted} left".format(
                        items=group[1],
                        singular_or_plural=singular_or_plural(group[1]),
                        completed=group[3],
                        uncompleted=group[2],
                    )
                )

                start_pos = current_pos - cursor
                todos_count = len(todos)
                menu.render_test(cursor, current_pos, max_rows, todos_count)
                to_be_rendered = todos[start_pos : (start_pos + max_rows)]
                for index, todo in enumerate(to_be_rendered):
                    is_deleted = todo[0] in deleted_todos
                    menu.render_todo(todo, index, cursor, is_deleted)

                current_todo = todos[current_pos]
                commands_offset = min(max_rows, todos_count)
                if current_todo[0] in deleted_todos:
                    menu.render_commands(commands_offset, mode=COMMAND_MODES.DELETE)
                else:
                    menu.render_commands(commands_offset)

                command = menu.get_command()

                if command == COMMANDS.DOWN:
                    current_pos += 1
                    if current_pos == todos_count:  # on last todo
                        cursor = 0
                        current_pos = 0
                    elif not (cursor + 2 == max_rows and current_pos != todos_count - 1):
                        cursor += 1
                elif command == COMMANDS.UP:
                    current_pos -= 1
                    if current_pos < 0:
                        cursor = commands_offset - 1
                        current_pos = todos_count - 1
                    elif not (cursor - 1 == 0 and current_pos != 0):
                        cursor -= 1

                if current_todo[0] in deleted_todos:
                    if command == COMMANDS.RECOVER:
                        deleted_todos.discard(current_todo[0])
                        if current_todo[3]:
                            group = (group[0], group[1] + 1, group[2], group[3] + 1)
                        else:
                            group = (group[0], group[1] + 1, group[2] + 1, group[3])
                else:
                    if command == COMMANDS.TOGGLE:
                        # toggle todo
                        if current_todo[3]:
                            # uncomplete todo
                            self.service.todo.uncomplete(current_todo[0])
                            group = group[:2] + (group[2] + 1, group[3] - 1)
                        else:
                            # complete todo
                            self.service.todo.complete(current_todo[0])
                            group = group[:2] + (group[2] - 1, group[3] + 1)
                        # update list
                        todos[current_pos] = current_todo[:3] + (not current_todo[3],)
                    elif command == COMMANDS.ADD:
                        # add empty line
                        current_pos += 1
                        todos = todos[:current_pos] + [("??????", "", "", None)] + todos[current_pos:]
                        if cursor + 2 < max_rows:
                            cursor += 1

                        # rerender todos
                        start_pos2 = current_pos - cursor
                        to_be_rendered2 = todos[start_pos2 : (start_pos2 + max_rows)]
                        for index, todo in enumerate(to_be_rendered2):
                            is_deleted = todo[0] in deleted_todos
                            menu.render_todo(todo, index, cursor, is_deleted)

                        # render add commands
                        menu.render_commands(min(todos_count + 1, max_rows), mode=COMMAND_MODES.ADD)

                        new_todo_name = menu.edit_text("", cursor)
                        if new_todo_name is not None:
                            new_id = self.service.todo.add(new_todo_name, new_todo_name, group[0], False)
                            todos[current_pos] = (new_id, new_todo_name, new_todo_name, False)
                            group = (group[0], group[1] + 1, group[2] + 1, group[3])
                        else:
                            todos = todos[:current_pos] + todos[current_pos + 1:]
                            current_pos -= 1
                            if cursor + 2 < max_rows:
                                cursor -= 1
                            menu.clear()
                    elif command == COMMANDS.EDIT:
                        menu.render_commands(commands_offset, mode=COMMAND_MODES.EDIT)
                        new_todo_name = menu.edit_text(current_todo[1], cursor)
                        if new_todo_name is not None:
                            self.service.todo.edit_name(current_todo[0], new_todo_name)
                            todos[current_pos] = (current_todo[0], new_todo_name) + current_todo[2:]
                    elif command == COMMANDS.DELETE:
                        deleted_todos.add(current_todo[0])
                        if current_todo[3]:
                            group = (group[0], group[1] - 1, group[2], group[3] - 1)
                        else:
                            group = (group[0], group[1] - 1, group[2] - 1, group[3])

                if command == COMMANDS.QUIT:
                    break

            for deleted_todo in deleted_todos:
                self.service.todo.delete(deleted_todo)
