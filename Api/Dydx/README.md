
# DyDX v4


This repository contains code and notebooks for solving three distinct tasks related to DyDX v4 . The tasks are implemented in both Python scripts and Jupyter Notebooks for easy execution and detailed walkthroughs.

## Structure
- `requirements.txt`: Lists all the dependencies required to run the scripts and notebooks.
- `PyFiles/`: Contains Python scripts extracted from the Jupyter Notebook for direct execution.
  - `Dydx_Task1.py`
  - `Dydx_Task2.py`
  - `Dydx_Task3.py`
- `IpynbFiles/`: Contains Jupyter Notebooks detailing the implementation of each task.
  - `Dydx_Tasks.ipynb`

## Installation
To set up your environment to run these tasks, follow these steps:
1. Clone this repository to your local machine.
2. Ensure you have Python 3.x installed.
3. Install the required dependencies by running `pip install -r requirements.txt` in your terminal.

## Tasks
### Task 1
[Given a set of tickers / markets (ie: ETH-USD, BTC-USD) create script that will listen to the dydx data feeds and will output in real time:
ticker, funding rate, openinterest, oracleprice, 24h volume, 24h trades, next funding
The script should run indefinitely until killed by ctrl-C  and publish updates to these quantities as they change. ]

**To run:** `python PyFiles/Dydx_Task1.py`

### Task 2
[Given a set of tickers / markets (ie: ETH-USD, BTC-USD) create script that will listen to the dydx data feeds via websocket and output in real time:
ticker,timestamp,bid, ask, bid_size, ask_size
The script should run indefinitely until killed by ctrl-C]

**To run:** `python PyFiles/Dydx_Task2.py`

### Task 3
[Using the dydx v4 api, write a script which monitors all of the open positions for your test account and prints out the relevant metrics:
Ticker, side, position size, leverage, liquidation price, unrealized pnl, realized pnl, margin usage, free collateral, avg open / close ]

**To run:** `python PyFiles/Dydx_Task3.py`

## Running the Notebooks
To explore the detailed implementation of each task, including data exploration, analysis, and visualization steps:
1. Ensure you have Jupyter Notebook or JupyterLab installed.
2. Navigate to the `IpynbFiles/` directory.
3. Run `jupyter notebook` or `jupyter lab` in your terminal.
4. Open `Dydx_Tasks.ipynb` from the list of notebooks.

