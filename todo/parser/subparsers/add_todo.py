from todo.constants import COMMANDS
from todo.parser.base import BaseParser


class AddTodoParser(BaseParser):
    """
    usage: td add [name] [--complete] [--uncomplete] [--group GROUP] [--edit | --details DETAILS]
           td a [name] [-c] [-u] [-g GROUP] [-e | -d DETAILS]

    add todo

    positional arguments:
      name                  the new todo's name

    optional arguments:
      -h, --help            show this help message and exit
      --complete, -c        complete todo
      --uncomplete, -u      uncomplete todo
      --group GROUP, -g GROUP
                            name of todo's group
      --edit, -e            edit the todo's details in your editor
      --details DETAILS, -d DETAILS
                            the todo's details

    The editor defaults to `vi`, but you can choose your preferred one be setting:
    ```
    [settings]
    editor: <your_editor>
    ```
    in ~/.td.cfg
    """

    command = COMMANDS.ADD_TODO

    def _add_arguments(self):
        self.parser.add_argument("name", action="store", help="the new todo's name")
        self.parser.add_argument(
            "--complete", "-c", dest="state", action="store_true", help="complete todo"
        )
        self.parser.add_argument(
            "--uncomplete", "-u", dest="state", action="store_false", help="uncomplete todo"
        )
        self.parser.add_argument("--group", "-g", action="store", help="name of todo's group")

        exclusive_parser = self.parser.add_mutually_exclusive_group()
        exclusive_parser.add_argument(
            "--edit", "-e", action="store_true", help="edit the todo's details in your editor"
        )
        exclusive_parser.add_argument("--details", "-d", action="store", help="the todo's details")
