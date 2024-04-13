from hyperliquid.info import Info
from hyperliquid.utils import constants
import datetime
import time

####  address provided for testnet @ hyperliquid
address = "0xcd5051944f780a621ee62e39e493c489668acf4d"
#####



def display_user_positions_with_additional_info(address):
    info = Info(constants.TESTNET_API_URL, skip_ws=True)
    user_state = info.user_state(address)
    all_mids = info.all_mids()  
    
    print("Positions:")
    for asset in user_state['assetPositions']:
        position = asset['position']
        coin = position['coin']
        entry_px = position['entryPx']
        szi = position['szi']
        leverage = position['leverage']
        liquidation_px = position['liquidationPx'] or "N/A"
        unrealized_pnl = position['unrealizedPnl']
        margin_used = position['marginUsed']
        current_px = all_mids[coin] 
        
     
        l2_snapshot = info.l2_snapshot(coin=coin)
        stamp = int(time.time())
        timestamp = datetime.datetime.fromtimestamp(stamp).strftime('%Y-%m-%d %H:%M:%S')
        
        #realized_pnl = "N/A" 
        #free_collateral = "N/A" 
        #avg_open_close = "N/A" 
        
        print(f"Ticker: {coin}, Entry Price: {entry_px}, Current Price: {current_px}, Position Size: {szi}, "
              f"Leverage: {leverage['type']} {leverage['value']}, Liquidation Price: {liquidation_px}, "
              f"Unrealized PnL: {unrealized_pnl}, Margin Used: {margin_used}, "
              f"Timestamp: {timestamp}")



display_user_positions_with_additional_info(address)
