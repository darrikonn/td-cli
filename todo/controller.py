import shutil
import textwrap
from sqlite3 import Error

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


def list_todos(completed):
    with Service() as service:
        completed_todos = service.get_completed_todos()
        uncompleted_todos = service.get_uncompleted_todos()
        todos = completed_todos if completed else uncompleted_todos

        cols, _ = shutil.get_terminal_size((80, 20))
        _render_header(len(uncompleted_todos), len(completed_todos), cols)

        for b in todos:
            prefix = '\033[34m{}  \033[37m'.format(b[0])
            wrapper = textwrap.TextWrapper(
                initial_indent=prefix,
                width=cols,
                subsequent_indent=' ' * 8,
            )
            click.echo(wrapper.fill(b[1]))


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
    except Error as e:
        click.secho(u'[*] Could not add a todo due to "{}"'.format(e), fg='red')


def _get_todo_or_raise(service, todo_id):
    todo = service.get_todo(todo_id)
    if not todo:
        try:
            if int(todo_id, 16) and len(todo_id) < 6:
                exit(click.secho(u'[*] todo {} not found'.format(todo_id), fg='red'))
        except Exception:
            pass
        exit(click.echo('Usage: todo <id> [OPTIONS]\n\nCommand not found'))
    return todo


def delete_todo(id, skip_prompt):
    try:
        with Service() as service:
            todo = _get_todo_or_raise(service, id)
            if not skip_prompt:
                click.confirm(
                    '[?] Are you sure you want to delete todo \033[34m{}\033[37m?'.format(todo[0]),
                    abort=True,
                )
            service.delete_todo(todo[0])
        click.secho(
            u'[-] {} deleted'.format(todo[0]),
            fg='red',
        )
    except Error as e:
        click.secho(u'[*] Could not delete a todo due to "{}"'.format(e), fg='red')


def complete_todo(id):
    try:
        with Service() as service:
            todo = _get_todo_or_raise(service, id)
            service.complete_todo(todo[0])
        click.secho(
            u'[*] {} completed'.format(todo[0]),
            fg='green',
        )
    except Error as e:
        click.secho(u'[*] Could not complete a todo due to "{}"'.format(e), fg='red')


def uncomplete_todo(id):
    try:
        with Service() as service:
            todo = _get_todo_or_raise(service, id)
            service.uncomplete_todo(todo[0])
        click.secho(
            u'[*] {} uncompleted'.format(todo[0]),
            fg='green',
        )
    except Error as e:
        click.secho(u'[*] Could not uncomplete a todo due to "{}"'.format(e), fg='red')


def get_todo(id):
    try:
        with Service() as service:
            todo = _get_todo_or_raise(service, id)
            cols, _ = shutil.get_terminal_size((80, 20))
            click.echo('-' * cols)
            click.echo('\033[34m{}  \033[37m{}'.format(todo[0], todo[1]).center(cols + 10, ' '))
            click.echo('-' * cols)
            click.echo(todo[2])
    except Error as e:
        click.secho(u'[*] Could not get a todo due to "{}"'.format(e), fg='red')


def edit_todo(id):
    try:
        with Service() as service:
            todo = _get_todo_or_raise(service, id)
            description = get_user_input('nvim', str.encode(todo[2]))
            service.edit_todo(todo[0], description)
            click.secho(
                u'[*] {} edited'.format(todo[0]),
                fg='green',
            )
    except Error as e:
        click.secho(u'[*] Could not edit a todo due to "{}"'.format(e), fg='red')
