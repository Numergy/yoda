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
from tests.helpers import AdapterTestHelper
from yoda.adapter import Git


class TestGit(AdapterTestHelper):
    """Git adapter test suite."""
    def setUp(self):
        """Set up git adapter and sandbox."""
        super(TestGit, self).setUp(Git)

    def test_status(self):
        """Test git status."""
        self.adapter.status()
        self.assert_executed_command("git status")

    def test_update(self):
        """Test git update."""
        self.adapter.update()
        self.assert_executed_command("git pull --rebase")

    def test_clone(self):
        """Test git clone."""
        self.adapter.clone("git@project.org:foo/bar")
        self.assert_executed_command("git clone %s %s" % (
            "git@project.org:foo/bar",
            os.path.join(self.sandbox.path, "repository")
        ), with_path=False)
