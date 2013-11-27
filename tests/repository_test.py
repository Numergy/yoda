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

from yoda import Repository, RepositoryAdapterNotFound, RepositoryPathInvalid
from yoda.adapter import Git as GitAdapter
from .utils import Sandbox


class TestRepository(unittest.TestCase):
    """ Repository object test suite """

    def setUp(self):
        """ Setup sandbox """
        self.sandbox = Sandbox()

    def tearDown(self):
        """ Destroy sandbox """
        self.sandbox.destroy()

    def test_path_not_exists(self):
        """ Test repository path when doesn't exists """
        self.assertRaises(
            RepositoryPathInvalid, Repository, "/dir/doesnt/exists")

    def test_repository_not_valid_path_isfile(self):
        """ Test repository is not valid because path is file """
        self.sandbox.touch("invalid_repo")

        self.assertRaises(
            RepositoryPathInvalid, Repository,
            os.path.join(self.sandbox.path, "invalid_repo"))

    def test_repository_not_valid_path_isdir(self):
        """ Test repository is not valid when path is directory,
        but adapter not found """
        self.sandbox.mkdir("invalid_repo")
        self.assertRaises(
            RepositoryAdapterNotFound, Repository,
            os.path.join(self.sandbox.path, "invalid_repo"))

    def test_repository_valid_scm_git(self):
        """ Test repository is valid and is a git repository """
        self.sandbox.mkdir("git_repo")
        self.sandbox.mkdir("git_repo/.git")

        repo = Repository("%s/git_repo" % self.sandbox.path)
        self.assertIsInstance(repo.adapter, GitAdapter)
