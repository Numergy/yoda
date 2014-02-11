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

from yoda import find_path
from yoda.subcommands import Subcommand


class Jump(Subcommand, object):

    def setup(self, name, config, subparser):
        self.subparser = subparser
        self.logger = logging.getLogger(__name__)
        super(Jump, self).setup(name, config, subparser)

    def parse(self):
        to_parser = self.subparser.add_parser(
            'jump',
            help='Jump to directory',
            description="Jump to a workspace or repository root directory.")
        to_parser.add_argument('name', type=str,
                               help='Workspace or repository name')

    def execute(self, args):
        path_list = find_path(args.name, self.config, True)

        if len(path_list) == 0:
            self.logger.error("No matches for `%s`" % args.name)
            return False

        for name, path in path_list.items():
            return self.__jump(path)

    def __jump(self, path):
        self.logger.info("Spawn new shell on `%s`" % path)
        self.logger.info(
            "Use Ctrl-D to exit and go back to the previous directory")
        os.system("cd %s; YODA_JUMP_SESSION=%s %s"
                  % (path, path, os.getenv("SHELL")))
        self.logger.info("Shell on `%s` closed." % path)
