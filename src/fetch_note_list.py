from api_client import Client
from config import *

if __name__ == "__main__":
    client = Client(use_proto=False)
    client.login()

    if not client.token:
        exit(1)

    res = client.authenticated_request("POST", "/notes")
    print(res)
    if res:
        print(res.content)
