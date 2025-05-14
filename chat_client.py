import asyncio
import websockets

SERVER_URL = "ws://127.0.0.1:12345"  # Użyj publicznego IP na Render

nickname = input("Podaj swój nick: ")

async def receive_messages(websocket):
    while True:
        try:
            msg = await websocket.recv()
            print(msg)
        except:
            print("Rozłączono z serwerem.")
            break

async def send_messages(websocket):
    while True:
        msg = input()
        await websocket.send(f"{nickname}: {msg}")

async def main():
    async with websockets.connect(SERVER_URL) as websocket:
        print("Połączono z czatem galaktycznym.")
        asyncio.create_task(receive_messages(websocket))
        await send_messages(websocket)

if __name__ == "__main__":
    asyncio.run(main())
