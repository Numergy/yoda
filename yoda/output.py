import sys


class output:
    GREEN = "\033[92m%s\033[0m"
    YELLOW = "\033[93m%s\033[0m"
    RED = "\033[91m%s\033[0m"

    def __init__(self, stdout=sys.stdout, stderr=sys.stderr):
        self.stdout = stdout
        self.stderr = stderr

    def info(self, message):
        self.stdout.write(message + "\n")

    def success(self, message):
        self.stdout.write(self.GREEN % message + "\n")

    def warn(self, message):
        self.stderr.write(self.YELLOW % message + "\n")

    def error(self, message):
        self.stderr.write(self.RED % message + "\n")
