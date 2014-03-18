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

import argparse
import os
import shutil
import unittest
import yaml
from mock import Mock
from yoda import Config


class Sandbox:
    """Sandbox environment utility."""
    path = None

    def __init__(self, path=None):
        """Init sandbox environment."""
        if path is None:
            path = os.path.dirname(os.path.realpath(__file__)) + "/sandbox"

        self.path = path
        if os.path.exists(path):
            self.destroy()

        os.mkdir(path)

    def mkdir(self, directory):
        """Create directory in sandbox.."""
        os.mkdir(os.path.join(self.path, directory))

    def touch(self, file):
        """Create file  into sandbox."""
        full_path = os.path.join(self.path, file)
        with open(full_path, 'w'):
            os.utime(full_path, None)

    def destroy(self):
        """Destroy sandbox environment."""
        if os.path.exists(self.path):
            shutil.rmtree(self.path)


class YodaTestHelper(unittest.TestCase):
    """Yoda test helper class.
    This class provides custom assertions for yoda's tests suite.
    """
    sandbox = None

    def setUp(self):
        """Setup sandbox."""
        self.sandbox = Sandbox()

    def tearDown(self):
        """Destroy sandbox."""
        self.sandbox.destroy()

    def assert_config_file_contains(self, config_file, expected):
        """Custom assert to check content of config_file"""
        file = open(config_file)
        config = yaml.load(file.read())
        file.close()
        self.assertEquals(config, expected)


class SubcommandTestHelper(YodaTestHelper):
    """Subcommand test helper class."""
    config = None
    parser = None
    subparser = None
    subcommand = None
    subcommand_str = None

    def setUp(self):
        """Setup test suite."""
        super(SubcommandTestHelper, self).setUp()
        self.parser = argparse.ArgumentParser(prog="yoda_test")
        self.subparser = self.parser.add_subparsers(dest="subcommand")

        self.config = Config(self.sandbox.path + "/config")

        if self.subcommand is not None and self.subcommand_str is not None:
            self.subcommand.setup(
                self.subcommand_str, self.config, self.subparser)

    def tearDown(self):
        """Tear down test suite."""
        super(SubcommandTestHelper, self).tearDown()
        self.parser = None
        self.subcommand = None

    def assert_subcommand_parsing(self, commands, expected):
        """This method provides a way to assert subcommand parsing."""
        self.subcommand.parse()
        args = self.parser.parse_args(commands)

        for k, v in expected.items():
            self.assertEqual(v, getattr(args, k))

    def assert_subcommand_parsing_raises_error(self, commands, error_expected):
        """This method provides a way to assert subcommand parsing."""
        self.subcommand.parse()
        self.assertRaises(
            error_expected,
            self.parser.parse_args, commands
        )

    def assert_subcommand_exec_raises_error(self, args, error_expected):
        """Asserts an error when execute subcommand with passed args."""
        self.subcommand.parse()
        self.assertRaises(error_expected, self.subcommand.execute, args)


class AdapterTestHelper(YodaTestHelper):
    """Adapter test helper class."""
    adapter_class = None
    adapter = None

    def setUp(self):
        """Generic setup for adapter test cases."""
        super(AdapterTestHelper, self).setUp()
        self.sandbox.mkdir("repository")

        self.adapter = self.adapter_class(
            os.path.join(self.sandbox.path, "repository"))
        self.adapter.execute = Mock(return_value=None)

    def tearDown(self):
        """Unset test object."""
        super(AdapterTestHelper, self).tearDown()
        self.adapter_class = None
        self.adapter = None

    def assert_executed_command(self, expected_cmd, with_path=True):
        """Assert that adapter has executed expected command."""
        if not with_path:
            self.adapter.execute.assert_called_once_with(expected_cmd)
        else:
            self.adapter.execute.assert_called_once_with(
                expected_cmd,
                os.path.join(self.sandbox.path, "repository"))
