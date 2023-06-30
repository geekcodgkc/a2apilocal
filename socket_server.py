import websockets
import asyncio

PORT = 65252

print("Server listening on port "+ str(PORT))

async def server(websocket, path):
    print("client connected")
    try:
        async for message in websocket:
            print("Recieved message from client" + message)
            await websocket.send("PONG "+ message)
    except:
        print("ERROR")

start_server = websockets.serve(server, "localhost", PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
