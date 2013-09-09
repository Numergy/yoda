#!/usr/bin/env python

import os

from yoda.config import Config
from yoda.output import Output
from yoda.subcommands import Subcommands
from yoda.subcommand.workspace import Workspace

yoda_config = Config("%s/.yodarc" % os.environ.get("HOME"))
out = Output()

subcmd = Subcommands(yoda_config)
subcmd.add_command(Workspace())
parser = subcmd.parse()
args = subcmd.parser.parse_args()

try:
    subcmd.execute(args)
except Exception as e:
    out.error(e.message)
