#!/usr/bin/env python

import os

from yoda.config import config
from yoda.output import output
from yoda.subcommands import subcommands
from yoda.subcommand.workspace import workspace

yoda_config = config("%s/.yodarc" % os.environ.get("HOME"))
out = output()

subcmd = subcommands(yoda_config)
subcmd.add_command(workspace())
parser = subcmd.parse()
args = subcmd.parser.parse_args()

try:
    subcmd.execute(args)
except Exception as e:
    out.error(e.message)
