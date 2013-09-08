import argparse


class subcommand:
    config = None
    subparser = None

    def setup(self, config, subparser):
        self.config = config
        self.subparser = subparser


class subcommands:
    config = None
    parser = None
    subparser = None
    commands = {}

    def __init__(self, config):
        self.config = config

        self.parser = argparse.ArgumentParser(prog="yoda")
        self.subparser = self.parser.add_subparsers(dest="subcommand")

    def add_command(self, command):
        command.setup(self.config, self.subparser)
        self.commands[command.__class__.__name__] = command

    def parse(self):
        for key, command in self.commands.items():
            command.parse()

    def execute(self, args):
        if (args.subcommand in self.commands):
            self.commands[args.subcommand].execute(args)
