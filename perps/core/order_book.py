from typing import Dict
from abc import abstractmethod, abstractproperty
import threading


class OrderBookBase:
    def __init__(self, coin: str = "ETH", poll_freq_ns=-1):
        self._coin = coin
        self.book_data = {"bids": [], "asks": [], "time": 0}
        self.listeners = []
        if poll_freq_ns > 0:
            self.poller = threading.Thread(target=self.poll)
            self.poller.start()

    def add_listener(self, listener):
        self.listeners.append(listener)

    def on_book_update(self, book_msg: Dict) -> None:
        self._on_book_update(book_msg)
        for listener in self.listeners:
            listener(book_msg)

    @abstractmethod
    def _on_book_update(self, book_msg: Dict) -> None:
        """Book updates"""
        pass

    @property
    def coin(self):
        return self._coin

    def bbo(self):
        try:
            best_bid = self.book_data["bids"][0]
            best_bid["px"] = float(best_bid["px"])
            best_bid["sz"] = float(best_bid["sz"])
            best_ask = self.book_data["asks"][0]
            best_ask["px"] = float(best_ask["px"])
            best_ask["sz"] = float(best_ask["sz"])
            return best_bid, best_ask
        except IndexError:
            return None

    def mid_price(self):
        best_bid, best_ask = self.bbo()
        if best_bid is None or best_ask is None:
            return None
        return (float(best_bid["px"]) + float(best_ask["px"])) / 2

    def poll(self):
        """Polling loop"""
        pass

    @abstractproperty
    def exchange(self):
        pass
