# This source file is part of Yoda.
#
# Yoda is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Yoda is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Yoda. If not, see <http://www.gnu.org/licenses/gpl-3.0.html>.


def find_path(name, config, wsonly=False):
    """Find path for given workspace and|or repository."""
    workspace = Workspace(config)
    config = config["workspaces"]

    path_list = {}

    if name.find('/') != -1:
        wsonly = False
        try:
            ws, repo = name.split('/')
        except ValueError:
            raise ValueError("There is too many / in `name` argument. "
                             "Argument syntax: `workspace/repository`.")
        if (workspace.exists(ws)):
            if (repo in config[ws]["repositories"]):
                path_name = "%s/%s" % (ws, repo)
                path_list[path_name] = config[ws]["repositories"][repo]

    for ws_name, ws in sorted(config.items()):
        if (name == ws_name):
            if wsonly is True:
                return {ws_name: ws["path"]}
            repositories = sorted(config[ws_name]["repositories"].items())
            for name, path in repositories:
                path_list["%s/%s" % (ws_name, name)] = path
            break

        for repo_name, repo_path in sorted(ws["repositories"].items()):
            if (repo_name == name):
                path_list["%s/%s" % (ws_name, repo_name)] = repo_path

    return path_list


def slashes2dash(string):
    """Replace slashes in given string to dash."""
    return string.replace("/", "-")


def yn_choice(message, default='n'):
    choices = 'Y/n' if default.lower() in ('y', 'yes') else 'y/N'
    choice = input("%s (%s) " % (message, choices))
    values = ('y', 'yes', '') if default == 'y' else ('y', 'yes')
    return choice.strip().lower() in values

from yoda.config import Config
from yoda.logger import Logger
from yoda.repository import Repository
from yoda.repository import RepositoryAdapterNotFound
from yoda.repository import RepositoryError
from yoda.repository import RepositoryPathInvalid
from yoda.subcommands import Subcommand
from yoda.subcommands import Subcommands
from yoda.workspace import Workspace
