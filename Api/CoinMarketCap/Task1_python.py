from sources import api
import requests
import csv
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import time
import random

######
API_KEY = api
output_directory = 'fetch_crypto_listing'
######


def fetch_cryptocurrency_listings(start, limit):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        'X-CMC_PRO_API_KEY': API_KEY
    }
    params = {
        'start': start,
        'limit': limit,
        'sort': 'market_cap',
        'sort_dir': 'desc'
    }

    backoff = 1
    max_backoff = 64

    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            total_count = data['status']['total_count']
            fetched_data = data['data']
            print(f"Fetched {start} - {start + len(fetched_data) - 1} of {total_count}")
            return fetched_data, total_count
        # 
        elif response.status_code == 429:
            print(f"Error 429: {response.json()['status']['error_message']}")
            wait_time = backoff + random.uniform(0, 1)  # Agregar un  retraso aleatorio
            print(f"Esperando {wait_time} segundos antes de volver a intentar...")
            time.sleep(wait_time)
            backoff = min(max_backoff, backoff * 2)  # Aumentar el tiempo de backoff exponencialmente
        else:
            print(f"Error: {response.status_code}")
            return []

def save_to_csv(data, output_dir):
    today = datetime.now().strftime("%m%d%Y")
    filename = f"latest_{today}.csv"
    filepath = os.path.join(output_dir, filename)

    os.makedirs(output_dir, exist_ok=True)

    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)

    latest_symlink = os.path.join(output_dir, "latest.csv")
    try:
        os.remove(latest_symlink)
    except FileNotFoundError:
        pass
    os.symlink(filename, latest_symlink)


def main():
    current_dir = os.getcwd()
    output_dir = os.path.join(current_dir, output_directory)

    start = 1
    limit = 5000
    total_count = None
    data = []

    with ThreadPoolExecutor() as executor:
        while total_count is None or start <= total_count:
            future = executor.submit(fetch_cryptocurrency_listings, start, limit)
            result, total_count = future.result()
            data.extend(result)
            start += limit

            if total_count is not None and len(data) >= total_count:
                break

    save_to_csv(data, output_dir)


if __name__ == '__main__':
    main()