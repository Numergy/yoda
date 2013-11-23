from yoda.workspace import Workspace as Ws
from yoda.subcommands import Subcommand
from yoda.output import Output


class Workspace(Subcommand):
    ws = None

    def setup(self, name, config, subparser):
        self.ws = Ws(config)
        Subcommand.setup(self, name, config, subparser)

    def parse(self):
        subparser = self.parser.add_subparsers(
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
        if args.workspace_subcommand is None:
            self.parser.print_help()
            return None

        out = Output()
        if (args.workspace_subcommand == "add"):
            self.ws.add(args.name, args.path)
            out.success("Workspace `%s` successfuly added" % args.name)
        elif (args.workspace_subcommand == "remove"):
            self.ws.remove(args.name)
            out.success("Workspace `%s` successfuly removed" % args.name)
        elif (args.workspace_subcommand == "list"):
            for name, ws in self.ws.list().items():
                out.success("%s" % name)
                out.info("\tpath: %s\n\n" % (ws["path"]))
