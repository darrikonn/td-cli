from sqlite3 import Error

from todo.commands.base import Command
from todo.exceptions import TodoException
from todo.renderers import RenderOutput


class Edit(Command):
    def run(self, args):
        try:
            group = self._get_group_or_raise(args.name)
            if group[0] is None or group[0] == "global":
                raise TodoException(
                    "Can't edit `{bold}<Group: global>{reset}`. It must always exist"
                )
            if not args.new_name:
                raise TodoException(
                    "Please provide a new name for the group using `--name` or `-n`"
                )
            new_group_name = self.service.group._interpret_group_name(args.new_name)
            if new_group_name is None:
                raise TodoException(
                    "Can't rename group to `{bold}<Group: global>{reset}`. It is reserved"
                )
            # Check if the new name already exists
            existing_group = self.service.group.get(new_group_name)
            if existing_group is not None and existing_group[0] != group[0]:
                raise TodoException("`{bold}<Group: %s>{reset}` already exists." % new_group_name)
            self.service.group.edit_name(new_group_name, group[0])

            RenderOutput("Edited {bold}{group_name}{reset}: {new_name}").render(
                group_name=group[0], new_name=new_group_name
            )
        except Error as e:
            raise TodoException(
                "Error occurred, could not edit `{bold}<Group: %s>{reset}`" % args.name, e
            )
