from abc import ABC, abstractmethod
from typing import List
import websocket
import json
import threading
from ..core.feed import Feed

#########
PREDEFINED_TICKERS = ["ethusdt", "btcusdt"]
########


class BinanceListener:
    """Dydx listener"""

    @abstractmethod
    def on_book_ticker(self, ticker: str, bbo: {}):
        """Listens to the book ticker feed"""


class BinanceFeed(Feed):
    """Binance Feed"""

    def __init__(
        self,
        tickers: List[str] = PREDEFINED_TICKERS,
    ):
        self.tickers = tickers
        websocket_url = "wss://fstream.binance.com/stream?streams=" + "/".join(
            [f"{symbol}@bookTicker" for symbol in self.tickers]
        )
        self.ws = websocket.WebSocketApp(
            websocket_url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        self.ws.on_open = self.on_open
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.start()
        self.listeners: List[BinanceListener] = []

    def add_listener(self, listener: BinanceListener):
        """Add listener"""
        self.listeners.append(listener)
        pass

    def run_ticks(self):
        pass

    def on_open(self, ws):
        """On open connection"""
        streams = "/".join([f"{symbol}@bookTicker" for symbol in self.tickers])
        ws.send(
            json.dumps({"method": "SUBSCRIBE", "params": streams.split("/"), "id": 1})
        )

    def on_message(self, ws, message):
        """On message received from websocket"""
        data = json.loads(message)
        if "stream" in data:
            stream_info = data["stream"]
            event_data = data["data"]
            if event_data["e"] == "bookTicker":
                self.handle_book_ticker(stream_info, event_data)

    def handle_book_ticker(self, stream_info, event_data):
        symbol = event_data["s"]
        best_bid = float(event_data["b"])
        best_ask = float(event_data["a"])
        best_bid_qty = float(event_data["B"])
        best_ask_qty = float(event_data["A"])
        bbo = {
            "ticker": symbol,
            "best_bid": best_bid,
            "best_ask": best_ask,
            "best_bid_qty": best_bid_qty,
            "best_ask_qty": best_ask_qty,
            "time": event_data["E"] / 1000,
        }
        for listener in self.listeners:
            listener.on_book_ticker(symbol, bbo)

    def on_error(self, ws, error):
        """On error"""
        print("Error:", error)

    def on_close(self, close_status_code, close_msg):
        """On close connection"""
        print("### CLOSED CONNECTION ###", close_status_code, close_msg)

