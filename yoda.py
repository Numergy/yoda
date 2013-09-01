#!/usr/bin/env python

import os

from yoda.config import config
from yoda.subcommands import subcommands

yoda_config = config("%s/.yodarc" % os.environ.get("HOME"))

subcmd = subcommands(yoda_config)
parser = subcmd.parse()
args = subcmd.parser.parse_args()

subcmd.exec(args)
