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


class Repository:
    path = None
    adapter = None

    scm_dirs = [".git"]

    def __init__(self, path):
        if not os.path.exists(path):
            raise ValueError(
                "Repository path doesn't exists (%s)" % path)

        self.path = path
        #TODO: Init adapter from repository type
        self.adapter = Git(path)

    def is_valid(self):
        if not os.path.isdir(self.path):
            return False

        return set(self.scm_dirs).intersection(
            set(os.listdir(self.path))) != set()

    def status(self):
        return self.adapter.status()
