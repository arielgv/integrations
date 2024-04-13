import time

class OMS:

    def __init__(self):
        self._last_trade_time = {}

    def open_orders(self, coin, exchange):
        pass

    def position_delta(self, exchange):
        return 0

    def positions(self, exchange):
        pass

    def position_size(self, coin, exchange) -> float:
        return 0

    def position_and_order_size(self, coin, exchange) -> float:
        return 0

    def equity(self, exchange):
        return 1e4

    def total_pos_size(self, exchange):
        pass

    def last_trade_time(self, coin, exchange) -> int:
        return 1000 * (time.time() - self._last_trade_time.get((coin, exchange), 0))

    def submit_market_order(self, coin, exchange, qty, side):
        print(f"Submitting market order for {qty} {coin} on {exchange} side {side}")
        self._update_last_trade_time(coin, exchange)

    def _update_last_trade_time(self, coin, exchange):
        self._last_trade_time[(coin, exchange)] = time.time()
