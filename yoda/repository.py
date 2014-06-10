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

from yoda.adapter import Bzr
from yoda.adapter import Git
from yoda.adapter import Hg
from yoda.adapter import Svn


class RepositoryError(Exception):
    """Generic repository error."""
    pass


class RepositoryPathInvalid(RepositoryError):
    """Repository path is invalid, doesn't exists or is not a directory."""
    pass


class RepositoryAdapterNotFound(RepositoryError):
    """Repository invalid because adapter not found."""
    pass


class Repository:
    path = None
    adapter = None

    scm_dirs = [".git", ".svn", ".bzr", ".hg"]

    def __init__(self, path):
        if not os.path.exists(path) or not os.path.isdir(path):
            raise RepositoryPathInvalid(
                "Path doesn't exists or isn't a directory (%s)\n" % path)

        try:
            scm = (set(self.scm_dirs) & set(os.listdir(path))).pop()
        except KeyError:
            raise RepositoryAdapterNotFound("Can't define repository type")
        else:
            self.path = path
            if scm == ".git":
                self.adapter = Git(path)
            if scm == ".svn":
                self.adapter = Svn(path)
            if scm == ".bzr":
                self.adapter = Bzr(path)
            if scm == ".hg":
                self.adapter = Hg(path)

    def get_scm(self):
        """Get scm used as string."""
        if self.adapter is None:
            return None
        return self.adapter.__class__.__name__

    def status(self):
        return self.adapter.status()

    def update(self):
        return self.adapter.update()


def clone(url, path):
    """Clone a repository."""
    adapter = None
    if url[:4] == "git@" or url[-4:] == ".git":
        adapter = Git(path)
    if url[:6] == "svn://":
        adapter = Svn(path)
    if url[:6] == "bzr://":
        adapter = Bzr(path)
    if url[:9] == "ssh://hg@":
        adapter = Hg(path)

    if adapter is None:
        raise RepositoryAdapterNotFound(
            "Can't find adapter for `%s` repository url" % url)

    return adapter.clone(url)
