from ...core.event_loop import EventLoop
from ...dydx.feed import DyDXFeed, DyDxExampleListener


class Strat():
    """Simple strategy that listens to blocks and prints them out."""
    pass



if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()
    strat = DyDxExampleListener()
    feed = DyDXFeed()
    feed.add_listener(strat)
    event_loop = EventLoop()
    event_loop.add_feed(feed)
    event_loop.run()
