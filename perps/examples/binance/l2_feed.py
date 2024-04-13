from ...core.event_loop import EventLoop
from ...core.timer_feed import TimerListener, TimerFeed
from ...binance.feed import BinanceFeed
from ...binance.order_book import OrderBook


class Strat(TimerListener):

    def __init__(self, order_book):
        self.order_book = order_book

    def on_timer(self):
        bbo = self.order_book.bbo()
        if not bbo:
            return
        print(
            f"{self.order_book.exchange}: {self.order_book.coin}, Got bbo: {bbo}, Mid price: {self.order_book.mid_price()}"
        )


if __name__ == "__main__":
    import sys
    import dotenv

    dotenv.load_dotenv()
    try:
        event_loop = EventLoop()
        ob = OrderBook(coin="ethusdt")
        strat = Strat(ob)
        timer_feed = TimerFeed(freq_ms=10 * 1000)
        timer_feed.add_listener(strat)
        feed = BinanceFeed()
        feed.add_listener(ob)
        event_loop.add_feed(feed)
        event_loop.add_feed(timer_feed)
        event_loop.run()
    except KeyboardInterrupt:
        print("\nExiting on ctrl-c")
        sys.exit(0)
