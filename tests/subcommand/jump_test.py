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

from tests.helpers import SubcommandTestHelper

from mock import call
from mock import Mock
from mock import patch
from tests.helpers import Sandbox
from yoda import Config
from yoda.subcommand import Jump


class TestSubcommandJump(SubcommandTestHelper):
    """Jump subcommand test suite."""

    def setUp(self):
        """Setup test suite."""
        self.subcommand = Jump()
        self.subcommand_str = "jump"
        super(TestSubcommandJump, self).setUp()

    def test_parse_jump(self):
        """Test jump to workspace."""
        self.assert_subcommand_parsing(["jump", "yoda"], {
            "subcommand": "jump",
            "name": "yoda"})

    def test_exec_jump(self):
        """Test exec jump subcommand."""
        args = Mock()
        args.name = "yoda/baz"

        self.subcommand._Jump__jump = Mock()

        mock_path = {"yoda/baz": "/tmp/yoda/baz"}

        with patch("yoda.subcommand.jump.find_path",
                   return_value=mock_path) as patch_fp:
            self.subcommand.execute(args)
            patch_fp.assert_called_once_with(
                "yoda/baz", self.subcommand.config, True)
            self.subcommand._Jump__jump.assert_called_once_with(
                "/tmp/yoda/baz")

    def test_exec_jump_no_matches(self):
        """Test exec jump subcommand when no matches."""
        args = Mock()
        args.name = "foo/bar"

        self.subcommand.logger = Mock()

        with patch("yoda.subcommand.jump.find_path", return_value={}):
            self.assertFalse(self.subcommand.execute(args))
            self.subcommand.logger.error.assert_called_once_with(
                "No matches for `foo/bar`")

    def test_exec_jump_method(self):
        """Test exec jump subcommand when no matches."""
        args = Mock()
        args.name = "foo/bar"

        self.subcommand.logger = Mock()
        os_system = Mock()

        with patch("os.system", return_value=os_system):
            mock_path = {"yoda/baz": "/tmp/yoda/baz"}
            with patch("yoda.subcommand.jump.find_path",
                       return_value=mock_path):
                self.subcommand.execute(args)
                os_system.assert_called_once
                calls = [
                    call("Spawn new shell on `/tmp/yoda/baz`"),
                    call("Use Ctrl-D to exit and go "
                         "back to the previous directory"),
                    call("Shell on `/tmp/yoda/baz` closed.")]
                assert self.subcommand.logger.info.mock_calls == calls
