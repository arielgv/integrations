import time
import threading
import eth_account
from eth_account.signers.local import LocalAccount
import json
import os

from hyperliquid.utils.signing import get_timestamp_ms
from hyperliquid.exchange import Exchange
from hyperliquid.info import Info
from hyperliquid.utils.types import (
    UserEventsMsg,
)
from ..core.timer_feed import TimerListener


def setup(base_url=None, skip_ws=False):
    config = os.environ
    account: LocalAccount = eth_account.Account.from_key(config["HYPER_SECRET"])
    address = config["HYPER_ADDRESS"]
    if address == "":
        address = account.address
    print("Running with account address:", address)
    if address != account.address:
        print("Running with agent address:", account.address)
    info = Info(base_url, skip_ws)
    user_state = info.user_state(address)
    margin_summary = user_state["marginSummary"]
    if float(margin_summary["accountValue"]) == 0:
        print("Not running the example because the provided account has no equity.")
        url = info.base_url.split(".", 1)[1]
        error_string = f"No accountValue:\nIf you think this is a mistake, make sure that {address} has a balance on {url}.\nIf address shown is your API wallet address, update the config to specify the address of your account, not the address of the API wallet."
        raise Exception(error_string)
    exchange = Exchange(account, base_url, account_address=address)
    return address, info, exchange


class HyperOMS(TimerListener):

    def __init__(self):
        self.address, self.info, self.exchange = setup()
        self.info.subscribe(
            {"type": "userEvents", "user": self.address}, self.on_user_events
        )
        self.positions = {}
        self.pending_orders = []
        self.user_state = {}
        self.poll()
        # self.poller = threading.Thread(target=self.poll)
        # self.poller.start()

    def on_user_events(self, user_events: UserEventsMsg) -> None:
        user_events_data = user_events["data"]
        return user_events_data

    def submit_market_order(self, coin, qty, side, slippage=0.01):
        if not self.ready:
            return
        is_buy = side == "buy"
        print(f"Submitting market order for {qty} {coin} side {side}")
        order_result = self.exchange.market_open(coin, is_buy, qty, None, slippage)
        if order_result["status"] == "ok":
            for status in order_result["response"]["data"]["statuses"]:
                try:
                    filled = status["filled"]
                    if coin not in self.positions:
                        self.positions[coin] = {"szi": 0}
                    self.positions[coin]["szi"] += float(filled["totalSz"]) * (
                        1 if is_buy else -1
                    )
                    self.positions[coin]['positionValue'] = abs(float(filled['avgPx']) * self.positions[coin]['szi'])
                    print(
                        f'Order #{filled["oid"]} filled {filled["totalSz"]} @{filled["avgPx"]}, new position size: {self.positions[coin]["szi"]}, position value: {self.positions[coin]["positionValue"]}'
                    )
                except KeyError:
                    print("Error...", status)

    def equity(self):
        if self.user_state:
            return float(self.user_state["marginSummary"]["accountValue"])
        else:
            return 0

    @property
    def ready(self):
        return self.user_state != {}

    def position_size(self, coin: str):
        return float(self.positions.get(coin.upper(), {"szi": 0})["szi"])

    def total_pos_size(self):
        if self.user_state:
            return float(self.user_state["marginSummary"]["totalNtlPos"])
        else:
            return 0

    def leverage(self):
        return self.total_pos_size() / (0.0001 + self.equity())

    def position_delta(self):
        if not self.user_state:
            return None
        delta = 0
        for _, position in self.positions.items():
            pos_value = float(position["positionValue"])
            size = float(position["szi"])
            delta += pos_value * (1 if size > 0 else -1)
        return delta

    def poll(self):
        print("OMS polling ...")
        open_orders = self.info.open_orders(self.address)
        # print("open_orders", open_orders)
        self.user_state = self.info.user_state(self.address)
        # print("user_state", self.user_state.keys())
        for position in self.user_state["assetPositions"]:
            coin = position["position"]["coin"].upper()
            self.positions[coin] = position["position"]
            self.positions[coin]["szi"] = float(self.positions[coin]["szi"])

    def on_timer(self):
        self.poll()
