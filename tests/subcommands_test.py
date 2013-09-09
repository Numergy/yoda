import unittest

from mock import Mock

from yoda.subcommands import Subcommand
from yoda.subcommands import Subcommands


class TestSubcommand(unittest.TestCase):
    """ Subcommand test suite """

    def test_setup(self):
        """ Test subcommand's attributes setup """
        subcmd = Subcommand()
        subcmd.setup("foo", "bar")
        self.assertEqual("foo", subcmd.config)
        self.assertEqual("bar", subcmd.subparser)


class TestSubcommands(unittest.TestCase):
    """ Workspace subcommands test suite """
    subcmds = None
    mocks = {}

    def setUp(self):
        """ Setup test suite """
        self.mocks["subcmd"] = Mock()
        self.mocks["subcmd"].setup.return_value = None
        self.mocks["subcmd"].parse.return_value = None
        self.mocks["subcmd"].execute.return_value = None

        self.mocks["config"] = Mock()
        self.subcmds = Subcommands(self.mocks["config"])

    def tearDown(self):
        """ Tear down test suite """
        self.mocks = None
        self.subcmds = None

    def test_add_command(self):
        """ Test add subcommand """
        self.subcmds.add_command(self.mocks["subcmd"])

        self.assertTrue("mock" in self.subcmds.commands)
        self.assertEqual(self.mocks["subcmd"], self.subcmds.commands["mock"])

    def test_parse(self):
        """ Test parse subcommand """
        self.subcmds.commands = {"Mock": self.mocks["subcmd"]}
        self.subcmds.parse()
        self.mocks["subcmd"].parse.assert_called_once()

    def test_execute(self):
        """ Test execute subcommand """
        args = Mock()
        args.subcommand = "Mock"
        self.subcmds.commands = {"Mock": self.mocks["subcmd"]}
        self.subcmds.execute(args)
        self.mocks["subcmd"].execute.assert_called_once()
