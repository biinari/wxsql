""" Load configuration from config/*.yml """

import os
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

class Config (object):
    """ Configuration settings manager """

    _config_dir = None

    __instance = None

    def __new__(cls, *args, **kwargs):
        """ Singleton pattern (not thread-safe) """
        if not cls.__instance:
            cls.__instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self, config_dir=None):
        """ Initialise Configuration manager with config directory. """
        super(Config, self).__init__(self)
        if config_dir:
            self._config_dir = config_dir
        else:
            self._config_dir = os.path.join(os.path.dirname(os.path.dirname(
                os.path.realpath(__file__))), 'config')

    def load(self, name):
        """ Load config from given yaml file name in config directory. """
        file_handle = file(self._get_file_name(name), 'r')
        setattr(self, name, yaml.load(file_handle, Loader=Loader))

    def dump(self, name):
        """ Dump given set of config settings into yaml file. """
        file_handle = file(self._get_file_name(name), 'w')
        yaml.dump(getattr(self, name), file_handle, Dumper=Dumper,
                  default_flow_style=False)

    def _get_file_name(self, name):
        """ Return file path for yaml config with given name. """
        return os.path.join(self._config_dir, '{}.yml'.format(name))

    def __getattr__(self, name):
        """ Automatically load config file if not already loaded. """
        try:
            self.load(name)
            return getattr(self, name)
        except IOError, exc:
            print exc
        except yaml.YAMLError, exc:
            print exc

def main():
    """ Sanity test for loading database settings. """
    config = Config()
    print config._config_dir
    config.load('database')
    print config.database

if __name__ == '__main__':
    main()
