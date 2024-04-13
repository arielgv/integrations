from web3 import Web3
import time
import os
#import dotenv
from datetime import datetime
from abis import STORAGE_CONFIG_ABI

#dotenv.load_dotenv()
#################### HTTP ALCHEMY URL ARBITRUM ####
ALCHEMY_URL = 'https://arb-mainnet.g.alchemy.com/v2/BR5NFYsO9xS7QvUNw853TPbS19MvqXs-'
w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))
STORAGE_CONFIG_ADDRESS = "0xF4F7123fFe42c4C90A4bCDD2317D397E0B7d7cc0"


price_monitor_contract = w3.eth.contract(address=STORAGE_CONFIG_ADDRESS, abi=STORAGE_CONFIG_ABI)

response = price_monitor_contract.functions.getMarketConfigs().call()

for item in response:
  print("Asset ID:", item[0].decode('utf-8'))
  print("Max Long Position Size:", item[1])
  print("Max Short Position Size:", item[2])
  print("Increase Position Fee Rate BPS:", item[3])
  print("Decrease Position Fee Rate BPS:", item[4])
  print("Initial Margin Fraction BPS:", item[5])
  print("Maintenance Margin Fraction BPS:", item[6]) 
  print("Max Profit Rate BPS:", item[7])
  print("Asset Class:", item[8])
  print("Allow Increase Position:", item[9])
  print("Active:", item[10])
  print("Max Skew Scale USD:", item[11][0])
  print("Max Funding Rate:", item[11][1])
  print("--------------------")