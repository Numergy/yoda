#!/usr/bin/env python

import argparse
import os

from yoda.workspace import workspace
from yoda.config import config

parser = argparse.ArgumentParser(prog="yoda")
subparsers = parser.add_subparsers(dest="subcommand")

workspace_parser = subparsers.add_parser("workspace")
workspace_subparsers = workspace_parser.add_subparsers(
    dest="workspace_subcommand")

workspace_add_parser = workspace_subparsers.add_parser(
    "add", help="Add workspace")
workspace_rm_parser = workspace_subparsers.add_parser(
    "remove", help="Remove existing workspace")
workspace_subparsers.add_parser(
    "list", help="Show registered workspace")

workspace_add_parser.add_argument("name", type=str, help="Workspace name")
workspace_add_parser.add_argument("path", type=str, help="Workspace path")
workspace_rm_parser.add_argument("name", type=str, help="Workspace name")


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
