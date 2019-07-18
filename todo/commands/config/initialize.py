from pathlib import Path

from todo.commands.base import Command
from todo.renderers import RenderInput, RenderOutput
from todo.settings import EXAMPLE_CONFIG


class Initialize(Command):
    def run(self, args):
        cwd = Path.expanduser(Path.cwd())
        location = Path(
            RenderInput("[?] Configuration location? [{cwd}] ").render(cwd=cwd) or cwd
        ).expanduser()
        if not location.is_dir():
            RenderOutput("Directory {red}{location}{reset} does not exist").render(
                location=location
            )
            return RenderOutput("Abort!").render()
        file = Path(f"{location}/.td.cfg")
        if file.exists():
            RenderOutput("Configuration file {red}{file}{reset} already exists").render(file=file)
            return RenderOutput("Abort!").render()

        group = RenderInput("[?] Choose your default group? ").render()
        if self.service.group.get(group) is None:
            RenderOutput("Group {red}{group}{reset} does not exist").render(group=group or '""')
            return RenderOutput("Abort!").render()

        with open(file, "w+") as f:
            f.write(EXAMPLE_CONFIG.format(group=group))

        RenderOutput("\nConfiguration file {green}successfully{reset} created!").render()
