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

import os.path
from yoda import Config


class Workspace:

    config = None

    def __init__(self, config):
        """ Workspace object initialization """
        if not isinstance(config, Config):
            raise TypeError("Variable config is not an instance of Config")
        self.config = config

    def add(self, name, path):
        """ Add a workspace entry in user config file """
        if not (os.path.exists(path)):
            raise ValueError("Workspace path `%s` dosn't exists." % path)

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

    def exists(self, name):
        """ Check if given workspace name exists """
        list = self.list()
        return name in list.keys()
