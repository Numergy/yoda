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

from pycolorizer import Color

from yoda import find_path
from yoda import Repository
from yoda import RepositoryError
from yoda.subcommands import Subcommand


class Status(Subcommand, object):

    def setup(self, name, config, subparser):
        self.subparser = subparser
        self.logger = logging.getLogger(__name__)
        super(Status, self).setup(name, config, subparser)

    def parse(self):
        """Parse status subcommand."""
        parser = self.subparser.add_parser(
            "status",
            help="Show repositories status",
            description="Show repositories status from name.")

        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--all', action='store_true', help="All workspaces")
        group.add_argument('name', type=str, help="Repo name", nargs='?')

    def execute(self, args):
        """Execute status subcommand."""
        if args.name is not None:
            self.print_workspace(args.name)
        elif args.all is not None:
            self.print_all()

    def print_all(self):
        """Print all workspaces status."""
        for ws_name in self.config['workspaces']:
            self.print_workspace(ws_name)

    def print_workspace(self, name):
        """Print workspace status."""
        path_list = find_path(name, self.config)

        if len(path_list) == 0:
            self.logger.error("No matches for `%s`" % name)
            return False

        for name, path in path_list.items():
            self.print_status(name, path)

    def print_status(self, repo_name, repo_path):
        """Print repository status."""
        color = Color()
        self.logger.info(color.colored(
            "=> [%s] %s" % (repo_name, repo_path), "green"))
        try:
            repo = Repository(repo_path)
            repo.status()
        except RepositoryError as e:
            self.logger.error(e)
            pass
        print("\n")
