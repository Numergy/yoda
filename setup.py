#!/usr/bin/env python
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

import os
from setuptools.command.install import install
from setuptools import setup
from subprocess import call


class InstallCommand(install):
    def run(self):
        bash_completion = os.path.expanduser(
            "~/.bash_completion.d/python-argcomplete.sh"
        )
        bash_dir = os.path.dirname(bash_completion)
        if os.path.exists(bash_dir) is False:
            os.mkdir(bash_dir)

        if os.path.exists(bash_completion) is False:
            os.system("activate-global-python-argcomplete --dest=" + bash_dir)

        super(InstallCommand, self).run()

setup(
    name="yoda",
    version="0.1",
    description="",
    license="",
    scripts=["scripts/yoda"],
    packages=["yoda", "yoda.subcommand", "yoda.adapter"],
    install_requires=[
        u"PyYaml",
        u"pycolorizer",
        u"PrettyTable",
        u"argcomplete"
    ],
    tests_require=[
        u"mock",
        u"nose",
        u"pep8",
        u"coverage"
    ],
    cmdclass={
        "install": InstallCommand,
    }
)
