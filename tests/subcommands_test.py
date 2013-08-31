import unittest
import argparse

from yoda.subcommands import workspace


class TestSubcommandsWorkspace(unittest.TestCase):
    """ Workspace subcommand test suite """

    def test_add(self):
        """ Test workspace add subcommand """
        parser = self.__get_parser()
        args = parser.parse_args(["workspace", "add", "foo", "/tmp/foo"])

        self.assertEqual("add", args.workspace_subcommand)
        self.assertEqual("foo", args.name)
        self.assertEqual("/tmp/foo", args.path)

    def test_remove(self):
        """ Test workspace remove subcommand """
        parser = self.__get_parser()
        args = parser.parse_args(["workspace", "remove", "foo"])

        self.assertEqual("remove", args.workspace_subcommand)
        self.assertEqual("foo", args.name)

    def test_list(self):
        """ Test workspace add subcommand """
        parser = self.__get_parser()
        args = parser.parse_args(["workspace", "list"])
        self.assertEqual("list", args.workspace_subcommand)

    def __get_parser(self):
        """ Get parser for tests """
        parser = argparse.ArgumentParser(prog="yoda_test")
        subparser = parser.add_subparsers(dest="subcommand_test")

        subcmd = workspace(subparser)
        subcmd.parse()

        return parser
