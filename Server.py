#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import json
from enum import Enum

class MessageType(Enum):
    Reset = 0,
    Initialize = 1,
    Solution = 2,
    Wait = 3

async def hello(websocket, path):
    print("Connection Established");

    # greeting = json.dumps({'messageType': MessageType.Initialize, 'Data': "Resetting"})
    # await websocket.send(greeting)
    # print(f"> {greeting}")

    while True:
        message = await websocket.recv()
        print(f"< {message}")
        if message == "Reset":
            arg = json.dumps({'messageType': MessageType.Reset, 'Data': "Resetting"})
            await websocket.send(arg)
            print(f"> Sent {arg}")


start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()