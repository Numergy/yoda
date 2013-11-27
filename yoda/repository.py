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

from yoda.adapter import Git


class RepositoryError(Exception):
    """ Genereic repository error """
    pass


class RepositoryPathInvalid(RepositoryError):
    """ Repository path is invalid, doesn't exists or is not a directory. """
    pass


class RepositoryAdapterNotFound(RepositoryError):
    """ Repository invalid because adapter not found """
    pass


class Repository:
    path = None
    adapter = None

    scm_dirs = [".git"]

    def __init__(self, path):
        if not os.path.exists(path) or not os.path.isdir(path):
            raise RepositoryPathInvalid(
                "Path doesn't exists or isn't a directory (%s)\n" % path)

        if len(set(self.scm_dirs) & set(os.listdir(path))) == 0:
            raise RepositoryAdapterNotFound("Can't define repository type")

        self.path = path
        #TODO: Init adapter from repository type
        self.adapter = Git(path)

    def status(self):
        return self.adapter.status()
