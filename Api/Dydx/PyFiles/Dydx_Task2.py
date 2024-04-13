import websocket
import json
import threading
from v4_client_py import IndexerClient
from v4_client_py.clients.constants import Network

####################
TICKERS = ["BTC-USD", "ETH-USD"]
####################


 
client = IndexerClient(
    config=Network.testnet().indexer_config,
)


def print_orderbook_info(ticker, data):
    time_response = client.utility.get_time()
    timestamp = time_response.data['iso']
    #timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{ticker}: ({timestamp})")
    if 'bids' in data and data['bids']:
        print(f"  Bid: {data['bids'][0][0]} | Bid Size: {data['bids'][0][1]}")
    if 'asks' in data and data['asks']:
        print(f"  Ask: {data['asks'][0][0]} | Ask Size: {data['asks'][0][1]}")
    print("---------------------------------------------")

def on_message(ws, message):
    data = json.loads(message)
    

    if data.get('type') == 'channel_data' and 'contents' in data:
        contents = data['contents']
        if 'bids' in contents or 'asks' in contents:
            ticker = data['id']
            print_orderbook_info(ticker, contents)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("### Connection closed ###")

def on_open(ws):
    def run(*args):
        for ticker in TICKERS:
   
            subscription_message = json.dumps({
                "type": "subscribe",
                "channel": "v4_orderbook",
                "id": ticker
            })
            ws.send(subscription_message)
            print(f"{ticker} Orderbook v4 subscription sended.")

    threading.Thread(target=run).start()


websocket_url = "wss://indexer.v4testnet.dydx.exchange/v4/ws"
ws = websocket.WebSocketApp(websocket_url, on_message=on_message, on_error=on_error, on_close=on_close)
ws.on_open = on_open
ws.run_forever()