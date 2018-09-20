from todo.commands.base import Command
from todo.commands.todo import List as ListTodos


class Get(Command):
    def run(self, args):
        setattr(args, "group", args.name)
        setattr(args, "state", None)
        setattr(args, "interactive", None)
        ListTodos(self.service).run(args)
