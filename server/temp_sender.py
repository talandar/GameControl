import asyncio
import websockets
import json


async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        msg = {}
        msg["MODULE"] = "ECHO"
        msg["ARGS"] = "KEEPALIVE"
        await websocket.send(json.dumps(msg))

        print(f"> {msg}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
