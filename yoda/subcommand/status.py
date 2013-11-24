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

from yoda.subcommands import Subcommand
from yoda import Repository, Output, Workspace


class Status(Subcommand):
    subparser = None
    config = None
    out = None
    matched = False

    def setup(self, name, config, subparser):
        self.subparser = subparser
        self.config = config
        self.out = Output()
        Subcommand.setup(self, name, self.config, subparser)

    def parse(self):
        """ Parse status subcommand """
        self.parser.add_argument(
            "name", type=str, help="Repo name")

    def execute(self, args):
        """ Execute status subcommand """
        workspace = Workspace(self.config)
        config = self.config.get()["workspaces"]

        #FIXME: Duplicate from Jump
        if args.name.find('/') != -1:
            result = args.name.split('/')
            if (workspace.exists(result[0])):
                if (result[1] in config[result[0]]["repositories"]):
                    self.matched = True
                    path = config[result[0]]["repositories"][result[1]]
                    return self.print_status(result[1], path)

        for ws_name, ws in sorted(config.items()):
            if (args.name == ws_name):
                repositories = sorted(config[ws_name]["repositories"].items())
                for name, path in repositories:
                    self.matched = True
                    self.print_status(name, path)
                return None

            for name, path in sorted(ws["repositories"].items()):
                if (args.name == name):
                    self.matched = True
                    self.print_status(name, path)

        if not self.matched:
            self.out.error("No matches for `%s`" % args.name)
            return False

    def print_status(self, repo_name, repo_path):
        """ Print repository status """
        try:
            repo = Repository(repo_path)
            self.out.success(
                "=> [%s] %s" % (repo_name, repo_path))
            repo.status()
            self.out.info("\n")
        except ValueError as e:
            self.out.error(e)
            pass
