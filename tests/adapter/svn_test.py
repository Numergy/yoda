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
from yoda.adapter import Svn


class TestSvn(AdapterTestHelper):
    """Svn adapter test suite."""
    def setUp(self):
        """Set up svn adapter and sandbox."""
        super(TestSvn, self).setUp(Svn)

    def test_status(self):
        """Test svn status."""
        self.adapter.status()
        self.assert_executed_command("svn status")

    def test_update(self):
        """Test svn update."""
        self.adapter.update()
        self.assert_executed_command("svn update")

    def test_clone(self):
        """Test svn clone."""
        self.adapter.clone("svn@project.org:foo/bar")
        self.assert_executed_command("svn checkout %s %s" % (
            "svn@project.org:foo/bar",
            os.path.join(self.sandbox.path, "repository")
        ), with_path=False)
