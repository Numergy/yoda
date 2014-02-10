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

import os.path
import unittest

from tests.utils import mock_config
from tests.utils import Sandbox
from yoda import Workspace


class TestWorkspace(unittest.TestCase):
    """Test workspace commands."""

    def test_add(self):
        """Test add workspace."""
        config = mock_config({
            "workspaces": {"foo": {"path": "/foo", "repositories": {}}}})
        ws = Workspace(config)
        ws.add("bar", os.path.realpath(__file__))
        config.write.assert_called_once_with(config.get())

    def test_add_existing_workspace(self):
        """Test add workspace with existing name."""
        config = mock_config({
            "workspaces": {"foo": {"path": "/foo", "repositories": {}}}})
        ws = Workspace(config)
        self.assertRaises(
            ValueError, ws.add, "foo", os.path.realpath(__file__))

    def test_add_with_nonexistent_path(self):
        """Test add workspace with path doesn't exists."""
        config = mock_config({"workspaces": {}})
        ws = Workspace(config)
        self.assertRaises(
            ValueError, ws.add, "foo", "/dir/doesnt/exists")

    def test_remove(self):
        """Test remove workspace."""
        config = mock_config({
            "workspaces": {"foo": {"path": "/foo", "repositories": {}}}})
        ws = Workspace(config)
        ws.remove("foo")
        config.write.assert_called_once()

    def test_remove_nonexistent(self):
        """Test remove workspace that doesn't exists."""
        config = mock_config({
            "workspaces": {"foo": {"path": "/foo", "repositories": {}}}})
        ws = Workspace(config)
        self.assertRaises(
            ValueError, ws.remove, "bar")

    def test_list(self):
        """Test list workspace."""
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
        """Test exists workspace."""
        config_mock_data = {
            "workspaces": {"foo": {"path": "/foo", "repositories": {}}}}
        ws = Workspace(mock_config(config_mock_data))
        self.assertTrue(ws.exists("foo"))

    def test_not_exists(self):
        """Test workspace doesn't exists."""
        config_mock_data = {
            "workspaces": {"foo": {"path": "/foo", "repositories": {}}}}
        ws = Workspace(mock_config(config_mock_data))
        self.assertFalse(ws.exists("bar"))

    def test_not_instance_of_config(self):
        """Test if parameter is an instance of Config."""
        self.assertRaises(TypeError, lambda: Workspace(()))

    def test_repository_exists(self):
        """Test workspace has repository."""
        config_mock_data = {"workspaces": {
            "foo": {"path": "/foo", "repositories": {"repo1": "/foo/repo1"}}}}
        ws = Workspace(mock_config(config_mock_data))
        self.assertTrue(ws.repository_exists("foo", "repo1"))

    def test_has_not_repo(self):
        """Test workspace has not repository."""
        config_mock_data = {"workspaces": {
            "foo": {"path": "/foo", "repositories": {"repo1": "/foo/repo1"}}}}
        ws = Workspace(mock_config(config_mock_data))
        self.assertFalse(ws.repository_exists("foo", "repo2"))

    def test_repository_exists_invalid_workspace(self):
        """Test workspace has not repository."""
        config_mock_data = {"workspaces": {
            "foo": {"path": "/foo", "repositories": {"repo1": "/foo/repo1"}}}}
        ws = Workspace(mock_config(config_mock_data))
        self.assertFalse(ws.repository_exists("bar", "repo1"))
