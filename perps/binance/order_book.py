import logging
from typing import Dict

from ..core.order_book import OrderBookBase
from .feed import BinanceListener


class OrderBook(OrderBookBase, BinanceListener):
    def __init__(self, coin: str = "ETH"):
        super().__init__(coin)

    def on_book_ticker(self, ticker: str, bbo: {}):
        if ticker.lower() == self.coin.lower():
            self.on_book_update(bbo)

    def _on_book_update(self, book_msg: Dict) -> None:
        """On book update"""
        logging.debug(f"book_msg {book_msg}")
        self.book_data = {
            "bids": [{"px": float(book_msg["best_bid"]), "sz": float(book_msg["best_bid_qty"])}],
            "asks": [{"px": float(book_msg["best_ask"]), "sz": float(book_msg["best_ask_qty"])}],
            "time": book_msg["time"],
        }

    @property
    def exchange(self):
        return "binance"
