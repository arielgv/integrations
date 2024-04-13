# Binance API Scripts

This repository contains Python scripts to interact with the Binance API for accessing various information related to cryptocurrency trading on the Binance exchange.

## Functionality

### Binance_task1.py
This script fetches funding rate intervals for specified symbols (default: ethusdt, btcusdt) and subscribes to the mark price stream for these symbols. It calculates and prints the normalized funding rate, mark price, index price, settle price, and next funding time.

### Binance_task2.py
This script subscribes to the book ticker stream for specified symbols (default: ethusdt, btcusdt) and prints the best bid, best ask, and their corresponding sizes whenever there are updates.

### Binance_task3.py
This script utilizes the Binance API to fetch account assets and open positions for futures trading. It prints wallet balances, open positions including position amount, position side, leverage, maintenance margin, entry price, unrealized profit, and update time.

## How to Run

1. Install dependencies by running:
`pip install -r requirements.txt`
2. Ensure you have valid API key and secret key for Binance Futures trading.
3. Set the API key and secret key as environment variables `BINANCE_API_KEY` and `BINANCE_API_SECRET` respectively.

## Note
- By default, the tickers used in the scripts are ethusdt and btcusdt. You can modify the `symbols` variable in the scripts to use different symbols if needed.
- The scripts are provided as Python files (.py) and also as Jupyter Notebooks (.ipynb). Both versions have the same functionality.

