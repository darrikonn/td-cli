
import shutil
import textwrap

import click

from .service import Service
from .utils import get_user_input


def _render_header(uncompleted_count, completed_count, cols):
    todos = '{} todos'.format(uncompleted_count + completed_count)
    uncompleted = '{} uncompleted'.format(uncompleted_count)
    completed = '\033[32m{}\033[37m completed'.format(completed_count)
    border = '=' * cols

    click.echo(border)
    click.secho(todos.center(cols, ' '), fg='blue')
    click.echo()
    click.echo(uncompleted.center(cols, ' '))
    click.echo(completed.center(cols + 10, ' '))
    click.echo(border)


class AliasedGroup(click.Group):

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            ctx.obj = cmd_name
            return click.Group.get_command(self, ctx, 'parser')
        return None


@click.group(invoke_without_command=True, cls=AliasedGroup)
@click.option('--completed/--uncompleted', '-c/-u', default=False)
@click.pass_context
def cli(ctx, completed):
    if ctx.invoked_subcommand is None:
        return ctx.forward(list_todos)


@cli.command('list')
@click.option('--completed/--uncompleted', '-c/-u', default=False)
def list_todos(completed):
    with Service() as service:
        completed_todos = service.get_completed_todos()
        uncompleted_todos = service.get_uncompleted_todos()
        todos = completed_todos if completed else uncompleted_todos

        cols, _ = shutil.get_terminal_size((80, 20))
        _render_header(len(uncompleted_todos), len(completed_todos), cols)

        for b in todos:
            prefix = '\033[34m{}  \033[37m'.format(b[0])
            wrapper = textwrap.TextWrapper(initial_indent=prefix, width=cols, subsequent_indent=' '*8)
            click.echo(wrapper.fill(b[1]))


@cli.command('add')
@click.argument('title')
@click.option('--edit', '-e', is_flag=True, default=False, help='A more descriptive message of the todo. Will be opened in your preferred editor')
def add_todo(title, edit):
    """
    Adds a new todo where the TITLE is the short description of your todo.
    Examples:
        > todo add 'This is my short description' -e
    """
    try:
        if edit:
            description = get_user_input('nvim')
        else:
            description = title

        with Service() as service:
            click.secho(
                u'[+] {} added'.format(service.add_todo(title, description)),
                fg='green',
            )
    except Exception as e:
        click.secho(u'[*] Could not add a todo due to "{}"'.format(e), fg='red')


@cli.command('parser')
@click.option('--edit', '-e', is_flag=True)
@click.option('--delete', '-d', is_flag=True)
@click.option('--complete', '-c', is_flag=True)
@click.option('--uncomplete', '-u', is_flag=True)
@click.option('--yes', '-y', is_flag=True)
@click.pass_obj
@click.pass_context
def parser_args(ctx, todo_id, *args, **kwargs):
    print('command', todo_id, args, kwargs)
    raise click.Abort()
    try:
        with Service() as service:
            todo = service.get_todo(id)
            if todo:
                click.echo(todo[0])
            else:
                click.secho(u'[*] todo {} not found'.format(id), fg='red')
    except Exception as e:
        click.secho(u'[*] Could not get a todo due to "{}"'.format(e), fg='red')

@cli.command('delete')
@click.argument('id')
@click.confirmation_option('--yes', '-y', prompt='Are you sure you want to delete this todo?')
def delete_todo(id):
    try:
        with Service() as service:
            todo = service.get_todo(id)
            if not todo:
                click.secho(u'[*] todo {} not found'.format(id), fg='red')
                exit(0)
            service.delete_todo(id)
        click.secho(
            u'[-] {} deleted'.format(id),
            fg='red',
        )
    except Exception as e:
        click.secho(u'[*] Could not delete a todo due to "{}"'.format(e), fg='red')


@cli.command('complete')
@click.argument('id')
def complete_todo(id):
    try:
        with Service() as service:
            todo = service.get_todo(id)
            if not todo:
                click.secho(u'[*] todo {} not found'.format(id), fg='red')
                exit(0)
            service.complete_todo(id)
        click.secho(
            u'[*] {} completed'.format(id),
            fg='green',
        )
    except Exception as e:
        click.secho(u'[*] Could not complete a todo due to "{}"'.format(e), fg='red')


@cli.command('uncomplete')
@click.argument('id')
def uncomplete_todo(id):
    try:
        with Service() as service:
            todo = service.get_todo(id)
            if not todo:
                click.secho(u'[*] todo {} not found'.format(id), fg='red')
                exit(0)
            service.uncomplete_todo(id)
        click.secho(
            u'[*] {} uncompleted'.format(id),
            fg='green',
        )
    except Exception as e:
        click.secho(u'[*] Could not uncomplete a todo due to "{}"'.format(e), fg='red')


@cli.command('get')
@click.argument('id')
def get_todo(id):
    try:
        with Service() as service:
            todo = service.get_todo(id)
            if todo:
                click.echo(todo[0])
            else:
                click.secho(u'[*] todo {} not found'.format(id), fg='red')
    except Exception as e:
        click.secho(u'[*] Could not get a todo due to "{}"'.format(e), fg='red')


@cli.command('edit')
@click.argument('id')
def edit_todo(id):
    try:
        with Service() as service:
            todo = service.get_todo(id)
            if not todo:
                click.secho(u'[*] todo {} not found'.format(id), fg='red')
                exit(0)
            description = get_user_input('nvim', str.encode(todo[0]))
            todo = service.edit_todo(id, description)
    except Exception as e:
        click.secho(u'[*] Could not edit a todo due to "{}"'.format(e), fg='red')





class Command(object):
    def __init__(self):
        self.todo = {}
        self.todos = {}

    todos = [
        ('completed', ('--completed/--uncompleted', '-c/-u')),
    ]

    todo = [
        ('edit', ('--edit', '-e')),
        ('delete', ('--delete', '-d')),
        ('complete', ('--complete', '-c')),
        ('uncomplete', ('--uncomplete', '-u')),
        ('yes',  ('--yes', '-y')),
    ]


click.pass_command = click.make_pass_decorator(Command, ensure=True)

def options(identifier, with_callback=True):
    def _options(func):
        def callback(key):
            def _callback(ctx, param, value):
                command = ctx.ensure_object(Command)
                getattr(command, identifier)[key] = value
                return value
            return _callback

        for key, option in reversed(getattr(Command, identifier)):
            func = click.option(*option, is_flag=True, expose_value=not with_callback, callback=callback(key) if with_callback else None)(func)
        return func
    return _options

@click.group(invoke_without_command=True, context_settings=dict(allow_interspersed_args=True))
@click.argument('id', required=False)
@options('todo')
@options('todos')
@click.pass_command
@click.pass_context
def cli2(ctx, command, id):
    print(command.todos, command.todo)
    if id:
        return ctx.forward(Todo)
    return ctx.forward(Todos)

@cli2.command('Todo')
@options('todo', with_callback=False)
def Todo(id, *args, **kwargs):
    print('todo', id, args, kwargs)

@cli2.command('Todos', context_settings=dict(ignore_unknown_options=True))
@options('todos', with_callback=False)
def Todos(*args, **kwargs):
    print('todos', args, kwargs)


def main():
    cli()
