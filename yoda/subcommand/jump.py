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

from yoda import Output
from yoda.subcommands import Subcommand


class Jump(Subcommand):

    def setup(self, name, config, subparser):
        self.subparser = subparser
        super(Jump, self).setup(name, config, subparser)

    def parse(self):
        to_parser = self.subparser.add_parser('jump', help='Jump to directory')
        to_parser.add_argument('to', type=str, help='Where to jump')

    def execute(self, args):
        config = self.config.get()["workspaces"]

        if args.to.find('/') != -1:
            result = args.to.split('/')
            if (result[0] in config):
                if (result[1] in config[result[0]]["repositories"]):
                    path = config[result[0]]["repositories"][result[1]]
                    return self.__jump(path)

        for ws_name, ws in config.items():
            if (args.to == ws_name):
                return self.__jump(ws["path"])

            for repo_name, repo_path in ws["repositories"].items():
                if (args.to == repo_name):
                    return self.__jump(repo_path)

    def __jump(self, path):
        out = Output()
        out.info("Spawn new shell on `%s`" % path)
        out.info("Use Ctrl-D (i.e. EOF) to exit and go back to the previous directory")
        os.system("cd %s; %s" % (path, os.getenv("SHELL")))
        out.info("Shell on `%s` closed." % path)
