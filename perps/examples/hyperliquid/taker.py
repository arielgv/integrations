from typing import List, Dict
import time
import numpy as np

from ...core.oms import OMS
from ...core.event_loop import EventLoop
from ...core.timer_feed import TimerFeed, TimerListener
from ...core.order_book import OrderBookBase
from ...hyperliquid.order_book import OrderBook as HyperOrderBook
from ...binance.feed import BinanceFeed
from ...binance.order_book import OrderBook as BinanceOrderBook


class Strat:

    def __init__(
        self, oms: OMS, max_pos_usd=10e3, max_trade_freq_ms=10e3, min_size_usd=100
    ):
        self.oms = oms
        self.max_pos_usd = max_pos_usd
        self.max_trade_freq_ms = max_trade_freq_ms
        self.min_size_usd = min_size_usd

    def on_alpha(self, name, coin, exchange, price, alpha, horizon_ms):
        if self.oms.last_trade_time(coin, exchange) < self.max_trade_freq_ms:
            return
        elif self.oms.open_orders(coin, exchange):
            print("open orders")
            return
        net_alpha = alpha + self.dollar_alpha(exchange)
        print("Got dollar alpha:", net_alpha - alpha, "Regular alpha", alpha)
        if net_alpha > 0:
            self.buy(coin, exchange, price)
        elif net_alpha < 0:
            self.sell(coin, exchange, price)

    def dollar_alpha(self, exchange):
        equity = self.oms.equity(exchange)
        delta = self.oms.position_delta(exchange)
        # At 3x leverage one direction we generate 1 bip of alpha in opposite direction
        return -1.0 * 3 * delta / equity / 1e4

    def buy(self, coin, exchange, price):
        pos_size = self.oms.position_size(coin, exchange)
        qty = int((self.max_pos_usd - pos_size) / price)
        if qty * price < self.min_size_usd:
            return
        self.oms.submit_market_order(coin, exchange, qty, "buy")

    def sell(self, coin, exchange, price):
        pos_size = self.oms.position_size(coin, exchange)
        qty = int((self.max_pos_usd + pos_size) / price)
        if qty * price < self.min_size_usd:
            return
        self.oms.submit_market_order(coin, exchange, qty, "sell")


class Alpha(TimerListener):

    def __init__(self, coin, order_books: List[OrderBookBase]):
        self.name = "BBOArb"
        self._coin = coin
        self.order_books = order_books
        self.listeners = []
        for ob in self.order_books:
            ob.add_listener(self.on_tick)

    def add_listener(self, listener):
        self.listeners.append(listener)

    def noitfy_listeners(self, coin, exchange, price, alpha, horizon_ms):
        for listener in self.listeners:
            listener.on_alpha(self.name, coin, exchange, price, alpha, horizon_ms)

    def on_tick(self, msg: Dict):
        self.find_arbs()

    def find_arbs(self):
        max_bid = sorted(
            self.order_books, key=lambda x: float(x.bbo()[0]["px"]) if x.bbo() else -1
        )[-1]
        min_ask = sorted(
            self.order_books,
            key=lambda x: float(x.bbo()[1]["px"]) if x.bbo() else np.inf,
        )[0]
        if max_bid.bbo()[0]["px"] > min_ask.bbo()[1]["px"]:
            # print(
            #     f"Buy on {min_ask.exchange} at {min_ask.bbo()[1]['px']}, sell on {max_bid.exchange} at {max_bid.bbo()[0]['px']}"
            # )
            if min_ask.exchange == "hyperliquid":
                alpha = 1
                price = min_ask.mid_price()
            else:
                alpha = -1
                price = max_bid.mid_price()
            self.noitfy_listeners(self._coin, "hyperliquid", price, alpha, 0)

    def on_timer(self):
        pass


if __name__ == "__main__":
    import sys
    import dotenv

    dotenv.load_dotenv()
    binance_tickers = [
        "memeusdt",
    ]
    binance_obs = {}
    try:
        event_loop = EventLoop()
        feed = BinanceFeed(tickers=binance_tickers)
        coin = binance_tickers[0].replace("usdt", "")
        binance_ob = BinanceOrderBook(coin=binance_tickers[0])
        feed.add_listener(binance_ob)
        hyper_ob = HyperOrderBook(coin=coin)
        obs = [binance_ob, hyper_ob]
        alpha = Alpha("meme", obs)
        strat = Strat(OMS())
        alpha.add_listener(strat)
        # default every ten seconds:
        timer_feed = TimerFeed(freq_ms=10 * 1000)
        timer_feed.add_listener(alpha)
        event_loop.add_feed(feed)
        event_loop.add_feed(timer_feed)
        event_loop.run()
    except KeyboardInterrupt:
        print("\nExiting on ctrl-c")
        sys.exit(0)
