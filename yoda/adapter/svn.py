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

from yoda.adapter import Abstract


class Svn(Abstract):
    """Svn Adapter."""

    executable = "svn"

    def status(self):
        """Show git status."""
        return self.exec_on_path("svn status")

    def clone(self, url):
        """Checkout repository from url."""
        return self.execute("svn checkout %s %s" % (url, self.path))

    def update(self):
        """Update repository."""
        return self.exec_on_path("svn update")

    def show(self):
        """Show repository details."""
        raise NotImplemented("TODO: Not implemented")
