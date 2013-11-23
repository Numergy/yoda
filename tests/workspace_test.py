import unittest
import os.path

from .utils import mock_config
from yoda import Workspace


class TestWorkspace(unittest.TestCase):
    """ Test workspace commands """

    def test_add(self):
        """ Test add workspace """
        config = mock_config({
            "workspaces": {"foo": {"path": "/foo", "repositories": {}}}})
        ws = Workspace(config)
        ws.add("bar", os.path.realpath(__file__))
        config.write.assert_called_once_with(config.get())

    def test_add_existing_workspace(self):
        """ Test add workspace with existing name """
        config = mock_config({
            "workspaces": {"foo": {"path": "/foo", "repositories": {}}}})
        ws = Workspace(config)
        self.assertRaises(
            ValueError, ws.add, "foo", os.path.realpath(__file__))

    def test_add_with_nonexistent_path(self):
        """ Test add workspace with path doesn't exists """
        config = mock_config({"workspaces": {}})
        ws = Workspace(config)
        self.assertRaises(
            ValueError, ws.add, "foo", "/dir/doesnt/exists")

    def test_remove(self):
        """ Test remove workspace """
        config = mock_config({
            "workspaces": {"foo": {"path": "/foo", "repositories": {}}}})
        ws = Workspace(config)
        ws.remove("foo")
        config.write.assert_called_once()

    def test_remove_nonexistent(self):
        """ Test remove workspace that doesn't exists """
        config = mock_config({
            "workspaces": {"foo": {"path": "/foo", "repositories": {}}}})
        ws = Workspace(config)
        self.assertRaises(
            ValueError, ws.remove, "bar")

    def test_list(self):
        """ Test list workspace """
        config_mock_data = {"workspaces": {
            "foo": {"path": "/foo", "repositories": {}},
            "bar": {"path": "/bar", "repositories": {}}}}

        ws = Workspace(mock_config(config_mock_data))
        list = ws.list()
        self.assertIn("foo", list)
        self.assertIn("bar", list)
        self.assertEqual(
            {"name": "foo",
             "path": "/foo",
             "repositories": {}}, list["foo"])
        self.assertEqual(
            {"name": "bar",
             "path": "/bar",
             "repositories": {}}, list["bar"])

    def test_exists(self):
        """ Test exists workspace """
        config_mock_data = {
            "workspaces": {"foo": {"path": "/foo", "repositories": {}}}}
        ws = Workspace(mock_config(config_mock_data))
        self.assertTrue(ws.exists("foo"))

    def test_not_exists(self):
        """ Test workspace doesn't exists"""
        config_mock_data = {
            "workspaces": {"foo": {"path": "/foo", "repositories": {}}}}
        ws = Workspace(mock_config(config_mock_data))
        self.assertFalse(ws.exists("bar"))

    def test_not_instance_of_config(self):
        """ Test if parameter is an instance of Config"""
        self.assertRaises(TypeError, lambda: Workspace(()))
