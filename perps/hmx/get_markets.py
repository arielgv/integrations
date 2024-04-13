"""Get markets for gmx"""

from typing import TypedDict, List
from web3 import Web3
from .abis import STORAGE_CONFIG_ABI


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


def get_markets(w3: Web3, block_num=None) -> List[HMXMarket]:
    """Fetches market infos"""
    config = w3.eth.contract(address=STORAGE_CONFIG, abi=STORAGE_CONFIG_ABI)
    results = config.functions.getMarketConfigs().call(
        block_identifier=block_num or "latest"
    )
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


if __name__ == "__main__":
    import os
    import dotenv
    dotenv.load_dotenv()
    WEB3_URL = os.getenv('RPC_URL')
    w3 = Web3(Web3.HTTPProvider(WEB3_URL))
    markets = get_markets(w3)
    for market in markets:
        print(market)
    print(f"Found {len(markets)} markets")
