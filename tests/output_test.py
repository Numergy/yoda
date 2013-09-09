import unittest

from mock import Mock
from yoda.output import output


class TestOutput(unittest.TestCase):
    """ Yoda output test suite """

    out = None
    stdout = None
    stderr = None

    def setUp(self):
        """ Setup output object """
        self.stdout = self.stderr = Mock()
        self.stdout.write.return_value = None
        self.stderr.write.return_value = None
        self.out = output(self.stdout, self.stderr)

    def test_info(self):
        """ Test printing an information message """
        self.out.info("foo")
        self.stdout.write.assert_called_once_with("foo\n")

    def test_success(self):
        """ Test printing a success message """
        self.out.success("bar")
        self.stdout.write.assert_called_once_with("\033[92mbar\033[0m\n")

    def test_warn(self):
        """ Test printing a warning message """
        self.out.warn("baz")
        self.stderr.write.assert_called_once_with("\033[93mbaz\033[0m\n")

    def test_error(self):
        """ Test printing an error message """
        self.out.error("foobar")
        self.stderr.write.assert_called_once_with("\033[91mfoobar\033[0m\n")
