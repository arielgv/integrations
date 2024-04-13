from web3 import Web3
import time
import os
import dotenv
from datetime import datetime
import abis
import rpc_and_wallet

ALCHEMY_URL = rpc_and_wallet.ALCHEMY_URL

dotenv.load_dotenv()
#################### HTTP ALCHEMY URL ARBITRUM ####
#ALCHEMY_URL = RPC URL
###################### HTTP ALCHEMY URL ARBITRUM ####

PRICE_MONITOR_ABI = abis.PRICE_MONITOR_ABI


w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))
PRICE_MONITOR_CONTRACT_ADDRESS = "0x9c83e1046dA4727F05C6764c017C6E1757596592"


price_monitor_contract = w3.eth.contract(address=PRICE_MONITOR_CONTRACT_ADDRESS, abi=PRICE_MONITOR_ABI)

def get_latest_price_and_update(asset_id, is_max):
   
    assetId_bytes = Web3.to_bytes(text=asset_id)
    assetId_hex = Web3.to_hex(assetId_bytes)
    
    assetId_padded = assetId_hex.ljust(66, '0')  # 66 caracteres considerando el prefijo '0x'
    response = price_monitor_contract.functions.getLatestPrice(assetId_padded, is_max).call()
    return {
        "price": response[0],
        "lastUpdate": response[1]
    }

if __name__ == "__main__":
    asset_ids = ["BTC", "ETH"]  # Lista de tickers a monitorear
    is_max = True  # Ajustar según sea necesario

    try:
        while True:
            for asset_id in asset_ids:
                result = get_latest_price_and_update(asset_id, is_max)
                LastUpdate = datetime.utcfromtimestamp(result['lastUpdate'])
                print(f"Ticker: {asset_id}, Price: {result['price']}, Last Update: {LastUpdate.strftime('%Y-%m-%d %H:%M:%S')}")
            time.sleep(10)  
    except KeyboardInterrupt:
        print("Script stopped by the user.")

##############################

ASSETS_IDS_LIST = """
asset_id  | ticker    
ETH         ETH-USD   
BTC         BTC-USD   
AAPL        AAPL-USD  
JPY         JPY-USD   
XAU         XAU-USD   
AMZN        AMZN-USD  
MSFT        MSFT-USD  
TSLA        TSLA-USD  
EUR         EUR-USD   
XAG         XAG-USD   
AUD         AUD-USD   
GBP         GBP-USD   
ADA         ADA-USD   
MATIC       MATIC-USD 
SUI         SUI-USD   
ARB         ARB-USD   
OP          OP-USD    
LTC         LTC-USD   
COIN        COIN-USD  
GOOG        GOOG-USD  
BNB         BNB-USD   
SOL         SOL-USD   
QQQ         QQQ-USD   
XRP         XRP-USD   
NVDA        NVDA-USD  
LINK        LINK-USD  
CHF         CHF-USD   
DOGE        DOGE-USD  
CAD         CAD-USD   
SGD         SGD-USD   
CNH         CNH-USD   
HKD         HKD-USD   
BCH         BCH-USD   
MEME        MEME-USD  
DIX         DIX-USD   
JTO         JTO-USD   
STX         STX-USD   
ORDI        ORDI-USD  
TIA         TIA-USD   
AVAX        AVAX-USD  
INJ         INJ-USD   
DOT         DOT-USD   
SEI         SEI-USD   
ATOM        ATOM-USD  
1000PEPE    1000PEPE-USD
1000SHIB    1000SHIB-USD
SEK         SEK-USD   
ICP         ICP-USD   
MANTA       MANTA-USD 

"""
