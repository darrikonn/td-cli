<p align="center">
  <img src="https://raw.githubusercontent.com/darrikonn/td-cli/master/img/td-cli.png" width=80 alt="Icon"/>
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/5694851/67482097-be2ecc80-f652-11e9-899d-1d9750929b7e.png" />
  <br />
  <br />
  <a href="https://pypi.org/project/td-cli/">
    <img src="https://img.shields.io/pypi/v/td-cli.svg?style=flat-square"/>
  </a>
  <a href="https://pypi.org/project/td-cli/">
    <img src="https://img.shields.io/pypi/dm/td-cli?style=flat-square"/>
  </a>
  <a href="https://github.com/darrikonn/td-cli/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/Licence-MIT-yellow.svg?longCache=true&style=flat-square"/>
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Made With-Python-red.svg?longCache=true&style=flat-square"/>
  </a>
  <a href="https://github.com/alebcay/awesome-shell#command-line-productivity">
    <img height="20" src="https://user-images.githubusercontent.com/2769158/44446193-327a6580-a5a1-11e8-91e2-21ca857f95d4.png"/>
  </a>
</h3>

<pre>
  <p align="center"><a href="https://pypi.org/project/td-cli/"><strong>td-cli</strong></a> is a command line todo manager, <br/>where you can organize and manage your todos across multiple projects</p>
  <p align="center"><img class="img-responsive" width="500" src="https://raw.githubusercontent.com/darrikonn/td-cli/master/img/td-cli.gif" alt="gif"/></p>
</pre>

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

- Run `td <id> complete` to complete your todo. You don't have to specify the whole `id`, a substring will do. It'll fetch the first one that it finds in the same order as when you list your todos.

Note that `global` is a preserved group name where you can list all your global groups. You can always set it as the default with:
```bash
td group global preset
```


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
When editing a todo, `td <id> edit`, you can both specify the todo's `name` and the todo's `details`. If no option is specified, your todo will be opened in `vi` by default (your `environement EDITOR` will override this) where you can edit the todo's details. You can change the default editor by updating your config:
```cfg
[settings]
editor: nvim
```

### Group
When listing todos, you have the option of specifying what group to list from:
```bash
td -g my-group
# or
td g my-group
```
If no group is provided, `td` will list from the current default group. You can globally set the default group with:
```bash
td g my-group preset
```

However, there's an option to set the default group per git project (this is not possible from the root config `~/.td.cfg`).
In the root of your git project, you can create a `.td.cfg` config file to specify what group to default on (this will override the global default group):
```cfg
[settings]
group: my-group
```
If you run `td` within your git project, td will default to *my-group*.

I recommend globally ignoring `.td.cfg` in `~/.gitignore`.
