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
from yoda.subcommand import Status


class TestSubcommandStatus(unittest.TestCase):
    """Status subcommand test suite."""
    sandbox = None
    config = None
    parser = None
    subparser = None
    status = None

    def setUp(self):
        """Setup test suite."""
        self.parser = argparse.ArgumentParser(prog="yoda_test")
        self.subparser = self.parser.add_subparsers(dest="subcommand_test")

        self.status = Status()
        config_data = {
            "workspaces": {
                "yoda": {
                    "path": "/yoda",
                    "repositories": {
                        "yoda": "/project/yoda"
                    }
                }
            }
        }

        self.sandbox = Sandbox()
        self.config = Config(self.sandbox.path + "/config")
        self.config.update(config_data)
        self.status.setup("status", self.config, self.subparser)

    def tearDown(self):
        """Tear down test suite."""
        self.parser = None
        self.status = None

    def test_parse_status(self):
        """Test parse status subcommand."""
        self.status.parse()

        args = self.parser.parse_args(["status", "ws1/repo1"])

        self.assertEqual("status", args.subcommand_test)
        self.assertEqual("ws1/repo1", args.name)

        args = self.parser.parse_args(["status", "--all"])

        self.assertEqual("status", args.subcommand_test)
        self.assertEqual(True, args.all)

        self.assertRaises(
            SystemExit,
            self.parser.parse_args, ["status", "--all", "ws1/repo1"]
        )

    def test_exec_status_workspace_only(self):
        """Test exec status subcommand."""
        args = Mock()
        args.name = "foo/bar"

        mock_path = {"foo/bar": "/tmp/foo/bar"}

        self.status.print_status = Mock()

        with patch("yoda.subcommand.status.find_path",
                   return_value=mock_path) as patch_fp:
            self.status.execute(args)
            patch_fp.assert_called_once_with("foo/bar", self.status.config)
            self.status.print_status.assert_called_once_with(
                "foo/bar", "/tmp/foo/bar")

    def test_exec_status_all_workspaces(self):
        """Test exec with all workspaces."""
        args = Mock()
        args.name = None
        args.all = True

        mock_path = {"foo/bar": "/tmp/foo/bar"}

        self.status.print_status = Mock()

        with patch("yoda.subcommand.status.find_path",
                   return_value=mock_path):
            self.status.execute(args)

    def test_exec_status_no_matches(self):
        """Test exec status subcommand with no matches."""
        args = Mock()
        args.name = "foobar"

        self.status.logger = Mock()
        self.status.print_status = Mock()

        with patch("yoda.subcommand.status.find_path", return_value={}):
            self.assertFalse(self.status.execute(args))
            self.status.logger.error.assert_called_once_with(
                "No matches for `foobar`")

    def test_print_status(self):
        """Test print_status."""
        self.status.logger = Mock()
        with patch("yoda.subcommand.status.Repository"):
            self.status.print_status("foo", "bar")
            self.status.logger.info.assert_has_calls(
                [call("\033[32m=> [foo] bar\033[0m")])
