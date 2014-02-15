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
import os
import sys
import unittest

from mock import Mock
from mock import patch
from tests.utils import Sandbox
from tests.utils import assert_config_file_contains
from yoda import Config
from yoda.subcommand import Workspace
from yoda.subcommand import WorkspaceSubcommands

builtins_module = "builtins" if sys.version[:1] == "3" else "__builtin__"


class TestSubcommandWorkspace(unittest.TestCase):
    """Workspace subcommand test suite."""
    sandbox = None
    parser = None
    subparser = None
    workspace = None

    def setUp(self):
        """Setup test suite."""
        self.parser = argparse.ArgumentParser(prog="yoda_test")
        self.subparser = self.parser.add_subparsers(dest="subcommand_test")
        self.sandbox = Sandbox()

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

        conf = Config(self.sandbox.path + "/config")
        conf.update(config_data)
        self.workspace = Workspace()
        self.workspace.setup(
            "workspace", conf, self.subparser)

    def tearDown(self):
        """Tear down test suite."""
        self.sandbox.destroy()
        self.parser = None
        self.workspace = None

    def test_parse_add(self):
        """Test workspace add parsing."""
        self.workspace.parse()
        args = self.parser.parse_args(["workspace", "add", "foo", "/tmp/foo"])

        self.assertEqual("workspace", args.subcommand_test)
        self.assertEqual("add", args.workspace_subcommand)
        self.assertEqual("foo", args.name)
        self.assertEqual("/tmp/foo", args.path)

    def test_parse_remove(self):
        """Test workspace remove parsing."""
        self.workspace.parse()
        args = self.parser.parse_args(["workspace", "remove", "foo"])

        self.assertEqual("workspace", args.subcommand_test)
        self.assertEqual("remove", args.workspace_subcommand)
        self.assertEqual("foo", args.name)

    def test_parse_list(self):
        """Test workspace list parsing."""
        self.workspace.parse()
        args = self.parser.parse_args(["workspace", "list"])
        self.assertEqual("workspace", args.subcommand_test)
        self.assertEqual("list", args.workspace_subcommand)

    def test_exec_add(self):
        """Test workspace add execution."""
        ws = Mock()
        ws.add = Mock()

        args = Mock()
        args.workspace_subcommand = "add"
        args.name = "foo"
        args.path = "/foo"

        self.workspace.ws = ws
        self.workspace.execute(args)

        ws.add.assert_called_with("foo", "/foo")

    def test_exec_remove(self):
        """Test workspace remove execution."""
        ws = Mock()
        ws.remove = Mock()

        args = Mock()
        args.workspace_subcommand = "remove"
        args.name = "foo"

        self.workspace.ws = ws
        self.workspace.execute(args)

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

        self.workspace.ws = ws
        self.workspace.execute(args)

        ws.list.assert_called_with()

    def test_exec_without_command(self):
        """Test workspace without subcommand."""
        ws = Mock()
        args = Mock()
        args.workspace_subcommand = None

        self.workspace.ws = ws
        self.assertIsNone(self.workspace.execute(args))

    def test_exec_with_wrong_command(self):
        """Test workspace without subcommand."""
        ws = Mock()
        args = Mock()
        args.workspace_subcommand = "test"

        self.workspace.ws = ws
        self.assertIsNone(self.workspace.execute(args))

    def test_load_workspaces_subcommands(self):
        """Test workspaces subcommands."""
        ws = Mock()
        ws.list = Mock(return_value={"foo":
                                     {"path": "/foo",
                                      "repositories": {}}})

        subcmd = Mock()
        subcmd.commands = {}

        self.workspace.ws = ws
        self.workspace.load_workspaces_subcommands(subcmd)

        self.assertTrue("foo" in subcmd.commands)
        self.assertIsInstance(subcmd.commands["foo"], WorkspaceSubcommands)


class TestWorkspacesSubcommands(unittest.TestCase):
    """Test suite for workspaces subcommands setup."""
    config = None
    parser = None
    config_data = None
    directory = None
    sandbox = None

    def setUp(self):
        """Setup test suite."""
        self.sandbox = Sandbox()

        self.parser = argparse.ArgumentParser(prog="yoda_test")
        self.config_data = {
            "workspaces": {
                "yoda": {
                    "path": self.sandbox.path
                }
            }
        }

        self.config = Config(self.sandbox.path + "/config")
        self.config.update(self.config_data)

    def tearDown(self):
        """Tear down test suite."""
        self.sandbox.destroy()
        self.parser = None

    def test_exec_without_command(self):
        """Test repository execute without subcommand."""
        subparser = self.parser.add_subparsers(dest="subcommand_test")
        ws_subcmds = WorkspaceSubcommands(
            "yoda", subparser, self.config
        )
        ws_subcmds.parse()

        try:
            args = self.parser.parse_args(["yoda"])
            self.assertIsNone(ws_subcmds.execute(args))
        except SystemExit:
            #Raised in Python 2.7.x
            self.assertEqual("2.7", sys.version[:3])

    def test_parse_add(self):
        """Test parse add subcommands."""
        subparser = self.parser.add_subparsers(dest="subcommand_test")
        ws_subcmds = WorkspaceSubcommands(
            "yoda", subparser, self.config
        )
        ws_subcmds.parse()

        args = self.parser.parse_args([
            "yoda", "add", "repo-name", "-u", "repo-url", "-p", "repo-path"])

        self.assertEqual("add", args.action)
        self.assertEqual("repo-name", args.repo_name)
        self.assertEqual("repo-url", args.url)
        self.assertEqual("repo-path", args.path)

    def test_execute_add_subcommand_repo_already_exists(self):
        """Test execute add subcommands when repo name already exists."""
        subparser = self.parser.add_subparsers(dest="subcommand")
        ws_subcmds = WorkspaceSubcommands(
            "yoda", subparser, self.config
        )
        ws_subcmds.parse()

        args = self.parser.parse_args(["yoda", "add", "repo-name"])
        self.sandbox.mkdir("tmp")
        ws_subcmds.execute(args)
        self.assertTrue(os.path.exists(self.sandbox.path + "/repo-name"))
        self.assertRaises(ValueError, lambda: ws_subcmds.execute(args))

    def test_execute_add_subcommand(self):
        """Test execute add subcommand."""
        subparser = self.parser.add_subparsers(dest="subcommand")
        ws_subcmds = WorkspaceSubcommands(
            "yoda", subparser, self.config
        )
        ws_subcmds.parse()

        args = self.parser.parse_args(
            ["yoda", "add", "other-repo", "-p",
             "%s/repo-name" % self.sandbox.path, "-u", "repo-url"])

        with patch(
                "yoda.subcommand.workspace.clone") as patch_clone:
            self.sandbox.mkdir("tmp")
            ws_subcmds.execute(args)
            patch_clone.assert_called_once_with(
                "repo-url",
                "%s/repo-name" % self.sandbox.path)

    @patch("%s.input" % builtins_module,
           Mock(side_effect=["n", "y"]))
    def test_execute_remove_subcommad(self):
        """Test execute remove subcommands."""
        self.config_data["workspaces"]["yoda"]["repositories"] = {
            "repo-name": self.sandbox.path + "/repo-name"
        }
        subparser = self.parser.add_subparsers(dest="subcommand")
        ws_subcmds = WorkspaceSubcommands(
            "yoda", subparser, self.config
        )
        ws_subcmds.parse()

        args = self.parser.parse_args(["yoda", "remove", "repo-name"])
        ws_subcmds.execute(args)
        self.assertFalse(os.path.exists(self.sandbox.path + "/repo-name"))

        args = self.parser.parse_args(["yoda", "remove", "1377"])
        self.assertRaises(ValueError, lambda: ws_subcmds.execute(args))

    def test_parse_sync_subcommand(self):
        """Test synchronize workspace."""
        subparser = self.parser.add_subparsers(dest="subcommand_test")
        ws_subcmds = WorkspaceSubcommands(
            "yoda", subparser, self.config
        )
        ws_subcmds.parse()

        args = self.parser.parse_args([
            "yoda", "sync"])

        self.assertEqual("sync", args.action)

    def test_execute_sync_subcommand(self):
        """Test execute sync subcommand."""
        self.config_data["workspaces"]["yoda"]["repositories"] = {
            "repo-name": self.sandbox.path + "/repo-name"
        }
        subparser = self.parser.add_subparsers(dest="subcommand")
        ws_subcmds = WorkspaceSubcommands(
            "yoda", subparser, self.config
        )
        ws_subcmds.parse()

        args = self.parser.parse_args(
            ["yoda", "sync", "yoda"]
        )
        self.sandbox.mkdir("tmp")

        self.assertFalse(ws_subcmds.execute(args))
        with patch(
                "yoda.subcommand.workspace.Repository.__init__",
                return_value=None):
            ws_subcmds.execute(args)

    def test_sync(self):
        """Test sync workspace."""
        self.sandbox.mkdir("my_ws")
        self.sandbox.mkdir("my_ws/my_repo")
        self.sandbox.mkdir("my_ws/my_repo/.git")

        self.config.update({
            "workspaces": {
                "my_ws": {
                    "path": os.path.join(self.sandbox.path, "my_ws"),
                    "repositories": {}}}})

        subparser = self.parser.add_subparsers(dest="subcommand")
        ws_subcmds = WorkspaceSubcommands(
            "yoda", subparser, self.config
        )
        ws_subcmds.sync("my_ws")

        assert_config_file_contains(
            self,
            self.config.config_file,
            {"workspaces": {
                "my_ws": {
                    "path": os.path.join(self.sandbox.path, "my_ws"),
                    "repositories": {
                        "my_repo": os.path.join(self.sandbox.path,
                                                "my_ws",
                                                "my_repo")}}}})
