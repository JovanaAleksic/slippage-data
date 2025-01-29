# Crypto Market Slippage Data

This repository contains code and data for analyzing market slippage in cryptocurrency trading, specifically focusing on the BTC/USDT trading pair on Binance US.

## Overview

The project collects real-time order book data to estimate potential slippage in cryptocurrency trading. Slippage refers to the difference between the expected price of a trade and the actual executed price, which typically occurs due to changes in market liquidity and order book depth.

## Data Collection

The data collection script (`slippage_creation.py`) continuously monitors the Binance US order book and calculates the following metrics:

- Best bid price
- Best ask price
- Bid-ask spread
- Estimated slippage for a 0.5 BTC order size
- Timestamp of each measurement

### Technical Details

- Data is collected every 1 second
- Order book depth is limited to top 10 price levels
- Slippage is estimated using the formula: `(order_size / (depth_at_bid + depth_at_ask)) * spread`
- Data is saved in batches of 1000 points to prevent data loss

## Dataset

The collected data is stored in `slippage_data.csv` with the following columns:

- `best_bid`: Best bid price in USDT
- `best_ask`: Best ask price in USDT
- `spread`: Difference between best ask and best bid
- `estimated_slippage`: Calculated potential slippage for a 0.5 BTC order
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

## Notes

- The script uses the public Binance US API and respects rate limits
- Network errors are handled with exponential backoff
- Data is collected and saved in batches to minimize potential data loss
- The estimated slippage is theoretical and based on current order book depth
