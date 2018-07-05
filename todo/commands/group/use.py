from todo.commands.base import Command
from todo.renderers import RenderOutput


class Use(Command):
    def run(self, name):
        group = self._get_group_or_raise(name)

        self.service.group.use(group[0])

        RenderOutput("Using group {blue}{group_name}").render(group_name=group[0] or "global")
