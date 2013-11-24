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

from yoda import Config
from .utils import Sandbox


class TestConfig(unittest.TestCase):
    """ Yoda configuration test suite """

    file = None

    def setUp(self):
        """ Setup test file """
        self.sandbox = Sandbox()
        self.file = self.sandbox.path + "/yoda_config_test.txt"
        file = open(self.file, "w")
        file.write("foo: \n  bar: baz\n  bur: buz\n")
        file.close()

    def tearDown(self):
        """ Remove test file """
        os.remove(self.file)

    def test_init(self):
        file = "/tmp/yoda_config.txt"
        conf = Config(file)
        self.assertTrue(os.path.exists(file))
        os.remove(file)

    def test_get(self):
        """ Test get configuration """
        conf = Config(self.file)
        config = conf.get()
        self.assertIn("foo", config)
        self.assertIn("bar", config["foo"])
        self.assertEqual("baz", config["foo"]["bar"])
        self.assertIn("bur", config["foo"])
        self.assertEqual("buz", config["foo"]["bur"])

    def test_write(self):
        """ Test write configuration """
        config = {
            "foobar": {
                "baz": "foo",
                "foo": "bar"
            }
        }

        conf = Config(self.file)
        conf.write(config)
        file = open(self.file, "r")
        content = file.read()
        file.close()

        self.assertEqual("foobar:\n  baz: foo\n  foo: bar\n", content)
