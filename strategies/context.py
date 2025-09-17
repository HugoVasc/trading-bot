from .interface import Strategy, TradingContext
from typing import List, Dict

class SandBoxTradingContext(TradingContext):
    def __init__(self, strategy: Strategy, price_fetcher, symbol: str, timeframe: str = "1h", limit: int = 100, verbose: bool = False):
        self.strategy = strategy
        self.price_fetcher = price_fetcher
        self.symbol = symbol
        self.timeframe = timeframe
        self.limit = limit
        self.verbose = verbose

    def run(self) -> List[Dict]:
        candles = self.price_fetcher.fetch_prices(self.symbol, self.timeframe, self.limit)
        actions = []

        for candle in candles:
            decision = self.strategy.decide(candle)
            actions.append(decision)
            if self.verbose:
                print(decision)

        return actions
