import json
import threading
from datetime import datetime
import websocket
import requests  

# obtención de intervalo de financiamiento para cada símbolo
def funder_interval_obtaining(Symbol):
    intervals = {}
    url = "https://fapi.binance.com/fapi/v1/fundingInfo"
    for symbols in Symbol:
        params = {'symbol': symbols}
        response = requests.get(url, params=params)
        data = response.json()
        if data and len(data) > 0:
            intervals[symbols] = data[-1]['fundingIntervalHours']
            print(f"Funding Rate Interval for {symbols}: {intervals[symbols]}")
        else:
            intervals[symbols] = 8  #if not found , default=8
    return intervals

########## TICKERS ########################
simbolos = ["ethusdt", "btcusdt"]
###########################################


funder_intervals = funder_interval_obtaining(simbolos)

def on_message(ws, message):
    data = json.loads(message)
    if 'stream' in data:
        stream_info = data['stream']
        event_data = data['data']
        symbol = event_data['s']
        mark_price = float(event_data['p'])
        funding_rate = float(event_data['r'])
        # Normaliza la tasa de financiamiento según el intervalo
        intervalo = funder_intervals.get(symbol, 8)  # Usa un valor predeterminado si es necesario
        normalized_funding_rate = funding_rate / intervalo
        index_price = float(event_data['i'])
        settle_price = float(event_data['P'])
        next_funding_time = datetime.fromtimestamp(event_data['T']/1000).strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"--- {stream_info.upper()} ---")
        print(f"Symbol: {symbol}")
        print(f"Mark Price: {mark_price:.2f}")
        print(f"Funding Rate (normalized): {normalized_funding_rate:.6f}")
        print(f"Index Price: {index_price:.2f}")
        print(f"Settle Price: {settle_price:.2f}")
        print(f"Next Funding Time: {next_funding_time}\n")

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
    print("### Connection closed ###")

def on_open(ws):
    print("WS connection opened")
    streams = "/".join([f"{symbol}@markPrice@1s" for symbol in simbolos])
    ws.send(json.dumps({
        "method": "SUBSCRIBE",
        "params": streams.split("/"),
        "id": 1
    }))

if __name__ == "__main__":
    print(simbolos)
    ws_app = websocket.WebSocketApp("wss://fstream.binance.com/stream?streams=" + "/".join([f"{symbol}@markPrice@1s" for symbol in simbolos]),
    #ws_app = websocket.WebSocketApp("wss://fstream.binance.com/stream?streams=" + "/".join([f"{symbol}@markPrice@1s" for symbol in ["ethusdt", "btcusdt"]]),
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
    ws_app.on_open = on_open
    thread = threading.Thread(target=ws_app.run_forever)
    thread.start()
