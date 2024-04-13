import rabbitx
from rabbitx.client import Client
from datetime import datetime
import time
from credentialsJWT import priv_key

api_NoTest = 'https://api.prod.rabbitx.io'

private_key = priv_key
client = Client(api_url=api_NoTest, private_key=private_key)

# Tickers of interest
interested_tickers = ['BTC-USD', 'ETH-USD']


def get_orderbook_data(ticker):
    orderbooks = client.orderbook.get(ticker)
    if orderbooks and isinstance(orderbooks, list) and len(orderbooks) > 0:
        
        orderbook = orderbooks[0]
        return orderbook
    else:
        return None

def get_market_data():
    markets = client.markets.list()
    filtered_data = []
    for market in markets:
        if market['id'] in interested_tickers:
            orderbook = get_orderbook_data(market['id'])
            if orderbook:
                readable_timestamp = datetime.fromtimestamp(orderbook['timestamp'] / 1e6).strftime('%Y-%m-%d %H:%M:%S')
                bid_size = orderbook['bids'][0][1] if orderbook['bids'] else 'N/A'
                ask_size = orderbook['asks'][0][1] if orderbook['asks'] else 'N/A'
            else:
                readable_timestamp, bid_size, ask_size = 'N/A', 'N/A', 'N/A'
            
            
            best_bid = market.get('best_bid', 'N/A')
            
            best_ask = market.get('best_ask', 'N/A')
            
            
            data = {
                'ticker': market['id'],
                'timestamp': readable_timestamp,
                'best_bid': best_bid,
                'best_ask': best_ask,
                'bid_size': bid_size,
                'ask_size': ask_size,
            }
            filtered_data.append(data)
    return filtered_data

def print_data(data):
    for item in data:
        print(f"Ticker: {item['ticker']}, Timestamp: {item['timestamp']}, Best Bid: {item['best_bid']}, Best Ask: {item['best_ask']}, Bid Size: {item['bid_size']}, Ask Size: {item['ask_size']}")

# Run once for debugging
while True:
    market_data = get_market_data()
    print_data(market_data)
    time.sleep(10)