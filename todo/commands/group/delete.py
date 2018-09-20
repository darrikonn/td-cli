from sqlite3 import Error

from todo.commands.base import Command
from todo.renderers import RenderInput, RenderOutput
from todo.utils import singular_or_plural


class Delete(Command):
    def run(self, args):
        try:
            group = self._get_group_or_raise(args.name)
            if group[0] is None:
                raise Exception("Cannot delete group global")
            if not args.skip_prompt:
                todo_count = group[2] + group[1]
                post_text = ""
                if todo_count > 0:
                    RenderOutput(
                        "By deleting group {blue}{group_name}{reset}, "
                        "you'll also delete {bold}{todo_count}{normal} todo{singular_or_plural} in that group"
                    ).render(
                        group_name=args.name,
                        todo_count=todo_count,
                        singular_or_plural=singular_or_plural(todo_count),
                    )
                    post_text = ", and {todo_count} todo{singular_or_plural}"
                choice = RenderInput(
                    "[?] Are you sure you want to delete group {blue}{group_name}{reset}? [Y|n] "
                ).render(group_name=group[0])
                if choice not in ("y", "yes", ""):
                    raise Exception("Abort!")
            self.service.group.delete(group[0])

            RenderOutput("{red}Deleted{reset} {bold}{group_name}{normal}" + post_text).render(
                group_name=group[0],
                todos=post_text,
                singular_or_plural=singular_or_plural(todo_count),
                todo_count=todo_count,
            )
        except Error as e:
            print(u'[*] Could not delete a group due to "{}"'.format(e))
