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

from yoda import Output, find_path
from yoda.subcommands import Subcommand


class Jump(Subcommand):

    def setup(self, name, config, subparser):
        self.subparser = subparser
        self.out = Output()
        super(Jump, self).setup(name, config, subparser)

    def parse(self):
        to_parser = self.subparser.add_parser('jump', help='Jump to directory')
        to_parser.add_argument('to', type=str, help='Where to jump')

    def execute(self, args):
        path_list = find_path(args.to, self.config)

        if len(path_list) == 0:
            self.out.error("No matches for `%s`" % args.to)
            return False

        for name, path in path_list.items():
            return self.jump(path)

    def jump(self, path):
        self.out.info("Spawn new shell on `%s`" % path)
        self.out.info(
            "Use Ctrl-D to exit and go back to the previous directory")
        os.system("cd %s; %s" % (path, os.getenv("SHELL")))
        self.out.info("Shell on `%s` closed." % path)
