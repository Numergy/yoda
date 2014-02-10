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
from mock import patch
import os.path
import unittest

from tests.utils import Sandbox
from yoda import Config
from yoda import Workspace


class TestWorkspace(unittest.TestCase):
    """Test workspace commands."""

    config = None
    sandbox = None

    def setUp(self):
        self.sandbox = Sandbox()
        self.config = Config(self.sandbox.path + "/config")

    def tearDown(self):
        self.sandbox.destroy()

    def test_add(self):
        """Test add workspace."""
        self.config.update({
            "workspaces": {"foo": {"path": "/foo", "repositories": {}}}})
        ws = Workspace(self.config)
        ws.add("bar", os.path.realpath(__file__))

    def test_add_existing_workspace(self):
        """Test add workspace with existing name."""
        self.config.update({
            "workspaces": {"foo": {"path": "/foo", "repositories": {}}}})
        ws = Workspace(self.config)
        self.assertRaises(
            ValueError, ws.add, "foo", os.path.realpath(__file__))

    def test_add_with_nonexistent_path(self):
        """Test add workspace with path doesn't exists."""
        self.config.update({"workspaces": {}})
        ws = Workspace(self.config)
        self.assertRaises(
            ValueError, ws.add, "foo", "/dir/doesnt/exists")

    def test_remove(self):
        """Test remove workspace."""
        self.config.update({
            "workspaces": {"foo": {"path": "/foo", "repositories": {}}}})
        ws = Workspace(self.config)
        ws.remove("foo")

    def test_remove_nonexistent(self):
        """Test remove workspace that doesn't exists."""
        self.config.update({
            "workspaces": {"foo": {"path": "/foo", "repositories": {}}}})
        ws = Workspace(self.config)
        self.assertRaises(
            ValueError, ws.remove, "bar")

    def test_list(self):
        """Test list workspace."""
        config_mock_data = {"workspaces": {
            "foo": {"path": "/foo", "repositories": {}},
            "bar": {"path": "/bar", "repositories": {}}}}
        self.config.update(config_mock_data)

        ws = Workspace(self.config)
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
        """Test exists workspace."""
        config_mock_data = {
            "workspaces": {"foo": {"path": "/foo", "repositories": {}}}}
        self.config.update(config_mock_data)
        ws = Workspace(self.config)
        self.assertTrue(ws.exists("foo"))

    def test_not_exists(self):
        """Test workspace doesn't exists."""
        config_mock_data = {
            "workspaces": {"foo": {"path": "/foo", "repositories": {}}}}
        self.config.update(config_mock_data)
        ws = Workspace(self.config)
        self.assertFalse(ws.exists("bar"))

    def test_not_instance_of_config(self):
        """Test if parameter is an instance of Config."""
        self.assertRaises(TypeError, lambda: Workspace(()))

    def test_repository_exists(self):
        """Test workspace has repository."""
        config_mock_data = {"workspaces": {
            "foo": {"path": "/foo", "repositories": {"repo1": "/foo/repo1"}}}}
        self.config.update(config_mock_data)
        ws = Workspace(self.config)
        self.assertTrue(ws.repository_exists("foo", "repo1"))

    def test_has_not_repo(self):
        """Test workspace has not repository."""
        config_mock_data = {"workspaces": {
            "foo": {"path": "/foo", "repositories": {"repo1": "/foo/repo1"}}}}
        self.config.update(config_mock_data)
        ws = Workspace(self.config)
        self.assertFalse(ws.repository_exists("foo", "repo2"))

    def test_repository_exists_invalid_workspace(self):
        """Test workspace has not repository."""
        config_mock_data = {"workspaces": {
            "foo": {"path": "/foo", "repositories": {"repo1": "/foo/repo1"}}}}
        self.config.update(config_mock_data)
        ws = Workspace(self.config)
        self.assertFalse(ws.repository_exists("bar", "repo1"))
