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

import os
import shutil

from yoda.workspace import Workspace as Ws
from yoda.subcommands import Subcommand
from yoda.output import Output


class Workspace(Subcommand):
    ws = None
    subparser = None
    config = None

    def setup(self, name, config, subparser):
        self.ws = Ws(config)
        self.subparser = subparser
        self.config = config
        Subcommand.setup(self, name, self.config, subparser)

    def parse(self):
        subparser = self.parser.add_subparsers(
            dest="workspace_subcommand")

        add_parser = subparser.add_parser(
            "add", help="Add workspace")
        rm_parser = subparser.add_parser(
            "remove", help="Remove existing workspace")
        subparser.add_parser(
            "list", help="Show registered workspace")
        sync_parser = subparser.add_parser(
            "sync", help="Synchronize all directories store in workspace")

        add_parser.add_argument("name", type=str, help="Workspace name")
        add_parser.add_argument("path", type=str, help="Workspace path")
        rm_parser.add_argument("name", type=str, help="Workspace name")
        sync_parser.add_argument(
            "name", type=str, help="Workspace name", nargs='?'
        )

    def execute(self, args):
        if args.workspace_subcommand is None:
            self.parser.print_help()
            return None

        out = Output()
        if (args.workspace_subcommand == "add"):
            self.ws.add(args.name, args.path)
            out.success("Workspace `%s` successfuly added" % args.name)
        elif (args.workspace_subcommand == "remove"):
            self.ws.remove(args.name)
            out.success("Workspace `%s` successfuly removed" % args.name)
        elif (args.workspace_subcommand == "sync"):
            repo_list = self.ws.sync(args.name)
            out.success("Workspace `%s` synchronized" % args.name)
            out.success("Added %d repositories:" % len(repo_list))
            for repo_name, path in repo_list.items():
                out.success(
                    out.color.colored(
                        " - %s" % repo_name, "blue"
                    )
                )
        elif (args.workspace_subcommand == "list"):
            color = out.color
            messages = []
            for name, ws in self.ws.list().items():
                messages.append(
                    color.colored(
                        (" - %s" % name),
                        fgcolor="green",
                        attrs=["dark"]
                    )
                )
                messages.append(
                    color.colored("\t - path: ", "blue") + "%s" % ws["path"]
                )

                repositories = ws["repositories"] \
                    if "repositories" in ws else {}
                if len(repositories) > 0:
                    messages.append(
                        out.color.colored("\t - repositories:", "blue"))
                    for repo_name, repo_path in repositories.items():
                        messages.append(
                            out.color.colored(
                                "\t\t - %s:\t" % repo_name, "cyan")
                            + "%s" % repo_path)
            out.info("\n".join(messages))

    def load_workspaces_subcommands(self, subcmd):
        for key, value in self.ws.list().items():
            ws_subcmds = WorkspaceSubcommands(key, self.subparser, self.config)
            subcmd.commands[key] = ws_subcmds


class WorkspaceSubcommands():
    name = None
    parser = None
    config = None

    def __init__(self, name, subparser, config):
        """ Initialize workspace name """
        self.name = name
        self.parser = subparser.add_parser(name)
        self.config = config

    def parse(self):
        subparser = self.parser.add_subparsers(
            dest="action")

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
            "remove", help=("Remove repository to %s workspace" % self.name))

        remove_parser.add_argument(
            "repo_name", type=str, help="Repository name"
        )

    def execute(self, args):
        if (args.action == "add"):
            self.add(args.subcommand, args.repo_name, args.url, args.path)
        elif (args.action == "remove"):
            self.remove(args.subcommand, args.repo_name)

    def add(self, ws_name, repo_name, url, path):
        config = self.config.get()
        ws = config["workspaces"][ws_name]
        repo_path = ws["path"] + "/" + repo_name if path is None else path

        if ("repositories" not in ws):
            ws["repositories"] = {}

        if (repo_name in ws["repositories"]):
            raise ValueError("Repository %s already exists" % repo_name)
        else:
            if (os.path.exists(repo_path) is False):
                os.mkdir(repo_path)
            #TODO: Implement clone from url

            ws["repositories"][repo_name] = repo_path
            self.config.write(config)
            out = Output()
            out.success("Repository %s added" % repo_name)

    def remove(self, ws_name, repo_name):
        config = self.config.get()
        ws = config["workspaces"][ws_name]
        if (repo_name not in config["workspaces"][ws_name]["repositories"]):
            raise ValueError(
                "%s not found in %s workspace" % (repo_name, ws_name)
            )

        repo_path = config["workspaces"][ws_name]["repositories"][repo_name]
        del config["workspaces"][ws_name]["repositories"][repo_name]
        self.config.write(config)
        out = Output()
        if (out.yn_choice("Do you want to delete this repository?")):
            shutil.rmtree(repo_path)
