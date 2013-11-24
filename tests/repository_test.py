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

from yoda import Repository
from .utils import Sandbox


class TestRepository(unittest.TestCase):
    """ Repository object test suite """

    def test_path_not_exists(self):
        """ Test repository path when doesn't exists """
        self.assertRaises(
            ValueError, Repository, "/dir/doesnt/exists")

    def test_repository_is_not_valid_path_isdir(self):
        """ Test repository is not valid because not scp directory """
        sandbox = Sandbox()
        sandbox.mkdir("invalid_repo")

        repo = Repository("%s/invalid_repo" % sandbox.path)
        self.assertFalse(repo.is_valid())

    def test_repository_is_not_valid_path_isfile(self):
        """ Test repository is not valid because path is file """
        sandbox = Sandbox()
        sandbox.touch("invalid_repo")

        repo = Repository("%s/invalid_repo" % sandbox.path)
        self.assertFalse(repo.is_valid())

    def test_repository_is_valid_scm_git(self):
        """ Test repository is valid and is a git repository """
        sandbox = Sandbox()
        sandbox.mkdir("git_repo")
        sandbox.mkdir("git_repo/.git")

        repo = Repository("%s/git_repo" % sandbox.path)
        self.assertTrue(repo.is_valid())
