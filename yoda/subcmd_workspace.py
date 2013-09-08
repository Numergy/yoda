from yoda.workspace import workspace as Workspace
from yoda.subcommands import subcommand


class workspace(subcommand):
    ws = None

    def setup(self, config, subparser):
        self.ws = Workspace(config)
        subcommand.setup(self, config, subparser)

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

    def execute(self, args):
        if (args.workspace_subcommand == "add"):
            self.ws.add(args.name, args.path)
        elif (args.workspace_subcommand == "remove"):
            self.ws.remove(args.name)
        elif (args.workspace_subcommand == "list"):
            for name, path in self.ws.list().items():
                print("%s\t=>\t%s" % (name, path))
