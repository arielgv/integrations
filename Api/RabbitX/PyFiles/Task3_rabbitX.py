from rabbitx import const
from rabbitx.client import Client, CandlePeriod, OrderSide, OrderType
from rabbitx.client import Client, WSClient, WSClientCallback
from websocket import WebSocketApp
from credentialsJWT import priv_key


TESTNETURL = 'https://api.testnet.rabbitx.io'


privkey = priv_key


client = Client(api_url=TESTNETURL, api_key='7kk9OJMjJIZvr9L/z9D5S/m6f3RYX0f1/PskltMvU8Q=',public_jwt="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MDAwMDAwMDAwIiwiZXhwIjo2NTQ4NDg3NTY5fQ.o_qBZltZdDHBH3zHPQkcRhVBQCtejIuyq8V1yj5kYq8", private_key=privkey)
client.onboarding.onboarding()
client.onboarding.init()
print(client.onboarding.onboarding())
print(client.trades.list(market_id="BTC-USD", p_limit=10))
print(client.markets.list())


client.positions.list()

EXPECTED_RESPONSE = """
GET /positions
Example response

{
    "success": true,
    "error": "",
    "result": [
            {'entry_price': '25532.188679245283018867924528301886794',
              'fair_price': '24351',
              'id': 'pos-BTC-USD-tr-7615',
              'liquidation_price': '26027.959333211210844477010441472797217',
              'margin': '64.53015',
              'market_id': 'BTC-USD',
              'notional': '1290.603',
              'profile_id': 7615,
              'side': 'short',
              'size': '0.053',
              'unrealized_pnl': '62.603000000000000000000000000000000082'}
    ]
}
"""