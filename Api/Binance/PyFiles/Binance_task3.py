from binance.client import Client
import os
from datetime import datetime
import time

api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')

client = Client(api_key, api_secret)

def timestamp_to_date(timestamp):
    return datetime.fromtimestamp(int(timestamp) / 1000).strftime('%Y-%m-%d %H:%M:%S')

def print_account_assets():
    account_info = client.get_account()
    assets = [asset for asset in account_info['balances'] if float(asset['free']) > 0.0]
    if assets:
        print("Assets:")
        for asset in assets:
            print(f"Asset: {asset['asset']}, Wallet Balance: {asset['free']}, Update Time: {timestamp_to_date(account_info['updateTime'])}")
    else:
        print("No assets to display.")

def print_open_positions():
    positions = client.futures_account()['positions']
    open_positions = [position for position in positions if float(position['positionAmt']) != 0.0]
    if open_positions:
        print("Open Positions:")
        for position in open_positions:
            print(f"Symbol: {position['symbol']}, Position Amount: {position['positionAmt']}, Position Side: {position['positionSide']}, "
                  f"Leverage: {position['leverage']}, Maint Margin: {position['maintMargin']}, Entry Price: {position['entryPrice']}, "
                  f"Unrealized Profit: {position['unrealizedProfit']}, Update Time: {timestamp_to_date(position['updateTime'])}")
    else:
        print("No open positions to display.")

try:
    while True:
        print_account_assets()
        print_open_positions()
        time.sleep(10)  # 10 segundos refresh
except KeyboardInterrupt:
    print("Script terminated by user.")
