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

from mock import patch
from tests.utils import Sandbox
from yoda.adapter import Git as GitAdapter
from yoda.adapter import Svn as SvnAdapter
from yoda import Repository
from yoda.repository import clone
from yoda import RepositoryAdapterNotFound
from yoda import RepositoryPathInvalid


class TestRepository(unittest.TestCase):
    """Repository object test suite."""

    def setUp(self):
        """Setup sandbox."""
        self.sandbox = Sandbox()

    def tearDown(self):
        """Destroy sandbox."""
        self.sandbox.destroy()

    def test_path_not_exists(self):
        """Test repository path when doesn't exists."""
        self.assertRaises(
            RepositoryPathInvalid, Repository, "/dir/doesnt/exists")

    def test_repository_not_valid_path_isfile(self):
        """Test repository is not valid because path is file."""
        self.sandbox.touch("invalid_repo")

        self.assertRaises(
            RepositoryPathInvalid, Repository,
            os.path.join(self.sandbox.path, "invalid_repo"))

    def test_repository_not_valid_path_isdir(self):
        """
        Test repository is not valid when path is directory,
        but adapter not found.
        """
        self.sandbox.mkdir("invalid_repo")
        self.assertRaises(
            RepositoryAdapterNotFound, Repository,
            os.path.join(self.sandbox.path, "invalid_repo"))

    def test_repository_valid_scm_git(self):
        """Test repository is valid and is a git repository."""
        self.sandbox.mkdir("git_repo")
        self.sandbox.mkdir("git_repo/.git")

        repo = Repository("%s/git_repo" % self.sandbox.path)
        self.assertIsInstance(repo.adapter, GitAdapter)

    def test_repository_valid_scm_svn(self):
        """Test repository is valid and is a git repository."""
        self.sandbox.mkdir("svn_repo")
        self.sandbox.mkdir("svn_repo/.svn")

        repo = Repository("%s/svn_repo" % self.sandbox.path)
        self.assertIsInstance(repo.adapter, SvnAdapter)

    def test_get_scm(self):
        """Test get scm for a repository."""
        self.sandbox.mkdir("git_repo")
        self.sandbox.mkdir("git_repo/.git")

        repo = Repository("%s/git_repo" % self.sandbox.path)
        self.assertEqual("Git", repo.get_scm())

    def test_get_scm_none(self):
        """Test get scm for a repository when adapter is None."""
        self.sandbox.mkdir("git_repo")
        self.sandbox.mkdir("git_repo/.git")

        repo = Repository("%s/git_repo" % self.sandbox.path)
        repo.adapter = None
        self.assertEqual(None, repo.get_scm())


class TestClone(unittest.TestCase):
    """Clone function test suite."""

    def setUp(self):
        """Setup sandbox."""
        self.sandbox = Sandbox()

    def tearDown(self):
        """Destroy sandbox."""
        self.sandbox.destroy()

    def test_clone_git_repository_http(self):
        """Test clone git repository over http."""
        with patch("yoda.repository.Git.clone") as patch_clone:
            clone(
                "https://git.project.org/foo/bar.git",
                "%s/bar" % self.sandbox.path)
            patch_clone.assert_called_once_with(
                "https://git.project.org/foo/bar.git")

    def test_clone_git_repository_ssh(self):
        """Test clone git repository over ssh."""
        with patch("yoda.repository.Git.clone") as patch_clone:
            clone(
                "git@project.org:foo/bar",
                "%s/bar" % self.sandbox.path)
            patch_clone.assert_called_once_with(
                "git@project.org:foo/bar")

    def test_clone_git_repository_adapter_not_found(self):
        """Test clone git repository when adapter not found."""
        self.assertRaises(
            RepositoryAdapterNotFound,
            clone,
            "https://project.org/foo/bar",
            "%s/bar" % self.sandbox.path)

    def test_clone_svn_repository(self):
        """Test clone svn repository over http."""
        with patch("yoda.repository.Svn.clone") as patch_clone:
            clone(
                "svn://numergy/yoda",
                "%s/bar" % self.sandbox.path)
            patch_clone.assert_called_once_with(
                "svn://numergy/yoda")
