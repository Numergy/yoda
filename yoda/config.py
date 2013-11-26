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

import yaml
import os.path


class Config:

    config_file = None

    def __init__(self, config_file):
        """ Workspace object initialization """
        self.config_file = config_file
        if not os.path.exists(config_file):
            config = {"workspaces": {}}
            self.write(config)

    def get(self):
        """ Get config file contents """
        file = open(self.config_file)
        config = yaml.load(file.read())
        file.close()
        return config

    def write(self, data):
        """
        Write config in configuration file.
        Data must me a dict.
        """
        file = open(self.config_file, "w+")
        file.write(yaml.dump(data, default_flow_style=False))
        file.close()
