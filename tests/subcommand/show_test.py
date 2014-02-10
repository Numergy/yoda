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
import unittest

from mock import call
from mock import Mock
from mock import patch
from tests.utils import Sandbox
from yoda import Config
from yoda.subcommand import Show


class TestSubcommandShow(unittest.TestCase):
    """Show subcommand test suite."""
    config = None
    sandbox = None
    parser = None
    subparser = None
    show = None

    def setUp(self):
        """Setup test suite."""
        self.parser = argparse.ArgumentParser(prog="yoda_test")
        self.subparser = self.parser.add_subparsers(dest="show_subcommand")

        self.sandbox = Sandbox()
        self.config = Config(self.sandbox.path + "/config")

        config_data = {
            "workspaces": {
                "my_workspace": {
                    "path": "/my_workspace",
                    "repositories": {
                        "repo1": "/my_workspace/repo1"
                    }
                },
                "another_workspace": {
                    "path": "/another_workspace",
                    "repositories": {
                        "repo1": "/another_workspace/repo1"
                    }
                }
            }
        }

        self.config.update(config_data)

        self.show = Show()
        self.show.setup("show", self.config, self.subparser)

    def tearDown(self):
        """Tear down test suite."""
        self.sandbox.destroy()
        self.parser = None
        self.show = None

    def test_parse_show(self):
        """Test show to workspace."""

        self.show.parse()

        args = self.parser.parse_args(["show", "ws1"])

        self.assertEqual("show", args.show_subcommand)
        self.assertEqual("ws1", args.name)

        args = self.parser.parse_args(["show", "--all"])

        self.assertEqual("show", args.show_subcommand)
        self.assertTrue(args.all)

        self.assertRaises(
            SystemExit,
            self.parser.parse_args, ["show", "--all", "ws1/repo1"]
        )

    def test_exec_show(self):
        """Test exec show subcommand."""
        args = Mock()
        args.name = "my_workspace"

        self.show.show_workspace = Mock()
        self.show.execute(args)
        self.show.show_workspace.assert_called_once_with("my_workspace")

    def test_exec_show_all(self):
        """Test exec show all workspace details subcommand."""
        args = Mock()
        args.name = None
        args.all = True

        self.show.show_workspace = Mock()
        self.show.execute(args)

        calls = [call("my_workspace"), call("another_workspace")]
        self.show.show_workspace.assert_has_calls(calls)

    def test_show_workspace_no_matches(self):
        """Test exec show subcommand when no matches."""
        args = Mock()
        args.name = "not_exists"

        self.assertRaises(ValueError, self.show.execute, args)
