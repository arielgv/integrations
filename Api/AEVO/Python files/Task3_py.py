import asyncio
import json
import websockets
from websockets.exceptions import ConnectionClosedError

from api import API_KEY, API_SECRET

ApiKey = API_KEY
ApiSecret = API_SECRET

async def subscribe_to_positions():
    print(ApiKey)
    uri = "wss://ws.aevo.xyz"  
    try:
        async with websockets.connect(uri) as websocket:
      
            auth_msg = json.dumps({
                "op": "auth",
                "data": {
                    "key": ApiKey,
                    "secret": ApiSecret,
                }
            })
            await websocket.send(auth_msg)
            auth_response = await websocket.recv()
            print("Respuesta de autenticación:", auth_response)

            subscribe_msg = json.dumps({
                "op": "subscribe",
                "data": ["positions"]
            })
            await websocket.send(subscribe_msg)
            print("Suscrito a actualizaciones de posiciones")


            while True:
                response = await websocket.recv()
                print("Actualización recibida:", response)
    except ConnectionClosedError as e:
        print(f"La conexión se cerró inesperadamente: {e}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

asyncio.run(subscribe_to_positions())
