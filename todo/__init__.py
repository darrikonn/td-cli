import click

from . import controller


class GroupWithFallbackCommand(click.Group):
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        ctx.obj = cmd_name
        return click.Group.get_command(self, ctx, '<id>')


class MutualOption(click.Option):
    def __init__(self, *args, **kwargs):
            self.exclusive = set(kwargs.pop('exclusive', []))
            self.inclusive = set(kwargs.pop('inclusive', []))
            super(MutualOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.name in opts:
            if self.exclusive.intersection(opts):
                raise click.UsageError(
                    'Illegal usage\n\nYou can\'t `{}` and `{}` a todo in the same command'.format(
                        self.name,
                        ', '.join(self.exclusive),
                    ),
                )
            elif self.inclusive and not self.inclusive.intersection(opts):
                raise click.UsageError(
                    'Illegal usage\n\n`{}` is required if `{}` is used'.format(
                        ', '.join(self.inclusive),
                        self.name,
                    ),
                )
        return super(MutualOption, self).handle_parse_result(ctx, opts, args)


@click.group(invoke_without_command=True, cls=GroupWithFallbackCommand) #, context_settings=dict(allow_interspersed_args=True, ignore_unknown_options=True))
@click.option(
    '--completed/--uncompleted',
    '-c/-u',
    default=False,
    cls=MutualOption,
    exclusive=['new', 'edit'],
)
@click.option('--new', '-n')
@click.option(
    '--edit',
    '-e',
    is_flag=True,
    inclusive=['new'],
    cls=MutualOption,
    help='A more descriptive message of the todo. Will be opened in your preferred editor',
)
@click.pass_context
def cli(ctx, completed, new, edit):
    """
    # list uncompleted todos (can also pass the --uncompleted (-u) flag)

    > todo

    # create a new todo

    > todo -n 'My new todo'

    # create a new todo with and edit the description

    > todo -n 'My new todo' -e
    """
    if ctx.invoked_subcommand is None:
        if new:
            controller.add_todo(new, edit)
        else:
            controller.list_todos(completed)


@cli.command('<id>') #, context_settings=dict(allow_interspersed_args=True, ignore_unknown_options=True))
@click.option('--complete', '-c', is_flag=True, cls=MutualOption, exclusive=['uncomplete'])
@click.option('--uncomplete', '-u', is_flag=True, cls=MutualOption)
@click.option('--edit', '-e', is_flag=True, cls=MutualOption)
@click.option(
    '--delete',
    '-d',
    is_flag=True,
    cls=MutualOption,
    exclusive=['edit', 'complete', 'uncomplete'],
)
@click.option('skip_prompt', '--yes', '-y', is_flag=True)
@click.pass_obj
def id_parser(todo_id, *args, **kwargs):
    print(kwargs)
    if not any(kwargs[command] for command in kwargs if command != 'skip_prompt'):
        return controller.get_todo(todo_id)
    if kwargs['delete']:
        controller.delete_todo(todo_id, kwargs['skip_prompt'])
    elif kwargs['edit']:
        controller.edit_todo(todo_id)
    if kwargs['complete']:
        controller.complete_todo(todo_id)
    elif kwargs['uncomplete']:
        controller.complete_todo(todo_id)


def main():
    cli()
