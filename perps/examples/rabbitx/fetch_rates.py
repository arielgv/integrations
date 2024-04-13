from typing import Dict
import pandas as pd
import numpy as np
from web3 import Web3

from perps.rabbitx.api import RabbitXApi

from ...core.event_loop import EventLoop
from ...core.timer_feed import TimerFeed, TimerListener


class Strat(TimerListener):
    """Simple strategy that listens to blocks and prints them out."""

    def __init__(self, w3: Web3):
        self.markets: Dict = {}
        self.api = RabbitXApi()
        self.funding_rates = {}

    def update_rates(self):
        market_data = self.api.get_market_data()
        for idx, market in enumerate(market_data):
            coin = market["ticker"].split("-")[0]
            record = {
                "ticker": market["ticker"],
                "coin": coin,
                "m_idx": idx,
                "fr": float(market["funding_rate"]),
                "fr_ann": float(market["funding_rate"]) * 365 * 24 * 100,
                "oi": float(market["open_interest"]),
                "adv": float(market.get("average_daily_volume", np.nan)),
                "next_fr_ts": market["next_funding_rate_timestamp"],
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
        ).sort_values(by="fr", ascending=False, key=abs)
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
