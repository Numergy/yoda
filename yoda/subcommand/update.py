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
from yoda import find_path, Repository, Output


class Update(Subcommand):

    def setup(self, name, config, subparser):
        self.subparser = subparser
        self.out = Output()
        super(Update, self).setup(name, config, subparser)

    def parse(self):
        """ Parse update subcommand """
        parser = self.subparser.add_parser(
            "update",
            help="Show repositories update",
            description="Show repositories update from name.")
        parser.add_argument(
            "name", type=str, help="Repo name")

    def execute(self, args):
        """ Execute update subcommand """
        path_list = find_path(args.name, self.config)

        if len(path_list) == 0:
            self.out.error("No matches for `%s`" % args.name)
            return False

        for name, path in path_list.items():
            self.print_update(name, path)

    def print_update(self, repo_name, repo_path):
        """ Print repository update """
        try:
            repo = Repository(repo_path)
            self.out.success(
                "=> [%s] %s" % (repo_name, repo_path))
            repo.update()
            self.out.info("\n")
        except ValueError as e:
            self.out.error(e)
            pass
