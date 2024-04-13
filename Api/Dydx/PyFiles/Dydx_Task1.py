import websocket
import json
import threading

#########
PREDEFINED_TICKERS = ["BTC-USD", "ETH-USD"]
########

current_data = {ticker: {} for ticker in PREDEFINED_TICKERS}

def print_ticker_info(ticker):
    ticker_data = current_data[ticker]
    formatted_info = f"""
    Ticker: {ticker}
    Funding Rate: {ticker_data.get('nextFundingRate', 'N/A')}
    Open Interest: {ticker_data.get('openInterest', 'N/A')}
    Oracle Price: {ticker_data.get('oraclePrice', 'N/A')}
    24h Volume: {ticker_data.get('volume24H', 'N/A')}
    24h Trades: {ticker_data.get('trades24H', 'N/A')}
    Next Funding: {ticker_data.get('nextFundingRate', 'N/A')}
    ---------------------------------------------
    """
    print(formatted_info)

def update_ticker_info(ticker, data):
    current_data[ticker].update(data)

def on_message(ws, message):
    data = json.loads(message)
    
    if data.get('type') == 'subscribed' and 'markets' in data.get('contents', {}):
        markets_data = data['contents']['markets']
        for ticker in PREDEFINED_TICKERS:
            market_data = markets_data.get(ticker)
            if market_data:
                update_ticker_info(ticker, market_data)
                print_ticker_info(ticker)

    elif data.get('type') == 'channel_data' and 'trading' in data.get('contents', {}):
        trading_data = data['contents']['trading']
        for ticker in PREDEFINED_TICKERS:
            if ticker in trading_data:
                update_ticker_info(ticker, trading_data[ticker])
                print_ticker_info(ticker)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("### CLOSED CONNECTION ###")

def on_open(ws):
    def run(*args):
    
        subscription_message = json.dumps({
            "type": "subscribe",
            "channel": "v4_markets",
        })
        ws.send(subscription_message)
        print("Market channel subscription: v4_markets.")

    threading.Thread(target=run).start()

websocket_url = "wss://indexer.v4testnet.dydx.exchange/v4/ws"
ws = websocket.WebSocketApp(websocket_url, on_message=on_message, on_error=on_error, on_close=on_close)
ws.on_open = on_open
ws.run_forever()
