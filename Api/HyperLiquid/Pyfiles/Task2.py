from hyperliquid.info import Info
from hyperliquid.utils import constants
import datetime
import time


TICKERS = ["BTC", "ETH"]

def calculate_total_size(levels):
    return sum(float(level['sz']) for level in levels)

def process_ticker(ticker):
    info = Info(constants.TESTNET_API_URL, skip_ws=True)
    l2_snapshot = info.l2_snapshot(coin=ticker)

    bids = l2_snapshot['levels'][0]
    asks = l2_snapshot['levels'][1]

    total_bid_size = calculate_total_size(bids)
    total_ask_size = calculate_total_size(asks)

    best_bid = bids[0]['px']
    best_ask = asks[0]['px']

    timestamp = datetime.datetime.fromtimestamp(l2_snapshot['time'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
    print(f"Ticker: {ticker}, Timestamp: {timestamp}, Bid: {best_bid}, Ask: {best_ask}, Bid Size: {total_bid_size}, Ask Size: {total_ask_size}")

def main():
    while True:
        for ticker in TICKERS:
            process_ticker(ticker)
        time.sleep(10)

if __name__ == "__main__":
    main()