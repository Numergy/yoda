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
import sys

from mock import Mock
from mock import patch
from ..utils import mock_config, Sandbox
from yoda.subcommand import Jump


class TestSubcommandJump(unittest.TestCase):
    """ Workspace subcommand test suite """
    parser = None
    subparser = None
    jump = None
    sandbox = None

    def setUp(self):
        """ Setup test suite """
        self.parser = argparse.ArgumentParser(prog="yoda_test")
        self.subparser = self.parser.add_subparsers(dest="jump_subcommand")
        self.sandbox = Sandbox()
        self.sandbox.mkdir("workspace")
        self.sandbox.mkdir("workspace/repository")

        config_data = {
            "workspaces": {
                "test": {
                    "path": self.sandbox.path + "/test",
                    "repositories": {
                        "repo-test": self.sandbox.path + "/test/1337"
                    }
                },
                "yoda": {
                    "path": self.sandbox.path + "/workspace",
                    "repositories": {
                        "repo": self.sandbox.path + "/workspace/repository"
                    }
                }
            }
        }
        self.jump = Jump()
        self.jump.setup(
            "jump", mock_config(config_data), self.subparser)

    def tearDown(self):
        """ Tear down test suite """
        self.sandbox.destroy()
        self.parser = None
        self.jump = None

    def test_exec_jump(self):
        """ Test jump to workspace """
        args = Mock()
        args.jump_subcommand = "jump"
        args.to = "yoda"

        self.jump.jump = Mock()
        self.jump.execute(args)

        self.jump.jump.assert_called_once_with(
            self.sandbox.path + "/workspace")

    def test_parse_jump(self):
        """ Test jump to workspace """
        self.jump.parse()
        args = self.parser.parse_args(["jump", "yoda"])

        self.assertEqual("jump", args.jump_subcommand)
        self.assertEqual("yoda", args.to)

    def test_exec_jump_to_repository(self):
        """ Test jump to repository """
        args = Mock()
        args.jump_subcommand = "jump"
        args.to = "repo"

        self.jump.jump = Mock()
        self.jump.execute(args)

        self.jump.jump.assert_called_once_with(
            self.sandbox.path + "/workspace/repository")

    def test_exec_jump_to_repository_from_workspace(self):
        """ test jump to repository from workspace """
        args = Mock()
        args.jump_subcommand = "jump"
        args.to = "yoda/repo"

        self.jump.jump = Mock()
        self.jump.execute(args)

        self.jump.jump.assert_called_once_with(
            self.sandbox.path + "/workspace/repository")

    def test_exec_to_invalid_repository(self):
        """ test Jump to repository from workspace """
        args = Mock()
        args.jump_subcommand = "jump"
        args.to = "yoda/1337"

        self.assertFalse(self.jump.execute(args))

    def test_exec_to_invalid_workspace(self):
        """ test Jump to repository from workspace """
        args = Mock()
        args.jump_subcommand = "jump"
        args.to = "fake/1337"

        self.assertFalse(self.jump.execute(args))

    def test_exec_jump_with_no_workspace(self):
        """ Test jump with no workspace """

        config_data = {
            "workspaces": {
            }
        }
        self.jump = Jump()
        self.jump.setup(
            "jump", mock_config(config_data), self.subparser)
        args = Mock()
        args.jump_subcommand = "jump"
        args.to = "test"

        self.assertIsNone(self.jump.execute(args))
