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

from pycolorizer import Color
import sys


class Output:
    color = None
    stderr = None
    stdout = None

    def __init__(self, stdout=sys.stdout, stderr=sys.stderr):
        self.stdout = stdout
        self.stderr = stderr
        self.color = Color()

    def info(self, message):
        self.stdout.write(str(message) + "\n")

    def success(self, message):
        self.stdout.write(self.color.colored(str(message), "green") + "\n")

    def warn(self, message):
        self.stderr.write(self.color.colored(str(message), "yellow") + "\n")

    def error(self, message):
        self.stderr.write(self.color.colored(str(message), "red") + "\n")

    def yn_choice(self, message, default='n'):
        choices = 'Y/n' if default.lower() in ('y', 'yes') else 'y/N'
        choice = input("%s (%s) " % (message, choices))
        values = ('y', 'yes', '') if default == 'y' else ('y', 'yes')
        return choice.strip().lower() in values
