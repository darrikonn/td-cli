from todo.commands.base import Command
from todo.constants import INTERACTIVE_COMMANDS as COMMANDS
from todo.renderers import RenderOutput, RenderOutputWithTextwrap
from todo.utils import interpret_state, singular_or_plural
from todo.utils.menu import Menu


class List(Command):
    def run(self, args):
        if args.group is None:
            group = self.service.group.get_active_group()
        else:
            group = self.service.group.get(args.group)

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
            RenderOutputWithTextwrap("{completed} {bold}{todo_id}{reset}  ", "{name}").render(
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

    def _render_todos_interactive(self, todos, group, state):
        todos_count = len(todos)
        if todos_count == 0:
            return RenderOutput(
                "No{state} {bold}{blue}{name}{reset} {bold}todos{reset} to be listed"
            ).render(state=interpret_state(state), name=group[0] or "global")

        with Menu() as menu:
            menu.clear()
            menu.render_header("{group_name}".format(group_name=group[0]))

            current_pos = 0
            while True:
                menu.refresh()
                menu.render_subheader(
                    "{items} item{singular_or_plural}: {completed} completed, {uncompleted} left".format(
                        items=group[1],
                        singular_or_plural=singular_or_plural(group[1]),
                        completed=group[3],
                        uncompleted=group[2],
                    )
                )

                for index, todo in enumerate(todos):
                    menu.render_todo(todo, index, current_pos)

                menu.render_commands(todos_count)

                command = menu.get_command()

                if command == COMMANDS.DOWN:
                    current_pos = current_pos + 1 if current_pos + 1 < todos_count else 0
                elif command == COMMANDS.UP:
                    current_pos = current_pos - 1 if current_pos > 0 else todos_count - 1

                todo = todos[current_pos]
                if command == COMMANDS.TOGGLE:
                    # toggle todo
                    if todo[3]:
                        # uncomplete todo
                        self.service.todo.uncomplete(todo[0])
                        group = group[:2] + (group[2] + 1, group[3] - 1)
                    else:
                        # complete todo
                        self.service.todo.complete(todo[0])
                        group = group[:2] + (group[2] - 1, group[3] + 1)
                    # update list
                    todos[current_pos] = todo[:3] + (not todo[3],)
                elif command == COMMANDS.QUIT:
                    break
