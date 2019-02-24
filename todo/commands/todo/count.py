from todo.commands.base import Command
from todo.exceptions import TodoException
from todo.renderers import RenderOutput


class Count(Command):
    def run(self, args):
        if args.group is None:
            group = self.service.group.get_active_group()
        else:
            group = self.service.group.get(args.group)

        if group is None:
            raise TodoException("<Group: {name}> not found".format(name=args.group))

        todos = self.service.todo.get_all(group[0], args.state)

        RenderOutput("{count}").render(count=len(todos))
