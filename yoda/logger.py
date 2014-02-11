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

import copy
import logging
import os
import traceback

from prettytable import PrettyTable

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': RED,
    'ERROR': RED
}
FORMAT = """[%(asctime)s] [%(levelname)s] <%(name)s> - \
%(message)s (%(filename)s:%(lineno)d)"""
LFORMAT = "%(levelname)s: %(message)s"


class Formatter(logging.Formatter):
    def format(self, record):
        rec = copy.copy(record)

        if isinstance(rec.msg, Exception) and self._fmt == FORMAT:
            rec.msg = "%s\n%s" % (rec.msg, traceback.format_exc())

        if isinstance(rec.msg, PrettyTable):
            rec.msg = "\n%s" % rec.msg

        level = record.levelname

        if level in COLORS:
            lvlname = COLOR_SEQ % (30 + COLORS[level]) + level + RESET_SEQ
            rec.levelname = lvlname

        if level == "INFO" and self._fmt != FORMAT:
            formatter = Formatter("%(message)s")
            return formatter.format(rec)

        return logging.Formatter.format(self, rec)


class Logger(logging.Logger):
    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.DEBUG)

    def set_file_handler(self, logfile):
        """Set FileHandler"""
        handler = logging.FileHandler(logfile)
        handler.setLevel(logging.NOTSET)
        handler.setFormatter(Formatter(FORMAT))

        self.addHandler(handler)

    def set_console_handler(self, debug=False):
        """Set Console handler."""
        console = logging.StreamHandler()
        console.setFormatter(Formatter(LFORMAT))
        if not debug:
            console.setLevel(logging.INFO)

        self.addHandler(console)
