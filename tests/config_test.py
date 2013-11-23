import os
import unittest

from yoda import Config


class TestConfig(unittest.TestCase):
    """ Yoda configuration test suite """

    file = "/tmp/yoda_config_test.txt"

    def setUp(self):
        """ Setup test file """
        file = open(self.file, "w")
        file.write("foo: \n  bar: baz\n  bur: buz\n")
        file.close()

    def tearDown(self):
        """ Remove test file """
        os.remove(self.file)

    def test_init(self):
        file = "/tmp/yoda_config.txt"
        conf = Config(file)
        self.assertTrue(os.path.exists(file))
        os.remove(file)

    def test_get(self):
        """ Test get configuration """
        conf = Config(self.file)
        config = conf.get()
        self.assertIn("foo", config)
        self.assertIn("bar", config["foo"])
        self.assertEqual("baz", config["foo"]["bar"])
        self.assertIn("bur", config["foo"])
        self.assertEqual("buz", config["foo"]["bur"])

    def test_write(self):
        """ Test write configuration """
        config = {
            "foobar": {
                "baz": "foo",
                "foo": "bar"
            }
        }

        conf = Config(self.file)
        conf.write(config)
        file = open(self.file, "r")
        content = file.read()
        file.close()

        self.assertEqual("foobar:\n  baz: foo\n  foo: bar\n", content)
