import time
from hyperliquid.info import Info
from web3 import Web3
from .abis import CALCULATOR_ABI, STORAGE_CONFIG_ABI

CALCULATOR_CONTRACT_ADDRESS = "0x0FdE910552977041Dc8c7ef652b5a07B40B9e006"
STORAGE_CONFIG = "0xF4F7123fFe42c4C90A4bCDD2317D397E0B7d7cc0"


class HyperLiquidApi:

    def __init__(self, w3: Web3):
        self.calculator_contract = w3.eth.contract(
            address=CALCULATOR_CONTRACT_ADDRESS, abi=CALCULATOR_ABI
        )
        self.config_contract = w3.eth.contract(
            address=STORAGE_CONFIG, abi=STORAGE_CONFIG_ABI
        )
        self.info = Info(skip_ws=True)
        self.init()

    def init(self):
        self.market_configs = self.get_market_configs()
        self.markets = self.get_markets()

    def get_markets(self):
        try:
            return self.info.meta()
        except Exception as e:
            print(f"Error obtaining markets: {e}")
            return []

    def get_market_configs(self):
        results = self.config_contract.functions.getMarketConfigs().call()
        configs = []
        for _, result in enumerate(results):
            ticker = result[0].replace(b"\x00", b"").decode("utf-8") + "-USD"
            configs.append([ticker] + [el for el in result[1:]])
        return configs

    def get_last_funding_rate(self, ticker):
        try:
            end_time = int(time.time() * 1000)  # Current time
            start_time = end_time - 24 * 60 * 60 * 1000  # 24 hours ago
            response = self.info.funding_history(
                coin=ticker, startTime=start_time, endTime=end_time
            )
            if response:
                return response[-1]
            return None
        except Exception as e:
            # print(f"Error obtaining funding rate for {ticker}: {e}")
            return None

    def get_funding_rate_velocity(self, market_index):
        return self.calculator_contract.functions.getFundingRateVelocity(
            market_index
        ).call()
