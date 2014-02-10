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
import yaml


class Config(dict):

    config_file = None

    def __init__(self, config_file, *args, **kwargs):
        """Workspace object initialization."""
        self.config_file = config_file
        super(Config, self).__init__(*args, **kwargs)
        if not os.path.exists(config_file) or config_file is None:
            self.update({"workspaces": {}})
            self.write()
        else:
            file = open(self.config_file)
            config = yaml.load(file.read())
            file.close()
            if config is not None:
                self.update(config)

    def __delitem__(self, key):
        super(Config, self).__delitem__(key)
        self.write()

    def __setitem__(self, key, value):
        super(Config, self).__setitem__(key, value)
        self.write()

    def update(self, *args, **kwargs):
        super(Config, self).update(*args, **kwargs)
        self.write()

    def write(self):
        """
        Write config in configuration file.
        Data must me a dict.
        """
        file = open(self.config_file, "w+")
        file.write(yaml.dump(dict(self), default_flow_style=False))
        file.close()
