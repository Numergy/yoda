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

import logging
import shutil

import os
from pycolorizer import Color
from yoda import Config
from yoda import Repository
from yoda.repository import clone
from yoda import RepositoryError
from yoda import yn_choice


class Workspace:

    config = None

    def __init__(self, config):
        """Workspace object initialization."""
        if not isinstance(config, Config):
            raise TypeError("Variable config is not an instance of Config")
        self.config = config

    def add(self, name, path):
        """Add a workspace entry in user config file."""
        if not (os.path.exists(path)):
            raise ValueError("Workspace path `%s` doesn't exists." % path)

        if (self.exists(name)):
            raise ValueError("Workspace `%s` already exists." % name)

        self.config["workspaces"][name] = {"path": path, "repositories": {}}
        self.config.write()

    def remove(self, name):
        """Remove workspace from config file."""
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

    def sync(self, ws_name):
        """Synchronise workspace's repositories."""
        path = self.config["workspaces"][ws_name]["path"]
        repositories = self.config["workspaces"][ws_name]["repositories"]

        logger = logging.getLogger(__name__)
        color = Color()

        for r in os.listdir(path):
            try:
                repo = Repository(os.path.join(path, r))
            except RepositoryError:
                continue
            else:
                repositories[r] = repo.path

        for repo_name, path in repositories.items():
            logger.info(color.colored(
                " - %s" % repo_name, "blue"))

        self.config["workspaces"][ws_name]["repositories"]
        self.config.write()

    def rm_repo(self, wname, rname):
        if (rname not in self.config["workspaces"][wname]["repositories"]):
            raise ValueError(
                "%s not found in %s workspace" % (rname, wname))

        repo_path = self.config["workspaces"][wname]["repositories"][rname]
        del self.config["workspaces"][wname]["repositories"][rname]

        self.config.write()

        if (yn_choice("Do you want to delete this repository?")):
            shutil.rmtree(repo_path)

    def add_repo(self, wname, rname, url=None, path=None):
        ws = self.config["workspaces"][wname]
        repo_path = ws["path"] + "/" + rname if path is None else path

        if ("repositories" not in ws):
            ws["repositories"] = {}

        if (rname in ws["repositories"]):
            raise ValueError("Repository %s already exists" % rname)

        result = None
        if url is not None:
            result = clone(url, repo_path)

        if result is not None and result.returncode != 0:
            raise RepositoryError("Can't clone this repository")

        if (os.path.exists(repo_path) is False):
            os.mkdir(repo_path)

        self.config["workspaces"][wname] = ws
        self.config["workspaces"][wname]["repositories"][rname] = repo_path
        self.config.write()
