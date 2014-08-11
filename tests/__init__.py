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
import sys
import unittest

from mock import Mock
from mock import patch
from tests.helpers import YodaTestHelper
from yoda import Config
from yoda import find_path
from yoda import slashes2dash
from yoda import yn_choice


class TestFindPathFunction(YodaTestHelper):
    """Test suite for find_path function."""
    def setUp(self):
        """Setup test suite."""
        super(TestFindPathFunction, self).setUp()
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

        self.config = Config(self.sandbox.path + "/config")
        self.config.update(config_data)

    def test_find_path_workspace(self):
        """Test find_path for workspace."""
        res = find_path("yoda", self.config)
        self.assertEqual(4, len(res))
        self.assertIn("yoda/yoda", res)
        self.assertIn("yoda/other", res)
        self.assertIn("yoda/1337", res)
        self.assertIn("sliim/yoda", res)

    def test_find_path_workspace_only(self):
        """Test find_path for workspace only."""
        res = find_path("sliim", self.config, True)
        self.assertEqual(1, len(res))
        self.assertIn("sliim", res)

    def test_find_path_repository(self):
        """Test find_path for repository."""
        res = find_path("other", self.config)
        self.assertEqual(1, len(res))
        self.assertIn("yoda/other", res)

    def test_find_path_workspace_and_repository(self):
        """Test find_path for workspace/repository."""
        res = find_path("yoda/1337", self.config)
        self.assertEqual(1, len(res))
        self.assertIn("yoda/1337", res)

    def test_find_path_no_matches(self):
        """Test find_path when no matches found."""
        self.assertEqual({}, find_path("foo/bar", self.config))

    def test_find_path_no_workspace(self):
        """Test find_path when no workspace registered."""
        self.config = Config(self.sandbox.path + "/fake-config")
        self.assertEqual({}, find_path(
            "yoda/yoda", self.config))

    def test_find_path_raise_value_error(self):
        """
        Test find_path raises a ValueError when there is more than one slash.
        """
        self.assertRaises(ValueError, find_path, "foo/bar/baz", self.config)


class TestSlashesToDashFunction(YodaTestHelper):
    """Test suite for slashes2dash function."""
    def test_without_slashes(self):
        """Test slashes2dash function without slashes in string."""
        self.assertEqual("foo", slashes2dash("foo"))

    def test_with_slashes(self):
        """Test slashes2dash function with slashes in string."""
        self.assertEqual("foo-bar", slashes2dash("foo/bar"))

builtins_module = "builtins" if sys.version[:1] == "3" else "__builtin__"


class YNChoiceTest(unittest.TestCase):
    """Test suite for yn_choice function."""
    @patch("%s.input" % builtins_module,
           Mock(side_effect=["n", "y", "1337"]))
    def test_yn_choice(self):
        """Test printing input question."""
        self.assertFalse(yn_choice("Test?"))
        self.assertTrue(yn_choice("Test?"))
        self.assertFalse(yn_choice("Test?"))
