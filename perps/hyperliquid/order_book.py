import logging
import threading
import time

from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils import constants
from hyperliquid.utils.signing import get_timestamp_ms
from hyperliquid.utils.types import (
    SIDES,
    Dict,
    L2BookMsg,
    L2BookSubscription,
    Literal,
    Optional,
    Side,
    TypedDict,
    Union,
    UserEventsMsg,
)

from ..core.order_book import OrderBookBase


def side_to_int(side: Side) -> int:
    return 1 if side == "A" else -1


def side_to_uint(side: Side) -> int:
    return 1 if side == "A" else 0


class OrderBook(OrderBookBase):
    def __init__(self, coin):
        coin = coin.upper()
        self.info = Info(skip_ws=False)
        subscription: L2BookSubscription = {"type": "l2Book", "coin": coin}
        self.info.subscribe(subscription, self.on_book_update)
        super().__init__(coin)

    def _on_book_update(self, book_msg: L2BookMsg) -> None:
        logging.debug(f"book_msg {book_msg}")
        book_data = book_msg["data"]
        if book_data["coin"] != self._coin:
            print("Unexpected book message, skipping")
            return
        self.book_data = {
            "bids": book_data["levels"][0],
            "asks": book_data["levels"][1],
            "time": book_data["time"],
        }

    @property
    def exchange(self):
        return "hyperliquid"
