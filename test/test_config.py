""" Test Config class. """

import unittest

import os

from app.config import Config

class TestConfig (unittest.TestCase):
    """ Test Config class. """

    def setUp(self):
        """ Set up Config instance. """
        config_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  'config')
        self.config = Config(config_dir)

    def test_singleton_shared_state(self):
        """ Check that two instances share state. """
        second = Config()
        second.foo = 'bar'
        self.assertEqual('bar', self.config.foo)
        self.config.bar = 'bash'
        self.assertEqual('bash', second.bar)

    def test_separate_tests(self):
        """ Test that tests do not affect each other's copy of config. """
        # Note, this relies on an implementation detail
        self.assertNotIn('foo', self.config.__dict__)

    def test_load(self):
        """ Test loading a yaml config file. """
        self.config.load('database')
        self.assertIsNotNone(self.config.database)

    def test_auto_load(self):
        """ Test autoloading a yaml config file. """
        self.assertIsNotNone(self.config.database)

if __name__ == '__main__':
    unittest.main()
