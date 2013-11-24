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
from yoda import Repository, Output


class Status(Subcommand):
    subparser = None
    config = None

    def setup(self, name, config, subparser):
        self.subparser = subparser
        self.config = config
        Subcommand.setup(self, name, self.config, subparser)

    def parse(self):
        """ Parse status subcommand """
        self.parser.add_argument(
            "name", type=str, help="Repo name")

    def execute(self, args):
        """ Execute status subcommand """
        out = Output()

        config = self.config.get()
        for name, path in config["workspaces"][args.name]["repositories"].items():
            repo = Repository(path)
            out.success("=> %s" % path)
            repo.status()
            out.info("\n")
