from todo.constants import COMMANDS
from todo.parsers.base import BaseParser, set_value
from todo.settings import config


class GroupParser(BaseParser):
    arguments = ("name",)
    has_command_prefix = True

    def _interpret(self, parsed_args):
        if parsed_args.delete_group:
            return {COMMANDS.DELETE_GROUP: {"name": parsed_args.name}}
        elif parsed_args.preset_group:
            return {COMMANDS.PRESET_GROUP: {"name": parsed_args.name}}
        elif parsed_args.add_todo:
            return {COMMANDS.ADD_TODO: {"group_name": parsed_args.name, "name": parsed_args.add_todo}}
        else:
            return {
                COMMANDS.GET_GROUP: {
                    "name": parsed_args.name,
                    "state": config["default_state"] if parsed_args.state is None else parsed_args.state,
                }
            }

    def _add_arguments(self):
        parser_group = self.parser.add_mutually_exclusive_group()
        parser_group.add_argument("--delete", "-d", dest=COMMANDS.DELETE_GROUP, action="store_true")
        parser_group.add_argument("--completed", "-c", dest="state", nargs=0, action=set_value(True))
        parser_group.add_argument("--uncompleted", "-u", dest="state", nargs=0, action=set_value(False))
        parser_group.add_argument("--add", "-a", action="store", dest=COMMANDS.ADD_TODO)
        parser_group.add_argument("--preset", "-p", action="store_true", dest=COMMANDS.PRESET_GROUP)
