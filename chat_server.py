import asyncio
import websockets
import threading
import os

clients = set()
log_file = "chat_log.txt"

async def register(websocket):
    clients.add(websocket)

async def unregister(websocket):
    clients.remove(websocket)

async def broadcast(message):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(message + "\n")
    for client in clients:
        try:
            await client.send(message)
        except:
            clients.remove(client)

async def handle_client(websocket, path):
    await register(websocket)
    try:
        async for message in websocket:
            await broadcast(message)
    finally:
        await unregister(websocket)

async def main():
    server = await websockets.serve(handle_client, '0.0.0.0', 12345)
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
