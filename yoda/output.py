import sys


class output:
    GREEN = "\033[92m%s\033[0m"
    YELLOW = "\033[93m%s\033[0m"
    RED = "\033[91m%s\033[0m"

    def info(self, message):
        sys.stdout.write(message + "\n")

    def success(self, message):
        sys.stdout.write(self.GREEN % message + "\n")

    def warn(self, message):
        sys.stderr.write(self.YELLOW % message + "\n")

    def err(self, message):
        sys.stderr.write(self.RED % message + "\n")
