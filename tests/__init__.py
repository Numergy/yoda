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

from .utils import mock_config, Sandbox

from yoda import find_path


class TestFindPathFunction(unittest.TestCase):
    """ Test suite for find_path function """

    def setUp(self):
        """ Setup test suite """
        self.sandbox = Sandbox()
        self.sandbox.mkdir("yoda")
        self.sandbox.mkdir("yoda/yoda")
        self.sandbox.mkdir("yoda/other")

        self.sandbox.mkdir("sliim")
        self.sandbox.mkdir("sliim/emacs.d")
        self.sandbox.mkdir("sliim/yoda")

        config_data = {
            "workspaces": {
                "yoda": {
                    "path": os.path.join(self.sandbox.path, "yoda"),
                    "repositories": {
                        "yoda": os.path.join(self.sandbox.path, "yoda/yoda"),
                        "other": os.path.join(self.sandbox.path, "yoda/other"),
                        "1337": os.path.join(self.sandbox.path, "yoda/1337")
                    }
                },
                "sliim": {
                    "path": os.path.join(self.sandbox.path, "sliim"),
                    "repositories": {
                        "misc": os.path.join(self.sandbox.path, "sliim/misc"),
                        "yoda": os.path.join(self.sandbox.path, "sliim/yoda")
                    }
                }
            }
        }

        self.config = mock_config(config_data)

    def tearDown(self):
        """ Destroy sandbox """
        self.sandbox.destroy()

    def test_find_path_workspace(self):
        """ Test find_path for workspace """
        res = find_path("yoda", self.config)
        self.assertEqual(4, len(res))
        self.assertIn("yoda/yoda", res)
        self.assertIn("yoda/other", res)
        self.assertIn("yoda/1337", res)
        self.assertIn("sliim/yoda", res)

    def test_find_path_workspace_only(self):
        """ Test find_path for workspace only """
        res = find_path("sliim", self.config, True)
        self.assertEqual(1, len(res))
        self.assertIn("sliim", res)

    def test_find_path_repository(self):
        """ Test find_path for repository """
        res = find_path("other", self.config)
        self.assertEqual(1, len(res))
        self.assertIn("yoda/other", res)

    def test_find_path_workspace_and_repository(self):
        """ Test find_path for workspace/repository"""
        res = find_path("yoda/1337", self.config)
        self.assertEqual(1, len(res))
        self.assertIn("yoda/1337", res)

    def test_find_path_no_matches(self):
        """ Test find_path when no matches found """
        self.assertEqual({}, find_path("foo/bar", self.config))

    def test_find_path_no_workspace(self):
        """ Test find_path when no workspace registered """
        self.assertEqual({}, find_path(
            "yoda/yoda", mock_config({"workspaces": {}})))
