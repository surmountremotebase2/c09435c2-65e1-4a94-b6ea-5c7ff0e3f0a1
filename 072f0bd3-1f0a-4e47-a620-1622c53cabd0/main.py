from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]

    @property
    def interval(self):
        # Defines the interval for data collection. For this strategy, daily data is used.
        return "1day"

    @property
    def assets(self):
        # Specifies the assets that this strategy will make decisions for.
        return self.tickers

    def run(self, data):
        # The core logic of the trading strategy.
        
        # Short and long windows define the lookback period for calculating moving averages.
        short_window = 50
        long_window = 200

        # Checking if enough data is available for both short and long moving averages.
        if len(data['ohlcv']) >= long_window:
            # SMA calculation for both short and long windows for the AAPL ticker.
            short_sma = SMA("AAPL", data['ohlcv'], short_window)[-1]
            long_sma = SMA("AAPL", data['ohlcv'], long_window)[-1]
            
            # Decision making based on the crossover logic.
            if short_sma > long_sma:
                # If the short SMA is above the long SMA, we allocate 100% to AAPL.
                allocation_dict = {"AAPL": 1.0}
            else:
                # If the short SMA is below the long SMA, we do not hold AAPL.
                allocation_dict = {"AAPL": 0.0}
        else:
            # If not enough data is available, no allocation is made.
            allocation_dict = {"AAPL": 0.0}
        
        # Logging the decision for diagnostic purposes.
        log(f"Allocating {allocation_dict['AAPL']*100}% to AAPL")

        # Returning the defined target allocations as a TargetAllocation object.
        return TargetAllocation(allocation_dict)