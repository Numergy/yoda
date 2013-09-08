#!/usr/bin/env python

import os

from yoda.config import config
from yoda.subcommands import subcommands
from yoda.subcmd_workspace import workspace

yoda_config = config("%s/.yodarc" % os.environ.get("HOME"))

subcmd = subcommands(yoda_config)
subcmd.add_command(workspace())
parser = subcmd.parse()
args = subcmd.parser.parse_args()

subcmd.execute(args)
