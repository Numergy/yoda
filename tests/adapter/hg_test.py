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
from yoda.adapter import Hg


class TestHg(AdapterTestHelper):
    """Hg adapter test suite."""
    def setUp(self):
        """Set up hg adapter."""
        super(TestHg, self).setUp(Hg)

    def test_status(self):
        """Test hg status."""
        self.adapter.status()
        self.assert_executed_command("hg status")

    def test_update(self):
        """Test hg update."""
        self.adapter.update()
        self.assert_executed_command("hg pull -u")

    def test_clone(self):
        """Test clone mercurial repository."""
        self.adapter.clone("ssh://hg@project.org/foo/bar")
        self.assert_executed_command("hg clone %s %s" % (
            "ssh://hg@project.org/foo/bar",
            os.path.join(self.sandbox.path, "repository")
        ), with_path=False)
