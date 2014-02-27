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
import unittest

from mock import Mock

from tests.utils import Sandbox

from yoda.adapter import Svn


class TestGit(unittest.TestCase):
    """Svn adapter test suite."""
    sandbox = None
    svn = None

    def setUp(self):
        """Set up svn adapter and sandbox."""
        self.sandbox = Sandbox()
        self.sandbox.mkdir("repo")

        self.svn = Svn(os.path.join(self.sandbox.path, "repo"))
        self.svn.execute = Mock(return_value=None)

    def tearDown(self):
        """Unset test object."""
        self.sandbox.destroy()
        self.svn = None

    def test_status(self):
        """Test svn status."""
        self.svn.status()
        self.svn.execute.assert_called_once_with(
            "svn status",
            os.path.join(self.sandbox.path, "repo"))

    def test_update(self):
        """Test svn update."""
        self.svn.update()
        self.svn.execute.assert_called_once_with(
            "svn update",
            os.path.join(self.sandbox.path, "repo"))

    def test_clone(self):
        """Test svn status."""
        self.svn.clone("svn@project.org:foo/bar")
        self.svn.execute.assert_called_once_with(
            "svn checkout %s %s" % (
                "svn@project.org:foo/bar",
                os.path.join(self.sandbox.path, "repo")))
