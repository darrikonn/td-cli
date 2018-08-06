from todo.constants import COMMANDS
from todo.parsers.base import BaseParser


class TodoParser(BaseParser):
    arguments = ("id",)

    def _interpret(self, parsed_args):
        if parsed_args.complete_todo:
            return {COMMANDS.COMPLETE_TODO: {"id": parsed_args.id}}
        elif parsed_args.uncomplete_todo:
            return {COMMANDS.UNCOMPLETE_TODO: {"id": parsed_args.id}}
        elif parsed_args.delete_todo:
            return {COMMANDS.DELETE_TODO: {"id": parsed_args.id, "skip_prompt": parsed_args.skip_prompt}}
        elif parsed_args.name_todo:
            return {COMMANDS.NAME_TODO: {"id": parsed_args.id, "name": parsed_args.name_todo}}
        elif parsed_args.edit_todo:
            return {COMMANDS.EDIT_TODO: {"id": parsed_args.id}}
        else:
            return {COMMANDS.GET_TODO: {"id": parsed_args.id}}

    def _add_arguments(self):
        self.parser.add_argument("--yes", "-y", dest="skip_prompt", action="store_true")

        parser_group_1 = self.parser.add_mutually_exclusive_group()
        parser_group_1.add_argument("--complete", "-c", dest=COMMANDS.COMPLETE_TODO, action="store_true")
        parser_group_1.add_argument("--uncomplete", "-u", dest=COMMANDS.UNCOMPLETE_TODO, action="store_true")

        parser_group_2 = self.parser.add_mutually_exclusive_group()
        parser_group_2.add_argument("--delete", "-d", dest=COMMANDS.DELETE_TODO, action="store_true")
        parser_group_2.add_argument("--name", "-n", dest=COMMANDS.NAME_TODO, action="store")
        parser_group_2.add_argument("--edit", "-e", dest=COMMANDS.EDIT_TODO, action="store_true")
