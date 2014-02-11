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

from prettytable import PrettyTable
from pycolorizer import Color

from yoda import find_path
from yoda import Output
from yoda import Repository
from yoda import RepositoryAdapterNotFound
from yoda.subcommands import Subcommand
from yoda import Workspace


class Show(Subcommand, object):

    workspace = None

    def setup(self, name, config, subparser):
        self.workspace = Workspace(config)
        self.subparser = subparser
        self.out = Output()
        super(Show, self).setup(name, config, subparser)

    def parse(self):
        """Parse show subcommand."""
        parser = self.subparser.add_parser(
            "show",
            help="Show workspace details",
            description="Show workspace details.")

        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--all', action='store_true', help="All workspaces")
        group.add_argument('name', type=str, help="Workspace name", nargs='?')

    def execute(self, args):
        """Execute show subcommand."""
        if args.name is not None:
            self.show_workspace(args.name)
        elif args.all is not None:
            self.show_all()

    def show_workspace(self, name):
        """Show specific workspace."""
        if not self.workspace.exists(name):
            raise ValueError("Workspace `%s` doesn't exists." % name)

        color = Color()
        workspaces = self.workspace.list()

        self.out.info("<== %s workspace ==>" % color.colored(name, "green"))
        self.out.info("\tPath: %s" % workspaces[name]["path"])
        self.out.info("\tNumber of repositories: %s"
                      % color.colored(
                          len(workspaces[name]["repositories"]),
                          "blue"))

        repo_colored = color.colored("Repositories", "blue")
        trepositories = PrettyTable(
            [repo_colored, "Path", "+"])
        trepositories.align[repo_colored] = "l"
        trepositories.align["Path"] = "l"

        for repo_name in workspaces[name]["repositories"]:
            fullname = "%s/%s" % (name, repo_name)
            fullpath = find_path(fullname, self.config)[fullname]
            try:
                repo = Repository(fullpath)
                repo_scm = repo.get_scm()
            except RepositoryAdapterNotFound:
                repo_scm = None
            trepositories.add_row(
                [color.colored(repo_name, "blue"), fullpath, repo_scm])

        self.out.info(trepositories)

    def show_all(self):
        """Show details for all workspaces."""
        for ws in self.workspace.list().keys():
            self.show_workspace(ws)
            self.out.info("\n\n")
