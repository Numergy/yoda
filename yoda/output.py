import sys
from pycolorizer import Color


class Output:
    color = None
    stderr = None
    stdout = None

    def __init__(self, stdout=sys.stdout, stderr=sys.stderr):
        self.stdout = stdout
        self.stderr = stderr
        self.color = Color()

    def info(self, message):
        self.stdout.write(message + "\n")

    def success(self, message):
        self.stdout.write(self.color.colored(message, "green") + "\n")

    def warn(self, message):
        self.stderr.write(self.color.colored(message, "yellow") + "\n")

    def error(self, message):
        self.stderr.write(self.color.colored(message, "red") + "\n")
