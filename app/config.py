"""
Load configuration from config/*.yml
"""

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

class Config (object):
    __data = {}

    __instance = None

    """ Singleton pattern (not thread-safe) """
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    """ Load config from given yaml file name in config/ """
    def load(self, name):
        file_handle = file(self._getFileName(name), 'r')
        setattr(self, name, yaml.load(file_handle, Loader=Loader))

    def dump(self, name):
        file_handle = file(self._getFileName(name) + '.auto', 'w')
        yaml.dump(getattr(self, name), file_handle, Dumper=Dumper,
                  default_flow_style=False)

    def _getFileName(self, name):
        return 'config/{}.yml'.format(name)

    def __getattr__(self, name):
        try:
            self.load(name)
            return getattr(self, name)
        except IOError, e:
            print e
        except yaml.YAMLError, e:
            print e

def main():
    config = Config()
    config.load('database')
    print config.database

if __name__ == '__main__':
    main()
