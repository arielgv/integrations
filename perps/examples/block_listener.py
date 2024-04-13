import os
from ..core.block_listener import BlockListener
from ..core.block_feed import BlockFeed
from ..core.event_loop import EventLoop


class Strat(BlockListener):
    """Simple strategy that listens to blocks and prints them out."""

    def on_block(self, block: {}):
        print(f"Got block: {block['number']}")


if __name__ == "__main__":
    from web3 import Web3
    import dotenv
    dotenv.load_dotenv()
    w3 = Web3(Web3.WebsocketProvider(os.getenv("WS_URL")))
    print(os.getenv("WS_URL"))
    strat = Strat()
    feed = BlockFeed(w3)
    feed.add_listener(strat)
    event_loop = EventLoop()
    event_loop.add_feed(feed)
    event_loop.run()
