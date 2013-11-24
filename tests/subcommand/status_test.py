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
import argparse

from mock import Mock
from ..utils import mock_config
from yoda.subcommand import Status


class TestSubcommandStatus(unittest.TestCase):
    """ Status subcommand test suite """
    parser = None
    subparser = None
    status = None

    def setUp(self):
        """ Setup test suite """
        self.parser = argparse.ArgumentParser(prog="yoda_test")
        self.subparser = self.parser.add_subparsers(dest="subcommand_test")

        config_data = {
            "workspaces": {
                "yoda": {
                    "path": "/yoda",
                    "repositories": {
                        "yoda": "/yoda/yoda",
                        "other": "/yoda/other",
                        "1337": "/yoda/1337"
                    }
                }
            }
        }

        self.status = Status()
        self.status.setup(
            "status", mock_config(config_data), self.subparser)

    def tearDown(self):
        """ Tear down test suite """
        self.parser = None
        self.status = None

    def test_parse_status(self):
        """ Test parse status subcommand """
        self.status.parse()

        args = self.parser.parse_args(["status", "ws1/repo1"])

        self.assertEqual("status", args.subcommand_test)
        self.assertEqual("ws1/repo1", args.name)