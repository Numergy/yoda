#!/usr/bin/env python

import os

from yoda.subcommands import subcommands
from yoda.workspace import workspace
from yoda.config import config

subcmd = subcommands()
parser = subcmd.parse()
args = parser.parse_args()

config = config("%s/.yodarc" % os.environ.get("HOME"))

if (args.subcommand == "workspace"):
    ws = workspace(config)
    if (args.workspace_subcommand == "add"):
        ws.add(args.name, args.path)
    elif (args.workspace_subcommand == "remove"):
        ws.remove(args.name)
    if (args.workspace_subcommand == "list"):
        for name, path in ws.list().items():
            print("%s\t=>\t%s" % (name, path))
elif (args.subcommand == "status"):
    print("status")
elif (args.subcommand == "update"):
    print("update")
