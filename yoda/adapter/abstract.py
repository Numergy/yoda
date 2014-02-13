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

from abc import ABCMeta
from abc import abstractmethod
from distutils.spawn import find_executable
import logging
import subprocess


class Abstract:
    """SCM Adapter interface."""
    __metaclass__ = ABCMeta

    path = None
    executable = None

    def __init__(self, path):
        self.path = path

    def execute(self, command, path=None):
        """Execute command with os.popen and return output."""
        self.check_executable()
        stdout, stderr = subprocess.Popen(
            command,
            shell=True,
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        ).communicate()

        logger = logging.getLogger(__name__)
        if stdout:
            logger.info(stdout.decode("utf-8"))

        if stderr:
            logger.error(stderr.decode("utf-8"))

    def exec_on_path(self, command):
        """Execute command in repository path."""
        self.execute("%s" % (command), self.path)

    def check_executable(self):
        """Check adapter executable exists."""
        if not find_executable(self.executable):
            raise Exception("Executable %s not found" % self.executable)

    @abstractmethod
    def status(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def clone(self):
        pass
