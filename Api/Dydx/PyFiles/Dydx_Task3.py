from v4_client_py import IndexerClient
from v4_client_py.clients.constants import Network, BECH32_PREFIX
from v4_client_py.chain.aerial.wallet import LocalWallet#, BECH32_PREFIX
import requests


headers = {
  'Accept': 'application/json'
}


 #### MODIFY TO THE CORRECT ADDRESS
r = requests.get('https://dydx-testnet.imperator.co/v4/addresses/[use the correct address]', headers = headers)
r= r.json()


client = IndexerClient(
    config=Network.testnet().indexer_config,
)

 #### MODIFY TO THE CORRECT ADDRESS
# address is the wallet address on dYdX chain, subaccount_number is the subaccount number
address = 'usethecorrectaddress'
subaccounts_response = client.account.get_subaccounts(address)
subaccounts = subaccounts_response.data['subaccounts']


# SUBACCOUNT NUMBER

subaccount_number = 0
######################


perpetual_positions_response = client.account.get_subaccount_perpetual_positions(address, subaccount_number)
perpetual_positions = perpetual_positions_response.data['positions']

def print_positions(positions):
    for pos in positions:
        ticker = pos['market']
        side = pos['side']
        size = pos['size']
        leverage = "N/A"  # No presente en la documentacion 
        liquidation_price = "N/A"  # No presente en la documentacion 
        unrealized_pnl = pos['unrealizedPnl']
        realized_pnl = pos['realizedPnl']
        margin_usage = "N/A"  # No presente en la documentacion 
        free_collateral = r['subaccounts'][0]['freeCollateral']  
        avg_open_close = pos['sumOpen'] + '/' + pos['sumClose']  
        
        print(f"Ticker : {ticker}\nSide : {side}\nPosition Size : {size}\nLeverage : {leverage}\nLiquidation Price : {liquidation_price}\nUnrealized PnL : {unrealized_pnl}\nRealized PnL : {realized_pnl}\nMargin Usage : {margin_usage}\nFree Collateral : {free_collateral}\nsumOpen / sumClose : {avg_open_close}")


print_positions(perpetual_positions)
