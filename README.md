
# Crypto Market Slippage Data

This repository contains code and data for analyzing market slippage in cryptocurrency trading, specifically focusing on the BTC/USDT trading pair on Binance US.

## Overview

The project collects real-time order book data to estimate actual slippage in cryptocurrency trading. Slippage refers to the difference between the expected price of a trade and the actual executed price, which occurs due to changes in market liquidity and order book depth.

## Data Collection

The data collection script (`slippage_creation.py`) continuously monitors the Binance US order book and calculates the following metrics:

- Best bid price
- Best ask price
- Bid-ask spread
- Actual slippage for both buy and sell orders (based on simulated order impact)
- Timestamp of each measurement

### Technical Details

- Data is collected every 1 second (adjustable by changing the `delay` parameter)
- Order book depth is limited to the top 50 price levels
- Data is saved in batches of 1000 points to prevent data loss
- Actual slippage is calculated by simulating how an order would impact the market using real-time liquidity at different price levels

## Dataset

The collected data is stored in `slippage_data_partX.csv` with the following columns:

- `best_bid`: Best bid price in USDT
- `best_ask`: Best ask price in USDT
- `spread`: Difference between best ask and best bid
- `buy_slippage`: Actual slippage for a 1 BTC buy order
- `sell_slippage`: Actual slippage for a 1 BTC sell order
- `timestamp`: Unix timestamp of the measurement

### Data Collection Status

🔴 **Active Collection in Progress**

The dataset is currently being actively collected and will be updated regularly.

## Requirements

- Python 3.6+
- ccxt
- pandas
- matplotlib

## Usage

To run the data collection script:

```bash
python slippage_creation.py
```

The script will run indefinitely until interrupted with Ctrl+C. Upon interruption, it will save any remaining data before terminating.

### Notes:
- The script uses the public Binance US API and respects rate limits.
- Network errors are handled with exponential backoff.