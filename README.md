<p align="center"><img src="https://raw.githubusercontent.com/darrikonn/td-cli/master/img/td-cli.png" width=80 alt="Icon"/></p>

<h1 align="center" style="text-align: center">td-cli</h1>

<p align="center"><a href="https://pypi.org/project/td-cli/"><strong>td-cli</strong></a> is a command line todo manager, <br/>where you can organize and manage your todos across multiple projects</p>
<p align="center"><img class="img-responsive" width="500" src="https://raw.githubusercontent.com/darrikonn/td-cli/master/img/td-cli.gif" alt="gif"/></p>
<p align="center"><img src="https://badge.fury.io/py/td-cli.svg" /></p>

<hr />

## Installation
[**td-cli**](https://pypi.org/project/td-cli/) only works for `python 3`, so it needs to be installed with `pip3`
```bash
pip3 install td-cli
```

## Getting started
Run `td --help` to see possible commands.

Here are some to get you started:
- Run `td` to list all your todos.

- Run `td add "my new awesome todo"` to add a new todo.

- Run `td <id> complete` to complete your todo.


## API
Check out the [`api`](https://github.com/darrikonn/td-cli/blob/master/API.md).

## Configuring
### Database name
Your database instance will be located in your home directory (`~/`).
By default it'll be named `todo`.

You can change your database name by specifying `database_name` in your `~/.td.cfg` file:
```cfg
[settings]
database_name: something_else
```
This results in a database instance at `~/.something_else.db`

### Editor
When editing a todo, `td <id> edit`, you can both specify the todo's `name` and the todo's `details`. If no option is specified, your todo will be opened in `vi` by default where you can edit the todo's details. You can change the default editor by updating your config:
```cfg
[settings]
editor: nvim
```
