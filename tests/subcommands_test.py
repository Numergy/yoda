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

from mock import Mock
import unittest
from yoda import Subcommand
from yoda import Subcommands


class TestSubcommand(unittest.TestCase):
    """Subcommand test suite."""

    def test_setup(self):
        """Test subcommand's attributes setup."""
        subcmd = Subcommand()

        subparser = Mock()
        subparser.add_parser.return_value = "baz"

        subcmd.setup("foo", "bar", subparser)
        self.assertEqual("bar", subcmd.config)
        self.assertEqual("baz", subcmd.parser)
        subparser.add_parser.assert_called_once_with("foo")


class TestSubcommands(unittest.TestCase):
    """Workspace subcommands test suite."""
    subcmds = None
    mocks = {}

    def setUp(self):
        """Setup test suite."""
        self.mocks["subcmd"] = Mock()
        self.mocks["subcmd"].setup.return_value = None
        self.mocks["subcmd"].parse.return_value = None
        self.mocks["subcmd"].execute.return_value = None

        self.mocks["config"] = Mock()
        self.subcmds = Subcommands(self.mocks["config"])

    def tearDown(self):
        """Tear down test suite."""
        self.mocks = None
        self.subcmds = None

    def test_add_command(self):
        """Test add subcommand."""
        self.subcmds.add_command(self.mocks["subcmd"])

        self.assertTrue("mock" in self.subcmds.commands)
        self.assertEqual(self.mocks["subcmd"], self.subcmds.commands["mock"])

    def test_parse(self):
        """Test parse subcommand."""
        self.subcmds.commands = {"Mock": self.mocks["subcmd"]}
        self.subcmds.parse()
        self.mocks["subcmd"].parse.assert_called_once()

    def test_execute(self):
        """Test execute subcommand."""
        args = Mock()
        args.subcommand = "Mock"
        self.subcmds.commands = {"Mock": self.mocks["subcmd"]}
        self.subcmds.execute(args)
        self.mocks["subcmd"].execute.assert_called_once()

    def test_execute_without_subcommand(self):
        """Test execute without subcommand."""
        args = Mock()
        args.subcommand = None
        self.subcmds.commands = {"Mock": self.mocks["subcmd"]}
        self.assertIsNone(self.subcmds.execute(args))
        self.mocks["subcmd"].execute.assert_called_once()

    def test_execute_with_wrong_command(self):
        """Test execute with wrong subcommand."""
        args = Mock()
        args.subcommand = "fake"
        self.subcmds.commands = {"Mock": self.mocks["subcmd"]}
        self.assertIsNone(self.subcmds.execute(args))
        self.mocks["subcmd"].execute.assert_called_once()
