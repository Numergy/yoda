from yoda.workspace import Workspace as Ws
from yoda.subcommands import Subcommand
from yoda.output import Output


class Workspace(Subcommand):
    ws = None
    subparser = None

    def setup(self, name, config, subparser):
        self.ws = Ws(config)
        self.subparser = subparser
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
            color = out.color
            messages = []
            for name, ws in self.ws.list().items():
                messages.append(
                    color.colored(
                        (" - %s" % name),
                        fgcolor="green",
                        attrs=["dark"]
                    )
                )
                messages.append(
                    color.colored("\t - path: ", "blue") + "%s" % ws["path"]
                )
                if ("repositories" in ws):
                    messages.append(
                        out.color.colored("\t - repositories:", "cyan")
                    )
                    for repo_name, repo_path in ws["repositories"].items():
                        messages.append(
                            out.color.colored("\t\t - name: ", "blue")
                            + "%s" % repo_name
                        )
                        messages.append(
                            out.color.colored("\t\t - path: ", "blue")
                            + "%s" % repo_path
                        )
            out.info("\n".join(messages))

    def load_workspaces_subcommands(self, subcmd):
        for key, value in self.ws.list().items():
            ws_subcmds = WorkspaceSubcommands(key, self.subparser)
            subcmd.commands[key] = ws_subcmds


class WorkspaceSubcommands():
    name = None
    parser = None

    def __init__(self, name, subparser):
        """ Initialize workspace name """
        self.name = name
        self.parser = subparser.add_parser(name)

    def parse(self):
        subparser = self.parser.add_subparsers(
            dest="%s_subcommand" % self.name)

        add_parser = subparser.add_parser(
            "add", help="Add repositories to %s workspace" % self.name)

        add_parser.add_argument("repo_name", type=str, help="Repository name")

    def execute(self, args):
        print("TODO: Implement me!")
