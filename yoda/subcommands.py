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
