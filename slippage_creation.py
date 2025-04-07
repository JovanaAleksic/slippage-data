import ccxt
import time
import pandas as pd
from ccxt.base.errors import NetworkError
from datetime import datetime

exchange = ccxt.binanceus()


def get_actual_slippage(symbol="BTC/USDT", order_size=1, is_buy=True):
    """Simulate an order and calculate actual slippage based on order book impact."""
    try:
        order_book = exchange.fetch_order_book(symbol, limit=50)

        if is_buy:
            prices = [ask[0] for ask in order_book['asks']]
            sizes = [ask[1] for ask in order_book['asks']]
        else:
            prices = [bid[0] for bid in order_book['bids']]
            sizes = [bid[1] for bid in order_book['bids']]

        total_filled = 0
        total_cost = 0
        for price, size in zip(prices, sizes):
            if order_size > total_filled:
                size_to_fill = min(order_size - total_filled, size)
                total_filled += size_to_fill
                total_cost += size_to_fill * price
            else:
                break

        # Actual slippage = (total cost of the order - expected cost at the best price)
        expected_cost = order_size * prices[0]  # Best ask or bid price
        slippage = (total_cost - expected_cost) / order_size
        return slippage

    except Exception as e:
        print(f"Error calculating actual slippage: {e}")
        return None


def get_order_book(symbol="BTC/USDT", max_retries=3):
    """Fetch Binance order book and estimate slippage."""
    for attempt in range(max_retries):
        try:
            order_book = exchange.fetch_order_book(symbol, limit=10)

            best_bid = order_book['bids'][0][0] if order_book['bids'] else None
            best_ask = order_book['asks'][0][0] if order_book['asks'] else None
            spread = best_ask - best_bid if best_ask and best_bid else None

            # Calculate actual slippage for both buy and sell orders
            buy_slippage = get_actual_slippage(symbol, order_size=1, is_buy=True)
            sell_slippage = get_actual_slippage(symbol, order_size=1, is_buy=False)

            return {
                "best_bid": best_bid,
                "best_ask": best_ask,
                "spread": spread,
                "buy_slippage": buy_slippage,
                "sell_slippage": sell_slippage,
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

    if batch_number == 0:
        df.to_csv("slippage_data_part2.csv", index=False)
    else:
        df.to_csv("slippage_data_part2.csv", mode='a', header=False, index=False)

    print(f"Saved batch {batch_number} at {datetime.now()}")


def collect_data(total_points=float('inf'), batch_size=1000, delay=1):
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
collect_data(
    total_points=float('inf'),  # Collect indefinitely
    batch_size=1000,  # Save every 1000 points
    delay=1  # 1-second delay between requests
)
