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
import os

from mock import Mock

from ..utils import Sandbox

from yoda.adapter import Git


class TestGit(unittest.TestCase):
    """ Git adapter test suite """
    sandbox = None
    git = None

    def setUp(self):
        """ Set up git adapter and sandbox """
        self.sandbox = Sandbox()
        self.sandbox.mkdir("repo")

        self.git = Git(os.path.join(self.sandbox.path, "repo"))
        self.git.execute = Mock(return_value=None)

    def tearDown(self):
        """ Unset test object """
        self.sandbox.destroy()
        self.git = None

    def test_status(self):
        """ Test git status """
        self.git.status()
        self.git.execute.assert_called_once_with(
            "git status",
            os.path.join(self.sandbox.path, "repo"))

    def test_update(self):
        """ Test git update """
        self.git.update()
        self.git.execute.assert_called_once_with(
            "git pull --rebase",
            os.path.join(self.sandbox.path, "repo"))

    def test_clone(self):
        """ Test git status """
        self.git.clone("git@project.org:foo/bar")
        self.git.execute.assert_called_once_with(
            "git clone %s %s" % (
                "git@project.org:foo/bar",
                os.path.join(self.sandbox.path, "repo")))
