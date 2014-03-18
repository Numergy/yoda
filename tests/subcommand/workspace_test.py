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

import os
import sys

from tests.helpers import SubcommandTestHelper

from mock import Mock
from mock import patch
from yoda import Config
from yoda.subcommand import Workspace
from yoda.subcommand import WorkspaceSubcommands

builtins_module = "builtins" if sys.version[:1] == "3" else "__builtin__"


class TestSubcommandWorkspace(SubcommandTestHelper):
    """Workspace subcommand test suite."""

    def setUp(self):
        """Setup test suite."""
        self.subcommand = Workspace()
        self.subcommand_str = "workspace"
        super(TestSubcommandWorkspace, self).setUp()

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

    def test_parse_add(self):
        """Test workspace add parsing."""
        self.assert_subcommand_parsing(
            ["workspace", "add", "foo", "/tmp/foo"], {
                "subcommand": "workspace",
                "workspace_subcommand": "add",
                "name": "foo",
                "path": "/tmp/foo"})

    def test_parse_remove(self):
        """Test workspace remove parsing."""
        self.assert_subcommand_parsing(["workspace", "remove", "foo"], {
            "subcommand": "workspace",
            "workspace_subcommand": "remove",
            "name": "foo"})

    def test_parse_list(self):
        """Test workspace list parsing."""
        self.assert_subcommand_parsing(["workspace", "list"], {
            "subcommand": "workspace",
            "workspace_subcommand": "list"})

    def test_exec_add(self):
        """Test workspace add execution."""
        ws = Mock()
        ws.add = Mock()

        args = Mock()
        args.workspace_subcommand = "add"
        args.name = "foo"
        args.path = "/foo"

        self.subcommand.ws = ws
        self.subcommand.execute(args)

        ws.add.assert_called_with("foo", "/foo")

    def test_exec_remove(self):
        """Test workspace remove execution."""
        ws = Mock()
        ws.remove = Mock()

        args = Mock()
        args.workspace_subcommand = "remove"
        args.name = "foo"

        self.subcommand.ws = ws
        self.subcommand.execute(args)

        ws.remove.assert_called_with("foo")

    def test_exec_list(self):
        """Test workspace list execution."""
        ws_list = {
            "yoda": {
                "path": "/project/yoda",
                "repositories": {
                    "yoda": "/project/yoda/src"
                }
            },
            "test": {
                "path": "/project/test"
            }
        }

        ws = Mock()
        ws.list = Mock(return_value=ws_list)

        args = Mock()
        args.workspace_subcommand = "list"

        self.subcommand.ws = ws
        self.subcommand.execute(args)

        ws.list.assert_called_with()

    def test_exec_without_command(self):
        """Test workspace without subcommand."""
        ws = Mock()
        args = Mock()
        args.workspace_subcommand = None

        self.subcommand.ws = ws
        self.assertIsNone(self.subcommand.execute(args))

    def test_exec_with_wrong_command(self):
        """Test workspace without subcommand."""
        ws = Mock()
        args = Mock()
        args.workspace_subcommand = "test"

        self.subcommand.ws = ws
        self.assertIsNone(self.subcommand.execute(args))

    def test_load_workspaces_subcommands(self):
        """Test workspaces subcommands."""
        ws = Mock()
        ws.list = Mock(return_value={"foo":
                                     {"path": "/foo",
                                      "repositories": {}}})

        subcmd = Mock()
        subcmd.commands = {}

        self.subcommand.ws = ws
        self.subcommand.load_workspaces_subcommands(subcmd)

        self.assertTrue("foo" in subcmd.commands)
        self.assertIsInstance(subcmd.commands["foo"], WorkspaceSubcommands)


class TestWorkspacesSubcommands(SubcommandTestHelper):
    """Test suite for workspaces subcommands setup."""
    config_data = None
    directory = None

    def setUp(self):
        """Setup test suite."""
        super(TestWorkspacesSubcommands, self).setUp()
        self.subcommand = WorkspaceSubcommands(
            "yoda", self.subparser, self.config
        )

        self.config_data = {
            "workspaces": {
                "yoda": {
                    "path": self.sandbox.path
                }
            }
        }

        self.config.update(self.config_data)

    def test_parse_add(self):
        """Test parse add subcommands."""
        self.assert_subcommand_parsing(
            ["yoda", "add", "repo-name", "-u", "repo-url", "-p", "repo-path"],
            {
                "action": "add",
                "repo_name": "repo-name",
                "url": "repo-url",
                "path": "repo-path"
            }
        )

    def test_parse_remove(self):
        """Test parse remove subcommands."""
        self.assert_subcommand_parsing(
            ["yoda", "remove", "repo-name"], {
                "action": "remove",
                "repo_name": "repo-name"}
        )

    def test_parse_sync(self):
        """Test parse sync subcommands."""
        self.assert_subcommand_parsing(
            ["yoda", "sync"], {"action": "sync"})

    def test_exec_without_command(self):
        """Test repository execute without subcommand."""
        self.subcommand.parse()

        try:
            args = self.parser.parse_args(["yoda"])
            self.assertIsNone(self.subcommand.execute(args))
        except SystemExit:
            #Raised in Python 2.7.x
            self.assertEqual("2.7", sys.version[:3])

    def test_execute_add_subcommand_repo_already_exists(self):
        """Test execute add subcommands when repo name already exists."""
        self.subcommand.parse()

        args = self.parser.parse_args(["yoda", "add", "repo-name"])
        self.sandbox.mkdir("tmp")
        self.subcommand.execute(args)
        self.assertTrue(os.path.exists(self.sandbox.path + "/repo-name"))
        self.assertRaises(ValueError, lambda: self.subcommand.execute(args))

    def test_execute_add_subcommand(self):
        """Test execute add subcommand."""
        self.subcommand.parse()

        args = self.parser.parse_args(
            ["yoda", "add", "other-repo", "-p",
             "%s/repo-name" % self.sandbox.path, "-u", "repo-url"])

        with patch(
                "yoda.workspace.clone") as patch_clone:
            self.sandbox.mkdir("tmp")
            self.subcommand.execute(args)
            patch_clone.assert_called_once_with(
                "repo-url",
                "%s/repo-name" % self.sandbox.path)

    @patch("%s.input" % builtins_module,
           Mock(side_effect=["n", "y"]))
    def test_execute_remove_subcommand(self):
        """Test execute remove subcommand."""
        self.subcommand.parse()

        self.config_data["workspaces"]["yoda"]["repositories"] = {
            "repo-name": self.sandbox.path + "/repo-name"
        }

        args = self.parser.parse_args(["yoda", "remove", "repo-name"])
        self.subcommand.execute(args)
        self.assertFalse(os.path.exists(self.sandbox.path + "/repo-name"))

        args = self.parser.parse_args(["yoda", "remove", "1377"])
        self.assertRaises(ValueError, lambda: self.subcommand.execute(args))

    def test_execute_sync_subcommand(self):
        """Test execute sync subcommand."""
        self.subcommand.parse()

        self.config_data["workspaces"]["yoda"]["repositories"] = {
            "repo-name": self.sandbox.path + "/repo-name"
        }

        args = self.parser.parse_args(
            ["yoda", "sync", "yoda"])

        self.assertFalse(self.subcommand.execute(args))
        with patch(
                "yoda.subcommand.workspace.Ws.sync",
                return_value=None):
            self.subcommand.execute(args)
