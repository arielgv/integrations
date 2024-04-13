from typing import List
from rabbitx.client import Client
from datetime import datetime

api_NoTest = "https://api.prod.rabbitx.io"

# fake pkey for testing:
priv_key = "0x1f173c6505de4108c564e21de1df1c8d3e8893b09c42f88af739148fc57ec946"

client = Client(api_url=api_NoTest, private_key=priv_key)


class RabbitXApi:

    def __init__(self, private_key=None) -> None:
        if private_key is None:
            private_key = priv_key
        self.client = Client(api_url=api_NoTest, private_key=private_key)

    def get_market_data(self, tickers: List = []):
        markets = self.client.markets.list()
        filtered_data = []
        for market in markets:
            if tickers and market["id"] not in tickers:
                continue
            next_funding_rate_timestamp_readable = datetime.fromtimestamp(
                market["next_funding_rate_timestamp"]
            ).strftime("%Y-%m-%d %H:%M:%S")
            data = {
                "ticker": market["id"],
                "funding_rate": market.get("instant_funding_rate", "N/A"),
                "open_interest": market.get("open_interest", "N/A"),
                "24h_volume": market.get(
                    "average_daily_volume", "N/A"
                ),  # Using average_daily_volume as a proxy
                "next_funding_rate_timestamp": next_funding_rate_timestamp_readable,
            }
            filtered_data.append(data)
        return filtered_data

