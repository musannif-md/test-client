from api_client import Client
from config import *

if __name__ == "__main__":
    client = Client(use_proto=False)
    client.signup()

    if not client.token:
        exit(1)

    payload = {
        "username": USERNAME,
        "note_name": "test-note-1",
        "content": "I sure\n hope\n\tthis works...",
    }

    res = client.authenticated_request("POST", "/del-note", payload)
    print(res)
