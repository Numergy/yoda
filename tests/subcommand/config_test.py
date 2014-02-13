# This source file is part of Yoda.
#
# Yoda is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Yoda is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Yoda. If not, see <http://www.gnu.org/licenses/gpl-3.0.html>.

import argparse
from logging import RootLogger
import unittest

from mock import call
from mock import Mock
from mock import patch
from tests.utils import Sandbox
from yoda import Config
from yoda.subcommand import Config as CfgSubcommand
from yoda.subcommand import Jump


class TestSubcommandJump(unittest.TestCase):
    """Jump subcommand test suite."""
    config = None
    sandbox = None
    parser = None
    subparser = None
    cfg_subcommand = None

    def setUp(self):
        """Setup test suite."""
        self.parser = argparse.ArgumentParser(prog="yoda_test")
        self.subparser = self.parser.add_subparsers(dest="config_subcommand")

        self.sandbox = Sandbox()
        self.config = Config(self.sandbox.path + "/config")

        self.cfg_subcommand = CfgSubcommand()
        self.cfg_subcommand.setup("config", self.config, self.subparser)

    def tearDown(self):
        """Tear down test suite."""
        self.sandbox.destroy()
        self.parser = None
        self.cfg_subcommand = None

    def test_parse_config(self):
        """Test config to workspace."""
        self.cfg_subcommand.parse()
        args = self.parser.parse_args(["config", "set", "test", "test2"])

        self.assertEqual("config", args.config_subcommand)
        self.assertEqual("set", args.action)
        self.assertEqual("test", args.key)
        self.assertEqual("test2", args.value)

    def test_exec_config_with_undefined_action(self):
        """Test exec config with undefined subcommand."""
        args = Mock()
        args.action = "yoda"
        self.cfg_subcommand.execute(args)

    def test_exec_config_with_set(self):
        """Test exec config with set subcommand."""
        args = Mock()
        args.action = "set"
        args.key = "logfile"
        args.value = "/tmp/yoda.log"
        self.cfg_subcommand.execute(args)
        self.assertEqual("/tmp/yoda.log", self.config["logfile"])

    def test_exec_config_with_set_workspaces(self):
        """Test exec config with set workspaces subcommand."""
        args = Mock()
        args.action = "set"
        args.key = "workspaces"
        args.value = False
        self.assertFalse(self.cfg_subcommand.execute(args))

    def test_exec_config_with_get(self):
        """Test exec config with get subcommand."""
        args = Mock()
        args.action = "get"
        args.key = "logfile"
        self.assertFalse(self.cfg_subcommand.execute(args))
