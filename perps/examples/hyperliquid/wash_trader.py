from typing import List, Dict
import time
import numpy as np

from ...core.event_loop import EventLoop
from ...core.timer_feed import TimerFeed, TimerListener
from ...core.order_book import OrderBookBase
from ...hyperliquid.order_book import OrderBook as HyperOrderBook
from ...binance.feed import BinanceFeed
from ...binance.order_book import OrderBook as BinanceOrderBook
from ...hyperliquid.oms import HyperOMS


class Strat(TimerListener):

    def __init__(
        self, oms: HyperOMS, max_pos_usd=10e3, max_trade_freq_ms=10e3, min_size_usd=100
    ):
        self.coin = "MEME"
        self.qty = 1000
        self.oms = oms
        self.max_pos_usd = max_pos_usd
        self.max_trade_freq_ms = max_trade_freq_ms
        self.min_size_usd = min_size_usd
        self.last_trade_side = "buy"

    def on_timer(self):
        if not self.oms.ready:
            return
        pos_size = self.oms.position_size(self.coin)
        print("position size", pos_size)
        if pos_size < 0:
            self.buy(self.qty - pos_size)
        else:
            self.sell(self.qty + pos_size)
        if self.oms.user_state:
            print(f"oms position delta {self.oms.position_delta()}")
            print(f"oms total position size    {self.oms.total_pos_size()}")
            print(f"oms equity {self.oms.equity()}")
            print(f"leverage {self.oms.leverage()}")

    def buy(self, qty):
        self.oms.submit_market_order(self.coin, qty, "buy")
        self.last_trade_side = "buy"

    def sell(self, qty):
        self.oms.submit_market_order(self.coin, qty, "sell")
        self.last_trade_side = "sell"


if __name__ == "__main__":
    import sys
    import dotenv

    dotenv.load_dotenv()
    try:
        event_loop = EventLoop()
        oms = HyperOMS()
        strat = Strat(oms)
        # default every ten seconds:
        timer_feed = TimerFeed(freq_ms=10 * 1000)
        timer_feed.add_listener(strat)
        timer_feed.add_listener(oms)
        event_loop.add_feed(timer_feed)
        event_loop.run()
    except KeyboardInterrupt:
        print("\nExiting on ctrl-c")
        sys.exit(0)
