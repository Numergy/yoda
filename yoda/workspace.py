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

from os.path import exists
from yoda import Config


class Workspace:

    config = None

    def __init__(self, config):
        """Workspace object initialization."""
        if not isinstance(config, Config):
            raise TypeError("Variable config is not an instance of Config")
        self.config = config

    def add(self, name, path):
        """Add a workspace entry in user self.config file."""
        if not (exists(path)):
            raise ValueError("Workspace path `%s` doesn't exists." % path)

        if (self.exists(name)):
            raise ValueError("Workspace `%s` already exists." % name)

        self.config["workspaces"][name] = {"path": path, "repositories": {}}
        self.config.write()

    def remove(self, name):
        """Remove workspace from self.config file."""
        if not (self.exists(name)):
            raise ValueError("Workspace `%s` doesn't exists." % name)

        self.config["workspaces"].pop(name, 0)
        self.config.write()

    def list(self):
        """List all available workspaces."""
        ws_list = {}

        for key, value in self.config["workspaces"].items():
            ws_list[key] = dict({"name": key}, **value)

        return ws_list

    def get(self, name):
        """
        Get workspace infos from name.
        Return None if workspace doesn't exists.
        """
        ws_list = self.list()
        return ws_list[name] if name in ws_list else None

    def exists(self, name):
        """Check if given workspace name exists."""
        return name in self.list().keys()

    def repository_exists(self, workspace, repo):
        """Return True if workspace contains repository name."""
        if not self.exists(workspace):
            return False

        workspaces = self.list()
        return repo in workspaces[workspace]["repositories"]
