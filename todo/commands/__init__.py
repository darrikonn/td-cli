from todo.commands import config, group, todo
from todo.constants import COMMANDS
from todo.services import Service


class Commands:
    commands_dict = {
        COMMANDS.ADD_TODO: todo.Add,
        COMMANDS.COMPLETE_TODO: todo.Complete,
        COMMANDS.COUNT_TODOS: todo.Count,
        COMMANDS.DELETE_TODO: todo.Delete,
        COMMANDS.EDIT_TODO: todo.Edit,
        COMMANDS.GET_TODO: todo.Get,
        COMMANDS.LIST_TODOS: todo.List,
        COMMANDS.UNCOMPLETE_TODO: todo.Uncomplete,
        COMMANDS.INITIALIZE_CONFIG: config.Initialize,
        COMMANDS.ADD_GROUP: group.Add,
        COMMANDS.DELETE_GROUP: group.Delete,
        COMMANDS.GET_GROUP: group.Get,
        COMMANDS.LIST_GROUPS: group.List,
        COMMANDS.PRESET_GROUP: group.Preset,
    }

    def __init__(self, command):
        self.command = command

    def run(self, arguments):
        with Service() as service:
            command = self.commands_dict[self.command](service)
            command.run(arguments)
