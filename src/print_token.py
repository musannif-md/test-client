from api_client import Client
from config import *


def main():
    client = Client(use_proto=False)
    client.login()

    if not client.token:
        exit(1)

    print(client.token)


if __name__ == "__main__":
    main()
