import argparse


class subcommand:
    subparser = None

    def __init__(self, subparser):
        self.subparser = subparser


class workspace(subcommand):

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


class subcommands:
    workspace = None

    def parse(self):
        parser = argparse.ArgumentParser(prog="yoda")
        subparsers = parser.add_subparsers(dest="subcommand")

        ws = workspace(subparsers)
        ws.parse()

        return parser
