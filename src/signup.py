from api_client import Client
from config import *

un: str = "masroof-maindak"
pw: str = "SecurePassword"


def main():
    client = Client(use_proto=False)
    client.signup(un, pw)

    if not client.token:
        exit(1)

    client2 = Client(use_proto=False)
    client2.login(un, pw)

    if not client.token:
        exit(1)


if __name__ == "__main__":
    main()
