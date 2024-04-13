from typing import List
from rich.console import Console
from rich.table import Table

from ...core.event_loop import EventLoop
from ...core.timer_feed import TimerFeed, TimerListener
from ...core.order_book import OrderBookBase
from ...hyperliquid.order_book import OrderBook as HyperOrderBook
from ...binance.feed import BinanceFeed
from ...binance.order_book import OrderBook as BinanceOrderBook


class Strat(TimerListener):

    def __init__(self, coin, order_books: List[OrderBookBase]):
        self._coin = coin
        self.order_books = order_books

    def on_timer(self):
        self.print_table()

    def print_table(self):
        table = Table(title=f"BBO for {self._coin.upper()}")
        table.add_column("Exchange")
        table.add_column("Best Bid")
        table.add_column("Bid Size")
        table.add_column("Best Ask")
        table.add_column("Ask Size")
        for ob in self.order_books:
            bbo = ob.bbo()
            if not bbo:
                continue
            table.add_row(
                ob.exchange,
                str(bbo[0]["px"]),
                str(bbo[0]["sz"]),
                str(bbo[1]["px"]),
                str(bbo[1]["sz"]),
            )

        if not table.rows:
            return

        console = Console()
        console.print(table)


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
        strat = Strat("meme", obs)
        # default every ten seconds:
        timer_feed = TimerFeed(freq_ms=10 * 1000)
        timer_feed.add_listener(strat)
        event_loop.add_feed(feed)
        event_loop.add_feed(timer_feed)
        event_loop.run()
    except KeyboardInterrupt:
        print("\nExiting on ctrl-c")
        sys.exit(0)
