from todo.parsers.base import BaseParser, set_value


class GroupParser(BaseParser):
    arguments = ("name",)
    has_command_prefix = True

    def _interpret(self, parsed_args):
        if parsed_args.delete_group:
            return {"delete_group": {"name": parsed_args.name}}
        elif parsed_args.preset_group:
            return {"preset_group": {"name": parsed_args.name}}
        elif parsed_args.add_todo:
            return {
                "add_todo": {
                    "group_name": parsed_args.name,
                    "name": parsed_args.add_todo,
                }
            }
        else:
            return {"get_group": {"name": parsed_args.name, "state": parsed_args.state}}

    def _add_arguments(self):
        parser_group = self.parser.add_mutually_exclusive_group()
        parser_group.add_argument(
            "--delete", "-d", dest="delete_group", action="store_true"
        )
        parser_group.add_argument(
            "--completed", "-c", dest="state", nargs=0, action=set_value(True)
        )
        parser_group.add_argument(
            "--uncompleted", "-u", dest="state", nargs=0, action=set_value(False)
        )
        parser_group.add_argument("--add", "-a", action="store", dest="add_todo")
        parser_group.add_argument(
            "--preset", "-p", action="store_true", dest="preset_group"
        )
