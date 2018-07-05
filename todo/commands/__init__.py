from todo.commands import group, interactive, todo
from todo.services import Service


class Commands:
    commands_dict = {
        'add_todo': todo.Add,
        'complete_todo': todo.Complete,
        'delete_todo': todo.Delete,
        'edit_todo': todo.EditDetails,
        'get_todo': todo.Get,
        'list_todos': todo.List,
        'uncomplete_todo': todo.Uncomplete,

        'add_group': group.Add,
        'delete_group': group.Delete,
        'get_group': group.Get,
        'list_groups': group.List,
        'use_group': group.Use,

        'interactive': interactive.Interactive
    }

    def __init__(self, arguments, commands):
        self.commands = commands
        self.arguments = arguments

    def _get_arg(self, arg, is_valid):
        if is_valid:
            return (arg, )
        return tuple()

    def run(self):
        with Service() as service:
            for cmd, arg in self.commands.items():
                command = self.commands_dict[cmd](service)
                command.run(
                    *self._get_arg(arg, command.is_valid_argument(arg)),
                    **self.arguments
                )
