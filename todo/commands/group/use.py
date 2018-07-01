from todo.commands.base import Command


class Use(Command):
    def run(self, name):
        group = self._get_group_or_raise(name)

        self.service.group.use(group[0])
        print('Using group "{}"'.format(group[0] or 'global'))
