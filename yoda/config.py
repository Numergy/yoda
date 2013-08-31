import yaml
import os.path


class config:

    config_file = None

    def __init__(self, config_file):
        """ Workspace object initialization """
        self.config_file = config_file
        if not (os.path.exists(config_file)):
            config = {"workspaces": {}}
            self.write(config)

    def get(self):
        """ Get config file contents """
        file = open(self.config_file)
        config = yaml.load(file.read())
        file.close()
        return config

    def write(self, data):
        """ Write config in configuration file.
        Given config must me a dict"""
        file = open(self.config_file, "w+")
        file.write(yaml.dump(data))
        file.close()
