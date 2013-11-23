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

import unittest
import argparse

from mock import Mock
from ..utils import mock_config
from yoda.subcommand import Workspace, WorkspaceSubcommands


class TestSubcommandWorkspace(unittest.TestCase):
    """ Workspace subcommand test suite """
    parser = None
    subparser = None
    workspace = None

    def setUp(self):
        """ Setup test suite """
        self.parser = argparse.ArgumentParser(prog="yoda_test")
        self.subparser = self.parser.add_subparsers(dest="subcommand_test")

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
        self.workspace = Workspace()
        self.workspace.setup(
            "workspace", mock_config(config_data), self.subparser)

    def tearDown(self):
        """ Tear down test suite """
        self.parser = None
        self.workspace = None

    def test_parse_add(self):
        """ Test workspace add parsing """
        self.workspace.parse()
        args = self.parser.parse_args(["workspace", "add", "foo", "/tmp/foo"])

        self.assertEqual("add", args.workspace_subcommand)
        self.assertEqual("foo", args.name)
        self.assertEqual("/tmp/foo", args.path)

    def test_parse_remove(self):
        """ Test workspace remove parsing """
        self.workspace.parse()
        args = self.parser.parse_args(["workspace", "remove", "foo"])

        self.assertEqual("remove", args.workspace_subcommand)
        self.assertEqual("foo", args.name)

    def test_parse_list(self):
        """ Test workspace list parsing """
        self.workspace.parse()
        args = self.parser.parse_args(["workspace", "list"])
        self.assertEqual("list", args.workspace_subcommand)

    def test_exec_add(self):
        """ Test workspace add execution """
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
        """ Test workspace remove execution """
        ws = Mock()
        ws.remove = Mock()

        args = Mock()
        args.workspace_subcommand = "remove"
        args.name = "foo"

        self.workspace.ws = ws
        self.workspace.execute(args)

        ws.remove.assert_called_with("foo")

    def test_exec_list(self):
        """ Test workspace list execution """
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
        """ Test workspace without subcommand """
        ws = Mock()
        args = Mock()
        args.workspace_subcommand = None

        self.workspace.ws = ws
        self.assertIsNone(self.workspace.execute(args))

    def test_exec_with_wrong_command(self):
        """ Test workspace without subcommand """
        ws = Mock()
        args = Mock()
        args.workspace_subcommand = "test"

        self.workspace.ws = ws
        self.assertIsNone(self.workspace.execute(args))

    def test_load_workspaces_subcommands(self):
        """ Test workspaces subcommands """
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
    """ Test suite for workspaces subcommands setup """
    parser = None

    def setUp(self):
        """ Setup test suite """
        self.parser = argparse.ArgumentParser(prog="yoda_test")

    def tearDown(self):
        """ Tear down test suite """
        self.parser = None

    def test_parse_add(self):
        """ Test parse add subcommands """
        subparser = self.parser.add_subparsers(dest="subcommand_test")
        ws_subcmds = WorkspaceSubcommands("foo", subparser)
        ws_subcmds.parse()

        args = self.parser.parse_args(["foo", "add", "repo-name"])

        self.assertEqual("add", args.foo_subcommand)
        self.assertEqual("repo-name", args.repo_name)
