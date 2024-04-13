from typing import List
import websocket
import json
import threading
from ..core.feed import Feed

#########
PREDEFINED_TICKERS = None # ["BTC-USD", "ETH-USD"]
########


INDEXER_API_HOST_MAINNET = "https://indexer.dydx.trade"
INDEXER_WS_HOST_MAINNET = "wss://indexer.dydx.trade/v4/ws"
INDEXER_WS_HOST_TESTNET = "wss://indexer.v4testnet.dydx.exchange/v4/ws"


class DyDxListener:
    """Dydx listener"""

    def on_markets(self, ticker: str, market_data: {}):
        """Listens to the market feed"""

    def on_trading(self, ticker: str, trading_data: {}):
        """Listens to the trading feed"""


class DyDXFeed(Feed):
    """DYDX Feed"""

    def __init__(
        self,
        websocket_url: str = INDEXER_WS_HOST_MAINNET,
        tickers: List[str] = PREDEFINED_TICKERS,
    ):
        self.tickers = tickers
        self.ws = websocket.WebSocketApp(
            websocket_url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        self.ws.on_open = self.on_open
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.start()
        self.listeners: List[DyDxListener] = []

    def add_listener(self, listener: DyDxListener):
        """Add listener"""
        self.listeners.append(listener)
        pass

    def run_ticks(self):
        pass

    def on_open(self, ws):
        """On open connection"""
        subscription_message = json.dumps(
            {
                "type": "subscribe",
                "channel": "v4_markets",
            }
        )
        ws.send(subscription_message)
        print("Market channel subscription: v4_markets.")

    def on_message(self, ws, message):
        """On message received from websocket"""
        data = json.loads(message)

        if data.get("type") == "subscribed" and "markets" in data.get("contents", {}):
            markets_data = data["contents"]["markets"]
            if self.tickers is None:
                self.tickers = list(markets_data.keys())
            for ticker in self.tickers:
                market_data = markets_data.get(ticker)
                if market_data:
                    for listener in self.listeners:
                        listener.on_markets(ticker, market_data)

        elif data.get("type") == "channel_data" and "trading" in data.get(
            "contents", {}
        ):
            trading_data = data["contents"]["trading"]
            for ticker in self.tickers:
                if ticker in trading_data:
                    for listener in self.listeners:
                        listener.on_trading(ticker, trading_data[ticker])

    def on_error(self, ws, error):
        """On error"""
        print("Error:", error)

    def on_close(self, close_status_code, close_msg):
        """On close connection"""
        print("### CLOSED CONNECTION ###", close_status_code, close_msg)


class DyDxExampleListener(DyDxListener):
    """Example listener for dydx feed"""

    def __init__(self):
        self.current_data = {}

    def on_markets(self, ticker: str, market_data: {}):
        print("Market data:", market_data)
        self.update_ticker_info(ticker, market_data)
        self.print_ticker_info(ticker)

    def on_trading(self, ticker: str, trading_data: {}):
        print("Trading data:", trading_data)
        self.update_ticker_info(ticker, trading_data)
        self.print_ticker_info(ticker)

    def update_ticker_info(self, ticker, data):
        """Update ticker info"""
        if ticker not in self.current_data:
            self.current_data[ticker] = {}
        self.current_data[ticker].update(data)

    def print_ticker_info(self, ticker):
        """print ticker info"""
        ticker_data = self.current_data[ticker]
        formatted_info = f"""
        Ticker: {ticker}
        Funding Rate: {ticker_data.get('nextFundingRate', 'N/A')}
        Open Interest: {ticker_data.get('openInterest', 'N/A')}
        Oracle Price: {ticker_data.get('oraclePrice', 'N/A')}
        24h Volume: {ticker_data.get('volume24H', 'N/A')}
        24h Trades: {ticker_data.get('trades24H', 'N/A')}
        Next Funding: {ticker_data.get('nextFundingRate', 'N/A')}
        ---------------------------------------------
        """
        print(formatted_info)
