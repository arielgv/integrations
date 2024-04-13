from rich.console import Console
from rich.table import Table
from ...core.event_loop import EventLoop
from ...core.timer_feed import TimerFeed, TimerListener
from ...hyperliquid.order_book import OrderBook


class Strat(TimerListener):

    def __init__(self, ):
        self.order_book = OrderBook()

    def on_timer(self):
        bbo = self.order_book.bbo()
        if not bbo:
            return
        print(f"{self.order_book.exchange}: {self.order_book.coin}, Got bbo: {bbo}, Mid price: {self.order_book.mid_price()}")



if __name__ == "__main__":
    import sys
    import dotenv
    dotenv.load_dotenv()
    try:
        exchanges = ["hyperliquid"]
        event_loop = EventLoop()
        strat = Strat()
        # default every ten seconds:
        feed = TimerFeed(freq_ms=10 * 1000)
        feed.add_listener(strat)
        event_loop.add_feed(feed)
        event_loop.run()
    except KeyboardInterrupt:
        print("\nExiting on ctrl-c")
        sys.exit(0)
