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

import mock
from mock import patch
import os
import subprocess
from testfixtures import LogCapture
from tests.helpers import YodaTestHelper
from yoda.adapter import Abstract
from yoda.adapter import ExecutableNotFoundException


class TestAdapterAbstract(YodaTestHelper):
    """Git adapter test suite."""
    adapter = None

    def setUp(self):
        """Set up git adapter and sandbox."""
        super(TestAdapterAbstract, self).setUp()
        self.sandbox.mkdir("repo")

        self.adapter = Abstract(os.path.join(self.sandbox.path, "repo"))
        self.adapter.executable = "git"

    def tearDown(self):
        """Unset test object."""
        super(TestAdapterAbstract, self).tearDown()
        self.adapter = None

    @patch("yoda.adapter.abstract.subprocess.Popen",
           return_value=mock.create_autospec(
               subprocess.Popen, return_value=mock.Mock()))
    def test_execute_success(self, mock_proc):
        """Test execute with success."""
        mock_com = mock_proc.return_value.communicate
        mock_com.return_value = [b"Yoda", b"Rosk"]
        mock_wait = mock_proc.return_value.wait
        mock_wait.return_value = 0
        with patch("yoda.adapter.abstract.find_executable",
                   return_value=True):
            with LogCapture() as lcap:
                self.assertEqual(
                    self.adapter.execute("git log"),
                    mock_proc.return_value)

        lcap.check(("yoda.adapter.abstract", "DEBUG",
                    "Executing command `git log` (cwd: None)"),
                   ("yoda.adapter.abstract", "INFO",
                    "Yoda"),
                   ("yoda.adapter.abstract", "INFO",
                    "Rosk"))

        mock_proc.assert_called_with(
            "git log",
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            cwd=None,
            shell=True)

    @patch("yoda.adapter.abstract.subprocess.Popen",
           return_value=mock.create_autospec(
               subprocess.Popen, return_value=mock.Mock()))
    def test_execute_failure(self, mock_proc):
        """Test execute with error."""
        mock_com = mock_proc.return_value.communicate
        mock_com.return_value = [b"Yoda", b"Rosk"]
        mock_wait = mock_proc.return_value.wait
        mock_wait.return_value = 1
        with patch("yoda.adapter.abstract.find_executable",
                   return_value=True):
            with LogCapture() as lcap:
                self.assertEqual(
                    self.adapter.execute("git log"),
                    mock_proc.return_value)

        lcap.check(("yoda.adapter.abstract", "DEBUG",
                    "Executing command `git log` (cwd: None)"),
                   ("yoda.adapter.abstract", "INFO",
                    "Yoda"),
                   ("yoda.adapter.abstract", "ERROR",
                    "Rosk"))

    def test_check_executable_with_wrong_executable(self):
        """Test check executable with wrong command."""
        self.adapter.executable = "wrong_executable"
        with patch("yoda.adapter.abstract.find_executable",
                   return_value=False):
            self.assertRaises(
                ExecutableNotFoundException,
                self.adapter.check_executable
            )

    def test_status(self):
        """Test abstract status."""
        self.assertIsNone(self.adapter.status())

    def test_show(self):
        """Test abstract show."""
        self.assertIsNone(self.adapter.show())

    def test_update(self):
        """Test abstract update."""
        self.assertIsNone(self.adapter.update())

    def test_clone(self):
        """Test abstract clone."""
        self.assertIsNone(self.adapter.clone())
