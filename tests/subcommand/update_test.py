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
from yoda import Config
from yoda.subcommand import Update


class TestSubcommandUpdate(SubcommandTestHelper):
    """Update subcommand test suite."""
    def setUp(self):
        """Setup test suite."""
        self.subcommand = Update()
        self.subcommand_str = "update"
        super(TestSubcommandUpdate, self).setUp()

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

    def test_parse_update(self):
        """Test parse update subcommand."""
        self.assert_subcommand_parsing(["update", "ws1/repo1"], {
            "subcommand": "update",
            "name": "ws1/repo1"})

    def test_parse_update_all(self):
        """Test update all workspaces"""
        self.assert_subcommand_parsing(["update", "--all"], {
            "subcommand": "update",
            "all": True})

    def test_parse_update_raises_error(self):
        """
        Test parse update subcommand raises error when --all specified
        with workspace or repository name.
        """
        self.assert_subcommand_parsing_raises_error(
            ["update", "--all", "ws1/repo1"],
            SystemExit)

    def test_exec_update_workspace_only(self):
        """Test exec update subcommand."""
        args = Mock()
        args.name = "foo/bar"

        mock_path = {"foo/bar": "/tmp/foo/bar"}

        self.subcommand.print_update = Mock()

        with patch("yoda.subcommand.update.find_path",
                   return_value=mock_path) as patch_fp:
            self.subcommand.execute(args)
            patch_fp.assert_called_once_with("foo/bar", self.subcommand.config)
            self.subcommand.print_update.assert_called_once_with(
                "foo/bar", "/tmp/foo/bar")

    def test_exec_update_all_workspaces(self):
        """Test exec with all workspaces."""
        args = Mock()
        args.name = None
        args.all = True

        mock_path = {"foo/bar": "/tmp/foo/bar"}

        self.subcommand.print_update = Mock()

        with patch("yoda.subcommand.update.find_path",
                   return_value=mock_path):
            self.subcommand.execute(args)

    def test_exec_update_no_matches(self):
        """Test exec update subcommand with no matches."""
        args = Mock()
        args.name = "foobar"

        self.subcommand.logger = Mock()
        self.subcommand.print_update = Mock()

        with patch("yoda.subcommand.update.find_path", return_value={}):
            self.assertFalse(self.subcommand.execute(args))
            self.subcommand.logger.error.assert_called_once_with(
                "No matches for `foobar`")

    def test_print_update(self):
        """Test print_update."""
        self.subcommand.logger = Mock()
        with patch("yoda.subcommand.update.Repository"):
            self.subcommand.print_update("foo", "bar")
            self.subcommand.logger.info.assert_has_calls(
                [call("\033[32m=> [foo] bar\033[0m")])
