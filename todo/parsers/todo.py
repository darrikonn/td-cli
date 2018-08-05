from todo.parsers.base import BaseParser


class TodoParser(BaseParser):
    arguments = ("id",)

    def _interpret(self, parsed_args):
        if parsed_args.complete_todo:
            return {"complete_todo": {"id": parsed_args.id}}
        elif parsed_args.uncomplete_todo:
            return {"uncomplete_todo": {"id": parsed_args.id}}
        elif parsed_args.delete_todo:
            return {
                "delete_todo": {
                    "id": parsed_args.id,
                    "skip_prompt": parsed_args.skip_prompt,
                }
            }
        elif parsed_args.name_todo:
            return {"name_todo": {"id": parsed_args.id, "name": parsed_args.name_todo}}
        elif parsed_args.edit_todo:
            return {"edit_todo": {"id": parsed_args.id}}
        else:
            return {"get_todo": {"id": parsed_args.id}}

    def _add_arguments(self):
        self.parser.add_argument("--yes", "-y", dest="skip_prompt", action="store_true")

        parser_group_1 = self.parser.add_mutually_exclusive_group()
        parser_group_1.add_argument(
            "--complete", "-c", dest="complete_todo", action="store_true"
        )
        parser_group_1.add_argument(
            "--uncomplete", "-u", dest="uncomplete_todo", action="store_true"
        )

        parser_group_2 = self.parser.add_mutually_exclusive_group()
        parser_group_2.add_argument(
            "--delete", "-d", dest="delete_todo", action="store_true"
        )
        parser_group_2.add_argument("--name", "-n", dest="name_todo", action="store")
        parser_group_2.add_argument(
            "--edit", "-e", dest="edit_todo", action="store_true"
        )
