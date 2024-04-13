from ..core.timer_feed import TimerFeed, TimerListener
from ..core.event_loop import EventLoop


class Strat(TimerListener):
    """Simple strategy that listens to blocks and prints them out."""

    def on_timer(self, fire_ms: int):
        print(f"Got timestamp: {fire_ms}")


if __name__ == "__main__":
    import os
    import dotenv
    from web3 import Web3

    dotenv.load_dotenv()
    WS_URL = os.getenv("WS_URL")
    assert WS_URL, "WS_URL must be set in .env file."
    w3 = Web3(Web3.WebsocketProvider(WS_URL))
    strat = Strat()
    feed = TimerFeed(1000 * 10)
    feed.add_listener(strat)
    event_loop = EventLoop()
    event_loop.add_feed(feed)
    event_loop.run()
