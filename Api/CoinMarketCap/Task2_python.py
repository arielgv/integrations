import os
import requests
from datetime import datetime, timedelta
from time import sleep
from sources import api

url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/historical'
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api
}
######### SETTINGS ########
cryptocurrency_ids = "1,74"  ## IDS (string) comma separated
start_date_str = "2024-03-01" ## YYYY-MM-DD
end_date_str = "2024-03-02" ## YYYY-MM-DD
max_requests_per_minute = 30 ## Max requests per minute (30 = basic , HOBBYIST &  Startup plans). If exceded = time.sleep(60)
output_directory = "output_prices"
##########################






start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
end_date = datetime.strptime(end_date_str, "%Y-%m-%d")



if not os.path.exists(output_directory):
    os.makedirs(output_directory)

output_file = os.path.join(output_directory, f"prices_{start_date_str}_{end_date_str}.csv")

with open(output_file, 'w') as file:
    file.write("Cryptocurrency,Timestamp,Price (USD),Price (ETH),Price (BTC)\n")

    current_date = start_date
    request_count = 0
    max_requests_per_minute = 30

    while current_date < end_date:
        if request_count >= max_requests_per_minute:
            print(f"Request limit reached. waiting 60 secs...")
            sleep(60)
            request_count = 0

        params = {
            'id': cryptocurrency_ids,
            'time_start': (current_date - timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            'time_end': (current_date + timedelta(days=1) - timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            'interval': '5m',
            'convert': 'USD,ETH,BTC'
        }
        print(f"Fetching data with query\n {params}")

        response = requests.get(url, headers=headers, params=params)
        request_count += 1

        if response.status_code == 200:
            data = response.json()

            for cryptocurrency_id, cryptocurrency_data in data['data'].items():
                name = cryptocurrency_data['name']
                quotes = cryptocurrency_data['quotes']

                for quote in quotes:
                    timestamp = quote['timestamp']
                    price_usd = quote['quote']['USD']['price']
                    price_eth = quote['quote']['ETH']['price']
                    price_btc = quote['quote']['BTC']['price']

                    file.write(f"{name},{timestamp},{price_usd},{price_eth},{price_btc}\n")
        elif response.status_code == 429:
            print(f"Request limit reached. waiting 60 secs...")
            sleep(60)
        else:
            print(f"Request error: {response.status_code}\n{response.text}")

        current_date += timedelta(days=1)

print("Data saved in:", output_file)