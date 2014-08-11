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

from mock import call
from mock import Mock
from mock import patch
from tests.helpers import SubcommandTestHelper
from yoda.subcommand import Show


class TestSubcommandShow(SubcommandTestHelper):
    """Show subcommand test suite."""

    def setUp(self):
        """Setup test suite."""
        self.subcommand = Show()
        self.subcommand_str = "show"
        super(TestSubcommandShow, self).setUp()

        config_data = {
            "workspaces": {
                "my_workspace": {
                    "path": "/my_workspace",
                    "repositories": {
                        "repo1": self.sandbox.path + "/my_workspace/repo1"
                    }
                },
                "another_workspace": {
                    "path": "/another_workspace",
                    "repositories": {
                        "repo1": self.sandbox.path + "/another_workspace/repo1"
                    }
                }
            }
        }

        self.sandbox.mkdir("my_workspace")
        self.sandbox.mkdir("my_workspace/repo1")
        self.sandbox.mkdir("another_workspace")
        self.sandbox.mkdir("another_workspace/repo1")
        self.config.update(config_data)

    def test_parse_show(self):
        """Test show to workspace."""
        self.assert_subcommand_parsing(["show", "ws1"], {
            "subcommand": "show",
            "name": "ws1"})

    def test_parse_show_all(self):
        """Test show all workspaces."""
        self.assert_subcommand_parsing(["show", "--all"], {
            "subcommand": "show",
            "all": True})

    def test_parse_show_raises_error(self):
        """
        Test parse show subcommand raises error when --all specified
        with workspace name.
        """
        self.assert_subcommand_parsing_raises_error(
            ["show", "--all", "ws1/repo1"],
            SystemExit)

    def test_exec_show(self):
        """Test exec show subcommand."""
        args = Mock()
        args.name = "my_workspace"

        self.subcommand.show_workspace = Mock()
        self.subcommand.execute(args)
        self.subcommand.show_workspace.assert_called_once_with("my_workspace")

    def test_exec_show_all(self):
        """Test exec show all workspace details subcommand."""
        args = Mock()
        args.name = None
        args.all = True

        self.subcommand.show_workspace = Mock()
        self.subcommand.execute(args)

        self.subcommand.show_workspace.assert_has_calls(
            [call("my_workspace")])
        self.subcommand.show_workspace.assert_has_calls(
            [call("another_workspace")])

    def test_show_workspace_no_matches(self):
        """Test exec show subcommand when no matches."""
        args = Mock()
        args.name = "not_exists"

        self.assert_subcommand_exec_raises_error(
            args, ValueError)

    def test_show_workspace(self):
        """Test exec show subcommand with workspace."""
        args = Mock()
        args.name = "my_workspace"

        self.subcommand.logger = Mock()

        with patch("yoda.subcommand.show.slashes2dash",
                   return_value="my_workspace") as s2d:
            self.subcommand.execute(args)

        s2d.assert_called_once_with("my_workspace")

        calls = [
            call("<== \x1b[32mmy_workspace\x1b[0m workspace ==>"),
            call("\tPath: /my_workspace"),
            call("\tNumber of repositories: \x1b[33m1\x1b[0m")
        ]
        self.subcommand.logger.info.assert_has_calls(calls)
