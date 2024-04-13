"""
Main event loop class
"""
import time
from .feed import Feed


class EventLoop:
    """Main program event loop"""

    def __init__(self):
        self.feeds: [Feed] = []

    def add_feed(self, feed: Feed):
        """Add feed"""
        self.feeds.append(feed)

    def run(self):
        """run indefinitely"""
        while True:
            try:
                for feed in self.feeds:
                    feed.run_ticks()
                time.sleep(1e-4)
            except KeyboardInterrupt:
                break
