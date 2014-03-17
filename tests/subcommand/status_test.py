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

from tests.helpers import SubcommandTestHelper

from mock import call
from mock import Mock
from mock import patch
from tests.helpers import Sandbox
from yoda import Config
from yoda.subcommand import Status


class TestSubcommandStatus(SubcommandTestHelper):
    """Status subcommand test suite."""

    def setUp(self):
        """Setup test suite."""
        self.subcommand = Status()
        self.subcommand_str = "status"
        super(TestSubcommandStatus, self).setUp()

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
        self.config.update(config_data)

    def test_parse_status(self):
        """Test parse status subcommand."""
        self.assert_subcommand_parsing(["status", "ws1/repo1"], {
            "subcommand": "status",
            "name": "ws1/repo1"})

    def test_parse_status_all(self):
        """Test show status of all workspaces"""
        self.assert_subcommand_parsing(["status", "--all"], {
            "subcommand": "status",
            "all": True})

    def test_parse_status_raises_error(self):
        """
        Test show status raises error when --all specifier
        with workspace or repository name.
        """
        self.assert_subcommand_parsing_raises_error(
            ["status", "--all", "ws1/repo1"], SystemExit)

    def test_exec_status_workspace_only(self):
        """Test exec status subcommand."""
        args = Mock()
        args.name = "foo/bar"

        mock_path = {"foo/bar": "/tmp/foo/bar"}

        self.subcommand.print_status = Mock()

        with patch("yoda.subcommand.status.find_path",
                   return_value=mock_path) as patch_fp:
            self.subcommand.execute(args)
            patch_fp.assert_called_once_with("foo/bar", self.subcommand.config)
            self.subcommand.print_status.assert_called_once_with(
                "foo/bar", "/tmp/foo/bar")

    def test_exec_status_all_workspaces(self):
        """Test exec with all workspaces."""
        args = Mock()
        args.name = None
        args.all = True

        mock_path = {"foo/bar": "/tmp/foo/bar"}

        self.subcommand.print_status = Mock()

        with patch("yoda.subcommand.status.find_path",
                   return_value=mock_path):
            self.subcommand.execute(args)

    def test_exec_status_no_matches(self):
        """Test exec status subcommand with no matches."""
        args = Mock()
        args.name = "foobar"

        self.subcommand.logger = Mock()
        self.subcommand.print_status = Mock()

        with patch("yoda.subcommand.status.find_path", return_value={}):
            self.assertFalse(self.subcommand.execute(args))
            self.subcommand.logger.error.assert_called_once_with(
                "No matches for `foobar`")

    def test_print_status(self):
        """Test print_status."""
        self.subcommand.logger = Mock()
        with patch("yoda.subcommand.status.Repository"):
            self.subcommand.print_status("foo", "bar")
            self.subcommand.logger.info.assert_has_calls(
                [call("\033[32m=> [foo] bar\033[0m")])
