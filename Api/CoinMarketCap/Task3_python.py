import requests
import csv
import os
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from sources import api
import time
import json
import random

API_KEY = api

NUM_QUOTES = 288

def fetch_historical_quotes_data(cryptocurrency_id, date, output_dir):
    url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/historical"
    headers = {
        'X-CMC_PRO_API_KEY': API_KEY
    }
    time_start = (date - timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%SZ')
    time_end = date.strftime('%Y-%m-%dT23:59:59Z')
    params = {
        'id': cryptocurrency_id,
        'time_start': time_start,
        'time_end': time_end,
        'interval': '5m',
        'count': NUM_QUOTES,
        'convert': 'USD,ETH,BTC'
    }

    print(f"Sending request to API for cryptocurrency ID {cryptocurrency_id} on {date}")
    response = requests.get(url, headers=headers, params=params)
    print("***************")
    #print(response.text)
    print("***************")
    
    if response.status_code == 200:
        print(f"Received response from API for cryptocurrency ID {cryptocurrency_id} on {date}")
        json_data = response.json()['data']
        print(json.dumps(json_data, indent=2))
        if 'quotes' in json_data:
            quotes = json_data['quotes']
            print(f"Retrieved {len(quotes)} quotes for cryptocurrency ID {cryptocurrency_id} on {date}")
            return quotes
        else:
            print(f"No data found for cryptocurrency ID {cryptocurrency_id} on {date}")
            return []
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return []

def save_to_csv(data, output_dir, symbol, date):
    output_subdir = os.path.join(output_dir, symbol)
    os.makedirs(output_subdir, exist_ok=True)
    output_path = os.path.join(output_subdir, f"{date}.csv")

    #print(f"Saving data to CSV file: {output_path}")
    ##
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['timestamp', 'price_usd', 'volume_24h_usd', 'market_cap_usd',
                      'price_eth', 'volume_24h_eth', 'market_cap_eth',
                      'price_btc', 'volume_24h_btc', 'market_cap_btc']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for quote in data:
            timestamp = quote['timestamp']
            quote_usd = quote['quote']['USD']
            quote_eth = quote['quote']['ETH']
            quote_btc = quote['quote']['BTC']

            row = {
                'timestamp': timestamp,
                'price_usd': quote_usd['price'],
                'volume_24h_usd': quote_usd['volume_24h'],
                'market_cap_usd': quote_usd['market_cap'],
                'price_eth': quote_eth['price'],
                'volume_24h_eth': quote_eth['volume_24h'],
                'market_cap_eth': quote_eth['market_cap'],
                'price_btc': quote_btc['price'],
                'volume_24h_btc': quote_btc['volume_24h'],
                'market_cap_btc': quote_btc['market_cap']
            }
            writer.writerow(row)
    print(f"Data saved to CSV file: {output_path}")

def backfill_data(cryptocurrency_id, start_date, end_date, output_dir, overwrite):
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        output_path = os.path.join(output_dir, str(cryptocurrency_id), f"{date_str}.csv")

        if not overwrite and os.path.exists(output_path):
            with open(output_path, 'r') as csvfile:
                reader = csv.reader(csvfile)
                row_count = sum(1 for row in reader) - 1  # Subtract 1 for the header row
                if row_count >= NUM_QUOTES:
                    print(f"Skipping {cryptocurrency_id} - {date_str} (already exists with sufficient rows)")
                    current_date += timedelta(days=1)
                    continue

        print(f"Fetching data for {cryptocurrency_id} - {date_str}")
        data = fetch_historical_quotes_data(cryptocurrency_id, current_date, output_dir)
        save_to_csv(data, output_dir, str(cryptocurrency_id), date_str)
        current_date += timedelta(days=1)
        print(f"Waiting for 5 second before the next request...")
        time.sleep(5)

def main(watchlist_file, start_date, end_date, output_dir, overwrite):
    with open(watchlist_file, 'r') as file:
        watchlist = [line.strip() for line in file]

    print(f"Starting data backfill for {len(watchlist)} cryptocurrencies from {start_date} to {end_date}")
    with ThreadPoolExecutor() as executor:
        futures = []
        for cryptocurrency_id in watchlist:
            futures.append(executor.submit(backfill_data, cryptocurrency_id, start_date, end_date, output_dir, overwrite))

        for future in futures:
            future.result()
    print("Data backfill completed.")

if __name__ == '__main__':
    watchlist_file = 'watchlist.csv'
    start_date = datetime(2024, 3, 7)
    end_date = datetime(2024, 3, 8)
    output_dir = 'historical_data'
    overwrite = False

    main(watchlist_file, start_date, end_date, output_dir, overwrite)
    # watchlist : 1,1027,825