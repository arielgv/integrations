from rich.console import Console
from rich.table import Table
from ...core.event_loop import EventLoop
from ...core.timer_feed import TimerFeed, TimerListener
from ...binance.feed import BinanceFeed
from ...binance.order_book import BBO

COINS = []

# initialize coin feeds
# may need a feed factory to handle different exchanges

class Strat(TimerListener):

    def __init__(self, bbo: BBO):
        self.bbo = bbo

    def on_timer(self):
        for ticker in self.bbo.bbo:
            print(f"Got bbo for {ticker}: {self.bbo.bbo[ticker]}")


if __name__ == "__main__":
    import sys
    import dotenv

    dotenv.load_dotenv()
    try:
        exchanges = ["hyperliquid"]
        event_loop = EventLoop()
        # default every ten seconds:
        bbo = BBO()
        feed = BinanceFeed()
        feed.add_listener(bbo)
        strat = Strat(bbo)
        feed = TimerFeed(freq_ms=10 * 1000)
        feed.add_listener(strat)
        event_loop.add_feed(feed)
        event_loop.run()
    except KeyboardInterrupt:
        print("\nExiting on ctrl-c")
        sys.exit(0)
