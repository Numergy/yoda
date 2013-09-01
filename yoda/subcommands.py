import argparse

from yoda.workspace import workspace as Workspace


class subcommand:
    config = None
    subparser = None

    def __init__(self, config, subparser):
        self.config = config
        self.subparser = subparser


class workspace(subcommand):
    ws = None

    def __init__(self, config, subparser):
        self.ws = Workspace(config)
        subcommand.__init__(self, config, subparser)

    def parse(self):
        parser = self.subparser.add_parser("workspace")
        subparser = parser.add_subparsers(
            dest="workspace_subcommand")

        add_parser = subparser.add_parser(
            "add", help="Add workspace")
        rm_parser = subparser.add_parser(
            "remove", help="Remove existing workspace")
        subparser.add_parser(
            "list", help="Show registered workspace")

        add_parser.add_argument("name", type=str, help="Workspace name")
        add_parser.add_argument("path", type=str, help="Workspace path")
        rm_parser.add_argument("name", type=str, help="Workspace name")

    def exec(self, args):
        if (args.workspace_subcommand == "add"):
            self.ws.add(args.name, args.path)
        elif (args.workspace_subcommand == "remove"):
            self.ws.remove(args.name)
        elif (args.workspace_subcommand == "list"):
            for name, path in self.ws.list().items():
                print("%s\t=>\t%s" % (name, path))


class subcommands:
    config = None
    parser = None
    workspace = None

    def __init__(self, config):
        self.config = config

        self.parser = argparse.ArgumentParser(prog="yoda")
        subparsers = self.parser.add_subparsers(dest="subcommand")
        self.workspace = workspace(config, subparsers)

    def parse(self):
        self.workspace.parse()

    def exec(self, args):
        if (args.subcommand == "workspace"):
            self.workspace.exec(args)
