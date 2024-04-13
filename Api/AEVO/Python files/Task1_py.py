import requests
import time

#available assets:
# ["10000SATS","1000BONK","1000PEPE","ALT","APT","ARB","ATOM","AVAX","BANANA","BEAM","BEAMX","BITCOIN","BLAST","BLUR","BLZ","BNB","BTC","CANTO","CRV","DOGE","DYDX","DYM","ETH","FRIEND","GLMR","HIFI","HPOS","ILV","INJ","JITO","JUP","LDO","LINK","MANTA","MATIC","MEME","MINA","MKR","NMR","NTRN","OP","ORDI","OX","PARCL","PIXEL","PORTAL","PRIME","PYTH","RNDR","SEI","SHFL","SOL","STRAX","STRK","SUI","SYN","T","TAO","TIA","TRB","TRX","UMA","WLD","XRP","ZETA"]

tickers = ['ETH', 'BTC']  

while True:
    for ticker in tickers:

        asset_name = ticker + "-PERP"


        url = f"https://api.aevo.xyz/funding?instrument_name={asset_name}"


        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)


        print(f"RESPONSE {ticker}: {response.text}")

        url = f"https://api.aevo.xyz/statistics?asset={ticker}&instrument_type=PERPETUAL"
        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)

        print(response.text)

    time.sleep(10)
