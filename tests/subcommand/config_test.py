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

from logging import RootLogger

from tests.helpers import SubcommandTestHelper

from mock import call
from mock import Mock
from mock import patch
from yoda import Config
from yoda.subcommand import Config as CfgSubcommand


class TestSubcommandConfig(SubcommandTestHelper):
    """Jump subcommand test suite."""

    def setUp(self):
        """Setup test suite."""
        self.subcommand = CfgSubcommand()
        self.subcommand_str = "config"
        super(TestSubcommandConfig, self).setUp()

    def test_parse_config_set(self):
        """Test config set."""
        self.assert_subcommand_parsing(["config", "set", "test", "test2"], {
            "subcommand": "config",
            "action": "set",
            "key": "test",
            "value": "test2"})

    def test_parse_config_get(self):
        """Test config set."""
        self.assert_subcommand_parsing(["config", "get", "test"], {
            "subcommand": "config",
            "action": "get",
            "key": "test"})

    def test_exec_config_with_undefined_action(self):
        """Test exec config with undefined subcommand."""
        args = Mock()
        args.action = "yoda"
        self.subcommand.execute(args)

    def test_exec_config_with_set(self):
        """Test exec config with set subcommand."""
        args = Mock()
        args.action = "set"
        args.key = "logfile"
        args.value = "/tmp/yoda.log"
        self.subcommand.execute(args)
        self.assertEqual("/tmp/yoda.log", self.config["logfile"])

    def test_exec_config_with_set_workspaces(self):
        """Test exec config with set workspaces subcommand."""
        args = Mock()
        args.action = "set"
        args.key = "workspaces"
        args.value = False
        self.assertFalse(self.subcommand.execute(args))

    def test_exec_config_with_get(self):
        """Test exec config with get subcommand."""
        args = Mock()
        args.action = "get"
        args.key = "logfile"
        self.assertFalse(self.subcommand.execute(args))
