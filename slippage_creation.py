import ccxt
import time
import pandas as pd
import matplotlib.pyplot as plt
from ccxt.base.errors import NetworkError
from datetime import datetime

exchange = ccxt.binanceus()

def get_order_book(symbol="BTC/USDT", max_retries=3):
    """Fetch Binance order book and estimate slippage."""
    for attempt in range(max_retries):
        try:
            order_book = exchange.fetch_order_book(symbol, limit=10)
            
            best_bid = order_book['bids'][0][0] if order_book['bids'] else None
            best_ask = order_book['asks'][0][0] if order_book['asks'] else None
            spread = best_ask - best_bid if best_ask and best_bid else None
            
            order_size = 0.5
            depth_at_bid = sum([bid[1] for bid in order_book['bids']])
            depth_at_ask = sum([ask[1] for ask in order_book['asks']])
            
            slippage = (order_size / (depth_at_bid + depth_at_ask)) * spread if spread else None
            return {
                "best_bid": best_bid,
                "best_ask": best_ask,
                "spread": spread,
                "estimated_slippage": slippage,
                "timestamp": time.time()
            }
        except NetworkError as e:
            if attempt == max_retries - 1:
                print(f"Failed after {max_retries} attempts: {str(e)}")
                return None
            time.sleep(2 ** attempt)
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None

def save_batch(data, batch_number):
    """Save a batch of data to CSV"""
    if not data:
        return
    
    df = pd.DataFrame(data)
    
    # For first batch, write with headers
    if batch_number == 0:
        df.to_csv("slippage_data.csv", index=False)
    # For subsequent batches, append without headers
    else:
        df.to_csv("slippage_data.csv", mode='a', header=False, index=False)
    
    print(f"Saved batch {batch_number} at {datetime.now()}")
    print(f"Batch stats:\n{df.describe()}\n")

def collect_data(total_points=float('inf'), batch_size=1000, delay=10):
    """Collect data in batches"""
    data = []
    total_processed = 0
    batch_number = 0
    
    try:
        while total_processed < total_points:
            result = get_order_book()
            if result is not None:
                data.append(result)
                total_processed += 1
                
                # When batch is full, save and reset
                if len(data) >= batch_size:
                    save_batch(data, batch_number)
                    batch_number += 1
                    data = []  # Reset data list
                
                # Print progress
                if total_processed % 100 == 0:
                    print(f"Processed {total_processed} requests")
            
            time.sleep(delay)
            
    except KeyboardInterrupt:
        print("\nData collection interrupted by user")
        # Save any remaining data
        if data:
            save_batch(data, batch_number)
        print(f"Total points collected: {total_processed}")
    
    except Exception as e:
        print(f"Error during data collection: {str(e)}")
        if data:
            save_batch(data, batch_number)
        print(f"Total points collected: {total_processed}")

# Start collecting data
# Set total_points=float('inf') for infinite collection
collect_data(
    total_points=float('inf'),  # Collect indefinitely
    batch_size=1000,           # Save every 1000 points
    delay=1                   # 10 second delay between requests
)