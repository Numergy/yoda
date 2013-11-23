import os.path
from yoda import Config


class Workspace:

    config = None

    def __init__(self, config):
        """ Workspace object initialization """
        if not isinstance(config, Config):
            raise TypeError("Variable config is not an instance of Config")
        self.config = config

    def add(self, name, path):
        """ Add a workspace entry in user config file """
        if not (os.path.exists(path)):
            raise ValueError("Workspace path `%s` dosn't exists." % path)

        if (self.exists(name)):
            raise ValueError("Workspace `%s` already exists." % name)

        config = self.config.get()
        config["workspaces"][name] = {"path": path, "repositories": {}}

        self.config.write(config)

    def remove(self, name):
        """ Remove workspace from config file """
        config = self.config.get()

        if not (self.exists(name)):
            raise ValueError("Workspace `%s` doesn't exists." % name)

        config["workspaces"].pop(name, 0)

        self.config.write(config)

    def list(self):
        """ List all available workspaces """
        config = self.config.get()
        ws_list = {}

        for key, value in config["workspaces"].items():
            ws_list[key] = dict({"name": key}, **value)

        return ws_list

    def exists(self, name):
        """ Check if given workspace name exists """
        list = self.list()
        return name in list.keys()
