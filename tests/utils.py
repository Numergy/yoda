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

import mock
import os
import shutil

from mock import Mock
from mock import MagicMock
from yoda import Config


@mock.patch('yoda.config.Config.__init__',
            Mock(return_value=None))
def mock_config(data):
    config = Config()
    config.get = MagicMock(return_value=data)
    config.write = MagicMock(return_value=None)
    return config


class Sandbox:
    """ Sandbox environment utility """
    path = None

    def __init__(self, path=None):
        """ Init sandbox environment """
        if path is None:
            path = os.path.dirname(os.path.realpath(__file__)) + "/sandbox"

        self.path = path
        if os.path.exists(path):
            self.destroy()

        os.mkdir(path)

    def mkdir(self, directory):
        """ Create directory in sandbox. """
        os.mkdir(os.path.join(self.path, directory))

    def destroy(self):
        """ Destroy sandbox environment """
        if os.path.exists(self.path):
            shutil.rmtree(self.path)
