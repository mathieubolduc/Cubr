#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import json
from Cube import *
from CubeSolver import *
from enum import Enum
from CaptureCube import *

class MessageType(Enum):
    Reset = 0,
    Initialize = 1,
    Solution = 2,
    Wait = 3

async def hello(websocket, path):
    print("Connection Established");



    cube = show_webcam(mirror=True) #getScrambledCube()
    solver = CubeSolver(cube)
    solver.computeMoves()
    solution = solver.toElli()

    initial = json.dumps({'messageType': 1  , 'Data': solution})

    await websocket.send(initial)
    # print(f"> {greeting}")

    while True:
        message = await websocket.recv()
        print(f"< {message}")
        if message == "Reset":
            cube = getScrambledCube()
            solver = CubeSolver(cube)
            solver.computeMoves()
            solution = solver.toElli()

            initial = json.dumps({'messageType': 1, 'Data': solution})
            await websocket.send(initial)
            print(f"> Sent {initial}")


start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()