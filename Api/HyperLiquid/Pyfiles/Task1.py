import time
from datetime import datetime
from hyperliquid.info import Info
import abis
import rpc_and_wallet
from web3 import Web3

#Funding on Hyperliquid is designed to closely match the process used by centralized perpetual exchanges. 
#The funding rate formula applies to 8 hour funding rate. However, funding is paid every hour at one eighth of the computed rate for each hour.
#The specific formula is Funding Rate (F) = Average Premium Index (P) + clamp (interest rate - Premium Index (P), -0.0005, 0.0005). The premium is sampled every 5 seconds and averaged over the hour.


# ABIs & SC Address 
CALCULATOR_ABI = abis.CALCULATOR_ABI
CALCULATOR_CONTRACT_ADDRESS = '0x0FdE910552977041Dc8c7ef652b5a07B40B9e006'
STORAGE_CONFIG_ABI = abis.STORAGE_CONFIG_ABI 
STORAGE_CONFIG = "0xF4F7123fFe42c4C90A4bCDD2317D397E0B7d7cc0"

ALCHEMY_URL = rpc_and_wallet.ALCHEMY_URL

w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))

calculator_contract = w3.eth.contract(address=CALCULATOR_CONTRACT_ADDRESS, abi=CALCULATOR_ABI)
config_contract = w3.eth.contract(address=STORAGE_CONFIG, abi=STORAGE_CONFIG_ABI)

info = Info(skip_ws=True)
user_address = "0xcd5051944f780a621ee62e39e493c489668acf4d"
tickers = ["BTC"]#, "ETH"]

def get_market_index(ticker):
    results = config_contract.functions.getMarketConfigs().call()
    for idx, result in enumerate(results):
        market_ticker = result[0].replace(b"\x00", b"").decode("utf-8") + "-USD"
        #print('market ticker: ' , market_ticker + " " + 'Ticker: ' + ticker + ' index? = ', idx)
        if market_ticker == ticker + "-USD":
            print('market ticker: ' , market_ticker + " " + 'Ticker: ' + ticker + ' index = ', idx)
            return idx
    return None

def get_latest_funding_rate(coin):
    try:
        endTime = int(time.time() * 1000)  # Current time
        startTime = endTime - (24 * 60 * 60 * 1000)  # 24 hours ago
        response = info.funding_history(coin=coin, startTime=startTime, endTime=endTime)
        if response:
            return response[-1]
        else:
            print(f"No funding rate data found for {coin} in the given interval.")
            return None
    except Exception as e:
        print(f"Error obtaining funding rate for {coin}: {e}")
        return "error"

def get_funding_rate_velocity(market_index):

    return calculator_contract.functions.getFundingRateVelocity(market_index).call()

def get_current_prices():
    try:
        return info.all_mids()
    except Exception as e:
        print("Error obtaining current prices:", e)
        return {}

# Modificamos la función get_ticker_info para incluir la velocity
def get_ticker_info(user_address, tickers):
    user_state = info.user_state(user_address)
    current_prices = get_current_prices()
    
    for ticker in tickers:
        longPositionSize = 0
        shortPositionSize = 0
        for asset_position in user_state['assetPositions']:
            if asset_position['position']['coin'] == ticker:
                sz = float(asset_position['position']['szi'])
                if sz > 0:
                    longPositionSize += sz
                else:
                    shortPositionSize += abs(sz)
        
        market_index = get_market_index(ticker)
        if market_index is not None:
            funding_rate_velocity = get_funding_rate_velocity(market_index)
        else:
            funding_rate_velocity = "Market index not found"
        
        latest_funding_rate = get_latest_funding_rate(ticker)
        if latest_funding_rate == "error":
            return "error"
        
        current_price = current_prices.get(ticker, "Price not available")
        print(f"Ticker: {ticker}")
        print(f"Current Price: {current_price}")
        if latest_funding_rate is not None:
            print(f"Current Funding Rate: {latest_funding_rate['fundingRate']}")
            timestamp = latest_funding_rate['time']
            readable_time = datetime.utcfromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')
            print(f"Last Funding Time: {readable_time}")
        print(f"Funding Rate Velocity: {funding_rate_velocity}")
        print("----------")



retry_count = 0
while retry_count < 8:
    result = get_ticker_info(user_address, tickers)
    if result == "error":
        retry_count += 1
        print(f"Attempt {retry_count} failed, retrying in 10 seconds...")
        time.sleep(10)
    else:
        retry_count = 0
    time.sleep(10)  # Wait 10 seconds before the next execution

if retry_count >= 8:
    print("Unable to connect to the API after 8 attempts. Terminating the program.")