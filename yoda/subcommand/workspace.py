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
import os
import shutil

from os import listdir
from os.path import join
from prettytable import PrettyTable
from pycolorizer import Color

from yoda import Repository
from yoda.repository import clone
from yoda import RepositoryError
from yoda.subcommands import Subcommand
from yoda import Workspace as Ws
from yoda import yn_choice


class Workspace(Subcommand, object):
    ws = None
    subparser = None
    logger = None

    def setup(self, name, config, subparser):
        self.ws = Ws(config)
        self.subparser = subparser
        self.logger = logging.getLogger(__name__)
        super(Workspace, self).setup(name, config, subparser)

    def parse(self):
        parser = self.subparser.add_parser(
            "workspace",
            help="Workspace managment",
            description="Manage repository's workspace")
        subparser = parser.add_subparsers(
            dest="workspace_subcommand")

        add_parser = subparser.add_parser(
            "add", help="Add workspace")
        rm_parser = subparser.add_parser(
            "remove", help="Remove existing workspace")
        subparser.add_parser(
            "list", help="Show registered workspace")

        add_parser.add_argument("name", type=str, help="Workspace name")
        add_parser.add_argument("path", type=str, help="Workspace path")
        rm_parser.add_argument("name", type=str, help="Workspace name")

    def execute(self, args):
        if args.workspace_subcommand is None:
            self.parser.print_help()
            return None

        color = Color()
        if (args.workspace_subcommand == "add"):
            self.ws.add(args.name, args.path)
            self.logger.info(color.colored(
                "Workspace `%s` successfuly added" % args.name, "green"))
        elif (args.workspace_subcommand == "remove"):
            self.ws.remove(args.name)
            self.logger.info(color.colored(
                "Workspace `%s` successfuly removed" % args.name, "green"))
        elif (args.workspace_subcommand == "list"):
            table = PrettyTable(["Name", "Path"])
            table.align["Name"] = "l"
            table.align["Path"] = "l"
            for key, ws in sorted(self.ws.list().items()):
                table.add_row([key, ws["path"]])

            self.logger.info(table)

    def load_workspaces_subcommands(self, subcmd):
        for key, value in self.ws.list().items():
            ws_subcmds = WorkspaceSubcommands(key, self.subparser, self.config)
            subcmd.commands[key] = ws_subcmds


class WorkspaceSubcommands():
    name = None
    parser = None
    config = None
    logger = None

    def __init__(self, name, subparser, config):
        """Initialize workspace name."""
        self.name = name
        self.parser = subparser.add_parser(
            name,
            description="Manage repositories in %s workspace" % name)
        self.config = config
        self.logger = logging.getLogger(__name__)

    def parse(self):
        subparser = self.parser.add_subparsers(dest="action")

        add_parser = subparser.add_parser(
            "add", help=("Add repository to %s workspace" % self.name))

        add_parser.add_argument("repo_name", type=str, help="Repository name")
        add_parser.add_argument(
            "-u", "--url",
            type=str, help="Repository url",
            default=None, nargs='?'
        )
        add_parser.add_argument(
            "-p", "--path",
            type=str, help="Repository path",
            default=None, nargs='?'
        )

        remove_parser = subparser.add_parser(
            "remove", help=("Remove repository from %s workspace" % self.name))
        remove_parser.add_argument(
            "repo_name", type=str, help="Repository name"
        )

        sync_parser = subparser.add_parser(
            "sync", help="Synchronize all directories store in workspace"
        )
        sync_parser.add_argument(
            "name", type=str, help="Workspace name", nargs='?'
        )

    def execute(self, args):
        if (args.action == "add"):
            self.add(args.subcommand, args.repo_name, args.url, args.path)
        elif (args.action == "remove"):
            self.remove(args.subcommand, args.repo_name)
        elif (args.action == "sync"):
            self.sync(args.subcommand)

    def add(self, ws_name, repo_name, url, path):
        ws = self.config["workspaces"][ws_name]
        repo_path = ws["path"] + "/" + repo_name if path is None else path

        if ("repositories" not in ws):
            ws["repositories"] = {}

        if (repo_name in ws["repositories"]):
            raise ValueError("Repository %s already exists" % repo_name)

        if url is not None:
            clone(url, repo_path)

        if (os.path.exists(repo_path) is False):
            os.mkdir(repo_path)

        ws["repositories"][repo_name] = repo_path
        self.logger.info("Repository %s added" % repo_name)

    def remove(self, ws_name, repo_name):
        config = self.config
        if (repo_name not in config["workspaces"][ws_name]["repositories"]):
            raise ValueError(
                "%s not found in %s workspace" % (repo_name, ws_name)
            )

        repo_path = config["workspaces"][ws_name]["repositories"][repo_name]
        del config["workspaces"][ws_name]["repositories"][repo_name]

        if (yn_choice("Do you want to delete this repository?")):
            shutil.rmtree(repo_path)

    def sync(self, ws_name):
        """Synchronise workspace's repositories."""
        path = self.config["workspaces"][ws_name]["path"]
        repositories = self.config["workspaces"][ws_name]["repositories"]

        repo_list = {}

        for r in listdir(path):
            try:
                repo = Repository(join(path, r))
            except RepositoryError:
                continue
            else:
                repositories[r] = repo.path
                repo_list[r] = repo.path

        logger = logging.getLogger(__name__)
        color = Color()
        logger.info("Workspace `%s` synchronized" % ws_name)
        logger.info("Added %d repositories:" % len(repo_list))
        for repo_name, path in repo_list.items():
            logger.info(color.colored(
                " - %s" % repo_name, "blue"))
