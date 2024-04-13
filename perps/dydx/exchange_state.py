import pandas as pd
import numpy as np
from .feed import DyDxListener


class DyDxState(DyDxListener):
    """DyDx state"""

    def __init__(self):
        self.current_data = {}
        self.funding_rates = {}

    def on_markets(self, ticker: str, market_data: {}):
        self.update_ticker_info(ticker, market_data)

    def on_trading(self, ticker: str, trading_data: {}):
        self.update_ticker_info(ticker, trading_data)

    def update_ticker_info(self, ticker, data):
        """Update ticker info"""
        if ticker not in self.current_data:
            self.current_data[ticker] = {}
        self.current_data[ticker].update(data)
        record = {
            "ticker": ticker,
            "fr": float(self.current_data[ticker].get("nextFundingRate", np.nan)),
            "v24h": float(self.current_data[ticker].get("volume24H", np.nan)),
            "t24h": float(self.current_data[ticker].get("trades24H", np.nan)),
            "oi": float(self.current_data[ticker].get("openInterest", np.nan)),
        }
        self.funding_rates[ticker] = record

    @property
    def fr_df(self):
        return pd.DataFrame.from_records([el for _, el in self.funding_rates.items()])

    @property
    def name(self):
        return "dydx"

    @property
    def has_orderbook(self):
        return True

