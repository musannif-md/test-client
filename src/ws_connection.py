import asyncio
import websockets
import uuid
import json
import argparse

from api_client import Client
from config import *


async def connect_websocket(uri, token, is_session_starter=False):
    headers = {"Authorization": f"Bearer {token}"}
    session_id = uuid.UUID(int=USER_ID)
    uri += f"?sid={session_id}"

    if is_session_starter:
        uri += f"&note_name=test-note-1"

    try:
        async with websockets.connect(uri, additional_headers=headers) as websocket:

            async def send_message():
                loop = asyncio.get_event_loop()
                while True:
                    try:
                        user_input = await loop.run_in_executor(None, input, ">>> ")
                        if user_input.lower() == "close":
                            print("Initiating closing handshake...")
                            await websocket.close()
                            break
                        message = json.dumps({"text": user_input})
                        await websocket.send(message)
                    except Exception as e:
                        print(f"Send error: {e}")
                        break

            async def receive_message():
                while True:
                    try:
                        msg = await websocket.recv()
                        print(f"<<< Received: {msg}")
                    except websockets.ConnectionClosedOK:
                        print("WebSocket connection closed by the server.")
                        break
                    except websockets.ConnectionClosedError as e:
                        print(f"WebSocket closed with error: {e}")
                        break
                    except Exception as e:
                        print(f"Receive error: {e}")
                        break

            await asyncio.gather(send_message(), receive_message())

    except websockets.ConnectionClosedError as e:
        print(f"WebSocket closed with error: {e}")
    except ConnectionRefusedError:
        print(f"WebSocket connection refused at {uri}. Is the server running?")
    except Exception as e:
        print(f"Unexpected error during WebSocket connection: {e}")


async def main():
    parser = argparse.ArgumentParser(
        description="WebSocket client with optional note name."
    )
    parser.add_argument(
        "--first",
        action="store_true",
        help="Pass 'test-note-1' as note_name to the WebSocket endpoint.",
    )
    args = parser.parse_args()

    client = Client(use_proto=False)
    client.login()

    if not client.token:
        exit(1)

    print("Login successful. Connecting to WebSocket...")

    websocket_uri = f"ws://{BASE_URL.split('//')[1]}/connect"

    await connect_websocket(websocket_uri, client.token, True if args.first else False)


if __name__ == "__main__":
    asyncio.run(main())
