from todo.commands import group, interactive, todo
from todo.services import Service


class Commands:
    commands_dict = {
        "add_todo": todo.Add,
        "complete_todo": todo.Complete,
        "delete_todo": todo.Delete,
        "edit_todo": todo.EditDetails,
        "get_todo": todo.Get,
        "list_todos": todo.List,
        "name_todo": todo.EditName,
        "uncomplete_todo": todo.Uncomplete,
        "add_group": group.Add,
        "delete_group": group.Delete,
        "get_group": group.Get,
        "initialize_group": group.Initialize,
        "list_groups": group.List,
        "preset_group": group.Preset,
        "interactive": interactive.Interactive,
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
