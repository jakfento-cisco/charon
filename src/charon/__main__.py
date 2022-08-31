from argparse import ArgumentParser
import pwd
from typed_argparse import TypedArgs
from typing import List, NamedTuple

from charon.commands import FindFilesForUser


class UserInfo(NamedTuple):
    username: str
    uid: int
    homedir: str


class MyArgs(TypedArgs):
    exclude_user: List[str]


def getModuleArgs() -> MyArgs:
    parser = ArgumentParser(prog="charon", description="utility to remove stale users & their artifacts")
    parser.add_argument("--exclude-user",
                        help="list of users to exclude from removal",
                        metavar="USER",
                        nargs='+')

    return MyArgs(parser.parse_args())


def getAllNormalUsers() -> List[UserInfo]:
    all_users = pwd.getpwall()

    UID_MIN = None
    with open("/etc/login.defs", 'r') as login_defs:
        lines = login_defs.readlines()
        for line in lines:
            if line.startswith("UID_MIN"):
                UID_MIN = int(line.split()[1])
                break
    if UID_MIN is None:
        raise ValueError("could not parse UID_MIN from /etc/login.defs")

    return [
        UserInfo(username=el[0],
                 uid=el[2],
                 homedir=el[5]) for el in all_users if el[2] >= UID_MIN
    ]


def getAllFilesOwnedByUser(username: str):
    command = FindFilesForUser(username)
    results = command.run()
    return [
        line for line in results if "Permission Denied" not in line
    ]


if __name__ == "__main__":
    print(getModuleArgs())
    users = getAllNormalUsers()

    for user in users:
        files = getAllFilesOwnedByUser(user.username)
        print(f"User '{user.username}' has '{len(files)}' files.")
