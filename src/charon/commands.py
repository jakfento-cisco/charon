from abc import ABCMeta
import subprocess
from typing import List


class Command(metaclass=ABCMeta):
    def run(self):
        pass


class FindFilesForUser(Command):
    def __init__(self, username: str):
        self.username = username

    def run(self) -> List[str]:
        result = subprocess.run(["/usr/bin/find", "/", "-user", self.username], capture_output=True)
        return result.stdout.decode("utf-8").split("\n")
