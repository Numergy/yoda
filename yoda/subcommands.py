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

import argparse


class Subcommand:
    config = None
    parser = None

    def setup(self, name, config, subparser):
        self.parser = subparser.add_parser(name)
        self.config = config


class Subcommands:
    config = None
    parser = None
    subparser = None
    commands = {}

    def __init__(self, config):
        self.config = config

        self.parser = argparse.ArgumentParser(prog="yoda")
        self.subparser = self.parser.add_subparsers(dest="subcommand")

    def add_command(self, command):
        command_name = command.__class__.__name__.lower()
        command.setup(command_name, self.config, self.subparser)
        self.commands[command_name] = command

    def parse(self):
        for key, command in self.commands.items():
            command.parse()

    def execute(self, args):
        if args.subcommand is None:
            self.parser.print_help()
            return None

        if (args.subcommand in self.commands):
            self.commands[args.subcommand].execute(args)
