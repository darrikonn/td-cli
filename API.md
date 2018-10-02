# td
```
usage: td {add,add-group,[id],group,list,list-groups} ...

positional arguments:
  {...}                   commands
    add (a)               add todo
    add-group (ag)        add group
    [id]                  manage todo
    group (g)             manage group
    list (l, ls)          list todos       *DEFAULT*
    list-groups (lg, lsg) list groups

optional arguments:
  -h, --help            show this help message and exit
```
`td` defaults to `td list`

<hr />

## List todos
```
usage: td [--completed] [--uncompleted] [--group GROUP] [--interactive]
       td list [-c] [-u] [-g GROUP] [-i]
       td ls [-c] [-u] [-g GROUP] [-i]
       td l [-c] [-u] [-g GROUP] [-i]

optional arguments:
  -h, --help            show this help message and exit
  --completed, -c       filter by completed todos
  --uncompleted, -u     filter by uncompleted todos
  --group GROUP, -g GROUP
                        filter by name of group
  --interactive, -i     toggle interactive mode
```
`td` is the shortcut to `td list`

#### Examples
1. `td list --completed`
2. `td -c`
3. `td --interactive`

<hr />

## Add a todo
```
usage: td add [name] [--complete] [--uncomplete] [--group GROUP] [--edit | --details DETAILS]
       td a [name] [-c] [-u] [-g GROUP] [-e | -d DETAILS]

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
```
`--edit` and `--details` are mutually exclusive.

#### Examples
1. `td add 'my new todo' --edit`
2. `td a 'my new todo' -d 'the details'`

<hr />

## Manage todo
```
usage: td [id] {get,delete,uncomplete,complete,edit} ...

positional arguments:
  id                    the id of the todo {...}                 commands
    get (g)             show todo's details
    delete (d)          delete todo
    uncomplete (u)      uncomplete todo
    complete (c)        complete todo
    edit (e)            edit todo

optional arguments:
  -h, --help            show this help message and exit
```
`td [id]` defaults to `td [id] get`

### Get todo's details
```
usage: td [id]
       td [id] get
       td [id] g

optional arguments:
  -h, --help  show this help message and exit
```
`td [id]` is the shortcut to `td [id] get`

### Delete todo
```
usage: td [id] delete [-yes]
       td [id] d [-y]

optional arguments:
  -h, --help  show this help message and exit
  --yes, -y   skip yes/no prompt when deleting todo
```

### Complete todo
```
usage: td [id] complete
       td [id] c

optional arguments:
  -h, --help  show this help message and exit
```

### Uncomplete todo
```
usage: td [id] uncomplete
       td [id] u

optional arguments:
  -h, --help  show this help message and exit
```

### Edit todo
```
usage: td [id] edit [--name NAME] [--details DETAILS]
       td [id] e [-n NAME] [-d DETAILS]

optional arguments:
  -h, --help            show this help message and exit
  --name NAME, -n NAME  update todo's name
  --details DETAILS, -d DETAILS
                        update todo's detail
  --group GROUP, -g GROUP
                        set todo's group
```
If no optional arguments are provided, the todo will be
opened in your editor where you can edit the todo's details.

#### Examples
1. `td 1337`
2. `td 1337 complete`
3. `td 1337 u`
4. `td 1337 edit -n "new name" -d "details"`


<hr />

## List groups
```
usage: td list-groups [--completed] [--uncompleted]
       td lg [-c] [-u]
       td lsg [-c] [-u]

optional arguments:
  -h, --help         show this help message and exit
  --completed, -c    filter by completed groups
  --uncompleted, -u  filter by uncompleted groups
```

<hr />

## Add a group
```
usage: td add-group [name]
       td ag [name]

positional arguments:
  name        the new group's name

optional arguments:
  -h, --help  show this help message and exit
```

<hr />

## Manage group
```
usage: td group [name] {get,delete,preset} ...
       td g [name] {g,d,p} ...

positional arguments:
  name                  name of the group
  {...}                 commands
    get (g)             list group's todos
    delete (d)          delete group and its todos
    preset (p)          set group as the default group when listing todos

optional arguments:
  -h, --help  show this help message and exit
```
`td group [name]` defaults to `td group [name] get`

### List group's todos
```
usage: td group [name]
       td group [name] get
       td group [name] g

optional arguments:
  -h, --help         show this help message and exit
  --completed, -c    filter by completed todos
  --uncompleted, -u  filter by uncompleted todos
  --interactive, -i  toggle interactive mode
```
`td group [name]` is the shortcut to `td group [name] get`

### Delete group and its todos
```
usage: td group [name] delete [--yes]
       td group [name] d [-y]

optional arguments:
  -h, --help  show this help message and exit
  --yes, -y   skip yes/no prompt when deleting group
```

### Set group as default when listing todos
```
usage: td group [name] preset
       td group [name] p

optional arguments:
  -h, --help  show this help message and exit
```

#### Examples
1. `td group my-project`
2. `td g my-project --completed`
3. `td g my-project preset`
