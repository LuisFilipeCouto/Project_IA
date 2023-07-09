#########################################
# 89078  - Luis Filipe Correia do Couto #
# 103248 - Jose Miguel Guardado Silva   #
#########################################

import asyncio
import getpass
import json
import os
import websockets

# Student made code
from pathfinding import *

async def agent_loop(server_address="localhost:8000", agent_name="89078"):

    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        nextMoves = []

        while True:
            try:
                key = ""

                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server

                while websocket.messages:
                    state = json.loads(
                        await websocket.recv()
                )           

                if len(nextMoves) != 0:
                    key = nextMoves.pop(0)
                
                else:
                    t = SearchTree(state["grid"].split(" ")[1], state["dimensions"][0], state["cursor"], state["selected"])
                    nextMoves = t.solve(state["level"])

                await websocket.send(   
                    json.dumps({"cmd": "key", "key": key})
                )
                
                
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return


# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))