import os.path


class workspace:

    config = None

    def __init__(self, config):
        """ Workspace object initialization """
        #TODO: Check instance of config
        self.config = config

    def add(self, name, path):
        """ Add a workspace entry in user config file """
        if not (os.path.exists(path)):
            raise ValueError("Workspace path `%s` dosn't exists." % path)

        if (self.exists(name)):
            raise ValueError("Workspace `%s` already exists." % name)

        config = self.config.get()
        config["workspaces"][name] = path

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
        return config["workspaces"]

    def exists(self, name):
        """ Check if given workspace name exists """
        list = self.list()
        return name in list.keys()
