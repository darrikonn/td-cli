from todo.parsers.base import BaseParser, set_value
from todo.settings import config


class TodosParser(BaseParser):
    def _interpret(self, parsed_args):
        if parsed_args.add_todo:
            return {"add_todo": {"name": parsed_args.add_todo, "group_name": parsed_args.group}}
        elif parsed_args.interactive:
            return {"list_interactive_todos": {"state": parsed_args.state, "group_name": parsed_args.group}}
        else:
            return {
                "list_todos": {
                    "state": config["default_state"] if parsed_args.state is None else parsed_args.state,
                    "group_name": parsed_args.group,
                }
            }

    def _add_arguments(self):
        self.parser.add_argument("--interactive", "-i", dest="list_interactive_todos" action="store_true")
        self.parser.add_argument("--group", "-g", action="store")

        parser_group = self.parser.add_mutually_exclusive_group()
        parser_group.add_argument("--completed", "-c", dest="state", nargs=0, action=set_value(True))
        parser_group.add_argument("--uncompleted", "-u", dest="state", nargs=0, action=set_value(False))
        parser_group.add_argument("--add", "-a", dest="add_todo", action="store")
