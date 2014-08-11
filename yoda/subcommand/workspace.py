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
from prettytable import PrettyTable
from pycolorizer import Color
from yoda import slashes2dash
from yoda.subcommands import Subcommand
from yoda import Workspace as Ws


class Workspace(Subcommand, object):
    ws = None
    subparser = None

    def setup(self, name, config, subparser):
        self.ws = Ws(config)
        self.subparser = subparser
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
        logger = logging.getLogger(__name__)
        if args.workspace_subcommand is None:
            self.parser.print_help()
            return None

        color = Color()
        if (args.workspace_subcommand == "add"):
            ws_name = slashes2dash(args.name)
            self.ws.add(ws_name, args.path)
            logger.info(color.colored(
                "Workspace `%s` successfuly added" % ws_name, "green"))
        elif (args.workspace_subcommand == "remove"):
            ws_name = slashes2dash(args.name)
            self.ws.remove(ws_name)
            logger.info(color.colored(
                "Workspace `%s` successfuly removed" % ws_name, "green"))
        elif (args.workspace_subcommand == "list"):
            table = PrettyTable(["Name", "Path"])
            table.align["Name"] = "l"
            table.align["Path"] = "l"
            for key, ws in sorted(self.ws.list().items()):
                table.add_row([key, ws["path"]])

            logger.info(table)

    def load_workspaces_subcommands(self, subcmd):
        for key, value in self.ws.list().items():
            ws_subcmds = WorkspaceSubcommands(key, self.subparser, self.config)
            subcmd.commands[key] = ws_subcmds


class WorkspaceSubcommands():
    name = None
    parser = None
    config = None

    def __init__(self, name, subparser, config):
        """Initialize workspace name."""
        self.name = name
        self.parser = subparser.add_parser(
            name,
            description="Manage repositories in %s workspace" % name)
        self.config = config

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
        logger = logging.getLogger(__name__)
        ws = Ws(self.config)

        if (args.action == "add"):
            repo_name = slashes2dash(args.repo_name)
            ws.add_repo(args.subcommand, repo_name, args.url, args.path)
            logger.info("Repository `%s` added to `%s` workspace." %
                        (repo_name, args.subcommand))
        elif (args.action == "remove"):
            repo_name = slashes2dash(args.repo_name)
            ws.rm_repo(args.subcommand, repo_name)
            logger.info("Repository `%s` removed from `%s` workspace." %
                        (repo_name, args.subcommand))
        elif (args.action == "sync"):
            ws.sync(args.subcommand)
            logger.info("Workspace `%s` synchronized." % args.subcommand)
