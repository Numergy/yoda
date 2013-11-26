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

from os import listdir
from os.path import join, exists
from yoda import Config, Repository


class Workspace:

    config = None

    def __init__(self, config):
        """ Workspace object initialization """
        if not isinstance(config, Config):
            raise TypeError("Variable config is not an instance of Config")
        self.config = config

    def add(self, name, path):
        """ Add a workspace entry in user config file """
        if not (exists(path)):
            raise ValueError("Workspace path `%s` doesn't exists." % path)

        if (self.exists(name)):
            raise ValueError("Workspace `%s` already exists." % name)

        config = self.config.get()
        config["workspaces"][name] = {"path": path, "repositories": {}}

        self.config.write(config)

    def remove(self, name):
        """ Remove workspace from config file """
        config = self.config.get()

        if not (self.exists(name)):
            raise ValueError("Workspace `%s` doesn't exists." % name)

        config["workspaces"].pop(name, 0)

        self.config.write(config)

    def list(self):
        """ List all available workspaces """
        config = self.config.get()
        ws_list = {}

        for key, value in config["workspaces"].items():
            ws_list[key] = dict({"name": key}, **value)

        return ws_list

    def sync(self, name):
        """ Return workspace's repositories list """
        if not self.exists(name):
            raise ValueError("Unknown workspace `%s`" % name)

        config = self.config.get()
        path = config["workspaces"][name]["path"]
        repositories = config["workspaces"][name]["repositories"]

        repo_list = {}

        for r in listdir(path):
            repo = Repository(join(path, r))

            if repo.is_valid():
                repositories[r] = repo.path
                repo_list[r] = repo.path

        self.config.write(config)
        return repo_list

    def exists(self, name):
        """ Check if given workspace name exists """
        return name in self.list().keys()

    def repository_exists(self, workspace, repo):
        """ Return True if workspace contains repository name. """
        if not self.exists(workspace):
            return False

        workspaces = self.list()
        return repo in workspaces[workspace]["repositories"]
