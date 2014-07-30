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


class Update(Subcommand, object):

    def setup(self, name, config, subparser):
        self.subparser = subparser
        self.logger = logging.getLogger(__name__)
        super(Update, self).setup(name, config, subparser)

    def parse(self):
        """Parse update subcommand."""
        parser = self.subparser.add_parser(
            "update",
            help="Update repositories",
            description="Update one or more repositories.")

        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--all', action='store_true', help="All workspaces")
        group.add_argument('name', type=str, help="Repo name", nargs='?')

    def execute(self, args):
        """Execute update subcommand."""
        if args.name is not None:
            self.print_workspace(args.name)
        elif args.all is not None:
            self.print_all()

    def print_all(self):
        """Print all workspaces update."""
        for ws_name in self.config['workspaces']:
            self.print_workspace(ws_name)

    def print_workspace(self, name):
        """Print workspace update."""
        path_list = find_path(name, self.config)

        if len(path_list) == 0:
            self.logger.error("No matches for `%s`" % name)
            return False

        for name, path in path_list.items():
            self.print_update(name, path)

    def print_update(self, repo_name, repo_path):
        """Print repository update."""
        color = Color()
        self.logger.info(color.colored(
            "=> [%s] %s" % (repo_name, repo_path), "green"))
        try:
            repo = Repository(repo_path)
            repo.update()
        except RepositoryError as e:
            self.logger.error(e)
            pass
        print("\n")
