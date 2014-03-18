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
from yoda.subcommands import Subcommand


class Config(Subcommand, object):
    logger = None

    def setup(self, name, config, subparser):
        self.subparser = subparser
        self.logger = logging.getLogger(__name__)
        super(Config, self).setup(name, config, subparser)

    def parse(self):
        parser = self.subparser.add_parser(
            "config",
            help='Get and set global configurations')
        subparser = parser.add_subparsers(
            dest="action")

        set_parser = subparser.add_parser(
            "set",
            help="Set global configuration")
        set_parser.add_argument(
            "key",
            help="Configuration key")
        set_parser.add_argument(
            "value",
            help="Configuration value")
        get_parser = subparser.add_parser(
            "get",
            help="get global configuration")
        get_parser.add_argument(
            "key",
            help="Configuration key")

    def execute(self, args):
        if args.action == "set":
            if args.key.lower() != "workspaces":
                self.config[args.key] = args.value
            else:
                self.logger.error("Key \"workspaces\" is protected")
        elif args.action == "get":
            self.logger.info(self.config.get(args.key))
