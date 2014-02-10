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

from mock import Mock
from mock import patch
from yoda import Output


class TestOutput(unittest.TestCase):
    """Yoda output test suite."""

    out = None
    stdout = None
    stderr = None

    def setUp(self):
        """Setup output object."""
        self.stdout = self.stderr = Mock()
        self.stdout.write.return_value = None
        self.stderr.write.return_value = None
        self.out = Output(self.stdout, self.stderr)

    def test_info(self):
        """Test printing an information message."""
        self.out.info("foo")
        self.stdout.write.assert_called_once_with("foo\n")

    def test_success(self):
        """Test printing a success message."""
        self.out.success("bar")
        self.stdout.write.assert_called_once_with("\x1b[32mbar\x1b[0m\n")

    def test_warn(self):
        """Test printing a warning message."""
        self.out.warn("baz")
        self.stderr.write.assert_called_once_with("\x1b[33mbaz\x1b[0m\n")

    def test_error(self):
        """Test printing an error message."""
        self.out.error("foobar")
        self.stderr.write.assert_called_once_with("\x1b[31mfoobar\x1b[0m\n")

    @patch("builtins.input",
           Mock(side_effect=["n", "y", "1337"]))
    def test_yn_choice(self):
        """Test printing input question."""
        self.assertFalse(self.out.yn_choice("Test?"))
        self.assertTrue(self.out.yn_choice("Test?"))
        self.assertFalse(self.out.yn_choice("Test?"))
