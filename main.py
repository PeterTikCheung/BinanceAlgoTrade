from binance.client import Client
from binance import BinanceSocketManager
import time
import logging

# Logging setup
logging.basicConfig(filename="binance_bot.log", level=logging.INFO,
                    format='%(asctime)s %(message)s')

# Binance client setup
client = Client("IwEFWRF4Im9zhbjH3YtuPyw7SXG2zlIbnu7auwfYMugT7J3OD5KhBZilKH5WMxag", "XjL6RFWoT2DIlLgN3e02odOnKjWOknEOTssbVaRncPGb1I2r0H5eXq7urC3DUluo")

# Strategy parameters
fast_ma = 7
slow_ma = 14
symbol = "BTCUSDT"
amount = 0.02
previous_fast_ma = 0;
previous_slow_ma = 0;
# Start trading loop
while True:
    previous_fast_ma = fast_ma
    previous_slow_ma = slow_ma
    fast_ma_default = 7
    slow_ma_default = 14
    # Get latest klines from Binance
    klines = client.get_historical_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=fast_ma_default + slow_ma_default + 1)
    # Calculate moving averages
    fast_ma_values = [float(kline[4]) for kline in klines[-fast_ma_default:]]
    fast_ma = sum(fast_ma_values) / len(fast_ma_values)
    slow_ma_values = [float(kline[4]) for kline in klines[-slow_ma_default:]]
    slow_ma = sum(slow_ma_values) / len(slow_ma_values)
    print(fast_ma)
    print(slow_ma)
    # Check if fast moving average crosses above slow moving average
    if ((fast_ma > slow_ma) and (previous_fast_ma < previous_slow_ma)):
        # Buy
        try:
            order = client.order_market_buy(symbol=symbol, quantity=amount)
            logging.info("Bought %s %s at %s", amount, symbol, order["price"])
        except Exception as e:
            logging.error("Error buying: %s", e)
    # Check if fast moving average crosses below slow moving average
    elif fast_ma < slow_ma:
        # Sell
        try:
            order = client.order_market_sell(symbol=symbol, quantity=amount)
            logging.info("Sold %s %s at %s", amount, symbol, order["price"])
        except Exception as e:
            logging.error("Error selling: %s", e)
    else: logging.info("nothing to do")

    # Sleep for 5 minutes
    time.sleep(60)
