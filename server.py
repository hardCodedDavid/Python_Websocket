import asyncio
import websockets
import json

connected_clients = set()
todo_list = []

async def notify_clients():
    if connected_clients:  # asyncio.wait doesn't accept an empty list
        message = json.dumps(todo_list)
        await asyncio.wait([client.send(message) for client in connected_clients])

async def handler(websocket, path):
    # Register the client
    connected_clients.add(websocket)
    print(f"Client connected: {len(connected_clients)} total")

    # Send current to-do list to the newly connected client
    await websocket.send(json.dumps(todo_list))

    try:
        async for message in websocket:
            print(f"Received message: {message}")
            todo_item = json.loads(message)
            todo_list.append(todo_item)
            await notify_clients()
    except websockets.ConnectionClosed as e:
        print(f"Client disconnected: {e}")
    finally:
        # Unregister the client
        connected_clients.remove(websocket)
        print(f"Client disconnected: {len(connected_clients)} remaining")

start_server = websockets.serve(handler, "localhost", 8765)

print("WebSocket server started on ws://localhost:8765")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
