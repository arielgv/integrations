from typing import TypedDict, List
from web3 import Web3
import os
import dotenv
import time
import abis
import rpc_and_wallet

ALCHEMY_URL = rpc_and_wallet.ALCHEMY_URL
MARKETS_CONTRACT_ABI = abis.MARKETS_CONTRACT_ABI
NEXT_FUNDING_ABI = abis.NEXT_FUNDING_ABI
STORAGE_CONFIG_ABI = abis.STORAGE_CONFIG_ABI


class HMXMarket(TypedDict):
    """Stores market info in typed dic"""
    market_index: int
    ticker: str
    asset_id: str
    long_token: str
    short_token: str
    active: bool
    max_skew_scale_usd: int
    max_funding_rate: int

STORAGE_CONFIG = "0xF4F7123fFe42c4C90A4bCDD2317D397E0B7d7cc0"
MARKETS_CONTRACT_ADDRESS = "0x97e94BdA44a2Df784Ab6535aaE2D62EFC6D2e303"
NEXT_FUNDING_CONTRACT_ADDRESS = "0x0FdE910552977041Dc8c7ef652b5a07B40B9e006"

def get_markets(w3: Web3, block_num=None) -> List[HMXMarket]:
    """Fetches market infos"""
    config = w3.eth.contract(address=STORAGE_CONFIG, abi=STORAGE_CONFIG_ABI)
    results = config.functions.getMarketConfigs().call(block_identifier=block_num or "latest")
    markets: List[HMXMarket] = []
    for idx, result in enumerate(results):
        market = HMXMarket({})
        market["market_index"] = idx
        market["asset_id"] = result[0].replace(b"\x00", b"").decode("utf-8")
        market["ticker"] = market["asset_id"] + "-USD"
        market["active"] = result[-2]
        market["max_skew_scale_usd"] = result[-1][0]
        market["max_funding_rate"] = result[-1][1]
        markets.append(market)
    return markets

def find_market_index(markets: List[HMXMarket], search_term: str) -> int:
    
    for market in markets:
        if market['ticker'] == search_term or market['asset_id'] == search_term:
            return market['market_index']
    return -1  # if not found

def fetch_market_data(w3: Web3, market_index: int):
    
    markets_contract = w3.eth.contract(address=MARKETS_CONTRACT_ADDRESS, abi=MARKETS_CONTRACT_ABI)
    market_data = markets_contract.functions.markets(market_index).call()
    next_funding_contract = w3.eth.contract(address=NEXT_FUNDING_CONTRACT_ADDRESS, abi=NEXT_FUNDING_ABI)
    funding_rate_velocity = next_funding_contract.functions.getFundingRateVelocity(market_index).call()
    next_funding_rate = market_data[6] + funding_rate_velocity
    return {
        "longPositionSize": market_data[0],
        "shortPositionSize": market_data[3],
        "currentFundingRate": market_data[6],
        "lastFundingTime": market_data[7],
        "NextFundingRate": next_funding_rate
    }

if __name__ == "__main__":
    dotenv.load_dotenv()
    #ALCHEMY RPC URL
    #ALCHEMY_URL = Loaded rpc url
    w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))
    markets = get_markets(w3)

    tickers = ["BTC-USD", "ETH-USD"]  # TICKERS 

    try:
        while True:
            for ticker in tickers:
                market_index = find_market_index(markets, ticker)
                if market_index != -1:
                    market_data = fetch_market_data(w3, market_index)
                    print(f"{ticker}: {market_data}")
                else:
                    print(f"Market not found: {ticker}.")
            time.sleep(10)  
    except KeyboardInterrupt:
        print("Script ended by user.")
