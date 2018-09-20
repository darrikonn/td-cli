from todo.commands import group, todo
from todo.services import Service
from todo.constants import COMMANDS


class Commands:
    commands_dict = {
        COMMANDS.ADD_TODO: todo.Add,
        COMMANDS.COMPLETE_TODO: todo.Complete,
        COMMANDS.DELETE_TODO: todo.Delete,
        COMMANDS.EDIT_TODO: todo.Edit,
        COMMANDS.GET_TODO: todo.Get,
        COMMANDS.LIST_TODOS: todo.List,
        COMMANDS.UNCOMPLETE_TODO: todo.Uncomplete,
        COMMANDS.ADD_GROUP: group.Add,
        COMMANDS.DELETE_GROUP: group.Delete,
        COMMANDS.GET_GROUP: group.Get,
        COMMANDS.LIST_GROUPS: group.List,
        COMMANDS.PRESET_GROUP: group.Preset,
    }

    def __init__(self, arguments):
        self.arguments = arguments

    def _get_arg(self, arg, is_valid):
        if is_valid:
            return (arg,)
        return tuple()

    def run(self):
        with Service() as service:
            for cmd, kwargs in self.arguments.items():
                command = self.commands_dict[cmd](service)
                command.run(**kwargs)
