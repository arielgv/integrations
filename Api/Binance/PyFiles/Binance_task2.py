import json
import threading
from datetime import datetime
import websocket
import requests  

########## TICKERS ###########
symbols = ["ethusdt", "btcusdt"]
#(Case sensitive)


last_values = {}

def on_message(ws, message):
    data = json.loads(message)
    if 'stream' in data:
        stream_info = data['stream']
        event_data = data['data']

        symbol = event_data['s']
        timestamp = datetime.fromtimestamp(event_data['E']/1000).strftime('%Y-%m-%d %H:%M:%S')
        best_bid = float(event_data['b'])
        best_ask = float(event_data['a'])
        best_bid_qty = float(event_data['B'])
        best_ask_qty = float(event_data['A'])


        if symbol not in last_values:
            last_values[symbol] = {}

     
        actual_values = {'best_bid': best_bid, 'best_ask': best_ask, 'best_bid_qty': best_bid_qty, 'best_ask_qty': best_ask_qty}
        if actual_values != last_values[symbol]:
            # Hay cambios, actualizar los valores y imprimir la información
            last_values[symbol] = actual_values

            print(f"--- {stream_info.upper()} ---")
            print(f"Symbol: {symbol}")
            print(f"Timestamp: {timestamp}")
            if best_bid_qty == 0:
                print("Best Bid: Ignored due to bid size = 0")
            else:
                print(f"Best Bid: {best_bid:.2f}")
                print(f"Best Bid Size: {best_bid_qty:.2f}")

            if best_ask_qty == 0:
                print("Best Ask: Ignored due to ask size = 0")
            else:
                print(f"Best Ask: {best_ask:.2f}")
                print(f"Best Ask Size: {best_ask_qty:.2f}")
        # Si no hay cambios, no se imprime nada

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
    print("### Connection closed ###")

def on_open(ws):
    print("WS connection opened")
    streams = "/".join([f"{symbol}@bookTicker" for symbol in symbols])
    ws.send(json.dumps({
        "method": "SUBSCRIBE",
        "params": streams.split("/"),
        "id": 1
    }))

if __name__ == "__main__":
    print(symbols)
    ws_app = websocket.WebSocketApp("wss://fstream.binance.com/stream?streams=" + "/".join([f"{symbol}@bookTicker" for symbol in symbols]),
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
    ws_app.on_open = on_open
    thread = threading.Thread(target=ws_app.run_forever)
    thread.start()
