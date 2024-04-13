import concurrent
from typing import Dict
import pandas as pd
from web3 import Web3

from perps.hyperliquid.api import HyperLiquidApi

from ...core.event_loop import EventLoop
from ...core.timer_feed import TimerFeed, TimerListener
from ...hyperliquid.api import HyperLiquidApi


class Strat(TimerListener):
    """Simple strategy that listens to blocks and prints them out."""

    def __init__(self, w3: Web3):
        self.markets: Dict = {}
        self.api = HyperLiquidApi(w3)
        self.funding_rates = {}

    def update_rates(self):
        market_configs = self.api.market_configs
        res = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            res = [
                executor.submit(
                    self.api.get_last_funding_rate, market_config[0].split("-")[0]
                )
                for market_config in market_configs
            ]
            concurrent.futures.wait(res)
        for idx, market_config in enumerate(market_configs):
            fr = res[idx].result()
            if fr is None:
                continue
            record = {
                "ticker": market_config[0],
                "coin": fr["coin"],
                "m_idx": idx,
                "fr": float(fr["fundingRate"]),
                "fr_ann": float(fr["fundingRate"]) * 365 * 24 * 100,
                "pr": float(fr["premium"]),
                "fv": self.api.get_funding_rate_velocity(idx),
                "time": fr["time"],
            }
            self.funding_rates[record["ticker"]] = record

    def on_timer(self, fire_ms: int):
        print("Timer fired at", fire_ms)
        self.update_rates()
        if len(self.funding_rates) == 0:
            print("Fundings rates not found")
            return
        df = pd.DataFrame.from_records(
            [el for _, el in self.funding_rates.items()]
        ).sort_values(by="fr_mag", ascending=False, key=abs)
        print(df.head(100).to_string(index=False))


if __name__ == "__main__":
    import os
    import dotenv
    from web3 import Web3

    dotenv.load_dotenv()
    WS_URL = os.getenv("WS_URL")
    assert WS_URL, "WS_URL must be set in .env file."
    w3 = Web3(Web3.WebsocketProvider(WS_URL))
    strat = Strat(w3)
    # default every ten seconds:
    feed = TimerFeed(freq_ms=60 * 1000)
    feed.add_listener(strat)
    event_loop = EventLoop()
    event_loop.add_feed(feed)
    event_loop.run()
