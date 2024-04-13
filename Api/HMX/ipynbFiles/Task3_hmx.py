from web3 import Web3
import abis
import rpc_and_wallet
from datetime import datetime

#####
POSITIONS_ABI = abis.POSITIONS_ABI
ASSET_ID_32_ABI = abis.ASSET_ID_32_ABI
PRICE_MONITOR_ABI = abis.PRICE_MONITOR_ABI
CALCULATOR_ABI = abis.CALCULATOR_ABI
STORAGE_CONFIG_ABI = abis.STORAGE_CONFIG_ABI
#####
ALCHEMY_URL = rpc_and_wallet.ALCHEMY_URL
WALLET_ADDRESS = rpc_and_wallet.WALLET_ADDRESS
#####

# URL & CONTRACT ADDRESS

PERP_STORAGE_ADDRESS = '0x97e94BdA44a2Df784Ab6535aaE2D62EFC6D2e303'
ASSET_ID_CONTRACT_ADDRESS = '0xF4F7123fFe42c4C90A4bCDD2317D397E0B7d7cc0'
CALCULATOR_CONTRACT_ADDRESS = '0x0FdE910552977041Dc8c7ef652b5a07B40B9e006'
PRICE_MONITOR_CONTRACT_ADDRESS = '0x9c83e1046dA4727F05C6764c017C6E1757596592'

# hmx client & web3 connection.
from hmx2.hmx_client import Client
hmx_client = Client(rpc_url=ALCHEMY_URL)
w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))

# contracts
perp_storage_contract = w3.eth.contract(address=PERP_STORAGE_ADDRESS, abi=POSITIONS_ABI)
asset_id_contract = w3.eth.contract(address=ASSET_ID_CONTRACT_ADDRESS, abi=ASSET_ID_32_ABI)
calculator_contract = w3.eth.contract(address=CALCULATOR_CONTRACT_ADDRESS, abi=CALCULATOR_ABI)
price_monitor_contract = w3.eth.contract(address=PRICE_MONITOR_CONTRACT_ADDRESS, abi=PRICE_MONITOR_ABI)

def get_positions_by_subaccount(wallet_address):
    positions = perp_storage_contract.functions.getPositionBySubAccount(wallet_address).call()
    print(f"Found {len(positions)} positions")
    return positions

####
def check_for_liquidation(wallet_address):
    equity = calculator_contract.functions.getEquity(wallet_address, 0, asset_id32).call()
    mmr = calculator_contract.functions.getMMR(wallet_address).call()
    
    print(f"Equity (E30): {equity}")
    print(f"MMR (E30): {mmr}")
    equity_mmr_ratio = equity / mmr if mmr > 0 else 0
    print(f"Equity/MMR Ratio: {equity_mmr_ratio}")
    
    if equity < mmr:
        print("Liquidation condition met...")
        # 
    else:
        print("No liquidation required.")

####
        

positions = get_positions_by_subaccount(WALLET_ADDRESS)

for position in positions:
    #  asset_id32
    market_index = position[1]
    asset_id32 = asset_id_contract.functions.getMarketConfigByIndex(market_index).call()[0]
    print(f"Asset ID: {asset_id32}")

    # exit price
    exit_price, last_update = price_monitor_contract.functions.getLatestPrice(asset_id32, False).call()

    # hmx_client methods. position info & ticker
    ticker = hmx_client.public.get_price(position[1])['market']
    position_info = hmx_client.public.get_position_info(WALLET_ADDRESS, position[9], position[1])
    #print (position_info)

    #  unrealizedPnlE30 y unrealizedFeeE30
    unrealizedPnlE30, unrealizedFeeE30 = calculator_contract.functions.getUnrealizedPnlAndFee(WALLET_ADDRESS, exit_price, asset_id32).call()

    # position Info
    print(f"Ticker: {ticker}")
    print(f"Size: {position[6]}")  # position_size_e30
    print(f"Entry Price (E30): {position[2]}")  # avg_entry_price_e30
    print(f"Est. Exit Price (E30): {exit_price}")
    print(f"Unrealized PnL (E30): {unrealizedPnlE30}")
    print(f"Unrealized Fee (E30): {unrealizedFeeE30}")
    print(f"Profit / Loss: {position_info['pnl'] - position_info['funding_fee'] - position_info['borrowing_fee'] * 2}")
    check_for_liquidation(WALLET_ADDRESS)
    print("---------------------------------------------------")
    print(f"Current Timestamp: {datetime.now()}")
    print("---------------------------------------------------")
