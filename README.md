# YODA

```
 ::\`--._,'.::.`._.--'/:: Multiple
 ::::.  ` __::__ '  .::::    repositories
 ::::::-:.`'..`'.:-::::::        management.
 ::::::::\ `--' /:::::::: 
```
## Requirements

- PyYaml
- pycolorizer
- PrettyTable
- argcomplete

### Tests packages
- mock
- pep8
- flake8
- tox
- nose
- coverage

## Installation
Yoda is available only on github, it will be packaged on Pypi when first release.

Yoda is compatible with following python version:
- Python 2.7.x
- Python 3.x

```bash
pip install https://github.com/numergy/yoda.git
```

Uninstall yoda:
```bash
pip uninstall yoda
```

## Usage
```bash
$ yoda --help
usage: yoda [-h] [-d] [--version] [subcommand] ...

Manage your repositories easier. Each workspaces are subcommands, type `yoda
workspace_name -h` to show help.

positional arguments:
  [subcommand]
    jump        Jump to directory
    update      Update repositories
    status      Show repositories status
    workspace   Workspace managment
    show        Show workspace details

optional arguments:
  -h, --help    show this help message and exit
  -d, --debug   show debug informations
  --version     show program's version number and exit
```

#### yoda workspace
The `workspace` subcommand allows you to manages your yoda's workspaces.
A workspace contains some properties (path, repositories list).

You can create workspace simply with a `name` and a `path`:
```bash
yoda workspace add ws_name /path/to/workspace
```

To remove a workspace:
```bash
yoda workspace remove ws_name
```

To print workspace list:
```bash
yoda workspace list
```

#### yoda show
`show` subcommand allows you to print a workspace details. You can pass --all options to show details for all registered workspaces.
```bash
yoda show my_ws
```

#### yoda status
`status` subcommand allows you to show repositories status in a workspace.

For example, to show status of all repositories in `my_ws` workspace:
```bash
yoda status my_ws
```

You can show status for a single repository:
```bash
yoda status my_ws/my_repo
yoda status my_repo
```

To show status of all workspaces, use `--all` option:
```bash
yoda status --all
```

#### yoda update
`update` subcommand is similary of `status` subcommand.

To update all repositories in `my_ws` workspace:
```bash
yoda update my_ws
```

For a single repository:
```bash
yoda update my_ws/my_repo
```

To update all workspaces:
```bash
yoda update --all
```

#### yoda jump
`jump` subcommand allows you to spawn new shell in repository or workspace path.

```bash
sliim@host:~$ yoda jump my_ws/my_repo
Spawn new shell on `/path/to/my_ws/my_repo/`
Use Ctrl-D to exit and go back to the previous directory

sliim@host:/path/to/my_ws/my_repo$
```

#### Workspaces subcommands
Each defined workspace in yoda have subcommands, for example if you have a workspace named `my_ws` you can type:
```bash
$ yoda my_ws --help
usage: yoda my_ws [-h] {add,remove,sync} ...

Manage repositories in my_ws workspace

positional arguments:
  {add,remove,sync}
    add              Add repository to my_ws workspace
    remove           Remove repository from my_ws workspace
    sync             Synchronize all directories stored in workspace

optional arguments:
  -h, --help         show this help message and exit
```

## Zsh completions
To Enable zsh completions, copy file `tools/zsh-completions/_yoda` in your zsh completions directory.
Be sure you have enabled the zsh completions system.

For example with completions directory `~/.zsh.d/completions/`:
```zsh
fpath=($HOME/.zsh.d/completions $fpath)
autoload -U compinit
compinit -i
```

## Bash completions
Yoda use [argcomplete](https://github.com/kislyuk/argcomplete) for bash completion.

Global completion requires bash support for `complete -D`, which was introduced in bash 4.2. On older
systems, you will need to update bash to use this feature. Check the version of the running copy of bash with
`echo $BASH_VERSION`.

If global completion is not activated, put this piece of code in your `.bashrc`.

```bash
eval "$(register-python-argcomplete yoda)"
```

## Running tests
In project root directory, run following command to

To run unittests:
`$ nosetests`

To check code style:
`$ pep8 ./`

## License
See COPYING file.
