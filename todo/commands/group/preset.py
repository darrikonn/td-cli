from todo.commands.base import Command
from todo.renderers import RenderOutput


class Preset(Command):
    def run(self, name):
        group = self._get_group_or_raise(name)

        self.service.group.use(group[0])

        RenderOutput("Set {blue}{group_name}{reset} as default").render(
            group_name=group[0] or "global"
        )
