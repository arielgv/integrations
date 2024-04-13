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

def get_market_data():
    markets = client.markets.list()
    filtered_data = []
    for market in markets:
        if market['id'] in interested_tickers:
            next_funding_rate_timestamp_readable = datetime.fromtimestamp(market['next_funding_rate_timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            data = {
                'ticker': market['id'],
                'instant_funding_rate': market.get('instant_funding_rate', 'N/A'),
                'open_interest': market.get('open_interest', 'N/A'),
                '24h_volume': market.get('average_daily_volume', 'N/A'),  # Using average_daily_volume as a proxy
                'next_funding_rate_timestamp': next_funding_rate_timestamp_readable
            }
            filtered_data.append(data)
    return filtered_data

def print_data(data):
    for item in data:
        print(f"Ticker: {item['ticker']}, Instant Funding Rate: {item['instant_funding_rate']}, Open Interest: {item['open_interest']}, 24h Volume: {item['24h_volume']}, Next Funding Rate Timestamp: {item['next_funding_rate_timestamp']}")

while True:
    market_data = get_market_data()
    print_data(market_data)
    time.sleep(10)