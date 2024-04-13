import requests
import time
from datetime import datetime


#############################
tickers = ['ETH', 'BTC'] 
#############################

def get_best_bid_ask(ticker):
    url = f"https://api.aevo.xyz/orderbook?instrument_name={ticker}-PERP"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        best_bid = float(data["bids"][0][0])
        best_ask = float(data["asks"][0][0])
        mid_price = round((best_bid + best_ask) / 2, 2)
        
     
        last_updated_ns = int(data["last_updated"])
        last_updated = datetime.utcfromtimestamp(last_updated_ns / 1e9) 
        last_updated_str = last_updated.strftime('%Y-%m-%d %H:%M:%S UTC')
        
        return best_bid, best_ask, mid_price, last_updated_str
    else:
        print(f"Error al obtener los datos para {ticker}")
        return None, None, None, None

while True:
    for ticker in tickers:
        best_bid, best_ask, mid_price, last_updated = get_best_bid_ask(ticker)
        if best_bid and best_ask:
            print(f"Ticker: {ticker}, Best Bid: {best_bid}, Best Ask: {best_ask}, Mid Price: {mid_price}, Last Updated: {last_updated}")
        else:
            print(f"No se pudieron obtener los datos para {ticker}")
    
    time.sleep(10) 
