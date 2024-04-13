from typing import Dict
import pandas as pd
from .api import RabbitXApi
from ..core.timer_feed import TimerListener
from ..core.exchange_states import ExchangeState


class RabbitXState(TimerListener, ExchangeState):
    """Attempts to maintain correct exchange state"""

    def __init__(self):
        self.markets: Dict = {}
        self.api = RabbitXApi()
        self.funding_rates = {}

    def update_rates(self):
        try:
            market_data = self.api.get_market_data()
        except Exception as e:
            print("RabbitX: Update rates failed", e)
            return
        for idx, market in enumerate(market_data):
            coin = market["ticker"].split("-")[0]
            record = {
                "ticker": market["ticker"],
                "coin": coin,
                "m_idx": idx,
                "fr": float(market["funding_rate"]),
                "fr_ann": float(market["funding_rate"]) * 365 * 24 * 100,
                "oi": float(market["open_interest"]),
                "v24": float(market["24h_volume"]),
                "next_fr_ts": market["next_funding_rate_timestamp"],
            }
            self.funding_rates[record["ticker"]] = record
        self.fr_df = pd.DataFrame.from_records(
            [el for _, el in self.funding_rates.items()]
        ).sort_values(by="fr", ascending=False, key=abs)

    def on_timer(self):
        self.update_rates()

    @property
    def name(self):
        return "rabbitx"

    @property
    def has_orderbook(self):
        return True